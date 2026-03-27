# Your First Session with Eva-01 — Complete Prompt Guide

> You've installed OpenClaw and loaded your Eva-01 files. This guide walks you through your first session step by step — every prompt to type, what to expect back, and how to build the foundation for a Chief of Staff that gets smarter every day.

---

## Before You Start

Make sure the following are true:

- OpenClaw is installed and your API key is set (see `INSTALL-GUIDE.md` if not)
- Your Eva-01 files are in your workspace
- Your `openclaw.json` is in the workspace root (not `openclaw.json.example`)
- Your `USER.md` has your personalized information from the questionnaire

If all of that is in place, open Terminal, navigate to your workspace, and launch OpenClaw:

```
cd ~/eva-workspace
openclaw
```

Eva-01 will boot. She'll read her identity files, your profile, your handling manual, and your priorities. Then she'll greet you. This guide picks up from that moment.

---

## Phase 1: The Introduction (Minutes 1-5)

Eva just greeted you. She knows your name and your priorities from the questionnaire, but she doesn't truly *know* you yet. This phase establishes the relationship.

### Prompt 1.1 — Confirm Her Understanding

Type:

```
Before we start working together, I want to make sure you've got me right. Give me a quick summary of who I am, what I care about, and how I like things done.
```

**What to expect:** Eva will give you a concise summary drawn from your `USER.md` and `SOUL.md`. She should hit your name, company, stage, top priorities, communication preferences, and cognitive style.

**What to do:** Read it carefully. If anything is wrong or missing, correct her right now. For example:

```
Close, but a few corrections: I actually prefer bullet points over paragraphs in my briefings. And my co-founder's name is Marcus, not Mark. Also, my biggest priority right now isn't fundraising — it's shipping the beta by April 1st.
```

Eva will update her understanding. These corrections get stored in her memory and shape every future interaction.

### Prompt 1.2 — Set the Tone

Type:

```
Let me tell you how I want our working relationship to feel. I want you to be direct, even blunt. Don't sugarcoat things. If I'm wasting time on something, tell me. If I'm avoiding something important, call it out. I'd rather have an honest Chief of Staff than a polite one. Push back on me when you think I'm wrong.
```

Adjust this to match your actual preference — maybe you prefer warmth over bluntness, or you want Eva to be more deferential. The point is to explicitly set the dynamic on day one.

**What to expect:** Eva will acknowledge and reflect back the tone you've described. She'll calibrate immediately.

### Prompt 1.3 — Establish What Today Looks Like

Type:

```
Here's what my day looks like today: [describe your actual day — meetings, deadlines, tasks, anything relevant]. What should I focus on first?
```

For example:

```
Here's what my day looks like today: I have a 10am call with our lead investor to discuss bridge financing, a 1pm product review with the engineering team, and I need to send a follow-up email to a potential hire by end of day. I also haven't updated our board on last month's metrics. What should I focus on first?
```

**What to expect:** Eva will triage your day. She'll rank items by urgency and impact, flag what needs prep, and suggest a sequence. This is the first real taste of having a Chief of Staff. She's not just listing — she's deciding.

---

## Phase 2: Teaching Eva Your World (Minutes 5-15)

Eva knows the facts from your questionnaire. Now you teach her the texture — the stuff that lives in your head and nowhere else.

### Prompt 2.1 — Key People

Type:

```
Let me tell you about the key people in my world right now. I'm going to list them with a sentence or two about each. Store this — you'll need it constantly.

[List your key people. For example:]

- Marcus Chen — my co-founder and CTO. Brilliant engineer, hates meetings, needs context before decisions. We're aligned on vision but sometimes clash on timeline.
- Sarah Kim — our lead investor at Foundry VC. Direct, data-driven, wants to see revenue traction before Series A.
- David Reyes — head of product. New hire, three months in. Great instincts but still learning our users.
- Rachel — my wife. Teacher. Incredibly supportive but I've been absent lately.
```

**What to expect:** Eva will confirm she's stored each person and may ask clarifying questions. Answer these. They matter.

### Prompt 2.2 — Active Projects

Type:

```
Here are the major things I'm working on right now. These are my active threads:

[List your active projects. For example:]

1. Beta launch — shipping v1 to our first 50 users by April 1st. Engineering is on track but we're behind on onboarding docs.
2. Bridge round — raising $500K to extend runway to September.
3. Head of Sales hire — interviewing two final candidates this week.
4. Board deck — Q1 board meeting is April 15th. Haven't started yet.
```

