#!/usr/bin/env python3

import csv
from pathlib import Path

import pandas as pd


REGISTER_PATH = Path(
    "register/risk_register.csv"
)

OUTPUT_PATH = Path(
    "artifacts/control_crosswalk.csv"
)


CROSSWALK = {
    "AI-RISK-001": {
        "ai_600_1_practice":
            "AI600-SUP-06 - Measurement and Monitoring",
        "sp800_53_control":
            "SI-4; RA-3",
        "justification":
            "Continuous monitoring and risk assessment support detection "
            "and analysis of production distribution and performance drift. "
            "AI-specific drift thresholds remain necessary.",
        "residual_risk_after_control":
            "Medium",
    },

    "AI-RISK-002": {
        "ai_600_1_practice":
            "AI600-SUP-01 - Harmful Bias and Homogenization",
        "sp800_53_control":
            "RA-3; PT-2",
        "justification":
            "Risk assessment and privacy-processing controls support review "
            "of dataset composition and processing context, but subgroup "
            "fairness must be measured using AI-specific validation.",
        "residual_risk_after_control":
            "High",
    },

    "AI-RISK-003": {
        "ai_600_1_practice":
            "AI600-SUP-08 - Transparency and Explainability",
        "sp800_53_control":
            "NO ADEQUATE SP 800-53 MAPPING",
        "justification":
            "SP 800-53 provides governance, assessment, integrity, and "
            "monitoring safeguards but does not guarantee that a black-box "
            "neural-network prediction is clinically interpretable. "
            "Compensating AI-specific explainability and human-oversight "
            "controls are required.",
        "residual_risk_after_control":
            "High",
    },

    "AI-RISK-004": {
        "ai_600_1_practice":
            "AI600-SUP-03 - Information Security",
        "sp800_53_control":
            "SI-7; SI-4",
        "justification":
            "Software, information, and system integrity controls combined "
            "with monitoring can detect corrupted or manipulated inputs. "
            "Adversarial robustness testing remains an AI-specific safeguard.",
        "residual_risk_after_control":
            "Medium",
    },

    "AI-RISK-005": {
        "ai_600_1_practice":
            "AI600-SUP-05 - Value Chain and Component Integration",
        "sp800_53_control":
            "SR-3; SR-11",
        "justification":
            "Supply-chain risk management and component authenticity controls "
            "support supplier assurance, provenance review, and verification "
            "of externally sourced model components.",
        "residual_risk_after_control":
            "High",
    },

    "AI-RISK-006": {
        "ai_600_1_practice":
            "AI600-SUP-04 - Data Privacy",
        "sp800_53_control":
            "PT-2; AC-4",
        "justification":
            "Privacy processing and information-flow controls reduce exposure "
            "of sensitive neural and patient-linked information. Model inversion "
            "risk still requires AI-specific privacy testing.",
        "residual_risk_after_control":
            "Medium",
    },

    "AI-RISK-007": {
        "ai_600_1_practice":
            "AI600-SUP-02 - Human-AI Configuration",
        "sp800_53_control":
            "AT-3; RA-3",
        "justification":
            "Role-based training and risk assessment can reduce unsafe reliance "
            "on automated outputs, but automation bias cannot be eliminated "
            "through conventional security controls alone. Human-in-the-loop "
            "decision procedures are required.",
        "residual_risk_after_control":
            "High",
    },

    "AI-RISK-008": {
        "ai_600_1_practice":
            "AI600-SUP-07 - Governance and Accountability",
        "sp800_53_control":
            "SI-7; RA-3; RA-9",
        "justification":
            "Integrity, risk assessment, and criticality analysis support "
            "controlled model changes. AI-specific cohort re-validation "
            "and authorization gates are required before replacement models "
            "enter production.",
        "residual_risk_after_control":
            "Medium",
    },
}


def main() -> None:
    if not REGISTER_PATH.exists():
        raise FileNotFoundError(
            f"Risk register missing: {REGISTER_PATH}"
        )

    register = pd.read_csv(
        REGISTER_PATH
    )

    rows = []

    for _, risk in register.iterrows():
        risk_id = str(
            risk["risk_id"]
        ).strip()

        mapping = CROSSWALK.get(
            risk_id
        )

        if mapping is None:
            raise ValueError(
                f"No crosswalk mapping for {risk_id}"
            )

        rows.append(
            {
                "risk_id":
                    risk_id,

                "ai_600_1_practice":
                    mapping[
                        "ai_600_1_practice"
                    ],

                "sp800_53_control":
                    mapping[
                        "sp800_53_control"
                    ],

                "justification":
                    mapping[
                        "justification"
                    ],

                "residual_risk_after_control":
                    mapping[
                        "residual_risk_after_control"
                    ],
            }
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "risk_id",
                "ai_600_1_practice",
                "sp800_53_control",
                "justification",
                "residual_risk_after_control",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Created {OUTPUT_PATH}"
    )

    print(
        f"Crosswalk entries: {len(rows)}"
    )


if __name__ == "__main__":
    main()
