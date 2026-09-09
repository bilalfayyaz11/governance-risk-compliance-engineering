#!/usr/bin/env python3

from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List

import pandas as pd


REGISTER_PATH = Path(
    "register/risk_register.csv"
)

CROSSWALK_PATH = Path(
    "artifacts/control_crosswalk.csv"
)

TREATMENT_PLAN_PATH = Path(
    "artifacts/risk_treatment_plan.md"
)

AO_BRIEFING_PATH = Path(
    "artifacts/ao_briefing.md"
)


def compute_risk_posture(
    register_path: str,
) -> Dict[str, float]:
    """
    Load register, compute average and max risk_score,
    count unresolved risks, and return summary values.
    """
    df = pd.read_csv(
        register_path
    )

    unresolved_statuses = {
        "Open",
        "Planned",
        "Mitigating",
    }

    unresolved = df[
        df[
            "treatment_status"
        ].isin(
            unresolved_statuses
        )
    ]

    return {
        "average_risk_score":
            round(
                float(
                    df[
                        "risk_score"
                    ].mean()
                ),
                2,
            ),

        "max_risk_score":
            float(
                df[
                    "risk_score"
                ].max()
            ),

        "total_risks":
            float(
                len(df)
            ),

        "unmitigated_risks":
            float(
                len(unresolved)
            ),

        "critical_score_risks":
            float(
                (
                    df[
                        "risk_score"
                    ] >= 20
                ).sum()
            ),

        "high_score_risks":
            float(
                (
                    (
                        df[
                            "risk_score"
                        ] >= 15
                    )
                    &
                    (
                        df[
                            "risk_score"
                        ] < 20
                    )
                ).sum()
            ),
    }


TREATMENTS = {
    "AI-RISK-001": {
        "treatment": "Mitigate",
        "owner": "ML Operations Lead",
        "target_days": 45,
        "cadence": "Monthly and event-driven",
        "actions": [
            "Establish production feature-distribution monitoring.",
            "Define cohort-level drift thresholds.",
            "Trigger investigation when performance or distribution drift exceeds approved tolerances.",
            "Require documented review before retraining is initiated.",
        ],
    },

    "AI-RISK-002": {
        "treatment": "Mitigate",
        "owner": "Data Steward",
        "target_days": 60,
        "cadence": "Monthly and before model release",
        "actions": [
            "Document cohort representation across training and validation datasets.",
            "Measure subgroup false-positive and false-negative rates.",
            "Expand or rebalance data where clinically appropriate.",
            "Require cohort-level validation before authorization.",
        ],
    },

    "AI-RISK-003": {
        "treatment": "Mitigate / Accept Residual",
        "owner": "AI Governance Lead",
        "target_days": 30,
        "cadence": "Quarterly",
        "actions": [
            "Provide feature-attribution evidence where technically feasible.",
            "Display model confidence and known limitations to clinicians.",
            "Retain human-in-the-loop decision authority.",
            "Conduct clinician usability and trust evaluation.",
            "Escalate remaining black-box limitations for explicit residual-risk acceptance.",
        ],
    },

    "AI-RISK-004": {
        "treatment": "Mitigate",
        "owner": "Security Engineering Lead",
        "target_days": 45,
        "cadence": "Continuous monitoring and quarterly testing",
        "actions": [
            "Validate BCI signal integrity before inference.",
            "Detect malformed or anomalous input patterns.",
            "Perform adversarial robustness testing.",
            "Monitor inference services for integrity anomalies.",
        ],
    },

    "AI-RISK-005": {
        "treatment": "Transfer / Mitigate",
        "owner": "Supply Chain Risk Manager",
        "target_days": 60,
        "cadence": "Quarterly and supplier-change driven",
        "actions": [
            "Require supplier provenance and component documentation.",
            "Contractually require disclosure of material model and dataset changes.",
            "Verify model artifacts and supplier attestations.",
            "Reject unsupported components when provenance cannot meet minimum assurance requirements.",
        ],
    },

    "AI-RISK-006": {
        "treatment": "Mitigate",
        "owner": "Privacy Officer",
        "target_days": 45,
        "cadence": "Quarterly and after model changes",
        "actions": [
            "Minimize sensitive information retained in training and inference workflows.",
            "Restrict information flows through least-privilege interfaces.",
            "Perform model-inversion and inference privacy testing.",
            "Document authority and purpose for processing patient-linked information.",
        ],
    },

    "AI-RISK-007": {
        "treatment": "Mitigate",
        "owner": "Clinical Safety Lead",
        "target_days": 30,
        "cadence": "Quarterly",
        "actions": [
            "Train clinicians on AI limitations and automation bias.",
            "Require independent clinical confirmation before action.",
            "Display AI output as decision-support rather than diagnosis.",
            "Review override behavior and excessive reliance indicators.",
        ],
    },

    "AI-RISK-008": {
        "treatment": "Avoid / Mitigate",
        "owner": "Model Validation Lead",
        "target_days": 30,
        "cadence": "Every retraining event",
        "actions": [
            "Block deployment of retrained models until independent validation is complete.",
            "Repeat cohort-level fairness and performance testing.",
            "Compare replacement models against the authorized baseline.",
            "Require governance approval for material model changes.",
        ],
    },
}


