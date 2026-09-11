#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Dict


ASSESSMENT_DATE = "2026-09-12"


EU_EEA_COUNTRIES = {
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Iceland",
    "Ireland",
    "Italy",
    "Latvia",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Norway",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
}


ADEQUATE_DESTINATIONS = {
    "Andorra",
    "Argentina",
    "Brazil",
    "Canada",
    "Faroe Islands",
    "Guernsey",
    "Israel",
    "Isle of Man",
    "Japan",
    "Jersey",
    "New Zealand",
    "Republic of Korea",
    "South Korea",
    "Switzerland",
    "United Kingdom",
    "Uruguay",
    "European Patent Organisation",
}


def check_gdpr_adequacy(destination_country: str) -> Dict:
    """
    Evaluate a destination against the current EU adequacy framework.

    EEA destinations are not treated as Article 45 third-country
    adequacy cases.

    For non-EEA destinations, adequacy status is checked against the
    European Commission's adequacy list as of the assessment date.
    """
    if destination_country in EU_EEA_COUNTRIES:
        return {
            "country": destination_country,
            "adequate": True,
            "basis": (
                "Destination is within the EU/EEA. "
                "GDPR Chapter V third-country transfer safeguards "
                "are not triggered solely by this destination."
            ),
            "classification": "EEA destination",
        }

    if destination_country in ADEQUATE_DESTINATIONS:
        return {
            "country": destination_country,
            "adequate": True,
            "basis": (
                "European Commission adequacy decision applies "
                f"as of {ASSESSMENT_DATE}."
            ),
            "classification": "Adequate third country",
        }

    return {
        "country": destination_country,
        "adequate": False,
        "basis": (
            "No European Commission Article 45 adequacy decision "
            f"identified as of {ASSESSMENT_DATE}."
        ),
        "classification": "Non-adequate third country",
    }


def has_special_category_data(data_tiers: Dict[str, str]) -> bool:
    return any(
        tier == "Special Category"
        for tier in data_tiers.values()
    )


def check_pdpl_transfer_rules(
    destination_country: str,
    data_tiers: Dict[str, str],
    origin_country: str = "Saudi Arabia",
) -> Dict:
    """
    Evaluate the Saudi PDPL cross-border framework.

    Article 29 is an outbound-transfer provision. Therefore it is
    directly relevant only where the transfer originates in Saudi
    Arabia and personal data is transferred or disclosed outside
    the Kingdom.
    """
    special_category = has_special_category_data(data_tiers)

    if origin_country != "Saudi Arabia":
        return {
            "applicable": False,
            "origin_country": origin_country,
            "destination_country": destination_country,
            "reason": (
                "Saudi PDPL Article 29 outbound-transfer rules are "
                "not directly triggered because this transfer does "
                "not originate in Saudi Arabia."
            ),
            "risk_assessment_required": False,
            "safeguards_required": False,
            "sensitive_data_present": special_category,
        }

    if destination_country == "Saudi Arabia":
        return {
            "applicable": False,
            "origin_country": origin_country,
            "destination_country": destination_country,
            "reason": (
                "No cross-border transfer outside the Kingdom occurs."
            ),
            "risk_assessment_required": False,
            "safeguards_required": False,
            "sensitive_data_present": special_category,
        }

    return {
        "applicable": True,
        "origin_country": origin_country,
        "destination_country": destination_country,
        "reason": (
            "Saudi-origin personal data is transferred outside "
            "the Kingdom, so Article 29 and the transfer regulation "
            "must be assessed."
        ),
        "risk_assessment_required": special_category,
        "safeguards_required": True,
        "sensitive_data_present": special_category,
        "conditions": [
            "Transfer must not prejudice national security or "
            "the vital interests of the Kingdom.",
            "Destination protection must be assessed against "
            "Saudi transfer requirements.",
            "Transfer must be limited to the minimum personal "
            "data necessary for the stated purpose.",
            "Appropriate safeguards must be documented where "
            "required.",
            "A transfer risk assessment is required for "
            "continuous or large-scale transfers of sensitive data.",
        ],
    }


