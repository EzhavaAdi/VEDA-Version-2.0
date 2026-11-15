# VEDA V2 — Dummy APS Test Data

12 real rows from the Scania APS training dataset.
Upload any file on the Platform page -> APS section -> Run APS Diagnosis

| # | File | Expected | Probability | Description |
|---|---|---|---|---|
| 1 | `aps_01_severe_aps_failure.csv` | `pos` | 0.999 | Confirmed APS failure — real sensor data row 1 |
| 2 | `aps_02_compressor_fault.csv` | `pos` | 0.992 | APS compressor fault — real sensor data row 2 |
| 3 | `aps_03_pressure_system_failure.csv` | `pos` | 0.993 | Air pressure system failure — row 3 |
| 4 | `aps_04_dryer_related_fault.csv` | `pos` | 0.999 | Air dryer related APS fault — row 4 |
| 5 | `aps_05_intermittent_aps_fault.csv` | `pos` | 0.999 | Intermittent APS fault detected — row 5 |
| 6 | `aps_06_critical_aps_failure.csv` | `pos` | 1.000 | Critical APS failure — immediate service needed |
| 7 | `aps_07_healthy_truck.csv` | `neg` | 0.000 | Healthy truck — no APS issues detected |
| 8 | `aps_08_routine_check_ok.csv` | `neg` | 0.000 | Routine inspection — all APS readings normal |
| 9 | `aps_09_post_service_clear.csv` | `neg` | 0.000 | Post-service check — APS system clear |
| 10 | `aps_10_high_mileage_healthy.csv` | `neg` | 0.000 | High mileage truck — APS healthy |
| 11 | `aps_11_new_vehicle_baseline.csv` | `neg` | 0.056 | New vehicle baseline reading — no faults |
| 12 | `aps_12_non_aps_fault_other_system.csv` | `neg` | 0.000 | Non-APS fault elsewhere — APS itself is fine |
