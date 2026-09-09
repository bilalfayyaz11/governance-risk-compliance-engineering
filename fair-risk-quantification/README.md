# FAIR Risk Quantification Engine

## Overview

This implementation provides a quantitative cyber-risk analysis workflow based on FAIR concepts and Monte Carlo simulation.

The modeled scenario is:

Unauthorized access to a cloud-hosted patient records database due to compromised third-party vendor credentials.

The workflow converts uncertain threat, control, frequency, and loss assumptions into a dollar-denominated Annualized Loss Exposure distribution.

It combines:

- FAIR scenario decomposition
- calibrated uncertainty ranges
- Beta-PERT distributions
- lognormal loss modeling
- vectorized Monte Carlo simulation
- Loss Exceedance Curves
- tail-risk metrics
- control sensitivity analysis
- executive risk reporting

## Architecture

    FAIR Scenario
         |
         +-- Threat Event Frequency
         |
         +-- Threat Capability
         |
         +-- Control Strength
         |
         +-- Vulnerability
         |
         +-- Primary Loss
         |
         +-- Secondary Loss
                 |
                 v
    ┌─────────────────────────────┐
    │   Python Risk Engine        │
    │                             │
    │ • Beta-PERT sampling        │
    │ • Lognormal sampling        │
    │ • Logistic vulnerability    │
    │ • Conditional loss logic    │
    │ • Vectorized simulation     │
    └──────────────┬──────────────┘
                   |
                   v
    ┌─────────────────────────────┐
    │ Monte Carlo Simulation      │
    │                             │
    │ 50,000+ iterations          │
    │ ALE distribution            │
    │ P10 / P50 / P90 / P95      │
    │ P99 / CVaR95                │
    └──────────────┬──────────────┘
                   |
          ┌────────┴─────────┐
          |                  |
          v                  v
    Loss Exceedance     Control Sensitivity
    Curve               Comparison
          |                  |
          └────────┬─────────┘
                   |
                   v
          Executive Risk Report

## FAIR Model

The model follows:

    LEF = TEF × Vulnerability

where:

    TEF = Threat Event Frequency

and Vulnerability is derived from:

    Threat Capability
            versus
    Control Strength

Loss Magnitude is modeled as:

    LM = Primary Loss + Secondary Loss

Annualized Loss Exposure is then:

    ALE = LEF × LM

## Scenario

### Asset

Cloud-hosted patient records containing sensitive personal and healthcare information.

### Threat

A threat actor obtains or abuses valid third-party vendor credentials.

Possible paths include:

- phishing
- token theft
- credential compromise
- session hijacking
- unauthorized reuse of trusted access

### Loss Event

Compromised credentials are successfully used to gain unauthorized access to the patient records environment.

## FAIR Factors

The input factors are stored in:

    data/fair_factors.csv

Core factors include:

- Threat Event Frequency
- Threat Capability
- Control Strength
- Vulnerability
- Loss Event Frequency
- Primary Loss Magnitude
- Secondary Loss Probability
- Secondary Loss Magnitude

Each uncertain factor is represented with:

- minimum
- most likely
- maximum
- unit
- distribution
- assumption

## Distribution Design

### Beta-PERT

Bounded uncertain estimates are modeled with Beta-PERT.

The implementation reparameterizes the Beta distribution using:

    alpha = 1 + lambda × (mode - min) / (max - min)

    beta = 1 + lambda × (max - mode) / (max - min)

The sampled value is then rescaled back to:

    [min, max]

This is used for factors such as:

- Threat Event Frequency
- Threat Capability
- Control Strength
- Primary Loss
- Secondary Loss Probability

### Lognormal

Right-skewed financial losses are modeled using bounded lognormal approximations.

This is used for:

- regulatory impact
- reputation and attrition loss
- third-party dispute cost

The sampled values are clipped to calibrated physical bounds.

## Vulnerability Model

Vulnerability is not sampled independently.

It is derived from the relationship between:

    Threat Capability
            and
    Control Strength

The difference is transformed using a logistic function.

Conceptually:

    stronger threat capability
            ->
    higher vulnerability

    stronger control strength
            ->
    lower vulnerability

This prevents Vulnerability from being an arbitrary disconnected probability.

## Reusable Risk Engine

The core implementation is located in:

    scripts/fair_model.py

It provides:

    FairNode

A reusable distribution node capable of sampling:

- PERT
- lognormal
- Poisson
- Beta
- constant values

It also provides:

    build_risk_model()

which composes FAIR factors into a vectorized Annualized Loss Exposure model.

## Monte Carlo Simulation

The simulation workflow is implemented in:

    scripts/run_simulation.py

The baseline analysis runs:

    50,000 iterations

The control-sensitivity scenario runs another:

    50,000 iterations

The model is vectorized using NumPy rather than iterating through individual simulation events in Python.

This improves:

- execution speed
- reproducibility
- maintainability
- numerical consistency

## Risk Metrics

The analysis calculates:

- Mean ALE
- P10
- P50
- P90
- P95
- P99
- VaR-style P95
- CVaR95
- Maximum modeled exposure

Median and percentile metrics are emphasized because right-skewed cyber-loss distributions can make the mean misleading when used alone.

## Loss Exceedance Curve

The generated chart:

    loss_exceedance_curve.png

shows:

    X-axis = Annualized Loss Exposure

    Y-axis = Probability of Exceeding That Loss

The exceedance probability is computed from the sorted Monte Carlo distribution.

The curve is validated to ensure it is monotonically decreasing.

P90 and P95 thresholds are included to provide executive tail-risk context.

## Control Sensitivity Analysis

The model also evaluates:

    Control Strength +20%

