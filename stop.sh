#!/bin/bash
PID_FILE=/tmp/magicdpd_hugo.pid
STOPPED=0

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill "$PID" 2>/dev/null; then
        echo "Stopped process $PID (from pid file)"
        STOPPED=1
    fi
    rm "$PID_FILE"
fi

# Fallback: kill any hugo server process on port 1313
PIDS=$(pgrep -f "hugo server" 2>/dev/null)
if [ -n "$PIDS" ]; then
    echo "$PIDS" | xargs kill 2>/dev/null && echo "Stopped hugo server processes: $PIDS"
    STOPPED=1
fi

if [ "$STOPPED" -eq 0 ]; then
    echo "No running site found"
fi
