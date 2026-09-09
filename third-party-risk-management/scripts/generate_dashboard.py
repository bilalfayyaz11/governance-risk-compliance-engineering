import sqlite3
from pathlib import Path

DB = Path.home() / "tprm-lab/tprm.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

print("=" * 70)
print("THIRD-PARTY RISK MANAGEMENT DASHBOARD")
print("=" * 70)

print("\nVENDOR RISK SUMMARY")
print("-" * 70)

summary = conn.execute(
    """
    SELECT
        tier,
        COUNT(*) AS vendor_count,
        ROUND(AVG(score), 2) AS avg_score
    FROM vendors
    GROUP BY tier
    ORDER BY CASE tier
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
    END
    """
).fetchall()

for row in summary:
    print(
        f"{row['tier']:<10} "
        f"vendors={row['vendor_count']:<3} "
        f"avg_score={row['avg_score']}"
    )

print("\nVENDOR REGISTER")
print("-" * 70)

vendors = conn.execute(
    """
    SELECT
        name,
        tier,
        score,
        last_assessed,
        next_review
    FROM vendors
    ORDER BY score ASC
    """
).fetchall()

for vendor in vendors:
    print(
        f"{vendor['name']:<20} "
        f"{vendor['tier']:<10} "
        f"score={vendor['score']:<4} "
        f"next={vendor['next_review']}"
    )

print("\nOPEN RISK EXCEPTIONS")
print("-" * 70)

exceptions = conn.execute(
    """
    SELECT
        v.name AS vendor,
        e.control_gap,
        e.risk_rating,
        e.expiry_date
    FROM exceptions e
    JOIN vendors v
      ON v.id = e.vendor_id
    ORDER BY
        CASE e.risk_rating
            WHEN 'Critical' THEN 1
            WHEN 'High' THEN 2
            WHEN 'Medium' THEN 3
            ELSE 4
        END
    """
).fetchall()

for exception in exceptions:
    print(
        f"{exception['risk_rating']:<10} "
        f"{exception['vendor']:<20} "
        f"{exception['control_gap']} "
        f"(expires {exception['expiry_date']})"
    )

conn.close()