while holding the other scenario assumptions constant.

The resulting comparison is stored in:

    control_sensitivity_comparison.png

The purpose is to quantify how improved controls affect:

- median loss
- P90 loss
- P95 loss
- mean Annualized Loss Exposure

This converts control effectiveness into a measurable financial risk reduction rather than only a qualitative rating.

## Board-Ready Risk Report

The report generator is implemented in:

    scripts/generate_report.py

The resulting report is:

    risk_report.md

It includes:

- Executive Summary
- Scenario Description
- FAIR Factor Table
- Monte Carlo methodology
- Baseline quantitative results
- Loss Exceedance Curve
- Control sensitivity comparison
- CGRC-aligned treatment recommendation
- assumptions
- limitations
- monitoring indicators

## Risk Treatment

The recommended treatment is:

    MITIGATE

The primary reason is that increased Control Strength demonstrated measurable reduction in modeled tail risk.

Priority mitigation areas include:

- phishing-resistant MFA
- conditional access
- privileged-access management
- time-bounded vendor access
- third-party session monitoring
- credential lifecycle management
- rapid access revocation
- anomalous-login detection
- periodic vendor access review

## Cost-Benefit Logic

The simulation can support a quantitative treatment decision by comparing:

    annualized control cost

against:

    modeled annual loss reduction

If the expected reduction in Annualized Loss Exposure materially exceeds the annualized treatment cost, the control package has a stronger financial justification.

The modeled reduction should not be interpreted as a guaranteed saving.

It represents expected change under the stated assumptions.

## CGRC Risk Communication Alignment

This implementation supports risk communication by documenting:

- scenario definition
- asset exposure
- threat conditions
- explicit assumptions
- likelihood uncertainty
- financial impact uncertainty
- tail-risk metrics
- residual risk
- treatment options
- sensitivity analysis
- control-effectiveness implications
- monitoring indicators

## Jupyter Analysis

The complete executable notebook is:

    fair_risk_analysis.ipynb

It contains:

- FAIR factor calibration
- baseline Monte Carlo simulation
- quantitative metrics
- Loss Exceedance Curve
- improved-control scenario
- control comparison
- treatment recommendation
- limitations

The notebook was validated using:

    jupyter nbconvert --execute --to notebook --inplace fair_risk_analysis.ipynb

This confirms that the analysis executes end-to-end without notebook errors.

## Repository Structure

    fair-risk-quantification/
    ├── README.md
    ├── fair_risk_analysis.ipynb
    ├── risk_report.md
    ├── loss_exceedance_curve.png
    ├── control_sensitivity_comparison.png
    ├── ale_samples.npy
    ├── ale_samples_improved.npy
    ├── data/
    │   ├── fair_factors.csv
    │   └── scenario_assumptions.md
    ├── scripts/
    │   ├── fair_model.py
    │   ├── run_simulation.py
    │   ├── generate_report.py
    │   └── validate_factors.py
    └── output/
        ├── risk_summary.csv
        └── risk_summary.json

## Tools Used

- Python 3
- NumPy
- pandas
- SciPy
- Matplotlib
- Jupyter
- nbformat
- nbconvert
- FAIR quantitative risk concepts
- Monte Carlo simulation

## Key Skills Demonstrated

- quantitative cyber-risk modeling
- FAIR taxonomy decomposition
- uncertainty modeling
- Monte Carlo simulation
- Beta-PERT implementation
- lognormal loss modeling
- vectorized numerical computing
- tail-risk analysis
- Loss Exceedance Curves
- VaR-style metrics
- CVaR analysis
- sensitivity analysis
- control-effectiveness modeling
- quantitative risk communication
- executive risk reporting
- cost-benefit risk treatment analysis

## Real-World Use Case

Organizations often evaluate cyber risk using qualitative labels such as:

    Low
    Medium
    High
    Critical

Those labels do not answer:

- How much could the organization lose?
- What is the probability of exceeding a financial threshold?
- How large is the tail exposure?
- How much financial risk could stronger controls reduce?
- Is mitigation economically justified?

This implementation converts uncertain technical and business assumptions into a financial loss distribution that can support those decisions.

## Assumptions

The implementation uses calibrated scenario estimates rather than organization-specific historical evidence.

Assumptions include:

- threat frequency is uncertain
- threat capability varies
- control strength varies
- successful compromise probability depends on threat-versus-control strength
- secondary losses are conditional
- regulatory exposure is uncertain
- financial losses are right-skewed
- stronger controls affect vulnerability rather than directly reducing loss magnitude

## Limitations

The analysis does not include organization-specific:

- incident history
- vendor identity telemetry
- regulatory case history
- insurance claims
- customer churn records
- historical response cost
- actual control-testing evidence

The model should be recalibrated when better evidence becomes available.

The 20% improvement in Control Strength is a sensitivity scenario and should not be interpreted as a guarantee that any particular technology will produce that exact improvement.

## Engineering Decisions

### Native NumPy and SciPy Instead of Dependence on pyfair

The quantitative engine uses native scientific Python components.

This provides:

- transparent distribution logic
- explicit PERT implementation
- easier testing
- predictable vectorization
- fewer dependency risks
- better control over assumptions

### Reproducible Random Seeds

Distribution nodes use deterministic seeds to make repeated analysis reproducible.

### Separation of Model and Reporting

The system separates:

- factor definition
- risk-engine logic
- simulation
- visualization
- executive reporting

This allows the risk engine to be reused with different scenarios without rewriting the complete workflow.

### Explicit Calibration

Input ranges and assumptions remain visible rather than being hidden inside the simulation code.

This improves auditability and makes future recalibration easier.