BUSINESS_IMPACT = {
    "AI-RISK-001":
        "Undetected drift could cause clinically meaningful degradation in anomaly detection.",

    "AI-RISK-002":
        "Underrepresented cohorts could receive unequal clinical decision-support quality.",

    "AI-RISK-003":
        "Clinicians may lack sufficient reasoning evidence to safely trust or challenge model outputs.",

    "AI-RISK-004":
        "Manipulated or corrupted neural signals could generate incorrect anomaly flags.",

    "AI-RISK-005":
        "Unknown supplier provenance could introduce inherited bias, integrity, or compliance risk.",

    "AI-RISK-006":
        "Sensitive neural or patient information could be inferred or exposed.",

    "AI-RISK-007":
        "Automation bias could cause physicians to over-rely on model outputs.",

    "AI-RISK-008":
        "Unvalidated retraining could invalidate prior authorization evidence and introduce regressions.",
}


def load_inputs():
    if not REGISTER_PATH.exists():
        raise FileNotFoundError(
            f"Missing: {REGISTER_PATH}"
        )

    if not CROSSWALK_PATH.exists():
        raise FileNotFoundError(
            f"Missing: {CROSSWALK_PATH}"
        )

    register = pd.read_csv(
        REGISTER_PATH
    )

    crosswalk = pd.read_csv(
        CROSSWALK_PATH
    )

    return register, crosswalk


