# Advanced Configuration — Optional Optimizations

These are power-user tweaks. Eva-01 works perfectly on OpenClaw defaults. Everything here is optional.

**Reference config:** See `openclaw.json` in the blueprint root for all Eva-01 recommended settings.

**Warning:** These settings live in `openclaw.json`, which OpenClaw may change across versions. If something breaks after an update, remove advanced settings and go back to defaults.

---

## Model Routing (Cost Optimization)

By default, OpenClaw sends every message through your primary model. Add a `routing` block in `openclaw.json` to route simple messages to cheaper models. See `openclaw.json` for the config format. Expected savings: 50-70% on API costs.

OpenClaw's default classifier is keyword-based. For production accuracy, consider a `before_dispatch` hook with a custom classifier (see Hooks below).

To remove routing: delete the `routing` block. Everything reverts to your primary model.

---

## Memory Search Tuning

OpenClaw's default memory search works well out of the box. For more precise recall, enable hybrid search with temporal decay via the `memorySearch` section in `openclaw.json`.

---

## Heartbeat Interval

Default: 30 minutes (~48/day). Eva-01 recommends `"2h"` for most users. Valid values: `"30m"`, `"1h"`, `"2h"`, `"4h"`. Set `"0m"` to disable.

Channel options: `"last"` (most recent), `"telegram"`, `"discord"`, `"whatsapp"`, `"none"` (silent).

---

## Filesystem Policy (Security Hardening)

Restrict file access to the workspace folder only. See `filesystem` section in `openclaw.json`.

**Trade-off:** Agent can't clone repos to `~/Projects/`, can't create desktop backups, can't read files outside workspace. All project work must happen inside the workspace.

---

## Auto-Injection via Hooks

OpenClaw v2026.3.24 supports `boot-md` and `bootstrap-extra-files` under `hooks.internal.entries` (not under `agents.defaults`). If your version supports this, adding them gives you auto-injection of core files at session start — saving ~4,000 tokens per session versus manual loading.

Check your live config (`~/.openclaw/openclaw.json`) for a `hooks` section. If it exists and has `internal.entries`, you can add:
- `"boot-md": "SOUL.md"`
- `"bootstrap-extra-files": ["AGENTS.md", "USER.md", "MEMORY.md", "IDENTITY.md", "TOOLS.md"]`

If your version doesn't have a hooks section, skip this. Eva-01 detects whether auto-injection is active and loads files manually if needed.

---

## before_dispatch Hook (Advanced Routing)

OpenClaw v2026.3.24+ hooks run before message routing. A `before_dispatch` hook receives inbound metadata (sender, channel, message, session history length) and can override the routing tier. See OpenClaw's hooks documentation for the config format.

---

## Container Mode

When running `openclaw --container`: workspace is mounted at `/workspace`, `~/Projects/` may not exist (use `./projects/`), backup paths won't work (use workspace-relative paths), and git may not be available.

---

## Post-Update Checklist

After updating OpenClaw:

1. Run `openclaw doctor --fix` to auto-repair known config issues
2. Check `shipping/COMPATIBILITY.md` for known breaking changes
3. Review OpenClaw release notes: https://github.com/openclaw/openclaw/releases
4. Test Eva-01 in a quick session to verify everything works
