# AI Risk Treatment Plan

## Purpose

This plan defines treatment actions for unresolved AI risks associated with the clinical BCI decision-support system. Priority is driven by likelihood × impact scoring, residual risk after mapped controls, clinical safety impact, privacy exposure, and authorization relevance.

## Treatment Prioritization

| Risk ID | Initial Score | Residual Risk | Treatment | Owner | Target Date | Monitoring Cadence |
|---|---:|---|---|---|---|---|
| AI-RISK-001 | 20 | Medium | Mitigate | ML Operations Lead | 2026-10-24 | Monthly and event-driven |
| AI-RISK-002 | 20 | High | Mitigate | Data Steward | 2026-11-08 | Monthly and before model release |
| AI-RISK-003 | 20 | High | Mitigate / Accept Residual | AI Governance Lead | 2026-10-09 | Quarterly |
| AI-RISK-004 | 15 | Medium | Mitigate | Security Engineering Lead | 2026-10-24 | Continuous monitoring and quarterly testing |
| AI-RISK-005 | 16 | High | Transfer / Mitigate | Supply Chain Risk Manager | 2026-11-08 | Quarterly and supplier-change driven |
| AI-RISK-006 | 15 | Medium | Mitigate | Privacy Officer | 2026-10-24 | Quarterly and after model changes |
| AI-RISK-007 | 20 | High | Mitigate | Clinical Safety Lead | 2026-10-09 | Quarterly |
| AI-RISK-008 | 20 | Medium | Avoid / Mitigate | Model Validation Lead | 2026-10-09 | Every retraining event |

## Detailed Treatment Actions

### AI-RISK-001

- Lifecycle stage: Monitoring
- Harm category: Quality-of-service harm
- AI RMF function: Measure
- Initial risk score: 20
- Residual risk: Medium
- Treatment: Mitigate
- Owner: ML Operations Lead
- Monitoring cadence: Monthly and event-driven
- Required actions:
  - Establish production feature-distribution monitoring.
  - Define cohort-level drift thresholds.
  - Trigger investigation when performance or distribution drift exceeds approved tolerances.
  - Require documented review before retraining is initiated.

### AI-RISK-002

- Lifecycle stage: Training
- Harm category: Representational harm
- AI RMF function: Map
- Initial risk score: 20
- Residual risk: High
- Treatment: Mitigate
- Owner: Data Steward
- Monitoring cadence: Monthly and before model release
- Required actions:
  - Document cohort representation across training and validation datasets.
  - Measure subgroup false-positive and false-negative rates.
  - Expand or rebalance data where clinically appropriate.
  - Require cohort-level validation before authorization.

### AI-RISK-003

- Lifecycle stage: Deployment
- Harm category: Quality-of-service harm
- AI RMF function: Govern
- Initial risk score: 20
- Residual risk: High
- Treatment: Mitigate / Accept Residual
- Owner: AI Governance Lead
- Monitoring cadence: Quarterly
- Required actions:
  - Provide feature-attribution evidence where technically feasible.
  - Display model confidence and known limitations to clinicians.
  - Retain human-in-the-loop decision authority.
  - Conduct clinician usability and trust evaluation.
  - Escalate remaining black-box limitations for explicit residual-risk acceptance.

### AI-RISK-008

- Lifecycle stage: Retraining
- Harm category: Quality-of-service harm
- AI RMF function: Manage
- Initial risk score: 20
- Residual risk: Medium
- Treatment: Avoid / Mitigate
- Owner: Model Validation Lead
- Monitoring cadence: Every retraining event
- Required actions:
  - Block deployment of retrained models until independent validation is complete.
  - Repeat cohort-level fairness and performance testing.
  - Compare replacement models against the authorized baseline.
  - Require governance approval for material model changes.

### AI-RISK-007

- Lifecycle stage: Operation
- Harm category: Allocative harm
- AI RMF function: Govern
- Initial risk score: 20
- Residual risk: High
- Treatment: Mitigate
- Owner: Clinical Safety Lead
- Monitoring cadence: Quarterly
- Required actions:
  - Train clinicians on AI limitations and automation bias.
  - Require independent clinical confirmation before action.
  - Display AI output as decision-support rather than diagnosis.
  - Review override behavior and excessive reliance indicators.

### AI-RISK-005

- Lifecycle stage: Acquisition
- Harm category: Informational harm
- AI RMF function: Govern
- Initial risk score: 16
- Residual risk: High
- Treatment: Transfer / Mitigate
- Owner: Supply Chain Risk Manager
- Monitoring cadence: Quarterly and supplier-change driven
- Required actions:
  - Require supplier provenance and component documentation.
  - Contractually require disclosure of material model and dataset changes.
  - Verify model artifacts and supplier attestations.
  - Reject unsupported components when provenance cannot meet minimum assurance requirements.

### AI-RISK-004

- Lifecycle stage: Deployment
- Harm category: Quality-of-service harm
- AI RMF function: Manage
- Initial risk score: 15
- Residual risk: Medium
- Treatment: Mitigate
- Owner: Security Engineering Lead
- Monitoring cadence: Continuous monitoring and quarterly testing
- Required actions:
  - Validate BCI signal integrity before inference.
  - Detect malformed or anomalous input patterns.
  - Perform adversarial robustness testing.
  - Monitor inference services for integrity anomalies.

### AI-RISK-006

- Lifecycle stage: Deployment
- Harm category: Informational harm
- AI RMF function: Manage
- Initial risk score: 15
- Residual risk: Medium
- Treatment: Mitigate
- Owner: Privacy Officer
- Monitoring cadence: Quarterly and after model changes
- Required actions:
  - Minimize sensitive information retained in training and inference workflows.
  - Restrict information flows through least-privilege interfaces.
  - Perform model-inversion and inference privacy testing.
  - Document authority and purpose for processing patient-linked information.

## Risk Acceptance Requirements

Residual risk may be accepted only when:

- The remaining risk is explicitly documented.
- Compensating controls are implemented and evidenced.
- Clinical safety impact has been reviewed.
- The responsible owner accepts accountability.
- The Authorizing Official approves the residual risk.
- The acceptance decision has a defined review or expiration date.

## Reauthorization Triggers

- Material model retraining
- Introduction of a new dataset
- New patient population or clinical use context
- Significant subgroup-performance degradation
- Critical privacy or security incident
- Material supplier or model-component change
- Change to signal acquisition or preprocessing
- Failure of a compensating control
