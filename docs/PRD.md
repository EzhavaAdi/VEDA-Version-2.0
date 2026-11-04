# VEDA V2 — Product Requirements Document

**Product Name:** VEDA  
**Version:** 2.0  
**Product Type:** AI-powered Heavy Vehicle Diagnostics and Service Management Platform

## 1. Product Vision

VEDA is a unified vehicle intelligence and maintenance platform connecting heavy vehicle owners with registered mechanics and service centres.

The platform aims to simplify vehicle maintenance through AI-assisted predictive diagnostics, mechanic inspections, interactive 2D/3D vehicle visualization, spare-parts recommendations, transparent estimates and integrated payments.

VEDA will act as a bridge between vehicle owners and service centres, making vehicle servicing more transparent, efficient and data-driven.

## 2. Target Users

### 2.1 Vehicle Owners
- Register and manage their trucks.
- Find and connect with registered service centres.
- Submit service requests.
- View mechanic inspection reports.
- View AI-assisted diagnostic results.
- Explore faulty components through 2D and 3D visualization.
- Review recommended spare parts and repair costs.
- Approve or reject individual repair items.
- Track repair progress.
- View invoices and make payments.
- Access vehicle service history.

### 2.2 Service Centre Administrators
- Register and manage their service centre.
- Manage mechanics and staff.
- View all assigned customer vehicles.
- Accept or reject service requests.
- Assign mechanics to vehicles.
- Manage inventory and spare parts.
- Generate estimates and invoices.
- Track service orders and payments.

### 2.3 Mechanics
- Access assigned vehicle records.
- Enter manual inspection findings.
- Enter vehicle symptoms and measurements.
- Run available AI diagnostic models.
- Compare AI predictions with their inspection findings.
- Verify or reject AI-suggested faults.
- Identify suspected components.
- Recommend compatible spare parts.
- Prepare repair estimates.
- Update repair progress.

### 2.4 VEDA Administrators
- Manage registered users.
- Verify service centres.
- Manage platform access.
- Monitor service operations.
- Manage component catalogues.
- Review platform activity and audit records.

## 3. Business Model

VEDA follows a B2B2C business model.

- Vehicle owners use VEDA to manage servicing.
- Service centres onboard their mechanics and provide repair services.
- Spare parts are supplied through service-centre inventory.
- VEDA coordinates owner approvals, service records and payments.
- The platform may generate revenue through service transaction commissions or subscription plans in future.

Mechanics must belong to registered service centres in the initial version.

## 4. Core Application Workflow

1. Owner registers and logs into VEDA.
2. Owner registers their heavy vehicle.
3. Owner submits a service request to a service centre.
4. Service centre accepts the vehicle.
5. Mechanic receives the vehicle and performs a manual inspection.
6. Mechanic enters inspection findings and relevant readings.
7. VEDA processes supported information through its AI diagnostic engine.
8. AI predictions and mechanic findings are presented separately.
9. VEDA identifies suspected components using available evidence and diagnostic rules.
10. Mechanic reviews and verifies the findings.
11. VEDA displays the relevant vehicle components through 2D diagrams and 3D visualization where mappings exist.
12. The mechanic prepares an itemized repair estimate.
13. VEDA recommends compatible spare parts available in workshop inventory.
14. Owner reviews the diagnosis, cost and recommendations.
15. Owner approves or rejects individual repair items.
16. Mechanic performs only authorized repairs.
17. Mechanic updates repair progress.
18. Service centre performs final inspection.
19. VEDA generates the final invoice.
20. Owner completes payment.
21. Vehicle is delivered to the owner.
22. Service history is saved.

## 5. AI Diagnostic System

### 5.1 Initial Model
VEDA will initially integrate a predictive model trained using the Scania APS Failure dataset.

The model will be responsible only for its validated APS-related failure classification task.

### 5.2 AI Processing
The AI architecture should support:
- Data preprocessing.
- Feature validation.
- Predictive model inference.
- Failure classification.
- Diagnostic rule processing.
- Structured diagnostic outputs.
- Model version tracking.

### 5.3 Mechanic Integration

Mechanic inspection data will be combined with AI predictions as additional diagnostic evidence.

The system must maintain a distinction between:
- AI prediction.
- Mechanic observation.
- Rule-based inference.
- Mechanic-verified diagnosis.

