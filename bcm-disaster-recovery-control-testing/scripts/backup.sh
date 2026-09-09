#!/bin/bash

WORKLOAD_NAME="dr-stateful-workload"
DATA_DIR="$HOME/dr-lab/workload/data"
REPO="$HOME/dr-lab/backups-primary/restic-repo"
PASSWORD_FILE="$HOME/dr-lab/scripts/restic-password"
LOG_FILE="$HOME/dr-lab/scripts/backup.log"

TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

export RESTIC_PASSWORD_FILE="$PASSWORD_FILE"

log_entry() {
    printf '%s\n' "$1" >> "$LOG_FILE"
}

if [ ! -d "$REPO/data" ]; then
    if restic -r "$REPO" init >/tmp/restic-init.out 2>/tmp/restic-init.err; then
        log_entry "$TIMESTAMP status=success action=init repository=$REPO"
    else
        RC=$?
        log_entry "$TIMESTAMP status=failure action=init repository=$REPO exit_code=$RC"
        cat /tmp/restic-init.err >&2
        exit "$RC"
    fi
fi

TAG="${WORKLOAD_NAME}-$(date -u '+%Y%m%dT%H%M%SZ')"

if restic -r "$REPO" backup "$DATA_DIR" \
    --tag "$WORKLOAD_NAME" \
    --tag "$TAG" \
    >/tmp/restic-backup.out \
    2>/tmp/restic-backup.err
then
    RC=0
    SNAPSHOT=$(restic -r "$REPO" snapshots \
        --json \
        --latest 1 \
        | jq -r '.[0].short_id // "unknown"')

    log_entry "$TIMESTAMP status=success action=backup workload=$WORKLOAD_NAME snapshot=$SNAPSHOT tag=$TAG exit_code=0"
else
    RC=$?

    log_entry "$TIMESTAMP status=failure action=backup workload=$WORKLOAD_NAME exit_code=$RC"

    cat /tmp/restic-backup.err >&2
fi

exit "$RC"
