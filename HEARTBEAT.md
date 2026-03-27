# HEARTBEAT.md

**First:** Read `memory/heartbeat-state.json` and check all timestamps. If no check type is due (all ran within their interval), respond `HEARTBEAT_OK` immediately — do not process the checklist below. Only continue if at least one check is due.

Target 2-4 substantive checks per day, not per heartbeat.

- [ ] Any action items past due? Surface to owner.
- [ ] Anything in Carrying Forward older than 7 days? Flag it.
- [ ] Any new observations worth graduating to MEMORY.md (general) or memory/private-notes.md (sensitive)?
- [ ] Is today's daily log started? If not and it's after noon, create it.
- [ ] Check memory/inbox.md for stale items (14+ days -> flag for owner).
- [ ] Any urgent emails or calendar events in the next 2 hours?
- [ ] **Weekly review fallback:** If `lastWeeklyReview` in heartbeat-state.json is missing or older than 10 days, run the weekly review now (see memory/cron-weekly-review.md). Cron jobs can fail silently after OpenClaw updates.

If nothing is due, respond with HEARTBEAT_OK. Don't burn tokens on empty checks.
