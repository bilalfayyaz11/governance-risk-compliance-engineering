# AI Harm and Data Lineage Report

## System Context

The assessed system is a clinical decision-support capability built on a black-box neural-network BCI signal-classification model. It analyzes neural-signal features and flags anomalous activity for physician review.

The system is not authorized to independently diagnose patients, initiate treatment, deny care, or replace qualified clinical judgment.

## Data Lineage

    ┌───────────────────────────────┐
    │ Source Clinical BCI Datasets  │
    │                               │
    │ • Historical neural signals  │
    │ • Patient cohort metadata    │
    │ • Clinical labels            │
    │ • Device/source metadata     │
    └───────────────┬───────────────┘
                    │
                    │ provenance / consent /
                    │ cohort representation
                    ▼
    ┌───────────────────────────────┐
    │ Data Ingestion               │
    │                               │
    │ • Dataset collection         │
    │ • Source normalization       │
    │ • Identifier handling        │
    │ • Metadata capture           │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Preprocessing                │
    │                               │
    │ • Noise filtering            │
    │ • Signal segmentation        │
    │ • Artifact removal           │
    │ • Missing-value handling     │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Feature Engineering          │
    │                               │
    │ • Signal-derived features    │
    │ • Frequency-domain features  │
    │ • Temporal transformations   │
    │ • Normalization              │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Model Training               │
    │                               │
    │ • Neural-network training    │
    │ • Hyperparameter selection   │
    │ • Internal validation        │
    │ • Model artifact generation  │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Independent Validation       │
    │                               │
    │ • Cohort-level performance   │
    │ • Bias evaluation            │
    │ • Robustness testing         │
    │ • Clinical SME review        │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Deployment                   │
    │                               │
    │ • Approved model artifact    │
    │ • Production preprocessing   │
    │ • Inference service          │
    │ • Access controls            │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Clinical Decision Support    │
    │                               │
    │ • Neural anomaly flag        │
    │ • Confidence / explanation   │
    │ • Physician review           │
    │ • Human decision             │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Monitoring & Feedback        │
    │                               │
    │ • Performance drift          │
    │ • Bias drift                 │
    │ • Clinical incidents         │
    │ • Model retraining triggers  │
    └───────────────────────────────┘

## Provenance Assessment

| Lineage Link | Verification Status | Governance Concern |
|---|---|---|
| Source dataset → patient cohort metadata | Partially verifiable | Historical datasets may contain incomplete demographic and device-source metadata |
| Clinical labels → label-generation process | Partially verifiable | Labeling criteria and inter-rater consistency may not be fully documented |
| Third-party model component → original training sources | Unverifiable | Supplier may not provide complete training-data provenance |
| Raw BCI signals → preprocessing configuration | Verifiable if configuration is version-controlled | Unauthorized preprocessing changes can invalidate model assumptions |
| Preprocessing → feature-engineering pipeline | Verifiable if pipeline code and configuration are retained | Feature changes can introduce hidden model-performance changes |
| Feature set → training run | Verifiable if experiment metadata is retained | Missing experiment records reduce reproducibility |
| Training run → deployed model artifact | Verifiable using model hashes and release records | Artifact substitution or unapproved versions create integrity risk |
| Deployed model → clinical output | Verifiable through inference logging | Missing logs weaken traceability and incident investigation |
| Production feedback → retraining dataset | Partially verifiable | Feedback loops can amplify prior model or clinician bias |
| Retrained model → re-authorization evidence | Governance-dependent | Retraining without re-validation can bypass prior authorization assumptions |

## Key Data Lineage Gaps

### 1. Historical Cohort Metadata

Some training data may not contain sufficiently complete demographic, device, or acquisition-context metadata. This makes subgroup performance evaluation less reliable.

Affected AI RMF function: Map

### 2. Label Provenance

Clinical labels may have been derived from historical physician judgments without complete documentation of labeling procedures, disagreement rates, or quality assurance.

Affected AI RMF function: Measure

### 3. Third-Party Model Provenance

A third-party pretrained component may not expose complete details of its original datasets, preprocessing methods, or prior evaluation cohorts.

Affected AI RMF function: Govern

### 4. Retraining Feedback Loop

Production observations and clinician decisions may become future training inputs. Without explicit lineage controls, previous model recommendations can indirectly influence later labels and reinforce existing errors.

Affected AI RMF function: Manage

## Harm Taxonomy

The following taxonomy uses the required harm categories for this assessment:

- Representational harm
- Allocative harm
- Quality-of-service harm
- Informational harm

## Harm-to-Lifecycle Mapping

