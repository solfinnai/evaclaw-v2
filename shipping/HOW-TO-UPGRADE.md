# How to Upgrade Your Agent (For Humans)

Your agent just got a major upgrade. This guide walks you through installing it in about 5 minutes. Your agent does all the hard work. You just need to hand it the files and tell it to go.

**What stays safe:** All your personal stuff (your profile, memories, daily logs, priorities, projects) is untouched. The upgrade only changes the "operating system" your agent runs on, not any of your personal data.

**What changes (v4.2 → v4.3):**
- Fixed: BOOTSTRAP.md no longer uses `git add -A` (explicit file paths now, consistent with security guidance)
- Fixed: `openclaw.json` ships as ready-to-use config (was `openclaw.json.example`)
- Fixed: SOUL.md no longer duplicates file-loading rules from AGENTS.md
- Fixed: `memory/heartbeat-state.json` now initialized during bootstrap
- Fixed: Weekly review cron command is now explicit in BOOTSTRAP.md
- Fixed: Sliding window correctly documented as OpenClaw-managed (not agent self-enforced)
- Removed: Delegation ("Brain-Muscle") section (will return when OpenClaw ships multi-agent)
- Added: Heartbeat skip-if-nothing-due logic (reduces wasted API calls)
- Added: Research Autonomy Level 1 (quick searches auto-approved)
- Added: Future risk tracking in shipping/COMPATIBILITY.md (agent OS direction, sandbox readiness)
- Added: AGENTS-REFERENCE.md (extended rules split from AGENTS.md for lighter context)
- Added: FIRST-PROMPTS.md guided onboarding walkthrough in shipping/

---

## Step 0: Back Up Your Current Agent First

Before you upgrade anything, make a full backup of your agent as it is right now. That way, no matter what happens, you have a complete snapshot you can restore from.

Open a chat with your agent and send this:

---

> **COPY/PASTE PROMPT 0 — Full backup before upgrade:**

```
Before we do anything, I need a complete backup of my current agent.

1. Detect my operating system and use the appropriate backup location:
   - Mac: ~/Desktop/eva-backup-YYYY-MM-DD.zip
   - Windows: %USERPROFILE%\Desktop\eva-backup-YYYY-MM-DD.zip
   - Linux: ~/Desktop/eva-backup-YYYY-MM-DD.zip (or ~/eva-backup-YYYY-MM-DD.zip if no Desktop)
2. Create a zip file of my entire ~/.openclaw/workspace/ folder
3. Name it: eva-backup-YYYY-MM-DD.zip (use today's actual date)
4. Save it to my Desktop using the path above
5. After creating it, tell me the file size and confirm it includes all my files (USER.md, MEMORY.md, SOUL.md, AGENTS.md, daily logs, docs, everything)
6. Suggest I copy it to cloud storage (iCloud, Google Drive, OneDrive, Dropbox — whatever I have) for safekeeping
7. Confirm when done
```

---

Wait for your agent to confirm the backup is created. Then check your Desktop and make sure the zip file is there. Once you see it, move on to Step 1.

**Why this matters:** This backup is your safety net. If the upgrade goes sideways, if you accidentally delete something in a month, if you get a new computer, this zip has everything. Your personality, your memories, your daily logs, your projects, all of it. One file, fully portable.

---

## Step 1: Download the Upgrade

