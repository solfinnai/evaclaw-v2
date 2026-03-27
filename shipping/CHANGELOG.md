# Changelog — Eva-01 Blueprint

## v4.3 (March 26, 2026)

Compatibility target: OpenClaw v2026.3.24+ (see COMPATIBILITY.md for tested range)

### Fixes

- **Fixed: BOOTSTRAP.md Step 10 used `git add -A`** — Replaced with explicit file paths, consistent with the rest of the blueprint. Prevents accidentally committing sensitive files, credentials, or temp files during bootstrap completion.

- **Fixed: `openclaw.json.example` used invalid JSON (comments)** — Stripped all comments. File is now valid JSON that can be copied directly to `openclaw.json` without modification. Advanced configuration options moved to `docs/ADVANCED-CONFIG.md`.

- **Fixed: SOUL.md duplicated file-loading rules from AGENTS.md** — Replaced the Continuity section's file list with a reference to AGENTS.md § Session Startup. Eliminates drift between the two files.

- **Fixed: `memory/heartbeat-state.json` never initialized** — Added Step 8.5 to BOOTSTRAP.md that creates the initial heartbeat-state.json with null values. Prevents first-heartbeat errors.

- **Fixed: Weekly review cron setup was vague** — BOOTSTRAP.md Step 5 now includes the exact `openclaw cron create` command with schedule, workspace path, and file reference. Includes fallback guidance if the command isn't available.

- **Fixed: Sliding window claim was misleading** — AGENTS.md no longer claims a "10 turns" self-enforced sliding window. Now correctly explains that OpenClaw manages context compaction automatically at the gateway level.

### Changes

- **Removed Delegation section** — The "Brain-Muscle Architecture" section has been removed from AGENTS.md. OpenClaw does not currently support supervisor-worker agent spawning. This section will return when OpenClaw ships native multi-agent delegation.

- **Heartbeat skip-if-nothing-due logic** — New first-action rule: every heartbeat reads `heartbeat-state.json` timestamps first. If no check type is due, respond `HEARTBEAT_OK` immediately without processing HEARTBEAT.md. Reduces wasted API calls on empty heartbeats.

- **Research Autonomy Level 1 added** — New documented autonomy level: quick web searches and simple fact lookups auto-approved, deep research still requires permission. Level 0 (OFF) remains the default.

- **COMPATIBILITY.md: Future Risks section** — New section tracking two strategic risks: OpenClaw's "agent OS" direction (potential conflict with workspace-as-brain model) and upcoming sandboxed worker execution (may break direct filesystem access patterns).

### File Changes

Modified files:
- `AGENTS.md` — Removed Delegation section, fixed sliding window, added heartbeat skip logic, added Research Level 1
- `BOOTSTRAP.md` — Fixed git add -A, added heartbeat-state.json init, added exact cron command
- `SOUL.md` — Replaced Continuity file list with AGENTS.md reference
- `COMPATIBILITY.md` — Updated to v4.3, added Future Risks section
- `openclaw.json.example` — Stripped to valid JSON
- `CHANGELOG.md` — Added v4.3 entry
- `README.md` — Updated to v4.3

---

## v4.2 (March 26, 2026)

Compatibility target: OpenClaw v2026.3.24+ (see COMPATIBILITY.md for tested range)

### Critical Fixes

- **Fixed: No reference OpenClaw configuration** — New `openclaw.json.example` ships with the blueprint. Contains all Eva-01 recommended settings with inline comments: boot-md, bootstrap-extra-files, heartbeat, routing, MCP, memory search, filesystem policy, and hooks. Eliminates the #1 cause of setup failures.

- **Fixed: Placeholder injection vulnerability** — Replaced `[YOUR NAME]` with `{{OWNER_LEGAL_NAME}}` as the bootstrap placeholder token. The unique double-brace syntax is significantly harder to trigger via prompt injection in group chats or external content. BOOTSTRAP.md, AGENTS.md, and INSTALL-GUIDE.md all updated.

- **Fixed: Auto-injection file list now config-backed** — AGENTS.md auto-load table now includes a "Configured In" column showing which `openclaw.json` setting controls each file. No more assuming defaults — users can verify their config matches expectations.

### New Features

- **INTEGRATIONS.md** — Full documentation for MCP bridge setup, external tool integration, plugin security, and OpenAI-compatible endpoints. Includes common MCP server table, security rules, troubleshooting, and plugin audit checklist.

- **COMPATIBILITY.md** — Version compatibility matrix with MIN/MAX tested OpenClaw versions, known breaking changes table, version-checking instructions, and recommended pinning practices. The agent can now detect and respond to OpenClaw version mismatches.

