#!/bin/bash

DB="$HOME/dr-lab/workload/data/transactions.db"

TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
AMOUNT=$(awk -v min=10 -v max=500 \
    'BEGIN{srand(); printf "%.2f", min+rand()*(max-min)}')

sqlite3 "$DB" \
    "INSERT INTO transactions(created_at,amount,status)
     VALUES('$TIMESTAMP',$AMOUNT,'completed');"

COUNT=$(sqlite3 "$DB" \
    "SELECT COUNT(*) FROM transactions;")

echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') transaction_count=$COUNT amount=$AMOUNT" \
    >> "$HOME/dr-lab/scripts/transactions.log"