def build_treatment_plan(
    register: pd.DataFrame,
    crosswalk: pd.DataFrame,
) -> None:
    today = date.today()

    merged = register.merge(
        crosswalk,
        on="risk_id",
        how="left",
    )

    lines: List[str] = []

    lines.append(
        "# AI Risk Treatment Plan"
    )

    lines.append("")

    lines.append(
        "## Purpose"
    )

    lines.append("")

    lines.append(
        "This plan defines treatment actions for unresolved AI risks associated "
        "with the clinical BCI decision-support system. Priority is driven by "
        "likelihood × impact scoring, residual risk after mapped controls, "
        "clinical safety impact, privacy exposure, and authorization relevance."
    )

    lines.append("")

    lines.append(
        "## Treatment Prioritization"
    )

    lines.append("")

    lines.append(
        "| Risk ID | Initial Score | Residual Risk | Treatment | Owner | Target Date | Monitoring Cadence |"
    )

    lines.append(
        "|---|---:|---|---|---|---|---|"
    )

    for _, row in merged.iterrows():
        risk_id = row[
            "risk_id"
        ]

        treatment = TREATMENTS[
            risk_id
        ]

        target_date = (
            today
            + timedelta(
                days=treatment[
                    "target_days"
                ]
            )
        )

        lines.append(
            f"| {risk_id} "
            f"| {int(row['risk_score'])} "
            f"| {row['residual_risk_after_control']} "
            f"| {treatment['treatment']} "
            f"| {treatment['owner']} "
            f"| {target_date.isoformat()} "
            f"| {treatment['cadence']} |"
        )

    lines.append("")

    lines.append(
        "## Detailed Treatment Actions"
    )

    lines.append("")

    for _, row in merged.sort_values(
        by="risk_score",
        ascending=False,
    ).iterrows():

        risk_id = row[
            "risk_id"
        ]

        treatment = TREATMENTS[
            risk_id
        ]

        lines.append(
            f"### {risk_id}"
        )

        lines.append("")

        lines.append(
            f"- Lifecycle stage: {row['ai_lifecycle_stage']}"
        )

        lines.append(
            f"- Harm category: {row['harm_category']}"
        )

        lines.append(
            f"- AI RMF function: {row['affected_rmf_function']}"
        )

        lines.append(
            f"- Initial risk score: {int(row['risk_score'])}"
        )

        lines.append(
            f"- Residual risk: {row['residual_risk_after_control']}"
        )

        lines.append(
            f"- Treatment: {treatment['treatment']}"
        )

        lines.append(
            f"- Owner: {treatment['owner']}"
        )

        lines.append(
            f"- Monitoring cadence: {treatment['cadence']}"
        )

        lines.append(
            "- Required actions:"
        )

        for action in treatment[
            "actions"
        ]:
            lines.append(
                f"  - {action}"
            )

        lines.append("")

    lines.append(
        "## Risk Acceptance Requirements"
    )

    lines.append("")

    lines.append(
        "Residual risk may be accepted only when:"
    )

    lines.append("")

    lines.extend(
        [
            "- The remaining risk is explicitly documented.",
            "- Compensating controls are implemented and evidenced.",
            "- Clinical safety impact has been reviewed.",
            "- The responsible owner accepts accountability.",
            "- The Authorizing Official approves the residual risk.",
            "- The acceptance decision has a defined review or expiration date.",
        ]
    )

    lines.append("")

    lines.append(
        "## Reauthorization Triggers"
    )

    lines.append("")

    lines.extend(
        [
            "- Material model retraining",
            "- Introduction of a new dataset",
            "- New patient population or clinical use context",
            "- Significant subgroup-performance degradation",
            "- Critical privacy or security incident",
            "- Material supplier or model-component change",
            "- Change to signal acquisition or preprocessing",
            "- Failure of a compensating control",
        ]
    )

    TREATMENT_PLAN_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def build_ao_briefing(
    register: pd.DataFrame,
    crosswalk: pd.DataFrame,
) -> None:
    posture = compute_risk_posture(
        str(
            REGISTER_PATH
        )
    )

    merged = register.merge(
        crosswalk,
        on="risk_id",
        how="left",
    )

    unresolved = merged[
        merged[
            "treatment_status"
        ].isin(
            [
                "Open",
                "Planned",
                "Mitigating",
            ]
        )
    ].copy()

    residual_rank = {
        "Critical": 4,
        "High": 3,
        "Medium": 2,
        "Low": 1,
    }

    unresolved[
        "residual_rank"
    ] = unresolved[
        "residual_risk_after_control"
    ].map(
        residual_rank
    ).fillna(0)

    top3 = unresolved.sort_values(
        by=[
            "residual_rank",
            "risk_score",
        ],
        ascending=[
            False,
            False,
        ],
    ).head(3)

    high_residual = (
        crosswalk[
            "residual_risk_after_control"
        ].isin(
            [
                "High",
                "Critical",
            ]
        ).sum()
    )

    explainability_gap = (
        crosswalk[
            "sp800_53_control"
        ].astype(str)
        .str.contains(
            "NO ADEQUATE",
            case=False,
            na=False,
        )
        .any()
    )

    if (
        posture[
            "max_risk_score"
        ] >= 20
        or high_residual > 0
        or explainability_gap
    ):
        recommendation = (
            "AUTHORIZE WITH CONDITIONS"
        )
    else:
        recommendation = (
            "AUTHORIZE"
        )

    lines: List[str] = []

    lines.append(
        "# Authorizing Official Briefing"
    )

    lines.append("")

    lines.append(
        "## Decision Summary"
    )

    lines.append("")

    lines.append(
        f"**Recommendation: {recommendation}**"
    )

    lines.append("")

    lines.append(
        "The clinical BCI decision-support system presents material AI-specific "
        "risk but can proceed under controlled authorization conditions if the "
        "identified high-residual risks, human-oversight requirements, model-change "
        "controls, provenance gaps, and explainability limitations remain subject "
        "to documented treatment and continuing monitoring."
    )

    lines.append("")

    lines.append(
        "## Overall Risk Posture"
    )

    lines.append("")

    lines.append(
        f"- Total registered AI risks: {int(posture['total_risks'])}"
    )

    lines.append(
        f"- Average inherent risk score: {posture['average_risk_score']}/25"
    )

    lines.append(
        f"- Maximum inherent risk score: {int(posture['max_risk_score'])}/25"
    )

    lines.append(
        f"- Unresolved or actively mitigating risks: {int(posture['unmitigated_risks'])}"
    )

    lines.append(
        f"- Risks scoring 20–25: {int(posture['critical_score_risks'])}"
    )

    lines.append(
        f"- Risks scoring 15–19: {int(posture['high_score_risks'])}"
    )

    lines.append(
        f"- High/Critical residual risks after mapped controls: {int(high_residual)}"
    )

    lines.append("")

    lines.append(
        "## Top 3 Unresolved Risks"
    )

    lines.append("")

    for index, (_, row) in enumerate(
        top3.iterrows(),
        start=1,
    ):
        risk_id = row[
            "risk_id"
        ]

        lines.append(
            f"### {index}. {risk_id} — {row['harm_category']}"
        )

        lines.append("")

        lines.append(
            f"- Initial score: {int(row['risk_score'])}/25"
        )

        lines.append(
            f"- Residual risk: {row['residual_risk_after_control']}"
        )

        lines.append(
            f"- Lifecycle stage: {row['ai_lifecycle_stage']}"
        )

        lines.append(
            f"- Business impact: {BUSINESS_IMPACT[risk_id]}"
        )

        lines.append("")

    lines.append(
        "## Black-Box / Explainability Limitation"
    )

    lines.append("")

    lines.append(
        "The neural-network classifier remains a black-box model for which "
        "conventional SP 800-53 controls do not provide an adequate direct "
        "mapping for prediction-level explainability. Integrity, monitoring, "
        "risk assessment, privacy, training, and supply-chain controls can "
        "reduce surrounding system risk, but they do not make the internal "
        "decision logic inherently interpretable."
    )

    lines.append("")

    lines.append(
        "Residual explainability risk should therefore be accepted only with "
        "AI-specific compensating safeguards: human-in-the-loop authority, "
        "feature-attribution evidence where feasible, uncertainty communication, "
        "clinician usability validation, documented limitations, and explicit "
        "residual-risk approval."
    )

    lines.append("")

    lines.append(
        "## Authorization Conditions"
    )

    lines.append("")

    lines.extend(
        [
            "1. No autonomous diagnosis or treatment decision is permitted.",
            "2. Qualified clinicians retain final decision authority.",
            "3. Material retraining requires independent re-validation before deployment.",
            "4. Cohort-level performance and bias metrics must remain within approved thresholds.",
            "5. Production drift monitoring must remain active.",
            "6. Third-party model provenance gaps must be tracked and escalated.",
            "7. Sensitive neural-data privacy controls must be continuously enforced.",
            "8. High-residual risks require assigned owners and documented treatment milestones.",
            "9. Black-box explainability limitations require explicit residual-risk acceptance.",
            "10. Significant safety, privacy, model, data, or supplier changes trigger authorization review.",
        ]
    )

    lines.append("")

    lines.append(
        "## Authorization Rationale"
    )

    lines.append("")

    lines.append(
        "Denying authorization is not currently recommended because the system is "
        "designed as clinical decision support rather than autonomous clinical "
        "decision-making, and meaningful compensating controls are available for "
        "most identified risks. Unconditional authorization is also not appropriate "
        "because several risks remain high after conventional control mapping, "
        "particularly explainability, automation bias, cohort bias, and supplier "
        "provenance. Conditional authorization provides the most defensible posture "
        "while requiring continued evidence, monitoring, and human oversight."
    )

    AO_BRIEFING_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    register, crosswalk = (
        load_inputs()
    )

    build_treatment_plan(
        register,
        crosswalk,
    )

    build_ao_briefing(
        register,
        crosswalk,
    )

    posture = compute_risk_posture(
        str(
            REGISTER_PATH
        )
    )

    print(
        "AI RISK POSTURE"
    )

    print(
        "=" * 60
    )

    for key, value in posture.items():
        print(
            f"{key}: {value}"
        )

    print()

    print(
        f"Created: {TREATMENT_PLAN_PATH}"
    )

    print(
        f"Created: {AO_BRIEFING_PATH}"
    )


if __name__ == "__main__":
    main()
