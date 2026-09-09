#!/usr/bin/env python3

from pathlib import Path
import json

import numpy as np
import pandas as pd


SUMMARY_PATH = Path(
    "output/risk_summary.json"
)

FACTORS_PATH = Path(
    "data/fair_factors.csv"
)

REPORT_PATH = Path(
    "risk_report.md"
)


def money(value: float) -> str:
    return f"${value:,.0f}"


def pct(value: float) -> str:
    return f"{value:.1f}%"


def main():
    if not SUMMARY_PATH.exists():
        raise FileNotFoundError(
            "output/risk_summary.json missing"
        )

    if not FACTORS_PATH.exists():
        raise FileNotFoundError(
            "data/fair_factors.csv missing"
        )

    with open(
        SUMMARY_PATH,
        "r",
        encoding="utf-8",
    ) as handle:
        summary = json.load(
            handle
        )

    factors = pd.read_csv(
        FACTORS_PATH
    )

    baseline = summary[
        "baseline"
    ]

    improved = summary[
        "improved_control"
    ]

    reduction = summary[
        "risk_reduction"
    ]

    baseline_mean = float(
        baseline["mean"]
    )

    baseline_p50 = float(
        baseline["p50"]
    )

    baseline_p90 = float(
        baseline["p90"]
    )

    baseline_p95 = float(
        baseline["p95"]
    )

    baseline_p99 = float(
        baseline["p99"]
    )

    baseline_cvar95 = float(
        baseline["cvar95"]
    )

    improved_mean = float(
        improved["mean"]
    )

    improved_p50 = float(
        improved["p50"]
    )

    improved_p90 = float(
        improved["p90"]
    )

    improved_p95 = float(
        improved["p95"]
    )

    p95_reduction = float(
        reduction[
            "p95_reduction_pct"
        ]
    )

    mean_reduction = float(
        reduction[
            "mean_reduction_pct"
        ]
    )

    annual_mean_savings = (
        baseline_mean
        - improved_mean
    )

    p95_savings = (
        baseline_p95
        - improved_p95
    )

    factor_table = factors[
        [
            "factor",
            "node_group",
            "min",
            "most_likely",
            "max",
            "unit",
            "distribution",
        ]
    ].to_markdown(
        index=False
    )

    report = f"""# Quantitative Cyber Risk Report

## Executive Summary

The modeled scenario is unauthorized access to a cloud-hosted patient records database caused by compromised third-party vendor credentials.

The FAIR Monte Carlo analysis estimates a median annualized loss exposure of {money(baseline_p50)}, with 90% of modeled annual outcomes below approximately {money(baseline_p90)} and 95% below approximately {money(baseline_p95)}. Strengthening control effectiveness by 20% reduces modeled P95 annual loss exposure to approximately {money(improved_p95)}, a reduction of {pct(p95_reduction)}.

The quantitative evidence supports a **mitigate** treatment decision focused on stronger third-party identity, access, monitoring, and privileged-access controls.

## Scenario

**Risk statement**

Unauthorized access to a cloud-hosted patient records database due to compromised third-party vendor credentials.

### Asset

Cloud-hosted patient records containing sensitive personal and healthcare-related information.

### Threat

Threat actors obtaining or abusing legitimate third-party credentials through phishing, token theft, credential compromise, session hijacking, or similar identity attacks.

### Effect

Unauthorized access may produce direct technical and response costs as well as regulatory, legal, reputational, contractual, and customer-related consequences.

---

## FAIR Decomposition

The model follows the structure:

    Risk
      |
      +-- Loss Event Frequency
      |      |
      |      +-- Threat Event Frequency
      |      |
      |      +-- Vulnerability
      |             |
      |             +-- Threat Capability
      |             |
      |             +-- Control Strength
      |
      +-- Loss Magnitude
             |
             +-- Primary Loss
             |
             +-- Secondary Loss

The simulation evaluates:

    LEF = TEF × Vulnerability

and:

    Loss Magnitude =
        Primary Loss
        + Conditional Secondary Loss

Annualized Loss Exposure is then modeled as:

    ALE = LEF × Loss Magnitude

---

## FAIR Factor Table

{factor_table}

These inputs are calibrated scenario assumptions rather than claims about a specific organization's historical loss record.

---

## Monte Carlo Method

The model was executed using {int(baseline["iterations"]):,} vectorized Monte Carlo iterations.

Native NumPy and SciPy distributions were used to maintain transparent control over the probability model.

Distribution choices include:

- Beta-PERT for bounded uncertain estimates
- Lognormal distributions for right-skewed financial loss
- Logistic transformation for Threat Capability versus Control Strength
- Conditional Bernoulli behavior for secondary loss occurrence

Negative and non-physical results are clipped before aggregation.

---

## Baseline Quantitative Results

| Metric | Annualized Loss Exposure |
|---|---:|
| Mean | {money(baseline_mean)} |
| P50 / Median | {money(baseline_p50)} |
| P90 | {money(baseline_p90)} |
| P95 | {money(baseline_p95)} |
| P99 | {money(baseline_p99)} |
| CVaR95 | {money(baseline_cvar95)} |

### Interpretation

The median is preferred over the mean as the primary central estimate because the distribution is right-skewed.

The P95 result means that approximately 95% of simulated annual loss outcomes remain below {money(baseline_p95)}, while roughly 5% exceed that value.

The CVaR95 value of {money(baseline_cvar95)} represents the average loss within the most severe 5% of modeled outcomes.

---

## Loss Exceedance Curve

![Loss Exceedance Curve](loss_exceedance_curve.png)

The curve shows the probability that annualized loss will exceed a given dollar amount.

As loss magnitude increases, exceedance probability decreases monotonically.

The P90 and P95 markers provide decision-oriented tail-risk thresholds rather than relying only on average loss.

---

## Control Sensitivity Analysis

A second simulation increased modeled Control Strength by 20%.

| Metric | Baseline | Improved Controls | Reduction |
|---|---:|---:|---:|
| Mean ALE | {money(baseline_mean)} | {money(improved_mean)} | {pct(mean_reduction)} |
| P50 | {money(baseline_p50)} | {money(improved_p50)} | {pct((baseline_p50-improved_p50)/baseline_p50*100)} |
| P90 | {money(baseline_p90)} | {money(improved_p90)} | {pct((baseline_p90-improved_p90)/baseline_p90*100)} |
| P95 | {money(baseline_p95)} | {money(improved_p95)} | {pct(p95_reduction)} |

Estimated reduction in mean annualized exposure:

    {money(annual_mean_savings)}

Estimated reduction in P95 tail exposure:

    {money(p95_savings)}

![Control Sensitivity Comparison](control_sensitivity_comparison.png)

The sensitivity run demonstrates that stronger controls produce measurable financial risk reduction rather than merely improving a qualitative risk score.

---

## Recommended Risk Treatment

### Recommendation: Mitigate

The recommended treatment is to reduce the probability that compromised vendor credentials can create a successful loss event.

Priority controls should include:

- phishing-resistant multi-factor authentication
- conditional access for third-party identities
- privileged-access management
- time-bounded vendor access
- stronger credential and token lifecycle management
- continuous vendor-session monitoring
- anomalous-login detection
- access reviews
- rapid credential revocation
- vendor-specific logging and alerting

### Cost-Benefit Decision Rule

The model estimates approximately {money(annual_mean_savings)} of reduction in mean annualized exposure from a 20% improvement in Control Strength.

A rational mitigation investment should therefore be evaluated against the expected reduction in loss exposure.

For example, if the annualized implementation and operating cost of the proposed control package is materially below the modeled risk reduction, the mitigation has a favorable quantitative business case.

This analysis does not state that {money(annual_mean_savings)} is a guaranteed saving. It represents the modeled change in expected annualized loss under the stated assumptions.

---

## Alternative Risk Treatment Options

### Accept

Acceptance may be appropriate if:

- risk falls within formally approved appetite
- treatment cost exceeds expected benefit
- residual exposure is explicitly accepted by accountable leadership

The baseline P95 result should be considered before accepting the risk.

### Transfer

Transfer mechanisms may include:

- cyber insurance
- vendor indemnification
- contractual liability allocation
- financial guarantees

Transfer can reduce financial impact but generally does not remove operational or regulatory responsibility.

### Avoid

Avoidance would require eliminating the risky activity, such as removing the third-party access path or discontinuing the relevant service relationship.

This may be disproportionate if access can be safely retained through stronger controls.

### Mitigate

Mitigation is preferred because the sensitivity model demonstrates measurable reduction in both central and tail exposure.

---

## CGRC Risk Communication Alignment

This output supports quantitative risk communication by documenting:

- the risk scenario
- assets and threat conditions
- explicit assumptions
- uncertainty ranges
- likelihood-related factors
- financial impact ranges
- treatment options
- control effectiveness sensitivity
- residual risk
- executive-level decision metrics
- monitoring thresholds

The results can be incorporated into ongoing governance and risk-monitoring processes rather than treated as a one-time assessment.

---

## Recommended Monitoring Indicators

The following indicators should be monitored over time:

- number of active vendor identities
- privileged third-party accounts
- MFA coverage
- phishing-resistant MFA coverage
- anomalous vendor login frequency
- denied conditional-access events
- stale vendor credentials
- access-review exceptions
- vendor credential compromise events
- incident-response cost
- regulatory notification events
- observed control effectiveness

Material changes to these indicators should trigger recalibration of the FAIR input ranges.

---

## Assumptions

The model assumes:

1. Threat Event Frequency is estimated as an annual range rather than a fixed count.
2. Threat Capability and Control Strength are uncertain bounded variables.
3. Vulnerability is derived from the relationship between threat capability and resistance strength.
4. Primary loss occurs when the modeled loss event occurs.
5. Secondary loss does not occur in every event.
6. Financial losses are represented in USD.
7. Regulatory and reputation losses have right-skewed uncertainty.
8. The 20% improvement scenario modifies Control Strength while holding other factors constant.
9. Input ranges represent calibrated scenario estimates rather than authoritative historical observations.

---

## Limitations

### Data Quality

The analysis does not use organization-specific:

- breach-loss history
- vendor identity telemetry
- regulatory case history
- insurance claims
- incident-response cost records
- customer churn statistics

Results should therefore be interpreted as scenario-based estimates.

### Calibration

The accuracy of Monte Carlo output cannot exceed the quality of its input assumptions.

As better evidence becomes available, the min, most-likely, and max estimates should be recalibrated.

### Dependency Simplification

The model simplifies some relationships among:

- event frequency
- control effectiveness
- loss magnitude
- secondary loss

Real-world variables may be correlated.

### Regulatory Impact

Regulatory exposure varies by:

- jurisdiction
- organization type
- affected data
- incident severity
- regulator interpretation
- statutory requirements
- remediation behavior

The simulated regulatory loss should therefore not be interpreted as a legal prediction.

### Control Improvement

The 20% control-strength improvement is a sensitivity scenario, not a claim that any particular technical product will produce exactly that improvement.

---

## Decision Summary

Baseline median annualized loss exposure:

    {money(baseline_p50)}

Baseline P95 annualized loss exposure:

    {money(baseline_p95)}

Improved-control P95 exposure:

    {money(improved_p95)}

Modeled P95 reduction:

    {pct(p95_reduction)}

Recommended treatment:

    MITIGATE

Decision rationale:

    Strengthening third-party identity and access controls produces
    measurable reduction in both expected and tail financial exposure.

"""

    REPORT_PATH.write_text(
        report,
        encoding="utf-8",
    )

    print(
        f"PASS | Report written to {REPORT_PATH}"
    )

    print(
        f"Baseline P95: {money(baseline_p95)}"
    )

    print(
        f"Improved P95: {money(improved_p95)}"
    )

    print(
        f"P95 reduction: {pct(p95_reduction)}"
    )


if __name__ == "__main__":
    main()