Mechanic-confirmed findings must not accidentally leak into pre-diagnosis model inputs when evaluating predictive performance.

### 5.4 Component Identification

VEDA should identify suspected components at a generic component level using validated diagnostic evidence and rules.

The platform must not claim exact component identification when the available model or evidence cannot support it.

### 5.5 Remaining Useful Life

VEDA may display estimated remaining useful life only when a suitable dataset and validated predictive model are available.

Otherwise, it must explicitly indicate that insufficient data exists.

## 6. Vehicle Visualization

VEDA must provide two visualization methods.

### 2D Visualization
- Technical component diagrams.
- Component selection.
- Fault highlighting.
- Component labels.
- Normal and faulty states.

### 3D Visualization
- Interactive heavy-truck models.
- Rotation and zoom.
- Component selection.
- Fault highlighting.
- Component information.
- Before-and-after repair representation where supported.

Initial 3D assets may use legally available generic heavy-truck models.

Component highlighting must use actual mesh mappings, not guessed locations.

## 7. Spare Parts and Inventory

- Each service centre maintains its own inventory.
- Parts must have names, identifiers, prices and stock quantities.
- Compatibility with vehicle components must be recorded.
- AI or diagnostic rules may recommend relevant parts only when compatibility evidence exists.
- Owners can review recommended parts.
- Owners can approve or reject individual items.
- Inventory must be updated safely when parts are reserved or used.

## 8. Repair Estimates and Approval

Each estimate should contain:
- Component name.
- Identified issue.
- Recommended repair.
- Spare-part name.
- Quantity.
- Spare-part price.
- Labour cost.
- Total estimated cost.
- Estimated repair duration.

The owner must have control over individual estimate items.

Only approved repair items may proceed to authorized work.

## 9. Component Life and Maintenance Recommendations

Where sufficient validated information exists, VEDA may provide:
- Estimated remaining useful life.
- Consequences of delayed replacement.
- Expected replacement interval.
- Preventive maintenance recommendations.
- Expected repair cost.

These must be presented as estimates, not guaranteed outcomes.

## 10. Educational Video Recommendations

VEDA should include a feature for recommending relevant YouTube videos.

Videos may explain:
- Component functionality.
- Common failure symptoms.
- Repair procedures.
- Preventive maintenance.
- Replacement procedures.

Recommendations should be relevant to the identified component and must not replace professional repair instructions.

## 11. Authentication

- Phone-number-based authentication.
- OTP verification.
- Role-based access.
- Secure session management.

Development must use a mock or console OTP provider.

## 12. Payments

- Owner payments are coordinated through VEDA.
- Service centres receive payments through a supported payment arrangement.
- Mock payments will be used during local development.
- Real payment processing will be integrated after selecting a suitable payment provider and settlement model.

## 13. Technology Stack

**Frontend**
- React
- TypeScript
- Vite
- React Router
- Three.js
- React Three Fiber

**Backend**
- Python
- Django
- Django REST Framework

**Database**
- PostgreSQL

**AI**
- Python
- pandas
- NumPy
- scikit-learn
- XGBoost / PyTorch as appropriate

**Development**
- Kiro
- Git
- GitHub
- Local development environment

## 14. Hosting Strategy

Initial development and testing will take place locally.

Cloud deployment can be introduced after the MVP is stable.

## 15. MVP Objectives

The first working version must demonstrate:

1. Owner and service-centre registration.
2. Phone-based authentication.
3. Vehicle registration.
4. Service request creation.
5. Mechanic inspection.
6. APS AI model integration.
7. AI and mechanic finding comparison.
8. Component-level diagnosis workflow.
9. 2D/3D component visualization.
10. Spare-parts inventory.
11. Repair estimates.
12. Owner approvals.
13. Repair tracking.
14. Invoice generation.
15. Mock payment and vehicle delivery.

## 16. Future Scope

- Multiple truck manufacturers.
- Additional component-specific AI models.
- Telematics integration.
- Advanced predictive maintenance.
- Validated component-level RUL prediction.
- Automated spare-parts procurement.
- Advanced fleet analytics.
- Mobile application.
- Cloud deployment and multi-region support.

---

**Core Principle:**

VEDA is not simply an AI model wrapped in a website. It is a connected vehicle maintenance ecosystem where AI intelligence, mechanic expertise, vehicle owners and service-centre operations work together.