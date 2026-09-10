#!/usr/bin/env python3

from datetime import datetime, timezone
from pathlib import Path
import time

LOG_PATH = Path("/var/log/mock-app/access.log")

SUBJECTS = [
    ("ahmed.mansoori@example.com", "784-1990-1234567-1"),
    ("fatima.suwaidi@example.com", "784-1985-7654321-2"),
    ("sara.khan@example.com", "784-1992-1112223-4"),
    ("omar.hassan@example.com", "784-1988-7651234-5"),
    ("maryam.ali@example.com", "784-1994-5557771-6"),
]

SOURCE_IP = "203.0.113.77"
ENDPOINT = "/export/customers.csv"
RECORDS = 650
SESSION = "exfil-session-001"


def write_event(email: str, national_id: str, sequence: int) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()

    line = (
        f"MOCKAPP "
        f"src_ip={SOURCE_IP} "
        f"method=GET "
        f"endpoint={ENDPOINT} "
        f"records={RECORDS} "
        f"email={email} "
        f"national_id={national_id} "
        f"session={SESSION} "
        f"sequence={sequence} "
        f"timestamp={timestamp}\n"
    )

    with LOG_PATH.open("a", encoding="utf-8") as log:
        log.write(line)


if __name__ == "__main__":
    print("Generating simulated breach events...")

    for sequence, (email, national_id) in enumerate(SUBJECTS, start=1):
        write_event(email, national_id, sequence)

        print(
            f"event={sequence} "
            f"records={RECORDS} "
            f"email={email}"
        )

        time.sleep(1)

    print("Simulation complete.")
