"""
VEDA V2 — APS diagnostic rule engine

Combines AI predictions + mechanic inspection evidence to generate
component candidates with supporting evidence.

Rules are explicit and traceable — each rule documents its evidence basis.
Components are only suggested when validated evidence supports it.

RULES (from RULES.md):
- Never assign arbitrary confidence values.
- Never claim a component is definitely faulty without supporting evidence.
- Use validated diagnostic rules only.
- Distinguish AI_PREDICTION from MECHANIC_OBSERVATION from DIAGNOSTIC_RULE.
"""

import logging
from dataclasses import dataclass, field

logger = logging.getLogger("veda.ai.rules")


# ---------------------------------------------------------------------------
# Evidence collector
# ---------------------------------------------------------------------------

@dataclass
class RuleEvidence:
    evidence_type: str          # from EvidenceType choices
    evidence_reference: str     # ID or code of source record
    evidence_description: str


@dataclass
class ComponentCandidate:
    component_code:  str
    component_name:  str
    confidence_note: str        # plain-language note — never a fabricated number
    evidence:        list[RuleEvidence] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Rule: APS positive prediction → APS system candidates
# ---------------------------------------------------------------------------

APS_COMPONENT_CANDIDATES = [
    ("APS",             "Air Pressure System"),
    ("APS_COMPRESSOR",  "Air Compressor"),
    ("APS_DRYER",       "Air Dryer"),
    ("APS_GOVERNOR",    "Pressure Governor"),
    ("APS_VALVE",       "Air Control Valve"),
    ("APS_RESERVOIR",   "Air Reservoir / Tank"),
]


def apply_aps_prediction_rule(
    prediction_result: dict,
    ai_run_id: str,
) -> list[ComponentCandidate]:
    """
    Rule APS-001: When the APS classifier predicts a POSITIVE (APS failure),
    flag APS system components as candidates.

    This rule does NOT confirm which specific component is faulty —
    it only narrows suspicion to the APS subsystem.
    """
    if prediction_result.get("status") != "completed":
        return []
    if prediction_result.get("predicted_class") != "pos":
        return []

    prob = prediction_result.get("probability_positive", 0.0)
    candidates = []

    for code, name in APS_COMPONENT_CANDIDATES:
        evidence = RuleEvidence(
            evidence_type="AI_PREDICTION",
            evidence_reference=str(ai_run_id),
            evidence_description=(
                f"APS failure classifier predicted POSITIVE "
                f"(probability={prob:.2%}). "
                f"Component '{code}' is part of the APS system and is a candidate "
                f"for further mechanic inspection."
            ),
        )
        rule_evidence = RuleEvidence(
            evidence_type="DIAGNOSTIC_RULE",
            evidence_reference="APS-001",
            evidence_description=(
                "Rule APS-001: APS positive prediction implicates all APS subsystem "
                "components. Mechanic verification required to confirm specific fault."
            ),
        )
        candidates.append(ComponentCandidate(
            component_code=code,
            component_name=name,
            confidence_note=(
                f"APS system candidate based on classifier prediction "
                f"(prob_pos={prob:.2%}). Exact component unconfirmed."
            ),
            evidence=[evidence, rule_evidence],
        ))

    logger.info(
        f"Rule APS-001 triggered: {len(candidates)} APS component candidates "
        f"(prob_pos={prob:.2%})"
    )
    return candidates


# ---------------------------------------------------------------------------
# Rule: Mechanic observed HIGH/CRITICAL severity on APS component
# ---------------------------------------------------------------------------

def apply_mechanic_observation_rule(
    inspection_items: list[dict],
) -> list[ComponentCandidate]:
    """
    Rule MECH-001: When a mechanic records HIGH or CRITICAL severity
    on a component, add it as a candidate regardless of AI prediction.

    Mechanic evidence is independent — AI need not agree.
    """
    candidates = []
    for item in inspection_items:
        severity = item.get("severity", "NONE")
        if severity not in ("HIGH", "CRITICAL"):
            continue

        code = item.get("component_code", "")
        name = item.get("component_name", code)
        item_id = item.get("id", "")

        evidence = RuleEvidence(
            evidence_type="MECHANIC_OBSERVATION",
            evidence_reference=str(item_id),
            evidence_description=(
                f"Mechanic recorded {severity} severity on {code}: "
                f"{item.get('observed_condition', '')}"
            ),
        )
        rule_evidence = RuleEvidence(
            evidence_type="DIAGNOSTIC_RULE",
            evidence_reference="MECH-001",
            evidence_description=(
                "Rule MECH-001: Mechanic-observed HIGH or CRITICAL severity "
                "on a component is independent evidence of a potential fault."
            ),
        )
        candidates.append(ComponentCandidate(
            component_code=code,
            component_name=name,
            confidence_note=(
                f"Mechanic-identified candidate ({severity} severity). "
                "AI confirmation not required."
            ),
            evidence=[evidence, rule_evidence],
        ))

    if candidates:
        logger.info(f"Rule MECH-001: {len(candidates)} mechanic-identified candidates")
    return candidates


