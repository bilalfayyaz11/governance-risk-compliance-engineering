import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

BASE = Path.home() / "arx_project"
DATA = BASE / "data"
DATA.mkdir(parents=True, exist_ok=True)

raw_path = DATA / "patients_raw.csv"
analysis_path = DATA / "patients.csv"

zipcodes = [
    "10001", "10002", "10003", "10004", "10005",
    "20001", "20002", "20003", "20004", "20005",
    "30001", "30002", "30003", "30004", "30005",
    "40001", "40002", "40003", "40004", "40005",
]

nationalities = [
    "Saudi Arabia",
    "United Arab Emirates",
    "Kuwait",
    "Qatar",
    "Bahrain",
    "Oman",
    "Pakistan",
    "India",
    "Egypt",
    "Jordan",
]

diagnoses = [
    "Hypertension",
    "Diabetes",
    "Asthma",
    "Migraine",
    "Arthritis",
    "Anemia",
    "Dermatitis",
    "Gastritis",
]

genders = ["Male", "Female"]

start = date(2025, 1, 1)

rows = []

for i in range(1, 601):
    row = {
        "patient_id": f"P{i:06d}",
        "zipcode": random.choice(zipcodes),
        "age": random.randint(18, 85),
        "gender": random.choice(genders),
        "nationality": random.choice(nationalities),
        "diagnosis": random.choice(diagnoses),
        "admission_date": (
            start + timedelta(days=random.randint(0, 364))
        ).isoformat(),
    }
    rows.append(row)

with raw_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "patient_id",
            "zipcode",
            "age",
            "gender",
            "nationality",
            "diagnosis",
            "admission_date",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

# Remove the direct identifier before anonymization.
with analysis_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "zipcode",
            "age",
            "gender",
            "nationality",
            "diagnosis",
            "admission_date",
        ],
    )
    writer.writeheader()

    for row in rows:
        writer.writerow({
            key: row[key]
            for key in writer.fieldnames
        })

print(f"Raw records: {len(rows)}")
print(f"Raw dataset: {raw_path}")
print(f"Analysis dataset: {analysis_path}")
