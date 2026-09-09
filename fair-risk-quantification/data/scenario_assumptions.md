# FAIR Scenario Decomposition

## Risk Scenario

Unauthorized access to a cloud-hosted patient records database due to compromised third-party vendor credentials.

## Scope

The analysis models annual financial exposure associated with unauthorized access resulting from a third-party credential compromise.

The scenario assumes:

- The database contains sensitive patient records.
- A third-party vendor has legitimate access to part of the cloud environment.
- Vendor credentials may be stolen, phished, replayed, or otherwise compromised.
- Existing controls reduce but do not eliminate the probability of successful unauthorized access.
- Financial loss may include both direct operational loss and secondary regulatory or reputational consequences.

## FAIR Decomposition

    Risk
      |
      +-- Loss Event Frequency (LEF)
      |      |
      |      +-- Threat Event Frequency (TEF)
      |      |
      |      +-- Vulnerability
      |             |
      |             +-- Threat Capability (TC)
      |             |
      |             +-- Control / Resistance Strength (CS)
      |
      +-- Loss Magnitude (LM)
             |
             +-- Primary Loss Magnitude (PLM)
             |      |
             |      +-- Incident Response
             |      +-- System Recovery
             |      +-- Legal / Notification
             |
             +-- Secondary Loss Magnitude (SLM)
                    |
                    +-- Conditional Secondary Loss Probability
                    +-- Regulatory Impact
                    +-- Reputation / Attrition
                    +-- Third-Party Dispute

## Loss Event Frequency

FAIR represents Loss Event Frequency as a function of threat activity and vulnerability.

    LEF = TEF × Vulnerability

Threat Event Frequency represents the expected number of relevant credential-compromise threat events within one year.

Vulnerability represents the probability that a threat event produces a successful loss event.

## Vulnerability Model

Vulnerability is not modeled as an independent arbitrary percentage.

Instead, it is derived from the relationship between:

    Threat Capability
            versus
    Control / Resistance Strength

The simulation will convert the difference between Threat Capability and Control Strength into a bounded probability.

This prevents vulnerability from being modeled independently of the factors that are supposed to determine it.

## Threat Event Frequency

Estimated annual range:

    Minimum:      1 event/year
    Most likely:  4 events/year
    Maximum:     12 events/year

Rationale:

Third-party credentials are attractive targets because they may provide trusted access paths into cloud services. The estimate assumes several meaningful credential-compromise attempts per year while preserving uncertainty for both low-activity and elevated-threat conditions.

## Threat Capability

Estimated percentile range:

    Minimum:      45
    Most likely:  70
    Maximum:      95

Threat Capability represents the relative capability of actors attempting to compromise and use vendor credentials.

The range covers:

- Commodity phishing and credential theft
- Credential stuffing or token theft
- Skilled cloud-access abuse
- More sophisticated identity-focused intrusion activity

## Control Strength

Estimated percentile range:

    Minimum:      50
    Most likely:  72
    Maximum:      92

Control Strength represents resistance provided by measures such as:

- Multi-factor authentication
- Conditional access
- Privileged access restrictions
- Third-party access governance
- Session monitoring
- Cloud audit logging
- Credential rotation
- Vendor security requirements

The range intentionally overlaps Threat Capability because control effectiveness is uncertain and successful compromise remains possible.

## Primary Loss Magnitude

Primary losses occur directly because the event happened.

### Incident Response

Estimated range:

    $75,000
    $220,000 most likely
    $900,000 maximum

Includes:

- Forensic investigation
- Incident containment
- External specialists
- Internal response labor
- Breach-management coordination

### System Recovery

Estimated range:

    $40,000
    $130,000 most likely
    $600,000 maximum

Includes:

- Vendor credential revocation
- Identity reset
- Access remediation
- Cloud configuration review
- Service restoration
- Validation activities

### Legal and Notification

Estimated range:

    $50,000
    $175,000 most likely
    $700,000 maximum

Includes:

- External counsel
- Notification analysis
- Patient communication
- Contractual notification
- Breach administration

## Secondary Loss Event Frequency

Secondary effects do not occur for every successful loss event.

Conditional probability estimate:

    Minimum:      20%
    Most likely:  55%
    Maximum:      90%

This models uncertainty around whether a breach generates additional regulatory, reputational, contractual, or commercial consequences.

## Secondary Loss Magnitude

### Regulatory Impact

Estimated range:

    $100,000
    $650,000 most likely
    $4,000,000 maximum

This includes:

- Regulatory investigation
- Corrective actions
- External assurance
- Potential penalties
- Additional compliance obligations

The model does not assume that the statutory maximum fine is the expected loss.

### Reputation and Customer Attrition

Estimated range:

    $150,000
    $900,000 most likely
    $6,000,000 maximum

Includes:

- Customer attrition
- Contract delays
- Lost renewals
- Reputation-management costs
- Communications
- Reduced commercial confidence

### Third-Party Dispute

Estimated range:

    $50,000
    $300,000 most likely
    $1,800,000 maximum

Includes:

- Contractual dispute
- Supplier remediation
- Replacement supplier expense
- Recovery actions
- Additional assurance activity

## Calibration Philosophy

The values are scenario-analysis assumptions rather than claims about a specific organization's historical loss data.

The estimates are calibrated by:

1. Using ranges rather than single-point guesses.
2. Separating frequency from magnitude.
3. Separating primary loss from secondary loss.
4. Treating regulatory loss as uncertain rather than guaranteed.
5. Modeling control effectiveness independently from threat capability.
6. Maintaining wide upper bounds for low-frequency, high-impact outcomes.
7. Preserving a right-skewed loss structure suitable for Monte Carlo analysis.

## Modeling Decision

The simulation will use native NumPy and SciPy rather than relying on pyfair as the core engine.

Reasons:

- Full control over distribution design
- Explicit PERT implementation
- Transparent vectorized logic
- Easier testing of edge cases
- Better reproducibility
- No dependency on an old alpha library

## Currency

All loss magnitude estimates are modeled in United States dollars for consistency in quantitative reporting.

This does not imply that all underlying costs or penalties would actually be incurred in USD.