# ---------------------------------------------------------------------------
# Rule: Sensor reading out of normal range → add reading as evidence
# ---------------------------------------------------------------------------

APS_PRESSURE_NORMAL_MIN = 7.5   # bar
APS_PRESSURE_NORMAL_MAX = 8.5   # bar


def apply_sensor_rule(sensor_readings: list[dict]) -> list[RuleEvidence]:
    """
    Rule SENS-001: Attach out-of-range sensor readings as additional evidence.
    Does not create new component candidates — enriches existing ones.
    """
    extra_evidence = []
    for reading in sensor_readings:
        name  = reading.get("parameter_name", "").lower()
        value = reading.get("parameter_value")
        unit  = reading.get("unit", "")
        rid   = reading.get("id", "")
        comp  = reading.get("component_code", "")

        if value is None:
            continue

        try:
            val = float(value)
        except (TypeError, ValueError):
            continue

        # APS pressure out-of-range
        if "aps" in name and "pressure" in name and unit.lower() in ("bar", "kpa"):
            if unit.lower() == "kpa":
                val = val / 100  # convert to bar
            if not (APS_PRESSURE_NORMAL_MIN <= val <= APS_PRESSURE_NORMAL_MAX):
                extra_evidence.append(RuleEvidence(
                    evidence_type="SENSOR_READING",
                    evidence_reference=str(rid),
                    evidence_description=(
                        f"APS pressure reading {val:.2f} bar is outside normal range "
                        f"({APS_PRESSURE_NORMAL_MIN}–{APS_PRESSURE_NORMAL_MAX} bar). "
                        f"Component: {comp}."
                    ),
                ))
                logger.info(f"Rule SENS-001: APS pressure out of range ({val:.2f} bar)")

    return extra_evidence


# ---------------------------------------------------------------------------
# Aggregate all rules
# ---------------------------------------------------------------------------

def run_all_rules(
    prediction_result: dict,
    ai_run_id: str,
    inspection_items: list[dict],
    sensor_readings: list[dict],
) -> tuple[list[ComponentCandidate], list[RuleEvidence]]:
    """
    Apply all rules and return:
        candidates     — list of ComponentCandidate
        extra_evidence — standalone evidence items (sensor anomalies, etc.)
    """
    candidates: list[ComponentCandidate] = []
    extra_evidence: list[RuleEvidence] = []

    # Rule APS-001
    candidates += apply_aps_prediction_rule(prediction_result, ai_run_id)

    # Rule MECH-001
    mech_candidates = apply_mechanic_observation_rule(inspection_items)

    # Merge — if mechanic identifies a component already found by APS rule,
    # add mechanic evidence to the existing candidate instead of duplicating
    existing_codes = {c.component_code for c in candidates}
    for mc in mech_candidates:
        if mc.component_code in existing_codes:
            for c in candidates:
                if c.component_code == mc.component_code:
                    c.evidence += mc.evidence
                    c.confidence_note += " | Corroborated by mechanic observation."
        else:
            candidates.append(mc)

    # Rule SENS-001
    sensor_ev = apply_sensor_rule(sensor_readings)
    extra_evidence += sensor_ev

    # Attach sensor evidence to relevant candidates
    for ev in sensor_ev:
        for c in candidates:
            if "APS" in c.component_code and "APS" in ev.evidence_description.upper():
                c.evidence.append(ev)

    logger.info(
        f"Diagnosis rules complete: {len(candidates)} candidates, "
        f"{len(extra_evidence)} standalone evidence items."
    )
    return candidates, extra_evidence
