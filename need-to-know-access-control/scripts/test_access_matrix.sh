#!/usr/bin/env bash

BASE="$HOME/need-to-know-access"
OUT="$BASE/evidence"

mkdir -p "$OUT"

CSV="$OUT/access_test_matrix.csv"
RAW="$OUT/access_test_raw.log"

echo "role,query_type,expected_result,actual_result,status" > "$CSV"
: > "$RAW"

run_test() {
    ROLE="$1"
    PASS="$2"
    QUERY_TYPE="$3"
    EXPECTED="$4"
    SQL="$5"

    echo "===== $ROLE | $QUERY_TYPE =====" >> "$RAW"

    RESULT=$(
        PGPASSWORD="$PASS" \
        psql \
        -h localhost \
        -U "$ROLE" \
        -d agency_records \
        -v ON_ERROR_STOP=1 \
        -c "$SQL" \
        2>&1
    )

    RC=$?

    echo "$RESULT" >> "$RAW"
    echo >> "$RAW"

    if [ "$EXPECTED" = "Allowed" ]; then
        if [ "$RC" -eq 0 ]; then
            ACTUAL="Allowed"
            STATUS="PASS"
        else
            ACTUAL="Denied"
            STATUS="FAIL"
        fi
    else
        if [ "$RC" -ne 0 ]; then
            ACTUAL="Denied"
            STATUS="PASS"
        else
            ACTUAL="Allowed"
            STATUS="FAIL"
        fi
    fi

    printf '"%s","%s","%s","%s","%s"\n' \
        "$ROLE" \
        "$QUERY_TYPE" \
        "$EXPECTED" \
        "$ACTUAL" \
        "$STATUS" \
        >> "$CSV"
}

run_test \
"finance_role" \
"ChangeMe_FIN1" \
"SELECT allowed finance columns" \
"Allowed" \
"SELECT emp_id, full_name, department, salary FROM employee_records;"

run_test \
"finance_role" \
"ChangeMe_FIN1" \
"SELECT ssn" \
"Denied" \
"SELECT ssn FROM employee_records;"

run_test \
"finance_role" \
"ChangeMe_FIN1" \
"SELECT HR rows" \
"Allowed" \
"SELECT emp_id, full_name, department, salary FROM employee_records WHERE department='HR';"

run_test \
"audit_role" \
"ChangeMe_AUD1" \
"SELECT audit columns" \
"Allowed" \
"SELECT emp_id, department, audit_flag FROM employee_records;"

run_test \
"audit_role" \
"ChangeMe_AUD1" \
"SELECT salary" \
"Denied" \
"SELECT salary FROM employee_records;"

run_test \
"audit_role" \
"ChangeMe_AUD1" \
"SELECT non-flagged rows" \
"Allowed" \
"SELECT emp_id, department, audit_flag FROM employee_records WHERE audit_flag=false;"

run_test \
"hr_role" \
"ChangeMe_HR1" \
"SELECT all columns" \
"Allowed" \
"SELECT * FROM employee_records;"

run_test \
"hr_role" \
"ChangeMe_HR1" \
"SELECT ssn" \
"Allowed" \
"SELECT ssn FROM employee_records;"

echo
echo "===== ACCESS TEST MATRIX ====="
column -s, -t "$CSV" 2>/dev/null || cat "$CSV"

echo
echo "===== RAW TEST EVIDENCE ====="
cat "$RAW"

echo
echo "===== RLS ROW COUNT VALIDATION ====="

FINANCE_ROWS=$(
PGPASSWORD='ChangeMe_FIN1' \
psql \
-h localhost \
-U finance_role \
-d agency_records \
-Atqc "
SELECT COUNT(*)
FROM employee_records;
"
)

AUDIT_ROWS=$(
PGPASSWORD='ChangeMe_AUD1' \
psql \
-h localhost \
-U audit_role \
-d agency_records \
-Atqc "
SELECT COUNT(*)
FROM employee_records;
"
)

HR_ROWS=$(
PGPASSWORD='ChangeMe_HR1' \
psql \
-h localhost \
-U hr_role \
-d agency_records \
-Atqc "
SELECT COUNT(*)
FROM employee_records;
"
)

echo "finance_role rows: $FINANCE_ROWS"
echo "audit_role rows: $AUDIT_ROWS"
echo "hr_role rows: $HR_ROWS"

if [ "$FINANCE_ROWS" = "1" ]; then
    echo "PASS: finance sees only Finance department"
else
    echo "FAIL: finance row isolation"
fi

if [ "$AUDIT_ROWS" = "2" ]; then
    echo "PASS: audit sees only flagged rows"
else
    echo "FAIL: audit row isolation"
fi

if [ "$HR_ROWS" = "3" ]; then
    echo "PASS: HR sees all rows"
else
    echo "FAIL: HR visibility"
fi

echo
echo "===== TEST MATRIX SUMMARY ====="

TOTAL=$(
tail -n +2 "$CSV" | wc -l
)

PASSED=$(
grep -c ',"PASS"$' "$CSV" || true
)

FAILED=$(
grep -c ',"FAIL"$' "$CSV" || true
)

echo "Total tests: $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"

if [ "$FAILED" = "0" ]; then
    echo "PASS: segregation-of-duties matrix validated"
else
    echo "REVIEW: one or more access tests failed"
fi

echo
echo "===== REFRESH PGAUDIT EVIDENCE ====="

LOGFILE=$(
find /var/log/postgresql \
-type f \
-name "postgresql-*-main.log" \
2>/dev/null \
| sort \
| tail -n 1
)

if [ -n "$LOGFILE" ] && [ -f "$LOGFILE" ]; then
    sudo grep -E \
    "AUDIT:|finance_role|audit_role|hr_role|permission denied" \
    "$LOGFILE" \
    | tail -n 150 \
    | sudo tee \
    "$OUT/pgaudit_access_evidence.log" \
    >/dev/null

    sudo chown ubuntu:ubuntu \
    "$OUT/pgaudit_access_evidence.log"
fi

echo
echo "===== EVIDENCE FILES ====="
find "$OUT" -maxdepth 1 -type f -printf '%f\n' | sort

echo
echo "===== TASK 4 COMPLETE ====="
