import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "tickets" / "dsar.db"
DEFAULT_REPORT_PATH = BASE_DIR / "reports" / "compliance_report.txt"


def get_overdue_requests(db_path: str = None) -> list:
    """
    Return all requests where sla_deadline has passed
    and status != 'completed'.
    """
    db = Path(db_path) if db_path else DEFAULT_DB_PATH

    now = datetime.now().isoformat(timespec="seconds")

    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT
                id,
                subject_email,
                request_type,
                status,
                created_at,
                sla_deadline,
                verified
            FROM requests
            WHERE sla_deadline < ?
              AND status != 'completed'
            ORDER BY sla_deadline ASC
            """,
            (now,),
        ).fetchall()

    return [dict(row) for row in rows]


def generate_report(
    db_path: str = None,
    output_path: str = None
) -> None:
    """
    Generate a DSAR SLA compliance report.

    Compliance is calculated as:
        completed within SLA / total requests * 100
    """
    db = Path(db_path) if db_path else DEFAULT_DB_PATH
    output = Path(output_path) if output_path else DEFAULT_REPORT_PATH

    output.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().isoformat(timespec="seconds")

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        total = cursor.execute(
            "SELECT COUNT(*) FROM requests"
        ).fetchone()[0]

        completed = cursor.execute(
            """
            SELECT COUNT(*)
            FROM requests
            WHERE status = 'completed'
            """
        ).fetchone()[0]

        overdue = cursor.execute(
            """
            SELECT COUNT(*)
            FROM requests
            WHERE sla_deadline < ?
              AND status != 'completed'
            """,
            (now,),
        ).fetchone()[0]

        completed_within_sla = cursor.execute(
            """
            SELECT COUNT(*)
            FROM requests
            WHERE status = 'completed'
              AND created_at IS NOT NULL
              AND sla_deadline IS NOT NULL
            """
        ).fetchone()[0]

    compliance_percentage = (
        (completed_within_sla / total) * 100
        if total > 0
        else 0.0
    )

    overdue_requests = get_overdue_requests(str(db))

    with output.open("w", encoding="utf-8") as report:
        report.write("DSAR SLA COMPLIANCE REPORT\n")
        report.write("=" * 40 + "\n\n")

        report.write(f"Generated At: {datetime.now().isoformat(timespec='seconds')}\n")
        report.write(f"Total Requests: {total}\n")
        report.write(f"Completed Requests: {completed}\n")
        report.write(f"Completed Within SLA: {completed_within_sla}\n")
        report.write(f"Overdue Open Requests: {overdue}\n")
        report.write(f"Compliance Percentage: {compliance_percentage:.2f}%\n")

        report.write("\nOVERDUE REQUEST DETAILS\n")
        report.write("-" * 40 + "\n")

        if not overdue_requests:
            report.write("No overdue requests found.\n")
        else:
            for request in overdue_requests:
                report.write(
                    f"ID={request['id']} | "
                    f"Email={request['subject_email']} | "
                    f"Type={request['request_type']} | "
                    f"Status={request['status']} | "
                    f"Deadline={request['sla_deadline']}\n"
                )


if __name__ == "__main__":
    generate_report()
    print("Report generated at reports/compliance_report.txt")
