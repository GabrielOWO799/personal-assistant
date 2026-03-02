#!/bin/bash
# Cron wrapper script to ensure proper environment
# Enhanced with detailed logging and error handling

# Set up environment
export PATH="/home/linuxbrew/.linuxbrew/bin:/usr/local/bin:/usr/bin:/bin:/home/admin/.local/bin"
export PYTHONPATH="/home/admin/.local/lib/python3.8/site-packages:/home/admin/.openclaw/workspace"
export HOME="/home/admin"
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"

# Ensure workspace directory exists
cd /home/admin/.openclaw/workspace

# Create logs directory if not exists
mkdir -p /home/admin/.openclaw/workspace/logs

# Log execution with timestamp
LOG_FILE="/home/admin/.openclaw/workspace/logs/cron_$(date +%Y%m%d).log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting cron job: $1" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Current directory: $(pwd)" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Python path: $(which python3)" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Python version: $(python3 --version 2>&1)" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Environment variables set" >> "$LOG_FILE"

# Execute the script with error redirection
if [ -f "$1" ]; then
    bash "$1" >> "$LOG_FILE" 2>&1
    EXIT_CODE=$?
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Script completed with exit code: $EXIT_CODE" >> "$LOG_FILE"
    
    # Check for pending messages after execution
    PENDING_COUNT=$(ls /home/admin/.openclaw/workspace/messages/pending/ 2>/dev/null | wc -l)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Pending messages count: $PENDING_COUNT" >> "$LOG_FILE"
    
    if [ "$PENDING_COUNT" -gt 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: Found $PENDING_COUNT pending messages that may need processing" >> "$LOG_FILE"
    fi
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Script file not found: $1" >> "$LOG_FILE"
    EXIT_CODE=1
fi

# Final status
if [ "$EXIT_CODE" -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: Cron job completed successfully" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Cron job failed with exit code $EXIT_CODE" >> "$LOG_FILE"
    # Send error notification
    echo "Cron job failed: $1" > "/tmp/cron_error_$(date +%Y%m%d_%H%M%S).txt"
fi

exit $EXIT_CODE