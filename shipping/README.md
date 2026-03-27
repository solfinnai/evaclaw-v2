# Eva-01 — Your AI Chief of Staff (v4.3)

This folder is Eva-01's brain. Every file shapes who she is, what she knows, and how she works.

**Compatible with:** OpenClaw v2026.3.24+ (see `shipping/COMPATIBILITY.md` for tested range)
**Reference config:** `openclaw.json`

## Quick Start

**New to Eva-01?** -> Read `INSTALL-GUIDE.md`
**Upgrading from v4.1?** -> Read `HOW-TO-UPGRADE.md`

## What's Inside

### Files You Fill Out (your identity)
| File | What It Does | When to Edit |
|------|-------------|-------------|
| **IDENTITY.md** | Agent's name and vibe | Once, during setup |
| **USER.md** | Everything about YOU (15 sections) | Setup + whenever things change |
| **SOUL.md** | Agent's personality, voice, and how she handles your emotions | Setup + refine over time |
| **CURRENT-PRIORITIES.md** | What matters this week | Weekly |
| **GAME-OF-LIFE.md** | Life scorecard across 8 domains | Monthly |
| **TOOLS.md** | Your specific tools, devices, accounts | As needed |

### Files That Run Things (don't edit unless you know what you're doing)
| File | What It Does |
|------|-------------|
| **AGENTS.md** | Core operating rules, security directives, learning system |
| **AGENTS-REFERENCE.md** | Extended rules loaded on demand (data classification, group chats, heartbeat logic) |
| **HEARTBEAT.md** | What the agent checks periodically |
| **RESEARCH.md** | Research log + development wishlist |
| **INTEGRATIONS.md** | MCP bridges, plugin security, audit checklist |
| **BOOTSTRAP.md** | First-run setup (renamed to .completed after first session) |
| **openclaw.json** | OpenClaw configuration with all Eva-01 settings |

### Files the Agent Fills (she writes these, you read them)
| File | What It Does |
|------|-------------|
| **MEMORY.md** | Long-term memory — general observations safe for all contexts |
| **memory/private-notes.md** | Sensitive observations — only loaded in direct conversations |
| **memory/YYYY-MM-DD.md** | Daily logs (what happened each day) |
| **memory/inbox.md** | Stale item tracker (items carried forward too long) |
| **memory/security-log.md** | Security event audit trail (injection attempts, directive conflicts) |
| **memory/research/** | Research outputs when you ask her to look things up |

### Shipping & Docs (for humans, not the agent)
| File | What It Does |
|------|-------------|
| **shipping/COMPATIBILITY.md** | OpenClaw version tracking + breaking change matrix |
| **shipping/INSTALL-GUIDE.md** | Getting started from scratch |
| **shipping/HOW-TO-UPGRADE.md** | Upgrading from a previous version |
| **shipping/FIRST-PROMPTS.md** | Guided first-session walkthrough |
| **shipping/CHANGELOG.md** | Version history |

## How It Works

1. You fill out USER.md and SOUL.md (15 min)
2. Install OpenClaw and copy these files into your workspace folder
3. The shipped `openclaw.json` configures everything automatically
4. Start chatting via Telegram, Discord, or any supported channel
5. Eva-01 reads BOOTSTRAP.md on first contact and sets herself up
6. Every conversation makes her smarter about you
7. She writes general observations to MEMORY.md and sensitive notes to memory/private-notes.md
8. Weekly, she reviews the week and cleans up her memory

## Architecture: How Files Load

Eva-01 detects whether your OpenClaw version supports auto-injection (`boot-md` / `bootstrap-extra-files` config keys). If it does, core files are pre-loaded. If not, Eva-01 reads them manually at session start. Both modes work — no config changes needed.

**Core files (loaded every session, one way or another):** SOUL.md, AGENTS.md, USER.md, MEMORY.md, IDENTITY.md, TOOLS.md

**Session-start files (always loaded manually):** Today/yesterday daily logs, CURRENT-PRIORITIES.md, memory/private-notes.md (main session only)

**On-demand files (loaded only when relevant):** AGENTS-REFERENCE.md, GAME-OF-LIFE.md, RESEARCH.md, INTEGRATIONS.md

**Important:** If auto-injection IS active, MEMORY.md is loaded in ALL session types, including group chats. That's why sensitive observations go in memory/private-notes.md instead.

## Philosophy

Simple to start. Powerful to scale. The foundation never needs undoing.

Eva-01 works perfectly with just the core files and `openclaw.json`. Advanced config options are available in `docs/ADVANCED-CONFIG.md` when you're ready, but you may never need them.

## Security

Your data stays on YOUR machine. Eva-01 classifies everything into 4 tiers (Public, Internal, Confidential, Restricted) and never shares sensitive information outside your direct conversation. See the Constitutional Directives in AGENTS.md and full data classification rules in AGENTS-REFERENCE.md.

**v4.3 security improvements:**
- Unique placeholder token (`{{OWNER_LEGAL_NAME}}`) resistant to injection attacks
- Security event audit log (`memory/security-log.md`) for directive conflicts and injection attempts
- Constitutional Directive #6 now covers MCP bridges in addition to skills/plugins
- Directive integrity checking via git diff during weekly reviews
- Plugin security audit checklist in INTEGRATIONS.md
- Explicit `openclaw.json` configuration prevents misconfigured auto-injection
- Valid JSON config file (no more comment-parsing issues)

## Support

Visit **evaonline.xyz** for guides, plugins, and help.
