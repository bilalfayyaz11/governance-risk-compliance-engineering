# AI Governance Risk Management

## What This Does

This implementation builds a structured AI governance overlay for a clinical decision-support system based on a black-box BCI signal-classification model.

It combines AI-specific risk registration, NIST AI RMF profiling, bias and harm analysis, data-lineage assessment, SP 800-53 control mapping, residual-risk evaluation, treatment planning, and authorization decision support.

The workflow is designed to turn AI governance requirements into reproducible technical evidence instead of leaving them as static policy documentation.

## Architecture

    ┌──────────────────────────────────────────────┐
    │            CLINICAL AI USE CASE              │
    │                                              │
    │ Black-box BCI neural signal classifier       │
    │ Physician decision-support workflow          │
    └──────────────────────┬───────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │             AI RISK REGISTER                 │
    │                                              │
    │ • Lifecycle stage                            │
    │ • Harm category                              │
    │ • AI RMF function                            │
    │ • Likelihood / impact                        │
    │ • Bias vector                                │
    │ • Data provenance                            │
    │ • Risk score                                 │
    └──────────────────────┬───────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │             AI RMF PROFILE                   │
    │                                              │
    │ Govern                                       │
    │ Map                                          │
    │ Measure                                      │
    │ Manage                                       │
    └──────────────────────┬───────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │       HARM + DATA LINEAGE ANALYSIS           │
    │                                              │
    │ • Representational harm                      │
    │ • Allocative harm                            │
    │ • Quality-of-service harm                    │
    │ • Informational harm                         │
    │ • Provenance gaps                            │
    │ • Feedback-loop risk                         │
    └──────────────────────┬───────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │          CONTROL CROSSWALK                   │
    │                                              │
    │ AI-specific practices                        │
    │          ↕                                   │
    │ NIST SP 800-53 Rev. 5.2.0                    │
    │          ↕                                   │
    │ OSCAL control catalog                        │
    └──────────────────────┬───────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │          RISK TREATMENT LAYER                │
    │                                              │
    │ • Mitigate                                   │
    │ • Accept                                     │
    │ • Transfer                                   │
    │ • Avoid                                      │
    │ • Owners                                     │
    │ • Target dates                               │
    │ • Monitoring cadence                         │
    └──────────────────────┬───────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │        AUTHORIZATION DECISION                │
    │                                              │
    │ Aggregate posture                            │
    │ Top unresolved risks                         │
    │ Explainability limitations                   │
    │ Authorization conditions                     │
    │                                              │
    │ Recommendation:                              │
    │ AUTHORIZE WITH CONDITIONS                    │
    └──────────────────────────────────────────────┘

## System Scenario

The assessed system is a clinical decision-support capability derived from a black-box neural-network BCI signal-classification model.

The model analyzes neural-signal features and flags potentially anomalous neural activity for physician review.

The system is explicitly not intended to:

- Independently diagnose patients
- Initiate treatment
- Deny care
- Replace qualified clinical judgment
- Operate outside validated patient populations

## Core Components

### AI Risk Register

The risk register is implemented in:

    register/risk_register.py

The generated evidence artifact is:

    register/risk_register.csv

Each risk records:

- Risk ID
- AI lifecycle stage
- Harm category
- Affected AI RMF function
- Likelihood
- Impact
- Data-lineage source
- Bias vector
- Mapped controls
- Treatment status
- Calculated risk score

Risk scoring uses:

    Risk Score = Likelihood × Impact

Both likelihood and impact use a 1–5 scale.

## Registered AI Risks

The initial register includes eight high-value AI governance scenarios:

1. Training and production data drift
2. Label bias affecting underrepresented patient cohorts
3. Black-box explainability limitations
4. Adversarial or corrupted signal manipulation
5. Third-party model provenance gaps
6. Sensitive information leakage through model inversion
7. Automation bias affecting clinicians
8. Retraining without independent re-validation

## NIST AI RMF Profile

The use-case profile is stored in:

    profiles/use_case_profile.yaml

It maps the clinical AI system to the four AI RMF functions:

### Govern

Defines:

- AI Governance Lead
- Data Steward
- Clinical SME
- Authorization authority
- Governance requirements
- Accountability structure

### Map

Documents:

- Intended use
- Prohibited use
- Clinical context
- Foreseeable misuse
- Stakeholders
- Assumptions and dependencies

### Measure

Defines measurable controls for:

- Bias
- False-positive disparities
- False-negative disparities
- Explainability coverage
- Clinician explanation acceptance
- Sensitivity
- Specificity
- Performance drift

### Manage

Defines:

- Risk-prioritization criteria
- Retraining triggers
- Rollback triggers
- Human override conditions
- Treatment options
- Continuous monitoring
- Event-driven reassessment

The validator is implemented in:

    profiles/validate_profile.py

It verifies that Govern, Map, Measure, and Manage are all present and sufficiently populated.

