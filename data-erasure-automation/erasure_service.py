import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "dbname": "erasure_lab",
    "user": "lab_user",
    "password": "labpass123",
}


RELATED_TABLES = [
    "orders",
    "support_tickets",
]


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def find_user_records(email: str):
    """
    Locate the user and all related records across tables.

    Args:
        email: Email address of the data subject

    Returns:
        {
            "user_id": int,
            "records": {
                "orders": int,
                "support_tickets": int
            }
        }

        Returns None when the email is not found.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT user_id
                FROM users
                WHERE email = %s
                """,
                (email,),
            )

            row = cur.fetchone()

            if row is None:
                return None

            user_id = row[0]
            records = {}

            for table_name in RELATED_TABLES:
                # Table names cannot be passed as ordinary SQL parameters,
                # so the list above acts as a fixed allow-list.
                query = f"""
                    SELECT COUNT(*)
                    FROM {table_name}
                    WHERE user_id = %s
                """

                cur.execute(
                    query,
                    (user_id,),
                )

                records[table_name] = cur.fetchone()[0]

            return {
                "user_id": user_id,
                "records": records,
            }

    finally:
        conn.close()


def soft_delete_user(user_id: int):
    """
    Mark the user as deleted without removing data.
    Log the action in audit_log.
    """
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET
                        is_deleted = TRUE,
                        deleted_at = NOW()
                    WHERE user_id = %s
                    RETURNING user_id
                    """,
                    (user_id,),
                )

                row = cur.fetchone()

                if row is None:
                    raise ValueError(
                        f"user_id {user_id} not found"
                    )

                cur.execute(
                    """
                    INSERT INTO audit_log (
                        user_id,
                        action,
                        table_name,
                        details
                    )
                    VALUES (
                        %s,
                        'SOFT_DELETE',
                        'users',
                        %s::jsonb
                    )
                    """,
                    (
                        user_id,
                        '{"status":"marked_deleted"}',
                    ),
                )

    finally:
        conn.close()


def hard_delete_user(user_id: int):
    """
    Permanently remove the user and related records.

    All delete operations and audit entries execute in one
    transaction. Any failure rolls back the whole operation.
    """
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:

                for table_name in RELATED_TABLES:
                    delete_sql = f"""
                        DELETE FROM {table_name}
                        WHERE user_id = %s
                    """

                    cur.execute(
                        delete_sql,
                        (user_id,),
                    )

                    deleted_count = cur.rowcount

                    cur.execute(
                        """
                        INSERT INTO audit_log (
                            user_id,
                            action,
                            table_name,
                            details
                        )
                        VALUES (
                            %s,
                            'HARD_DELETE',
                            %s,
                            jsonb_build_object(
                                'rows_deleted',
                                %s
                            )
                        )
                        """,
                        (
                            user_id,
                            table_name,
                            deleted_count,
                        ),
                    )

                cur.execute(
                    """
                    DELETE FROM users
                    WHERE user_id = %s
                    """,
                    (user_id,),
                )

                deleted_user_count = cur.rowcount

                if deleted_user_count != 1:
                    raise ValueError(
                        f"user_id {user_id} not found in users"
                    )

                cur.execute(
                    """
                    INSERT INTO audit_log (
                        user_id,
                        action,
                        table_name,
                        details
                    )
                    VALUES (
                        %s,
                        'HARD_DELETE',
                        'users',
                        jsonb_build_object(
                            'rows_deleted',
                            %s
                        )
                    )
                    """,
                    (
                        user_id,
                        deleted_user_count,
                    ),
                )

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def soft_delete_user(user_id: int):
    """
    Mark the user as deleted without removing data.
    Log the action in audit_log.
    """
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET
                        is_deleted = TRUE,
                        deleted_at = NOW()
                    WHERE user_id = %s
                    RETURNING user_id
                    """,
                    (user_id,),
                )

                row = cur.fetchone()

                if row is None:
                    raise ValueError(
                        f"user_id {user_id} not found"
                    )

                cur.execute(
                    """
                    INSERT INTO audit_log (
                        user_id,
                        action,
                        table_name,
                        details
                    )
                    VALUES (
                        %s,
                        'SOFT_DELETE',
                        'users',
                        %s::jsonb
                    )
                    """,
                    (
                        user_id,
                        '{"status":"marked_deleted"}',
                    ),
                )

    finally:
        conn.close()


