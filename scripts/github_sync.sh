#!/bin/bash
# GitHub Memory Sync Script
# Syncs memory files to GitHub repository

cd /home/admin/.openclaw/workspace

# GitHub repository and token
REPO="GabrielOWO799/personal-assistant"
TOKEN="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"

# Create git config if not exists
if [ ! -d ".git" ]; then
    git init
    git remote add origin https://$TOKEN@github.com/$REPO.git
    git config --global user.email "assistant@openclaw.ai"
    git config --global user.name "OpenClaw Assistant"
fi

# Add memory files
git add MEMORY.md
git add memory/*.md
git add AGENTS.md
git add SOUL.md
git add USER.md
git add TOOLS.md
git add HEARTBEAT.md

# Commit and push
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
if ! git diff --quiet; then
    git commit -m "Memory sync: $TIMESTAMP"
    git push origin main
    echo "[$(date)] GitHub memory sync completed successfully" >> memory/$(date +%Y-%m-%d).md
else
    echo "[$(date)] GitHub memory sync: No changes to commit" >> memory/$(date +%Y-%m-%d).md
fi