## AI Harm and Data Lineage Analysis

The detailed report is stored in:

    evidence/harm_lineage_report.md

The data lineage follows:

    Source BCI datasets
            ↓
    Data ingestion
            ↓
    Preprocessing
            ↓
    Feature engineering
            ↓
    Model training
            ↓
    Independent validation
            ↓
    Deployment
            ↓
    Clinical decision support
            ↓
    Monitoring and feedback
            ↓
    Retraining

The assessment explicitly identifies provenance gaps where evidence is incomplete or unverifiable.

Examples include:

- Incomplete historical cohort metadata
- Unclear clinical label provenance
- Third-party pretrained model provenance gaps
- Feedback-loop contamination during retraining

## Harm Taxonomy

The governance analysis covers:

- Representational harm
- Allocative harm
- Quality-of-service harm
- Informational harm

Each harm is mapped to:

- A lifecycle stage
- An AI RMF function
- A governance gap
- A business or clinical impact

## Black-Box Explainability Gap

The neural-network model presents an important governance limitation.

Traditional SP 800-53 controls can support:

- Risk assessment
- Integrity
- Monitoring
- Privacy
- Training
- Supply-chain assurance
- Change control

However, these controls do not guarantee that a clinician can understand why a specific prediction was produced.

The control crosswalk therefore explicitly identifies at least one risk with:

    NO ADEQUATE SP 800-53 MAPPING

Compensating AI-specific safeguards include:

- Feature-attribution evidence where feasible
- Clinician-facing explanations
- Confidence and uncertainty communication
- Human-in-the-loop authority
- Structured usability validation
- Documented model limitations
- Residual-risk acceptance

## NIST SP 800-53 OSCAL Integration

The workflow uses the official NIST OSCAL control catalog.

The catalog validated during execution was:

    NIST SP 800-53 Rev. 5.2.0

Candidate controls used in the crosswalk include:

- AC-4 — Information Flow Enforcement
- AT-3 — Role-based Training
- PT-2 — Authority to Process Personally Identifiable Information
- RA-3 — Risk Assessment
- RA-9 — Criticality Analysis
- SI-4 — System Monitoring
- SI-7 — Software, Firmware, and Information Integrity
- SR-3 — Supply Chain Controls and Processes
- SR-11 — Component Authenticity

## Control Crosswalk

The control mapping is stored in:

    artifacts/control_crosswalk.csv

Each entry includes:

- Risk ID
- AI-specific practice
- SP 800-53 control
- Control-pairing justification
- Residual risk after control

The crosswalk demonstrates where conventional security controls reduce surrounding AI risk and where additional AI-specific safeguards are still required.

## AI 600-1 Usage

The supplemental mapping is stored in:

    profiles/ai_600-1_controls.yaml

NIST AI 600-1 is a Generative AI Profile, while this assessed BCI classifier is not a generative AI system.

For that reason, AI 600-1 concepts are used only as supplemental risk-management references where the underlying governance concept is relevant.

The implementation does not claim that AI 600-1 is a classifier-specific mandatory control catalog.

Supplemental risk areas include:

- Harmful bias
- Human-AI configuration
- Information security
- Data privacy
- Value-chain risk
- Measurement and monitoring
- Governance and accountability
- Transparency and explainability

## Risk Treatment Plan

The treatment plan is stored in:

    artifacts/risk_treatment_plan.md

Each risk includes:

- Initial score
- Residual risk
- Treatment approach
- Owner
- Target date
- Monitoring cadence
- Required actions

Treatment strategies include:

- Mitigate
- Accept
- Transfer
- Avoid

## Authorization Briefing

The executive authorization artifact is stored in:

    artifacts/ao_briefing.md

It includes:

- Aggregate risk posture
- Maximum risk score
- Average risk score
- Unresolved risk count
- Top three unresolved risks
- Business impact
- Explainability limitations
- Residual-risk rationale
- Authorization conditions

The resulting recommendation is:

    AUTHORIZE WITH CONDITIONS

## Authorization Conditions

The proposed authorization requires:

1. No autonomous diagnosis or treatment decisions.
2. Qualified clinicians retain final decision authority.
3. Material retraining requires independent re-validation.
4. Cohort-level bias and performance metrics must remain within approved thresholds.
5. Production drift monitoring remains active.
6. Third-party provenance gaps remain tracked and escalated.
7. Sensitive neural-data privacy protections remain enforced.
8. High-residual risks retain assigned owners and treatment milestones.
9. Black-box explainability limitations receive explicit residual-risk acceptance.
10. Significant model, data, supplier, privacy, security, or safety changes trigger authorization review.

## How to Run

Activate the environment:

    source venv/bin/activate

Validate the AI RMF profile:

    python profiles/validate_profile.py

Rebuild the risk register:

    python register/risk_register.py

Generate the control crosswalk:

    python artifacts/build_control_crosswalk.py