Download the upgrade package from [evaonline.xyz](https://evaonline.xyz).

You'll get a folder called `v4.3/` with the upgrade files inside. Remember where you saved it.

---

## Step 2: Give Your Agent the Upgrade

Open a chat with your agent (Telegram, Discord, or however you normally talk to it) and send this message:

---

> **COPY/PASTE PROMPT 1 — Start the upgrade:**

```
I have an Eva-01 v4.3 upgrade package. The upgrade folder is at: [REPLACE THIS WITH YOUR PATH, e.g., ~/Downloads/v4.3/]

Here's what I need you to do:

1. First, create a git checkpoint (if git is available): git add AGENTS.md AGENTS-REFERENCE.md SOUL.md HEARTBEAT.md BOOTSTRAP.md RESEARCH.md openclaw.json memory/cron-weekly-review.md docs/ADVANCED-CONFIG.md && git commit -m "pre-upgrade-v4.3 checkpoint"
2. The upgrade folder has updated versions of framework files
3. For these files, REPLACE my versions with the new ones:
   - AGENTS.md, AGENTS-REFERENCE.md, HEARTBEAT.md, RESEARCH.md, BOOTSTRAP.md
   - openclaw.json
   - memory/cron-weekly-review.md
   - docs/ADVANCED-CONFIG.md
4. For SOUL.md: merge carefully — keep my personality customizations (especially the Handling Manual if I customized it), update the Continuity section (it now references AGENTS.md instead of duplicating file lists)
5. DO NOT touch: USER.md, MEMORY.md, CURRENT-PRIORITIES.md, GAME-OF-LIFE.md, IDENTITY.md, INTEGRATIONS.md, or anything in memory/*.md (except cron-weekly-review.md)
6. Create memory/heartbeat-state.json if it doesn't exist: {"lastChecks": {}, "heartbeatCount": 0, "lastSubstantiveCheck": null, "lastWeeklyReview": null}
7. In AGENTS.md, replace {{OWNER_LEGAL_NAME}} with my actual name in the Constitutional Directives (same name as v4.2 had)
8. After upgrading (if git is available): git add AGENTS.md AGENTS-REFERENCE.md SOUL.md HEARTBEAT.md BOOTSTRAP.md RESEARCH.md openclaw.json memory/cron-weekly-review.md memory/heartbeat-state.json docs/ADVANCED-CONFIG.md && git commit -m "upgraded to eva-01 v4.3"
9. Walk me through what you changed
```

**Important:** Replace the path in the first line with wherever you actually saved the v4.3 folder!

---

## Step 3: Verify Everything Looks Good

Once your agent says it's done, send this:

---

> **COPY/PASTE PROMPT 2 — Verify the upgrade:**

```
Upgrade looks done. Let's verify:

1. Read my USER.md and confirm my personal info is still there and unchanged
2. Read my MEMORY.md and confirm my memories are still there and unchanged
3. Read AGENTS.md and confirm my name appears correctly in the Constitutional Directives (all 3 locations — should NOT say {{OWNER_LEGAL_NAME}})
4. Confirm memory/private-notes.md exists and is unchanged
5. Confirm memory/security-log.md exists
6. Confirm memory/heartbeat-state.json exists (new in v4.3)
7. Confirm shipping/COMPATIBILITY.md has BLUEPRINT_VERSION=4.3
8. Confirm openclaw.json is valid JSON and uses `"every": "2h"` (not `"interval"`)
9. Check that my daily logs in memory/ are all still there
10. Confirm the Delegation section is gone from AGENTS.md (removed in v4.3)
11. Tell me what version we're now running (should be v4.3)

If anything looks wrong, tell me and we'll roll it back.
```

---

## Step 4: Configure OpenClaw (Optional but Recommended)

Eva-01 ships with `openclaw.json` — a ready-to-use configuration file. If you haven't customized your OpenClaw config yet, now is a good time:

---

> **COPY/PASTE PROMPT 3 — Review config:**

```
Read openclaw.json and compare it against my current ~/.openclaw/openclaw.json. Tell me:
1. What settings I'm missing that Eva-01 recommends (model, heartbeat)
2. What settings I have that conflict with the reference
3. Whether my heartbeat is set to "every": "2h" (not "interval")

Don't change anything yet — just tell me what you'd recommend.
```

---

## Step 5: Done!

If everything checks out, you're upgraded. Your agent is now running v4.3 with:
- Ready-to-use `openclaw.json` (no more renaming from .example)
- Fixed heartbeat config key (`every` instead of `interval`)
- AGENTS.md split into core + AGENTS-REFERENCE.md (lighter context per session)
- Heartbeat skip-if-nothing-due (fewer wasted API calls)
- Simplified weekly review (5 steps instead of 11)
- FIRST-PROMPTS.md guided onboarding walkthrough
- Cleaner SOUL.md (no more duplicate file-loading rules)

You don't need to do anything else. Your agent will start using the new features automatically.

---

## If Something Went Wrong

Don't panic. Your agent created a backup before starting. Send this:

---

> **COPY/PASTE PROMPT 4 — Roll back (only if needed):**

```
Something doesn't look right after the upgrade. Please roll back to the pre-upgrade checkpoint.

Run: git log --oneline -5
Find the commit that says "pre-upgrade-v4.3 checkpoint"
Restore everything to that state
Confirm when done
```

---

This will undo the entire upgrade and put everything back exactly how it was. You can then reach out to us at evaonline.xyz for help, or try the upgrade again.

---

## FAQ

**Q: Will I lose my memories?**
No. MEMORY.md, memory/private-notes.md, your daily logs, and everything in the memory/ folder is completely untouched.

**Q: Will my agent's personality change?**
No. SOUL.md personality traits, voice, and emotional handling are preserved. If you customized the Handling Manual, your customizations are kept.

**Q: What if I customized AGENTS.md with my own rules?**
Your custom rules should be preserved during the merge. If you added custom sections, tell your agent to keep them. The upgrade only updates framework sections.

**Q: Can I upgrade again later?**
Yes. Each upgrade follows the same process. Download, paste the prompt, verify.

**Q: What's the most important change in v4.3?**
The heartbeat skip logic and valid JSON config. Your agent now skips empty heartbeats instantly instead of burning API calls, and the config file works out of the box without needing to strip comments.

---

## Making Backups a Habit

You don't just need backups before upgrades. Your agent learns something new about you every day. A backup from 3 months ago is missing 3 months of memories, preferences, and daily logs.

We recommend backing up once a week (or whenever you feel like your agent has learned a lot of new stuff). You can do it anytime by sending this to your agent:

---

> **COPY/PASTE PROMPT 5 — Anytime backup:**

```
Please create a complete backup of my entire agent workspace right now.

1. Detect my OS and use the appropriate Desktop path
2. Create a zip file of the full ~/.openclaw/workspace/ folder
3. Name it: eva-backup-YYYY-MM-DD.zip (use today's actual date)
4. Save it to my Desktop
5. After creating it, tell me the file size and confirm it includes all my files
6. Suggest I copy it to cloud storage for safekeeping
```

---

That's it. One prompt, full snapshot, timestamped on your desktop. Takes 30 seconds.

**Pro tip:** If you want your agent to do this automatically, ask it to set up a weekly cron job that creates the backup every Sunday. That way you never have to think about it.

---

That's it. You're done. Go talk to your upgraded agent.