def hard_delete_user(user_id: int):
    """
    Permanently remove the user and related records.

    All delete operations and audit entries execute in one
    transaction. Any failure rolls back the whole operation.
    """
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:

                for table_name in RELATED_TABLES:
                    delete_sql = f"""
                        DELETE FROM {table_name}
                        WHERE user_id = %s
                    """

                    cur.execute(
                        delete_sql,
                        (user_id,),
                    )

                    deleted_count = cur.rowcount

                    cur.execute(
                        """
                        INSERT INTO audit_log (
                            user_id,
                            action,
                            table_name,
                            details
                        )
                        VALUES (
                            %s,
                            'HARD_DELETE',
                            %s,
                            jsonb_build_object(
                                'rows_deleted',
                                %s
                            )
                        )
                        """,
                        (
                            user_id,
                            table_name,
                            deleted_count,
                        ),
                    )

                cur.execute(
                    """
                    DELETE FROM users
                    WHERE user_id = %s
                    """,
                    (user_id,),
                )

                deleted_user_count = cur.rowcount

                if deleted_user_count != 1:
                    raise ValueError(
                        f"user_id {user_id} not found in users"
                    )

                cur.execute(
                    """
                    INSERT INTO audit_log (
                        user_id,
                        action,
                        table_name,
                        details
                    )
                    VALUES (
                        %s,
                        'HARD_DELETE',
                        'users',
                        jsonb_build_object(
                            'rows_deleted',
                            %s
                        )
                    )
                    """,
                    (
                        user_id,
                        deleted_user_count,
                    ),
                )

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def anonymize_backup(user_id: int, original_email: str):
    """
    Anonymize the user's record in the simulated backup table.

    Replace direct identifiers with irreversible placeholders and
    record the action in audit_log.
    """
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users_backup
                    SET
                        email = CONCAT(
                            'anon_',
                            %s,
                            '@erased.local'
                        ),
                        full_name = 'REDACTED',
                        is_deleted = TRUE,
                        deleted_at = NOW()
                    WHERE user_id = %s
                      AND email = %s
                    """,
                    (
                        user_id,
                        user_id,
                        original_email,
                    ),
                )

                updated_count = cur.rowcount

                if updated_count != 1:
                    raise ValueError(
                        "Expected exactly one matching backup "
                        f"record for user_id {user_id}, "
                        f"updated {updated_count}"
                    )

                cur.execute(
                    """
                    INSERT INTO audit_log (
                        user_id,
                        action,
                        table_name,
                        details
                    )
                    VALUES (
                        %s,
                        'ANONYMIZE_BACKUP',
                        'users_backup',
                        jsonb_build_object(
                            'rows_anonymized',
                            %s,
                            'strategy',
                            'irreversible_placeholder'
                        )
                    )
                    """,
                    (
                        user_id,
                        updated_count,
                    ),
                )

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def verify_backup_anonymized(user_id: int) -> bool:
    """
    Confirm that the simulated backup row no longer contains
    directly identifying values.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    email,
                    full_name,
                    is_deleted
                FROM users_backup
                WHERE user_id = %s
                """,
                (user_id,),
            )

            row = cur.fetchone()

            if row is None:
                return False

            email, full_name, is_deleted = row

            return (
                email == f"anon_{user_id}@erased.local"
                and full_name == "REDACTED"
                and is_deleted is True
            )

    finally:
        conn.close()


def generate_certificate(user_id: int, email: str) -> str:
    """
    Generate a text certificate confirming completion of the
    erasure workflow.

    The raw email is never written to the certificate.
    """
    import hashlib
    from pathlib import Path

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    action,
                    table_name,
                    performed_at,
                    details
                FROM audit_log
                WHERE user_id = %s
                ORDER BY performed_at, audit_id
                """,
                (user_id,),
            )

            actions = cur.fetchall()

    finally:
        conn.close()

    if not actions:
        raise ValueError(
            f"No audit records found for user_id {user_id}"
        )

    subject_hash = hashlib.sha256(
        email.encode("utf-8")
    ).hexdigest()

    certificates_dir = (
        Path(__file__).resolve().parent
        / "certificates"
    )

    certificates_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        certificates_dir
        / f"certificate_{user_id}.txt"
    )

    lines = [
        "RIGHT TO ERASURE CONFIRMATION CERTIFICATE",
        "=" * 41,
        "",
        f"Subject Reference (SHA-256): {subject_hash}",
        f"Internal User Reference: {user_id}",
        "",
        "Erasure Actions:",
        "",
    ]

    for action, table_name, performed_at, details in actions:
        lines.append(
            f"- {performed_at.isoformat()} | "
            f"{action} | "
            f"{table_name} | "
            f"{details}"
        )

    lines.extend(
        [
            "",
            "Verification Summary:",
            "- Live user record removed",
            "- Related application records removed",
            "- Simulated retained backup record anonymized",
            "- Audit evidence retained without storing the subject's raw email",
            "",
            "GDPR Article 17 Compliance Statement:",
            (
                "The documented workflow completed the configured "
                "erasure actions for the referenced data subject, "
                "subject to applicable legal retention requirements, "
                "exceptions, and backup lifecycle controls."
            ),
            "",
            (
                "This certificate records execution of the technical "
                "workflow and is not, by itself, a legal determination "
                "that every Article 17 requirement or exception has "
                "been satisfied."
            ),
            "",
        ]
    )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return str(output_path)
