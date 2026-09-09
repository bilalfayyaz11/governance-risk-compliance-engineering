import csv
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path.home() / "tprm-lab/tprm.db"
CSV_PATH = Path.home() / "tprm-lab/reports/vendor_scores.csv"


CADENCE_DAYS = {
    "Critical": 90,
    "High": 182,
    "Medium": 365,
    "Low": 730,
}


def import_vendors(db_path: str, csv_path: str) -> int:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    inserted = 0
    assessed_date = date.today()

    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                vendor_name = row["vendor_name"].strip()
                score = float(row["score"])
                tier = row["tier"].strip()

                if tier not in CADENCE_DAYS:
                    raise ValueError(f"Invalid tier: {tier}")

                next_review = assessed_date + timedelta(
                    days=CADENCE_DAYS[tier]
                )

                conn.execute(
                    """
                    INSERT INTO vendors (
                        name,
                        tier,
                        score,
                        last_assessed,
                        next_review
                    )
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET
                        tier = excluded.tier,
                        score = excluded.score,
                        last_assessed = excluded.last_assessed,
                        next_review = excluded.next_review
                    """,
                    (
                        vendor_name,
                        tier,
                        score,
                        assessed_date.isoformat(),
                        next_review.isoformat(),
                    ),
                )

                inserted += 1

        conn.commit()
        return inserted

    finally:
        conn.close()


if __name__ == "__main__":
    count = import_vendors(DB_PATH, CSV_PATH)
    print(f"Imported vendors: {count}")
