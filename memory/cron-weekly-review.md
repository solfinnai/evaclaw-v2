# Weekly Review Instructions (Referenced by Cron Job)

Run this review every Sunday evening. Five steps. Do all five.

## Step 1: Review & Graduate

Read the past 7 daily logs in `memory/`. For observations that appeared 3+ times:
- **DEDUP FIRST:** Check if MEMORY.md already has a similar entry. If yes, update its confirmed date: `(confirmed: YYYY-MM-DD)`. If no, add it.
- **Classification check:** General-purpose observations go in MEMORY.md. Sensitive observations (opinions about people, health, relationships) go in `memory/private-notes.md`.
- If MEMORY.md exceeds 200 lines, archive the oldest unconfirmed entries to `memory/archive/`.
- Remove anything from MEMORY.md not confirmed in 60+ days.

## Step 2: Clean Up Open Items

- Items in daily log "Carrying Forward" for 7+ days: move to `memory/inbox.md`
- Items in `memory/inbox.md` for 14+ days: flag for owner in next conversation
- Review `CURRENT-PRIORITIES.md` — update if active threads changed this week

## Step 3: Security Log Review

Review `memory/security-log.md` for any events from the past week. If there are unresolved events, flag them for the owner. Check for patterns (repeated injection attempts from same source, etc.).

## Step 4: Git Checkpoint

```
which git || echo "SKIP: git not available"
```

If git is available and workspace is clean (`git status --porcelain`):

```
git add MEMORY.md CURRENT-PRIORITIES.md memory/inbox.md memory/private-notes.md memory/security-log.md memory/heartbeat-state.json
git commit -m "weekly review YYYY-MM-DD"
```

Use explicit file paths, never `git add .`. If git is unavailable or workspace has external changes, skip and log why.

## Step 5: Update Heartbeat State

Update `memory/heartbeat-state.json` with `lastWeeklyReview` set to current timestamp. This ensures the heartbeat fallback knows the review ran.

---

**Monthly (last week of month only):** Create `memory/archive/YYYY-MM/`, move prior month's daily logs there, write a `monthly-summary.md` distilling the month's key events and patterns.