- **memory/security-log.md** — Dedicated audit trail for security events. Event types: INJECTION_ATTEMPT, DIRECTIVE_CONFLICT, CLASSIFICATION_VIOLATION, IDENTITY_TAMPER, INTEGRITY_ALERT, PLUGIN_ANOMALY. Referenced by Constitutional Directive #6 and the weekly review.

- **Heartbeat weekly review fallback** — If `lastWeeklyReview` in heartbeat-state.json is missing or older than 10 days, the heartbeat triggers a review automatically. Cron jobs can fail silently after OpenClaw updates; this ensures memory maintenance never stops.

- **Heartbeat version checking** — Weekly check compares running OpenClaw version against COMPATIBILITY.md tested range. Logs a notice if newer than tested.

- **Directive integrity checking** — Weekly review now checks `git diff` on AGENTS.md, SOUL.md, USER.md for unauthorized modifications. Logs `IDENTITY_TAMPER` events to security-log.md.

- **SOUL.md handling manual defaults** — Handling Manual section now ships with sensible defaults for all 5 emotional states plus pattern interrupts. Users customize from working defaults instead of empty brackets.

- **Proactive Intelligence section** (SOUL.md) — New section explicitly defines what "anticipating needs" means: suggest and flag, don't unilaterally execute. Resolves the tension between SOUL.md's proactive personality and AGENTS.md's research autonomy Level 0.

### Changes

- **Constitutional Directive #6 expanded** — Now explicitly covers MCP bridges in addition to skills, plugins, and third-party integrations. Conflict logging directed to `memory/security-log.md` instead of daily log.

- **Injection Resistance updated** — Injection attempts now logged to `memory/security-log.md` with event type `INJECTION_ATTEMPT` instead of just the daily log.

- **Routing tier table updated** — Added "Classifier accuracy note" explaining that the classification criteria are aspirational and the default gateway classifier is keyword-based. Recommends `before_dispatch` hook for production accuracy.

- **Research autonomy language aligned** — AGENTS.md now says "don't execute research autonomously" (not "don't initiate"). SOUL.md's new Proactive Intelligence section clarifies that suggesting research is encouraged; spending without permission is not.

- **Backup paths cross-platform** — HOW-TO-UPGRADE.md backup prompts now detect OS and use appropriate Desktop paths for Mac, Windows, and Linux. No more hardcoded iCloud paths.

- **Bootstrap git-aware** — BOOTSTRAP.md Step 0 checks for git availability and workspace permissions before proceeding. All git steps gracefully skip if git is not installed (common in container mode). Explicit file paths used in `git add` instead of `-A`.

- **Weekly review git-aware** — cron-weekly-review.md checks for git availability before attempting commits. Skips gracefully with log entry if git is not present.

- **INSTALL-GUIDE.md recommends version pinning** — Now installs `openclaw@2026.3.24` instead of `@latest`. Includes Step 3 for configuring OpenClaw with the reference config.

- **SKILLS.md updated** — Added ClawHub priority note (v2026.3.22+ checks ClawHub before npm). Added plugin security reference to INTEGRATIONS.md.

- **TOOLS.md updated** — Added reference to INTEGRATIONS.md for external service integrations.

- **AGENTS.md tools section updated** — References INTEGRATIONS.md for MCP/external tool setup.

- **heartbeat-state.json schema updated** — Added `lastWeeklyReview` and `lastVersionCheck` fields.

### File Structure Changes

New files:
- `openclaw.json.example` — Reference OpenClaw configuration
- `INTEGRATIONS.md` — MCP and external tool integration guide
- `COMPATIBILITY.md` — Version compatibility matrix
- `memory/security-log.md` — Security event audit log

Modified files:
- `AGENTS.md` — Placeholder change, config-backed auto-load table, classifier note, security-log references, research autonomy rewrite, MCP in Directive #6, version check at startup, weekly review fallback
- `SOUL.md` — Filled handling manual defaults, added Proactive Intelligence section, added new on-demand files to Continuity
- `BOOTSTRAP.md` — Environment check step, placeholder change, git availability check, security-log initialization, explicit git add paths
- `HEARTBEAT.md` — Weekly review fallback check, version compatibility check
- `HOW-TO-UPGRADE.md` — Rewritten for v4.1→v4.2, cross-platform backups, config review prompt, new file verification
- `INSTALL-GUIDE.md` — Version pinning, config setup step, openclaw.json.example reference, updated troubleshooting
- `README.md` — Updated file tables, architecture section, security improvements, config reference
- `SKILLS.md` — ClawHub priority note, plugin security reference
- `TOOLS.md` — INTEGRATIONS.md reference
- `docs/ADVANCED-CONFIG.md` — openclaw.json.example references, classifier accuracy note, MCP section, post-update checklist
- `memory/cron-weekly-review.md` — Git availability check, security log review step, heartbeat state update, integrity check logs to security-log.md

