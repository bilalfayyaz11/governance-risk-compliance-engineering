import csv
from pathlib import Path

INPUT_FILE = Path.home() / "tprm-lab/responses/vendor_responses.csv"
OUTPUT_FILE = Path.home() / "tprm-lab/reports/vendor_scores.csv"

WEIGHT_MAP = {
    "GOV01": 1.5,
    "GOV02": 1.5,
    "GOV03": 1.5,

    "DATA01": 2.5,
    "DATA02": 2.5,
    "DATA03": 3.0,

    "IR01": 3.0,
    "IR02": 3.0,
    "IR03": 3.0,

    "SUB01": 2.0,
    "SUB02": 2.0,
    "SUB03": 2.0,

    "BCP01": 2.5,
    "BCP02": 2.5,
    "BCP03": 2.5,
}


def load_responses(csv_file: str) -> list:
    with open(csv_file, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def score_vendor(response: dict, weight_map: dict) -> float:
    weighted_total = 0.0
    total_weight = 0.0

    for question_code, weight in weight_map.items():
        raw_value = response.get(question_code, "")

        if raw_value == "":
            continue

        try:
            answer = float(raw_value)
        except ValueError:
            continue

        if answer < 0 or answer > 4:
            raise ValueError(
                f"Invalid score {answer} for {question_code}. Expected 0-4."
            )

        weighted_total += answer * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(weighted_total / total_weight, 2)


def tier_vendor(score: float) -> str:
    if score < 1.0:
        return "Critical"
    elif score < 2.0:
        return "High"
    elif score < 3.0:
        return "Medium"
    return "Low"


def main():
    responses = load_responses(INPUT_FILE)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["vendor_name", "score", "tier"]
        )
        writer.writeheader()

        for response in responses:
            vendor_name = response["vendor_name"]
            score = score_vendor(response, WEIGHT_MAP)
            tier = tier_vendor(score)

            writer.writerow(
                {
                    "vendor_name": vendor_name,
                    "score": score,
                    "tier": tier,
                }
            )

            print(
                f"{vendor_name:20} score={score:.2f} tier={tier}"
            )


if __name__ == "__main__":
    main()
