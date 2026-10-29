---
name: start-my-day
description: Build an intern's day from Zoho, their coaching and today's claims. Use for "start my day", "set up my day", "what do I call today", "my call sheet", "what's on my plate".
---

# Start my day

Read only, except for the daily log. Identify the intern first (CLAUDE.md). Use Prishtina time.

## Pull

  1. The newest dated line in interns/<name>/coaching.md. Read it out first.
  2. Zoho open calls for the intern (Overdue and Scheduled), with the Lead for each.
  3. The intern's claims with status claimed (not yet enrolled) from accounts/claims.md, and whether today's list has been split yet (lists/<today>-split.md). If not, offer to run split-list.
  4. Any Lead of theirs with a call-back Note due today.

## Build the call sheet

  - One line per Lead, not per call record. If a Lead has several open calls (US cadence stacks them), dial once and close the older calls: list them as "close N older".
  - Never put a Lead on the sheet if it has a DNC Note, a DNC registry flag, or a Not Qualified, Junk or Lost status. If its calls are still open, list it under "cancel these" instead.
  - Order: call-backs due today, then EU Leads (dial 12:00 to 15:00 Prishtina), then US Leads (dial 15:00 to 19:00 Prishtina, after 9:00 ET), oldest due first within each.
  - Each line: name, title, company, the posting that put them on the list (from the Lead Note), touch number, one-line opener. For the first 5, offer outsorcy-precall-brief.

## Numbers up top

Overdue calls now, live Leads in cadence, claims waiting to be enrolled, and whether the intern can enroll today under the capacity rules in claude/zoho-reference.md. Over the line: today is a clean-up day, say which calls to clear first.

## Write and hand back

  - Add today's entry at the top of interns/<name>/daily-log.md using the template there (plan section only). Commit and push.
  - Give the Slack post for #phase-2-ai-academy: feedback acting on, dials planned, Leads on the sheet, claims to enroll, one thing to improve. Four lines, no emoji.