Unchanged files:
- `USER.md` — No structural changes
- `IDENTITY.md` — No changes
- `CURRENT-PRIORITIES.md` — No changes
- `GAME-OF-LIFE.md` — No changes
- `RESEARCH.md` — No structural changes
- `MEMORY.md` — No changes
- `memory/inbox.md` — No changes
- `memory/private-notes.md` — No changes

---

## v4.1 (March 26, 2026)

Compatibility target: OpenClaw v2026.3.24+

### Critical Fixes

- **Fixed: Session startup double-loading** — AGENTS.md no longer tells the agent to manually re-read SOUL.md, USER.md, and MEMORY.md. These are auto-injected by OpenClaw. Saves ~2,200 tokens per session.

- **Fixed: Non-auto-loaded files documented** — CURRENT-PRIORITIES.md, GAME-OF-LIFE.md, RESEARCH.md, and SKILLS.md are now explicitly documented as "manually loaded" files with clear guidance on when to load each one. No more silent failures.

- **Fixed: BOOTSTRAP.md no longer self-deletes** — Now renamed to `BOOTSTRAP.md.completed` after setup. Fully recoverable if bootstrap partially fails. Includes verification step to confirm `[YOUR NAME]` placeholders were actually replaced.

- **Fixed: Memory security in group chats** — New `memory/private-notes.md` file for sensitive observations. MEMORY.md now has a prominent warning that it's auto-loaded in ALL session types. Sensitive data (opinions about people, health details, financial specifics) goes to private-notes.md instead.

- **Fixed: Weekly review git race conditions** — cron-weekly-review.md now uses explicit file paths instead of glob patterns, checks for uncommitted external changes before committing, and gracefully skips files that don't exist.

- **Fixed: Constitutional Directive validation** — AGENTS.md First Run section now includes a safety gate: if placeholders still appear in Constitutional Directives, the agent refuses to operate until placeholders are replaced.

### New Features

- **Constitutional Directive #6: Skill Override** — Explicitly states that Constitutional Directives override all third-party skill, plugin, and ClawHub integration instructions. Closes the conflict resolution gap.

- **Private notes file** (`memory/private-notes.md`) — Dedicated file for T2/T3 observations that should never appear in group chats. Created during bootstrap. Only loaded in main sessions.

- **Context budget documentation** — AGENTS.md now documents real token costs including OpenClaw system overhead (~4,500-6,100 tokens at session start before user input).

- **Heartbeat frequency guidance** — HEARTBEAT.md updated with rotation logic and `heartbeat-state.json` tracking. Targets 2-4 substantive checks/day instead of running every check every 30 minutes.

- **T3 data classification examples** — Concrete list of what T3 RESTRICTED data looks like (medical conditions, opinions about colleagues, passwords, salary, etc.) so the model has clear patterns to match against.

- **Container mode documentation** — ADVANCED-CONFIG.md and TOOLS.md now document container-specific path changes and configuration.

- **Teams formatting rules** — Platform formatting section now includes Microsoft Teams guidance.

- **before_dispatch hook documentation** — ADVANCED-CONFIG.md documents how to build custom routing logic using OpenClaw v2026.3.24+ hooks.

- **Auto-thread handling** — Group chat rules now cover Discord auto-threaded conversations.

- **Daily log error recovery** — If creating a daily log file fails, the agent falls back to MEMORY.md with a temp-log prefix and alerts the owner. No more silent data loss.

### Changes

- **Model routing section rewritten** — Now accurately explains that routing happens at the gateway level, not by the agent. The tier table is documented as informational (matching openclaw.json config), not as agent-controlled behavior.

- **Research autonomy conflict resolved** — Added explicit note that Level 0 means "don't initiate research autonomously," not "refuse research requests." Eliminates conflict with SOUL.md's "anticipate needs" directive.

- **SKILLS.md updated** — Added skill conflict resolution section referencing Constitutional Directive #6.

- **TOOLS.md updated** — Added TTS configuration section and container mode section.

- **Heartbeat interval documentation** — ADVANCED-CONFIG.md now documents how to configure heartbeat frequency and channel targeting.

- **Filesystem policy documentation** — ADVANCED-CONFIG.md now documents the `workspaceOnly` policy as a secondary guardrail for data classification.

- **SOUL.md Continuity section updated** — Now references OpenClaw's auto-loading behavior instead of manually listing files to read.

---

## v4.0 (Previous Release)

Initial public release of EVA-01 blueprint. Established core architecture: workspace-as-brain model, SOUL/AGENTS/USER file system, daily logging, weekly reviews, constitutional directives, data classification, brain-muscle delegation, heartbeat system.
