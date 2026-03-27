# Install Guide — Getting Eva-01 Running

Welcome! This guide gets you from zero to a working AI Chief of Staff in about 10 minutes.

## What You Need

- A computer (Mac, Windows, or Linux)
- An internet connection
- Node.js 22 or newer installed (Node 24 recommended) — download from https://nodejs.org
- An API key from Anthropic (Claude), OpenAI, or another supported provider

## Step 1: Install OpenClaw

Open your Terminal (Mac/Linux) or PowerShell (Windows) and run:

```
npm install -g openclaw@2026.3.24
```

**Why a specific version?** Eva-01 v4.3 is tested against OpenClaw v2026.3.24. Using `@latest` may pull a newer version with breaking changes. See `shipping/COMPATIBILITY.md` for the tested version range. You can update later once you've verified compatibility.

Then run the setup wizard:

```
openclaw onboard --install-daemon
```

The wizard walks you through everything: API keys, connecting a chat channel (Telegram, Discord, WhatsApp, etc.), and starting the background daemon. Follow the prompts.

When it asks about your workspace, note the path it gives you. By default this is `~/.openclaw/workspace/`. You'll need it for the next step.

### Heartbeat Configuration (Recommended)

After onboarding, configure the heartbeat interval. OpenClaw defaults to 30 minutes, which is frequent. For Eva-01, we recommend starting with 2 hours:

```
openclaw config set heartbeat.interval "2h"
```

You can always tighten it later. See `docs/ADVANCED-CONFIG.md` for all heartbeat options.

## Step 2: Install the Blueprint

Copy all the files from this blueprint folder into your OpenClaw workspace folder:

**Mac/Linux:**
```
cp -r ./v4.3/* ~/.openclaw/workspace/
```

**Windows (PowerShell):**
```
Copy-Item -Path .\v4.3\* -Destination ~\.openclaw\workspace\ -Recurse
```

If your workspace is in a different location (the onboard wizard told you where), use that path instead.

**Container mode:** If running `openclaw --container`, copy files to the mounted workspace path instead.

## Step 3: Configure OpenClaw for Eva-01

Eva-01 ships with `openclaw.json` — a configuration file with recommended settings (model, heartbeat interval). When you copied the blueprint files into your workspace, this was included automatically.

**If you already have an openclaw.json:** Back up your existing config, then merge the Eva-01 settings you want:
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup
```
Compare the shipped `openclaw.json` against yours. The key settings are `model.primary` (anthropic/claude-sonnet-4-6) and `heartbeat.every` ("2h"). Merge what makes sense — don't blindly replace, as your existing config has auth, channel, and plugin settings you'll lose.

**At minimum, verify these settings in your `openclaw.json`:**
- Your model provider and API key are configured
- `heartbeat.every` is set to `"2h"` (not the default `"30m"`)

**Note on auto-injection:** Some OpenClaw versions support `boot-md` and `bootstrap-extra-files` config keys that auto-load files at session start. If your version supports them, add `"boot-md": "SOUL.md"` and a `"bootstrap-extra-files"` array to your config. If your version doesn't (the gateway rejects unknown keys), skip them — Eva-01 will detect this and load files manually instead. Both modes work.

See `docs/ADVANCED-CONFIG.md` for all optional settings (routing, memory search, filesystem policy, hooks, MCP bridges).

## Step 4: Fill Out Your Profile

Open these two files in any text editor and fill them out:

1. **USER.md** — Everything about you. The more detail you provide, the better Eva-01 knows you. At minimum, fill in your name, role, and communication preferences.

2. **SOUL.md** — Eva-01's personality. The defaults are solid (including the Handling Manual), but customize anything that doesn't match how you want your agent to respond.

## Step 5: Start Talking

Open your chat channel (Telegram, Discord, whatever you connected during onboard) and send Eva-01 a message. Say hello.

On first contact, Eva-01 reads BOOTSTRAP.md and sets herself up automatically:
- Checks environment (git availability, workspace permissions)
- Learns your name from USER.md
- Personalizes her security directives (replaces `{{OWNER_LEGAL_NAME}}` in AGENTS.md)
- Verifies the replacement worked (safety check)
- Initializes version control for your workspace (if git is available)
- Creates her first daily log
- Verifies private notes and security log files exist
- Sets up the weekly memory review
- Introduces herself
- Renames BOOTSTRAP.md to BOOTSTRAP.md.completed (preserved for reference)

After that, Eva-01 is fully operational.

## What to Expect

Eva-01's core files (SOUL.md, AGENTS.md, USER.md, MEMORY.md, IDENTITY.md, TOOLS.md) are auto-loaded by OpenClaw every session. She'll know your name, your priorities, and your communication style from the first message.

The more you talk to her, the smarter she gets. She writes general observations to MEMORY.md (visible in all sessions), sensitive observations to memory/private-notes.md (private to direct chats), and raw logs to daily files.

## Customize

- Edit **SOUL.md** to change her personality and voice
- Edit **USER.md** to update your profile as things change
- Edit **CURRENT-PRIORITIES.md** weekly to keep her focused
- Edit **INTEGRATIONS.md** to set up external tools and MCP bridges
- **MEMORY.md** and **memory/private-notes.md** grow on their own as she learns about you

## Troubleshooting

**Agent doesn't seem to know who it is?**
Check your `openclaw.json` and make sure your model and heartbeat settings are correct. Eva-01 detects whether auto-injection is active and loads files manually if needed — the config doesn't have to be perfect.

**Agent didn't run BOOTSTRAP.md?**
Send this message: "Read BOOTSTRAP.md in your workspace and follow the instructions."

**AGENTS.md still has `{{OWNER_LEGAL_NAME}}` placeholders?**
Bootstrap may have failed partially. Tell your agent: "Check the Constitutional Directives in AGENTS.md. Replace every `{{OWNER_LEGAL_NAME}}` with my actual name: [your name]."

**Files not auto-loading?**
Eva-01 loads core files (SOUL.md, USER.md, MEMORY.md, etc.) either via auto-injection or manually at session start. If she seems to have no context, try sending: "Read SOUL.md and USER.md, then greet me."

**Need to start over?**
If BOOTSTRAP.md.completed exists, rename it back to BOOTSTRAP.md and tell the agent to re-run setup. Your workspace has git version control (if git was available), so you can also `git log` to see checkpoints and restore any previous state.

## Need Help?

Visit **evaonline.xyz** for guides, advanced plugins, and support.
