# VEDA V2 — UI/UX and Design System

**Version:** 2.0  
**Design Direction:** Premium Minimalist Automotive Technology  
**Design Philosophy:** Precision, Intelligence and Transparency

# 1. Brand Identity

## Brand Name

VEDA

## Brand Positioning

VEDA is a premium vehicle intelligence and maintenance ecosystem connecting vehicle owners, mechanics and service centres through predictive diagnostics and digital vehicle visualization.

## Brand Statement

"Precision. Intelligence. Mobility."

## Supporting Tagline

"Beyond the machine. Behind every move."

The brand should communicate:
- Engineering precision.
- Automotive intelligence.
- Trust and transparency.
- Industrial reliability.
- Technological sophistication.

# 2. Design Inspiration

The user has provided three website references.

Use these as visual inspiration, not as templates to copy.

## Reference 1 — AXIS Luxury Venue

Design characteristics:
- Large cinematic hero sections.
- Premium typography.
- Spacious layouts.
- Strong visual hierarchy.
- Minimal navigation.
- High-quality photography.
- Editorial storytelling.

Apply these characteristics to the VEDA landing page.

## Reference 2 — Monochrome Photography Website

Design characteristics:
- Black-and-white imagery.
- Selective colour reveal on hover.
- Minimal visual clutter.
- Strong contrast.
- Smooth image transitions.

Apply these characteristics to vehicle photographs, workshop imagery and promotional sections.

Images should transition naturally from monochrome to colour on hover.

This effect must not obscure diagnostic information or essential controls.

## Reference 3 — Playful Website

Design characteristics:
- Unexpected micro-interactions.
- Small moments of personality.
- Interesting hover effects.
- Memorable transitions.

Use these selectively.

VEDA must remain professional and trustworthy.

# 3. Colour System

Use a restrained automotive palette.

## Primary Colours

| Name | Hex | Usage |
|---|---|---|
| Carbon Black | #10110F | Primary dark backgrounds |
| Graphite | #1A1D18 | Cards and panels |
| Warm White | #F4F4F0 | Primary light backgrounds |
| Pure White | #FFFFFF | Text and surfaces |
| Industrial Lime | #B8E36A | Primary accent |
| Muted Grey | #858A7E | Secondary text |

## Status Colours

| Status | Colour |
|---|---|
| Normal | #829B75 |
| Suspected | #C89B4B |
| Mechanic Verified | #B96859 |
| Repaired | #91B957 |
| Information | #66869B |
| Unmapped | #858A7E |

Status must also be communicated through text and icons. Never rely on colour alone.

## Colour Usage Rules

- Use dark backgrounds for cinematic and technical sections.
- Use warm white for readable content-heavy pages.
- Use industrial lime sparingly for primary actions and active states.
- Avoid excessive gradients.
- Avoid unnecessary colourful cards.
- Maintain sufficient text contrast.
- Keep the design visually consistent across all dashboards.

# 4. Typography

## Primary Font

Manrope.

Use for:
- Headings.
- Body text.
- Navigation.
- Buttons.
- Dashboard content.

## Technical Font

DM Mono.

Use for:
- Vehicle identifiers.
- Component codes.
- Diagnostic readings.
- Technical metadata.
- Model versions.
- Measurement values.

## Typography Rules

- Large editorial headings.
- Clear hierarchy.
- Restrained letter spacing.
- Readable body text.
- Consistent font weights.
- Avoid excessive font sizes in dashboards.

# 5. Overall Application Experience

VEDA should have five distinct interface experiences:

1. Public landing page.
2. Vehicle owner workspace.
3. Service-centre administrator workspace.
4. Mechanic workspace.
5. VEDA administrator workspace.

The interfaces should share a design system but have different information priorities.

# 6. Public Landing Page

The landing page is the first impression of VEDA.

It should feel like a premium automotive technology brand.

## Section 1 — Navigation

- VEDA logo.
- Platform.
- Technology.
- How It Works.
- For Service Centres.
- Sign In.
- Get Started.

Navigation should be minimal and sticky where appropriate.

## Section 2 — Hero

A cinematic heavy-truck photograph or video.

Headline:

"UNDERSTAND THE MACHINE. BEFORE IT STOPS."

Supporting text:

"Intelligent diagnostics, transparent maintenance and connected service management for the next generation of heavy vehicles."

Primary action:
"Explore VEDA"

Secondary action:
"How It Works"

Use large typography and restrained animation.

## Section 3 — Introduction

Explain VEDA's mission.

Show how mechanics, vehicle owners and AI work together.

