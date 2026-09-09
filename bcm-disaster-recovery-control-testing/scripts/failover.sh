#!/bin/bash

PRIMARY_CONTAINER="dr-primary"
FAILOVER_CONTAINER="dr-secondary"

SECONDARY_DATA="$HOME/dr-lab/backups-secondary"
IMAGE="dr-stateful-workload:1.0"

LOG_FILE="$HOME/dr-lab/scripts/failover.log"
EVIDENCE_DIR="$HOME/dr-lab/docs/evidence"

mkdir -p "$EVIDENCE_DIR"

START_ISO=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
START_EPOCH=$(date +%s)

echo "Failover started: $START_ISO"

sudo docker stop "$PRIMARY_CONTAINER" >/dev/null 2>&1 || true
sudo docker rm -f "$FAILOVER_CONTAINER" >/dev/null 2>&1 || true

sudo chown -R 10001:10001 "$SECONDARY_DATA"

sudo docker run -d \
    --name "$FAILOVER_CONTAINER" \
    --restart unless-stopped \
    -p 127.0.0.1:8081:8080 \
    -v "$SECONDARY_DATA:/data" \
    "$IMAGE" \
    >/tmp/dr-failover-container-id

HEALTHY=0

for attempt in $(seq 1 30); do
    CODE=$(curl -s \
        --max-time 3 \
        -o /tmp/dr-secondary-health.json \
        -w '%{http_code}' \
        http://127.0.0.1:8081/health \
        || true)

    if [ "$CODE" = "200" ]; then
        HEALTHY=1
        break
    fi

    sleep 2
done

END_ISO=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
END_EPOCH=$(date +%s)

RTO_SECONDS=$((END_EPOCH - START_EPOCH))

if [ "$HEALTHY" -eq 1 ]; then
    STATUS="success"
else
    STATUS="failure"
fi

jq -nc \
    --arg start "$START_ISO" \
    --arg end "$END_ISO" \
    --arg status "$STATUS" \
    --arg container "$FAILOVER_CONTAINER" \
    --argjson actual_rto_seconds "$RTO_SECONDS" \
    '{
        action: "failover",
        status: $status,
        start: $start,
        end: $end,
        actual_rto_seconds: $actual_rto_seconds,
        container: $container
    }' \
    >> "$LOG_FILE"

{
    echo "Failover start: $START_ISO"
    echo "Failover end: $END_ISO"
    echo "Actual RTO seconds: $RTO_SECONDS"
    echo "Status: $STATUS"
} > "$EVIDENCE_DIR/failover-timing.txt"

echo
echo "Failover status: $STATUS"
echo "Actual RTO: $RTO_SECONDS seconds"

if [ "$HEALTHY" -eq 1 ]; then
    echo
    echo "Secondary health:"
    cat /tmp/dr-secondary-health.json
    echo

    echo
    echo "Secondary transaction sample:"
    curl -s \
        http://127.0.0.1:8081/transactions \
        | jq .
fi

if [ "$RTO_SECONDS" -le 900 ] && [ "$HEALTHY" -eq 1 ]; then
    echo "PASS | Failover met 15-minute RTO"
else
    echo "FAIL | Failover did not meet 15-minute RTO"
fi

if [ "$HEALTHY" -eq 1 ]; then
    exit 0
else
    exit 1
fi
