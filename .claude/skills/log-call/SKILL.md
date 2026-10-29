---
name: log-call
description: After an intern dials, update Zoho from the call result and line up the next touch. Use for "vm on Gil", "no answer on Anna", "Gil picked up", "logged call 3", "done with Anna, Bob and Carla", "booked a meeting with X", "X said don't call", or any report of a call outcome.
---

# Log a call

The intern sets the Call Result on the cadence call in the Zoho dialer. This skill does everything after that. Every Zoho write needs the intern's approval; batch several calls into one approval.

## 1. Find the call

For each person named: find the Lead (intern-owned) and its newest Completed call today. If the Call Result is empty, ask the intern to set it in the dialer first (the result belongs on the record with the recording). If the intern dialed from the Lead page instead of the cadence step, the cadence call is still open: tell them to set the result there and remember to dial from the cadence step next time.

## 2. Update the Lead

Use the table in claude/zoho-reference.md (Call Result to Lead Status and cadence). In particular:
  - Do not call: Lead Status Not Qualified, un-enroll from every cadence, cancel every open call for the Lead (Outgoing_Call_Status = Cancelled, normal update with cadences skipped), add Note "Asked not to be called on <date>". Set claims.md to closed if it was the last live Lead at the company.
  - Meeting booked: confirm it meets the playbook meeting definition. Lead Status Pre-Qualified, un-enroll, cancel open calls, write the handoff Note in the playbook shape, draft the Slack post tagging Blake and Travis. claims.md status meeting.
  - Interested or Not interested: Lead Status Contacted (Not Qualified for a firm no), un-enroll, cancel open calls.
  - Requested call back: Note with the day and time in Prishtina and the prospect's time zone; keep in cadence.
  - US cadence with several open calls for the same Lead: cancel the older open calls so one remains.

## 3. Next touch

Hand to outsorcy-high-touch-3day for what to send after this call (LinkedIn request, Email 1 or 2, Day 3 LinkedIn message, break-up). Keep the per-lead cadence state under the company in interns/<name>/prospect-notes.md.

## 4. Record

One line per call under the company in prospect-notes.md: date, person, result, what was said, next step. Commit and push.