| Harm ID | Harm Category | Scenario | Lifecycle Stage | AI RMF Function | Primary Governance Gap |
|---|---|---|---|---|---|
| HARM-001 | Representational harm | Underrepresented patient cohorts are insufficiently represented in training data | Data collection / Training | Map | Population representation and context assumptions are incomplete |
| HARM-002 | Representational harm | Historical clinical labels encode prior diagnostic or annotation bias | Labeling / Training | Measure | Label quality and subgroup error behavior are insufficiently measured |
| HARM-003 | Allocative harm | A false negative delays additional physician investigation for a patient | Deployment / Operation | Manage | Decision-support failures can influence allocation of clinical attention |
| HARM-004 | Allocative harm | Automation bias causes clinicians to prioritize model alerts over contradictory clinical evidence | Operation | Govern | Human oversight roles and decision boundaries may be weak |
| HARM-005 | Quality-of-service harm | Model accuracy degrades because production BCI signals drift from training distributions | Monitoring | Measure | Drift monitoring may not detect performance degradation early enough |
| HARM-006 | Quality-of-service harm | Model performance differs materially across patient cohorts | Validation / Monitoring | Measure | Subgroup sensitivity and specificity may not meet approved thresholds |
| HARM-007 | Quality-of-service harm | Black-box outputs lack sufficient explanation for safe clinician interpretation | Deployment / Operation | Govern | Conventional technical controls do not fully address explainability |
| HARM-008 | Quality-of-service harm | Adversarial or corrupted neural-signal input causes incorrect classification | Deployment | Manage | Input integrity and robustness controls may be insufficient |
| HARM-009 | Informational harm | Model inversion exposes sensitive neural or patient-associated information | Deployment | Manage | Privacy protections may not address AI-specific inference leakage |
| HARM-010 | Informational harm | Sensitive clinical metadata is retained unnecessarily during model development | Data preparation | Govern | Data minimization and retention requirements may be inadequate |
| HARM-011 | Informational harm | Third-party model provenance gaps prevent assurance that sensitive data was lawfully sourced | Acquisition | Govern | Supplier evidence and provenance are incomplete |
| HARM-012 | Quality-of-service harm | Retraining introduces regression or subgroup disparity without re-validation | Retraining | Manage | Change control does not guarantee re-validation before release |

## Harm Coverage by Lifecycle Stage

| Lifecycle Stage | Representational | Allocative | Quality-of-Service | Informational |
|---|---:|---:|---:|---:|
| Data collection | Yes | No | No | Yes |
| Labeling | Yes | No | Yes | No |
| Data preparation | Yes | No | Yes | Yes |
| Training | Yes | No | Yes | No |
| Validation | Yes | No | Yes | No |
| Acquisition | No | No | Yes | Yes |
| Deployment | No | Yes | Yes | Yes |
| Operation | No | Yes | Yes | Yes |
| Monitoring | No | Yes | Yes | No |
| Retraining | Yes | No | Yes | Yes |

## AI RMF Function Coverage

### Govern

Governance gaps include:

- Black-box explainability accountability
- Human oversight expectations
- Supplier provenance assurance
- Data retention and privacy accountability
- Authorization requirements for model change

### Map

Mapping gaps include:

- Incomplete representation of patient cohorts
- Unsupported populations
- Clinical context assumptions
- Device and acquisition variability
- Foreseeable misuse of AI output as an autonomous diagnosis

### Measure

Measurement gaps include:

- Cohort-specific performance
- Label quality
- Bias metrics
- Explainability adequacy
- Production drift
- Robustness testing

### Manage

Management gaps include:

- Retraining triggers
- Rollback criteria
- Human override
- Adversarial input handling
- Privacy incident response
- Re-validation after material changes

## Black-Box Explainability Gap

The system uses a black-box neural network. Traditional information-system controls can provide integrity, monitoring, change management, privacy, access control, and risk-management safeguards, but they do not by themselves guarantee that a clinician can understand why a specific model prediction occurred.

This risk therefore requires AI-specific compensating safeguards, including:

- Feature-attribution evidence where technically feasible
- Clinician-facing explanation interfaces
- Confidence and uncertainty communication
- Human-in-the-loop decision authority
- Structured clinician usability testing
- Documented limitations for unsupported explanations
- Residual-risk acceptance where sufficient interpretability cannot be technically achieved

## Feedback-Loop Risk

Clinical AI systems can create a feedback loop:

    Model recommendation
            │
            ▼
    Clinician observes output
            │
            ▼
    Clinical judgment may be influenced
            │
            ▼
    Outcome / label captured
            │
            ▼
    Data enters future retraining set
            │
            ▼
    Future model learns from potentially influenced labels

Without explicit lineage tracking and independent review, this loop can amplify automation bias or historical model errors.

Required governance safeguards include:

- Distinguish human-generated labels from AI-assisted labels
- Preserve provenance of retraining records
- Review retraining datasets for model-influenced outcomes
- Require cohort-level re-validation
- Require authorization review for material model changes

## Required Evidence for Authorization

The authorization package should retain evidence showing:

- Dataset source and ownership
- Data-use authorization
- Patient cohort composition
- Device and acquisition characteristics
- Label-generation methodology
- Preprocessing configuration
- Feature-engineering version
- Training-run metadata
- Model artifact hash
- Validation results
- Bias and subgroup-performance reports
- Explainability evaluation
- Production drift monitoring
- Retraining lineage
- Supplier provenance evidence
- Human-oversight procedures

## Conclusion

The most significant governance risks are not limited to model accuracy. They arise from incomplete provenance, cohort bias, black-box decision logic, automation bias, sensitive neural-data exposure, and lifecycle changes that can invalidate previous authorization evidence.

The lineage assessment identifies several partially verifiable or unverifiable links, particularly around historical cohort metadata, clinical labeling, third-party model provenance, and retraining feedback loops. These gaps require explicit governance treatment rather than assuming that conventional information-system controls alone are sufficient.
