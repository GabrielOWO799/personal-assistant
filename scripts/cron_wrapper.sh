#!/bin/bash
# Cron wrapper script to ensure proper environment
export PATH="/home/linuxbrew/.linuxbrew/bin:/usr/local/bin:/usr/bin:/bin"
export PYTHONPATH="/home/admin/.local/lib/python3.8/site-packages"
cd /home/admin/.openclaw/workspace

# Log execution
echo "$(date): Running $1" >> /home/admin/.openclaw/workspace/logs/cron.log 2>&1

# Execute the script
bash "$1" >> /home/admin/.openclaw/workspace/logs/cron.log 2>&1