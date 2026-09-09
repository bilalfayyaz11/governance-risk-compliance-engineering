#!/bin/bash

SOURCE="$HOME/dr-lab/workload/data/"
DEST="$HOME/dr-lab/backups-secondary/"
LOG_FILE="$HOME/dr-lab/scripts/replicate.log"

START=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
START_EPOCH=$(date +%s)

mkdir -p "$DEST"

rsync \
    --archive \
    --checksum \
    --delete-after \
    "$SOURCE" \
    "$DEST"

RC=$?

END=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
END_EPOCH=$(date +%s)

DURATION=$((END_EPOCH - START_EPOCH))

if [ "$RC" -eq 0 ]; then
    STATUS="success"
else
    STATUS="failure"
fi

jq -nc \
    --arg timestamp "$END" \
    --arg start "$START" \
    --arg end "$END" \
    --arg status "$STATUS" \
    --arg source "$SOURCE" \
    --arg destination "$DEST" \
    --argjson exit_code "$RC" \
    --argjson duration_seconds "$DURATION" \
    '{
        timestamp: $timestamp,
        action: "replication",
        status: $status,
        source: $source,
        destination: $destination,
        start: $start,
        end: $end,
        duration_seconds: $duration_seconds,
        exit_code: $exit_code
    }' \
    >> "$LOG_FILE"

exit "$RC"
