"""
Sample user record used to demonstrate data portability filtering.

Portable fields represent data supplied directly by the user.
Internal analytics and administrative annotations are excluded.
"""

USER_RECORD = {
    "user_id": "U1001",
    "full_name": "Aisha Al Farsi",
    "email": "aisha@example.com",
    "phone": "+971500000000",
    "signup_date": "2023-01-15",
    "preferences": {
        "newsletter": True
    },
    "internal_risk_score": 0.82,
    "admin_notes": "VIP customer"
}

PORTABLE_FIELDS = [
    "user_id",
    "full_name",
    "email",
    "phone",
    "signup_date",
    "preferences",
]

NON_PORTABLE_FIELDS = [
    "internal_risk_score",
    "admin_notes",
]
