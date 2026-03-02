This skill helps you search, install, update, and publish skills from ClawHub with caching and openclaw-core support.
This is most likely a fork of the
 [clawhud](/skills/openclaw/skills/clawhud)
skill from
 [openclaw](/skills/openclaw)

npx playbooks add skill openclaw/skills --skill clawhub

Review the files below or copy the command above to add this skill to your agents.

## Overview
This skill provides a command-line interface to search, install, update, and publish agent skills from clawhub.ai with advanced caching and compression for faster transfers. It relies on openclaw-core to perform network and file operations and supports hash-based updates, batch operations, and semantic version management. Use it to fetch skills on demand, keep installations synchronized, or publish optimized skill packages to the registry.

## How this skill works
The CLI queries the configured ClawHub registry to discover skills, downloads compressed skill archives into a local cache, and installs them into a target directory. Updates use file hashing to detect changes and preserve local modifications where possible; publishing packages a local skill folder, applies compression and metadata (slug, version, changelog), and uploads it under your authenticated account. Environment variables and a ~/.clawhubrc file let you override registry, workdir, and install paths.

## When to use it

- When you need to quickly discover and install new agent skills from clawhub.ai
- When you want automated, hash-based updates that preserve local edits
- When publishing new or updated skills with optimized size via compression
- When managing large sets of skills in CI/CD or batch scripts
- When working offline with cached versions of previously fetched skills

## Best practices

- Install and run openclaw-core before using any ClawHub commands—CLI requires it
- Pin critical skills to specific semver versions to avoid unexpected changes
- Run weekly updates (clawhub update --all) and review changelogs before applying
- Keep SKILL.md and tests up to date; validate locally before publishing
- Use environment variables or ~/.clawhubrc for reproducible install and registry settings

## Example use cases

- Search and install a database backup skill on a fresh host: clawhub search "postgres backups" && clawhub install pg-backup
- CI workflow that publishes a skill on tag push using clawhub publish with semantic versioning
- Mass update across developer machines: clawhub update --all --no-input --force in a scheduled job
- Prepare an offline deployment by pre-caching required skills and copying the cache to air-gapped hosts
- Publish a patch release with compressed upload and changelog: clawhub publish ./my-skill --slug my-skill --version patch --changelog "fix"

## FAQ
What happens if openclaw-core is not running?
ClawHub CLI operations will fail. Ensure openclaw-core is installed and the process is running before using the CLI.

How does the update command avoid overwriting local changes?
Updates use file hashing to identify base versions and preserve local modifications where possible; use --force to override hash checks.