def determine_mechanism(
    gdpr_result: Dict,
    pdpl_result: Dict,
    exporter_role: str = "Processor",
    importer_role: str = "Sub-processor",
) -> str:
    """
    Determine the GDPR transfer mechanism for the evaluated leg.

    This exercise uses SCCs as the selected Article 46 safeguard.
    """
    if gdpr_result["classification"] == "EEA destination":
        return "No Chapter V Mechanism Required"

    if gdpr_result["adequate"]:
        return "Adequacy Decision"

    if exporter_role == "Processor" and importer_role in {
        "Processor",
        "Sub-processor",
    }:
        return "SCC Module 3 Required + TIA"

    if exporter_role == "Controller" and importer_role == "Processor":
        return "SCC Module 2 Required + TIA"

    return "Article 46 Safeguard Required + TIA"


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent

    data_tiers = {
        "full_name": "Confidential",
        "work_email": "Internal",
        "emirates_id": "Confidential",
        "salary": "Confidential",
        "bank_iban": "Confidential",
        "performance_review": "Confidential",
        "health_accommodation": "Special Category",
    }

    # Leg 1: Dubai controller -> Frankfurt processor
    dubai_to_frankfurt_gdpr = check_gdpr_adequacy(
        "Germany"
    )

    dubai_to_frankfurt_pdpl = check_pdpl_transfer_rules(
        destination_country="Germany",
        data_tiers=data_tiers,
        origin_country="United Arab Emirates",
    )

    dubai_to_frankfurt_mechanism = determine_mechanism(
        dubai_to_frankfurt_gdpr,
        dubai_to_frankfurt_pdpl,
        exporter_role="Controller",
        importer_role="Processor",
    )

    # Leg 2: Frankfurt processor -> Riyadh sub-processor
    frankfurt_to_riyadh_gdpr = check_gdpr_adequacy(
        "Saudi Arabia"
    )

    frankfurt_to_riyadh_pdpl = check_pdpl_transfer_rules(
        destination_country="Saudi Arabia",
        data_tiers=data_tiers,
        origin_country="Germany",
    )

    frankfurt_to_riyadh_mechanism = determine_mechanism(
        frankfurt_to_riyadh_gdpr,
        frankfurt_to_riyadh_pdpl,
        exporter_role="Processor",
        importer_role="Sub-processor",
    )

    # Separate Saudi outbound test case so Article 29 is exercised
    # correctly rather than misapplied to an inbound transfer.
    riyadh_to_frankfurt_pdpl = check_pdpl_transfer_rules(
        destination_country="Germany",
        data_tiers=data_tiers,
        origin_country="Saudi Arabia",
    )

    special_category = has_special_category_data(
        data_tiers
    )

    obligations = []

    if not frankfurt_to_riyadh_gdpr["adequate"]:
        obligations.extend(
            [
                "Use an Article 46 safeguard for "
                "Frankfurt-to-Riyadh transfer.",
                "Use SCC Module 3 for the processor-to-"
                "sub-processor transfer configuration.",
                "Conduct and document a Transfer Impact "
                "Assessment.",
                "Assess destination-country laws and public "
                "authority access under SCC Clause 14.",
                "Evaluate supplementary technical, "
                "contractual, and organizational measures.",
            ]
        )

    if special_category:
        obligations.extend(
            [
                "Apply heightened scrutiny because health "
                "accommodation data constitutes GDPR "
                "Article 9 special-category data.",
                "Apply stronger data minimization and "
                "technical protection to special-category data.",
            ]
        )

    report = {
        "assessment_date": ASSESSMENT_DATE,
        "data_profile": {
            "special_category_data_present": special_category,
            "sensitivity_tiers": data_tiers,
        },
        "transfer_legs": {
            "dubai_to_frankfurt": {
                "route": "Dubai -> Frankfurt",
                "roles": "Controller -> Processor",
                "gdpr": dubai_to_frankfurt_gdpr,
                "selected_mechanism":
                    dubai_to_frankfurt_mechanism,
                "chapter_v_triggered": False,
                "reason": (
                    "The destination is within the EEA. "
                    "UAE non-adequacy does not by itself turn "
                    "an inbound UAE-to-Germany transfer into "
                    "a GDPR Chapter V export."
                ),
                "ksa_pdpl_article_29":
                    dubai_to_frankfurt_pdpl,
            },
            "frankfurt_to_riyadh": {
                "route": "Frankfurt -> Riyadh",
                "roles": "Processor -> Sub-processor",
                "gdpr": frankfurt_to_riyadh_gdpr,
                "selected_mechanism":
                    frankfurt_to_riyadh_mechanism,
                "chapter_v_triggered": True,
                "heightened_scrutiny":
                    special_category,
                "ksa_pdpl_article_29":
                    frankfurt_to_riyadh_pdpl,
            },
        },
        "ksa_pdpl_outbound_test_case": {
            "route": "Riyadh -> Frankfurt",
            "purpose": (
                "Exercise the Saudi Article 29 outbound "
                "transfer branch correctly."
            ),
            "result": riyadh_to_frankfurt_pdpl,
        },
        "triggered_obligations": obligations,
        "legal_logic_notes": [
            "Saudi Arabia is not on the European Commission "
            "adequacy list as of the assessment date.",
            "The UAE is not on the European Commission "
            "adequacy list as of the assessment date.",
            "UAE adequacy status is not the deciding factor "
            "for Dubai-to-Frankfurt because Germany is an "
            "EEA destination.",
            "Frankfurt-to-Riyadh is the relevant GDPR "
            "Chapter V onward transfer.",
            "For a processor-to-sub-processor configuration, "
            "Commission Decision 2021/914 Module 3 is the "
            "appropriate SCC module in this scenario.",
            "Saudi PDPL Article 29 addresses transfers from "
            "Saudi Arabia to destinations outside the Kingdom; "
            "it is not an outbound-transfer rule for the "
            "incoming Frankfurt-to-Riyadh leg.",
        ],
    }

    output_path = (
        base_dir
        / "assessment"
        / "adequacy_report.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            report,
            indent=2,
        )
    )

    print()
    print(f"Report written to: {output_path}")


if __name__ == "__main__":
    main()