**What to expect:** Eva will organize these and start connecting them to your priorities. She may flag dependencies or risks. This is her starting to think ahead for you.

### Prompt 2.3 — Your Communication Style

Type:

```
I want to show you how I actually write so you can match my voice. Here's a real email I sent recently:

[Paste an actual email you've sent — a follow-up, an investor update, a team message.]

This is my voice. When you draft emails for me, they should sound like this. Study it.
```

**What to expect:** Eva will analyze your writing style and confirm the patterns she's picking up. She'll use this as her benchmark for all future communications.

---

## Phase 3: Your First Real Tasks (Minutes 15-30)

Now you put Eva to work.

### Prompt 3.1 — Daily Briefing

```
Give me my daily briefing.
```

### Prompt 3.2 — Meeting Prep

```
Prep me for my [next meeting]. What should I know going in, what should I push on, and what's the ideal outcome?
```

### Prompt 3.3 — Draft an Email

```
Draft a follow-up email to [person] about [topic]. Keep it in my voice.
```

### Prompt 3.4 — Quick Decision Support

```
I'm trying to decide between [option A] and [option B]. Here's the context: [brief description]. What's your read?
```

---

## Phase 4: Setting Up Memory (Minutes 30-40)

Eva's memory is what makes her get better over time. This phase initializes it properly.

### Prompt 4.1 — Create Today's Daily Note

```
Create a daily note for today. Include everything we've discussed — the people I told you about, the projects, and any decisions or next steps from our conversation.
```

**What to expect:** Eva will create a file in `memory/` named with today's date. This is the raw material her memory system builds on.

### Prompt 4.2 — Initialize Tacit Knowledge

```
Based on everything we've talked about today, what have you learned about how I operate? Write it down in MEMORY.md. Be specific — communication patterns, decision patterns, energy patterns, anything you've noticed.
```

**What to expect:** Eva will write observations to `MEMORY.md`. Things like: "Owner prefers blunt feedback over diplomatic framing." "Owner's energy is highest in the morning." These observations compound over time.

---

## Phase 5: End-of-Session Protocol (Minutes 40-50)

### Prompt 5.1 — Capture Open Loops

```
Before we wrap, what are the open loops from today? Anything I committed to, anything that needs follow-up, anything you want to remind me about next time.
```

### Prompt 5.2 — Rate Your First Session

```
How would you rate our first session? What did you learn about me that you didn't know from my profile? What are you still missing?
```

**What to expect:** Eva will give you an honest self-assessment. She'll highlight gaps — maybe she needs more writing samples, or she's unsure about your decision style. This tells you what to feed her next time.

---

## The Next Five Sessions — Building Depth

### Session 2: Communication Mastery
Give Eva 3-5 more real emails you've sent — different types. Also tell her about your communication pet peeves.

### Session 3: Decision Framework
Walk Eva through a recent decision you made — how you thought about it, what inputs you needed, why you went the direction you did.

### Session 4: Stress Test
Give Eva a chaotic scenario and see how she triages it under pressure.

### Session 5: Workflow Run
Run a full Friday closeout: what shipped, what slipped, what carries over.

### Session 6: Emotional Intelligence Test
Tell Eva you're overwhelmed and see if she responds according to your handling preferences — not with a productivity lecture.

---

## Quick Reference — Prompts You'll Use Every Day

| When | Prompt |
|------|--------|
| Start of day | "Give me my daily briefing." |
| Before a meeting | "Prep me for my [meeting] with [person]." |
| After a meeting | "Let me debrief on the meeting I just had with [person]." |
| Need to write | "Draft an email to [person] about [topic]." |
| Inbox overwhelm | "Triage my inbox: [paste messages]" |
| Decision needed | "Help me decide between [A] and [B]." |
| Monday morning | "Let's do the Monday kickoff." |
| Friday afternoon | "Let's close out the week." |
| Feeling stuck | "I'm stuck on [thing]. Help me break it down." |
| End of session | "What are my open loops?" |
| Weekly update | "Update my priorities for this week." |

---

## What Happens Over Time

By week one, Eva knows your name, your priorities, and your schedule.

By week two, she knows your writing voice, your key relationships, and your decision patterns.

By month one, she anticipates what you need before you ask. She flags risks you haven't noticed. She remembers commitments you've forgotten.

By month three, Eva-01 knows you better than any human assistant could in a year. She's not just helpful — she's indispensable.

---

*This guide is included with your Eva-01 purchase. For additional help, visit https://evaclaw.vercel.app/#support or book a Zoom setup session.*