Use large imagery and editorial-style text blocks.

## Section 4 — Three Core Pillars

### Diagnose
AI-assisted vehicle diagnostics combined with mechanic expertise.

### Visualize
Interactive 2D and 3D component identification.

### Maintain
Transparent estimates, spare parts and repair tracking.

## Section 5 — Digital Vehicle Intelligence

Showcase the interactive truck visualization concept.

Use a premium technical presentation with component highlights.

## Section 6 — Connected Ecosystem

Illustrate the relationship between:
- Vehicle owners.
- Mechanics.
- Service centres.
- AI intelligence.
- Spare-parts inventory.

## Section 7 — Closing CTA

Headline:

"THE FUTURE OF VEHICLE MAINTENANCE STARTS HERE."

CTA:
"Enter VEDA"

# 7. Authentication Screens

Authentication must support phone-number-based OTP.

Screens:
- Phone number entry.
- OTP verification.
- Account setup.
- Role-specific onboarding.
- Profile completion.

Use a minimal layout.

Do not ask users for unnecessary information during initial registration.

# 8. Vehicle Owner Dashboard

The owner workspace should be simple, transparent and informative.

## Dashboard Sections

### Overview
- Registered vehicles.
- Active service requests.
- Pending approvals.
- Completed services.

### Vehicle Cards

Each vehicle card should display:
- Vehicle photograph or model.
- Registration number.
- Manufacturer and model.
- Current service status.
- Last service date.
- Odometer reading.

### Service Activity

Display:
- Service request status.
- Inspection status.
- AI diagnosis status.
- Pending estimates.
- Repair progress.
- Payment status.

### Pending Approvals

Each estimate item should show:
- Component.
- Identified issue.
- Recommended repair.
- Spare part.
- Cost.
- Labour.
- Estimated duration.
- Approval action.

The owner should be able to approve or reject individual items.

### Service History

Provide a chronological history of:
- Inspections.
- Diagnoses.
- Repairs.
- Parts replaced.
- Invoices.

# 9. Service Centre Dashboard

The service-centre dashboard is an operational workspace.

## Navigation

- Overview.
- Customers.
- Vehicles.
- Service Orders.
- Mechanics.
- Inspections.
- Estimates.
- Inventory.
- Invoices.
- Reports.
- Settings.

## Main Dashboard

Show:
- Incoming service requests.
- Vehicles currently in workshop.
- Pending mechanic assignments.
- Inspections in progress.
- Pending customer approvals.
- Repairs in progress.
- Completed services.

## Customer Vehicle Queue

Display each vehicle as a searchable service-order card.

Each card should show:
- Vehicle identity.
- Owner.
- Registration number.
- Service request.
- Assigned mechanic.
- Current status.
- Next required action.

# 10. Mechanic Workspace

This is one of VEDA's most important interfaces.

Mechanics must be able to enter inspection data quickly and clearly.

## Inspection Workspace

Sections:

1. Vehicle information.
2. Service request.
3. Inspection checklist.
4. Component observations.
5. Symptoms.
6. Measurements and readings.
7. Supporting notes.
8. Evidence attachments.
9. AI diagnostic execution.

## Diagnosis Workspace

Show three clearly separated information sections:

### AI Predictions
What the available AI model predicts.

### Mechanic Findings
What the mechanic observed during inspection.

### Diagnostic Reasoning
What VEDA identifies from available evidence and validated rules.

Include:
- Suspected component.
- Supporting evidence.
- Diagnostic status.
- Recommended additional inspection.
- Mechanic verification controls.

Do not display unsupported predictions as confirmed faults.

# 11. Digital Twin and Diagnosis Screen

This should become VEDA's signature feature.

## Layout

Create a two-panel diagnostic workspace.

Left panel:
- Vehicle component navigation.
- Component hierarchy.
- System selection.
- Fault list.
- Component search.

Main panel:
- Interactive 3D truck viewer.
- Camera rotation.
- Zoom.
- Reset camera.
- Component selection.
- Component highlighting.

Alternative view:
- 2D technical diagram.

## Component Information Panel

When a component is selected, show:

- Component name.
- Vehicle system.
- Current diagnostic state.
- Inspection observations.
- AI evidence.
- Mechanic verification.
- Recommended action.
- Compatible spare parts where validated.
- Estimated repair cost where available.
- Estimated remaining life only when supported by a validated model.

## Component Visual States

- NORMAL
- SUSPECTED
- MECHANIC_VERIFIED
- REPAIRED
- UNMAPPED

The selected component should be synchronized between the 2D and 3D views when mappings exist.

