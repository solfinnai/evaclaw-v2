# COMPATIBILITY.md — Version Compatibility Matrix

Eva-01 Blueprint v4.3 is tested against specific OpenClaw versions. This file tracks compatibility and helps the agent detect version mismatches.

## Current Compatibility

```
BLUEPRINT_VERSION=4.3
MIN_OPENCLAW_VERSION=2026.3.24
MAX_TESTED_OPENCLAW_VERSION=2026.3.24
COMPATIBILITY_CHECK_DATE=2026-03-26
```

## How Version Checking Works

During session startup, if the agent detects that OpenClaw has been updated since `MAX_TESTED_OPENCLAW_VERSION`, it should:

1. Log a notice (not an error): "OpenClaw version newer than last tested. Monitoring for issues."
2. Continue operating normally
3. Watch for any of these symptoms:
   - Auto-injected files missing or duplicated
   - Tool calls failing unexpectedly
   - Routing behaving differently
   - Heartbeat timing changes
   - Plugin/skill installation errors
4. If symptoms appear, log to `memory/security-log.md` as an `INTEGRITY_ALERT` and notify the owner

## Known Breaking Changes by OpenClaw Version

| OpenClaw Version | Breaking Change | Eva-01 Impact | Mitigation |
|-----------------|----------------|---------------|------------|
| v2026.3.22 | Plugin install checks ClawHub before npm | Skills may resolve to different packages | Use `--source npm` flag if needed |
| v2026.3.22 | Removed `CLAWDBOT_*` / `MOLTBOT_*` env vars | None (Eva-01 doesn't use legacy vars) | N/A |
| v2026.3.22 | Legacy Chrome extension relay removed | None (Eva-01 doesn't use Chrome relay) | N/A |
| v2026.3.22 | Dashboard UI broken for npm users | Control UI may not load | Upgrade to v2026.3.23-2+ |
| v2026.3.22 | WhatsApp integration broken for npm users | WhatsApp channel may fail | Upgrade to v2026.3.23-2+ |

## Recommended Practice

**Pin your OpenClaw version** in production:

```bash
npm install -g openclaw@2026.3.24
```

**Before updating OpenClaw:**

1. Create a workspace backup (see shipping/HOW-TO-UPGRADE.md, Prompt 5)
2. Check OpenClaw release notes: https://github.com/openclaw/openclaw/releases
3. Look for breaking changes that affect boot-md, bootstrap-extra-files, heartbeat, or filesystem policies
4. Update and run `openclaw doctor --fix` to auto-repair known config issues
5. Verify Eva-01 loads correctly in a test session

## Future Risks to Monitor

### OpenClaw "Agent OS" Direction

OpenClaw's 2026 roadmap signals a shift toward functioning as an "agent operating system" with platform-level identity, memory, and skill management. If OpenClaw ships native identity or memory systems, they could conflict with Eva-01's workspace-as-brain model (where SOUL.md, MEMORY.md, and AGENTS.md are the source of truth).

**Watch for:** New OpenClaw config options for agent identity, platform-managed memory, or built-in persona systems. If these appear, evaluate whether to adopt them or continue with workspace-managed files.

### Sandbox Readiness

OpenClaw plans to add sandboxed worker execution, isolating agents from the host filesystem. Eva-01 currently assumes direct filesystem access in several places:

- BOOTSTRAP.md (git init, file creation, cron setup)
- memory/cron-weekly-review.md (git add, git commit, file moves, archive creation)
- HEARTBEAT.md (file reads, state tracking)

When sandboxed execution ships, audit all file operations in the blueprint.

### Native Skills Expansion

OpenClaw v2026.3.24 ships 50+ bundled skills with one-click install in the Control UI. As this library grows, Eva-01's on-demand skill discovery via the `/tools` endpoint and Control UI may be sufficient without additional tracking. Monitor whether custom skill documentation adds value beyond what OpenClaw provides natively.