Generate the treatment plan and authorization briefing:

    python artifacts/generate_authorization_artifacts.py

## Verify the Risk Register

Run:

    wc -l register/risk_register.csv

The file should contain at least nine lines:

- One header
- Eight risk entries

## Verify the Control Crosswalk

Run:

    grep -i "NO ADEQUATE SP 800-53 MAPPING" artifacts/control_crosswalk.csv

This confirms that an AI-specific control gap has been explicitly documented instead of forcing an inaccurate traditional control mapping.

## Verify the Authorization Recommendation

Run:

    grep -i "AUTHORIZE WITH CONDITIONS" artifacts/ao_briefing.md

## Repository Structure

    ai-governance-risk-management/
    ├── README.md
    ├── register/
    │   ├── risk_register.py
    │   └── risk_register.csv
    ├── profiles/
    │   ├── use_case_profile.yaml
    │   ├── validate_profile.py
    │   └── ai_600-1_controls.yaml
    ├── evidence/
    │   └── harm_lineage_report.md
    └── artifacts/
        ├── build_control_crosswalk.py
        ├── control_crosswalk.csv
        ├── generate_authorization_artifacts.py
        ├── risk_treatment_plan.md
        └── ao_briefing.md

## Tools Used

- Python 3
- pandas
- PyYAML
- jsonschema
- jq
- Git
- Bash
- NIST AI RMF
- NIST SP 800-53 Rev. 5.2.0
- NIST OSCAL
- AI 600-1 supplemental risk concepts

## Key Skills Demonstrated

- AI governance engineering
- AI risk-register automation
- AI lifecycle risk analysis
- Bias-vector identification
- Algorithmic harm analysis
- Data provenance assessment
- Data-lineage mapping
- AI RMF profile engineering
- Governance-role definition
- Model-risk scoring
- Explainability risk assessment
- Model drift governance
- Human-in-the-loop control design
- Supply-chain AI risk analysis
- AI privacy risk analysis
- SP 800-53 control mapping
- OSCAL catalog querying
- Residual-risk analysis
- Compensating-control design
- AI risk treatment planning
- Authorization evidence generation
- Executive risk briefing automation
- Python-based governance workflows

## Real-World Use Case

This type of workflow can support organizations deploying high-impact AI systems in regulated or safety-sensitive environments.

Security, compliance, responsible AI, clinical governance, and authorization teams can use the same architecture to:

- Maintain AI-specific risk registers
- Validate governance profiles
- Trace model and data provenance
- Measure subgroup risk
- Document algorithmic harms
- Cross-map existing cybersecurity controls
- Identify AI-specific control gaps
- Assign treatment owners
- Define continuous monitoring
- Produce authorization evidence

The same approach can be extended to AI systems used in healthcare, finance, security operations, critical infrastructure, and enterprise decision support.

## Lessons Learned

- Conventional cybersecurity controls are necessary but not sufficient for many AI risks.
- Black-box explainability requires explicit AI-specific safeguards.
- Bias risk should be measured at subgroup level rather than only through aggregate model performance.
- Data lineage is essential for defensible AI authorization decisions.
- Retraining is a governance event, not just a technical model update.
- Supplier AI components require provenance and assurance evidence.
- Human oversight must be designed as an operational control rather than treated as a policy statement.
- Residual risk should remain visible after controls are applied.
- Authorization decisions become stronger when evidence is generated programmatically and can be reproduced.
- AI governance becomes more operational when risk, controls, evidence, treatment, and authorization are connected through one technical workflow.

## Troubleshooting Log

### Missing Virtual Environment

During execution, the previously created Python virtual environment was no longer present.

The environment was rebuilt conditionally rather than assuming previous runtime state.

Required Python dependencies were restored inside the isolated environment.

### Missing Risk Register Artifact

The risk register CSV was unexpectedly absent when the control-crosswalk generator was executed.

This caused several downstream verification failures because the crosswalk depended on:

    register/risk_register.csv

The failure was isolated to a single missing upstream artifact rather than being treated as multiple independent control-mapping errors.

The risk register was rebuilt and the downstream crosswalk generation was rerun successfully.

### Cascading Verification Failures

When the upstream risk register was missing, later checks for:

- Crosswalk generation
- AI practice coverage
- SP 800-53 coverage
- Residual risk
- Explicit control gaps

all failed.

The recovery process restored the upstream artifact first, preventing unnecessary changes to otherwise correct downstream components.

### OSCAL Catalog Validation

The environment successfully queried the official SP 800-53 Rev. 5.2.0 OSCAL catalog and confirmed all selected candidate controls before they were used in the crosswalk.

### AI 600-1 Scope

The assessed system is a classifier rather than a generative AI system.

AI 600-1 was therefore used only as a supplemental governance reference. The implementation explicitly avoids presenting the Generative AI Profile as a direct classifier-specific control baseline.