# 12. Spare Parts and Inventory Interface

Create an organized spare-parts browsing experience.

The interface may borrow the convenience of e-commerce platforms without becoming a public marketplace.

## Part Cards

Display:
- Part photograph.
- Part name.
- Part number.
- Compatible component.
- Compatibility status.
- Workshop stock.
- Unit price.
- Quantity.

## Owner Recommendation View

Display:
- Recommended part.
- Why it is recommended.
- Compatibility evidence.
- Price.
- Quantity.
- Estimated replacement labour.

Provide add/remove or approve/reject interactions as appropriate.

Do not recommend a part without compatibility evidence.

# 13. Estimate and Approval Interface

The owner should see a transparent breakdown.

Include:

- Component.
- Problem description.
- Recommended solution.
- Spare-part cost.
- Labour cost.
- Quantity.
- Total.
- Estimated completion duration.

Actions:
- Approve.
- Reject.
- Request clarification.

Show the estimate total updating when approved items change.

The backend remains responsible for validating final totals and approval state.

# 14. Repair Tracking Interface

Provide a clear progress timeline.

Possible stages:

- Vehicle received.
- Inspection started.
- Diagnosis completed.
- Estimate submitted.
- Owner approval received.
- Repair started.
- Final inspection.
- Invoice generated.
- Payment completed.
- Vehicle delivered.

Use timestamps and mechanic updates.

# 15. Administrator Dashboard

Provide a professional management interface.

Sections:
- Platform overview.
- Service-centre verification.
- User management.
- Centre activity.
- Vehicle records.
- Platform audit logs.
- Model versions.
- System configuration.

Avoid exposing private customer data unnecessarily.

# 16. Micro-interactions and Animations

Use restrained animations.

Examples:
- Image grayscale-to-colour reveal.
- Smooth navigation transitions.
- Subtle card hover elevation.
- Component selection transitions.
- Diagnostic status transitions.
- Animated service timeline.
- Smooth 3D camera controls.
- Loading skeletons.
- Toast notifications.

Use CSS transitions or suitable animation libraries.

Respect reduced-motion accessibility settings.

Do not animate every element.

# 17. Reusable Component Library

Build reusable components.

Suggested components:

```text
components/
├── common/
│   ├── Button
│   ├── Input
│   ├── Modal
│   ├── Badge
│   ├── Tooltip
│   └── Toast
│
├── layout/
│   ├── AppShell
│   ├── Sidebar
│   ├── Topbar
│   └── PageHeader
│
├── dashboard/
│   ├── StatCard
│   ├── ActivityFeed
│   └── DataTable
│
├── vehicles/
│   ├── VehicleCard
│   └── VehicleDetails
│
├── diagnosis/
│   ├── DiagnosisCard
│   ├── EvidencePanel
│   └── ComponentStatusLegend
│
├── visualization/
│   ├── TruckViewer3D
│   ├── ComponentSelector
│   └── DiagramViewer2D
│
├── inventory/
│   ├── PartCard
│   └── InventoryTable
│
└── approvals/
    ├── EstimateCard
    └── ApprovalItem
```

These are target components. Kiro should adapt them to the existing project rather than duplicate existing functionality.

# 18. Responsive Design

Desktop:
- Full navigation.
- Multi-column dashboards.
- Large visualization canvas.

Tablet:
- Collapsible navigation.
- Reduced card columns.
- Adapted visualization layout.

Mobile:
- Drawer navigation.
- Stacked dashboard cards.
- Touch-friendly buttons.
- Responsive forms.
- Touch-enabled 3D viewer.

Data tables must remain usable on small screens.

# 19. Accessibility

- Semantic HTML.
- Keyboard navigation.
- Visible focus indicators.
- Accessible form labels.
- Sufficient contrast.
- Accessible dialogs.
- Text labels alongside status colours.
- Reduced-motion support.

# 20. Data Presentation Rules

- Clearly distinguish demo data from real data.
- Never present fabricated AI predictions as real.
- Never show invented vehicle health scores.
- Never show invented RUL values.
- Never display unverified compatibility as confirmed.
- Clearly identify unavailable information.
- Use loading, empty and error states.

# 21. Final Design Principle

VEDA should feel like a premium automotive intelligence platform.

The public experience should be cinematic and memorable.

The owner experience should be transparent and reassuring.

The mechanic experience should be practical and efficient.

The service-centre experience should be operationally powerful.

The administrator experience should be controlled and data-driven.

All interfaces must feel like parts of the same product.

**The design must communicate engineering precision, trust and intelligence without unnecessary visual complexity.**