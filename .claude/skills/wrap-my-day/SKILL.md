---
name: wrap-my-day
description: Build an intern's end-of-day scorecard from Zoho, flag red lines, log it and give the Slack post. Use for "wrap my day", "end of day", "my scorecard", "EOD".
---

# Wrap my day

Numbers come from Zoho, not from memory. The intern adds only what Zoho cannot know: one win, one blocker, LinkedIn requests sent, mock calls if any.

## Pull for today (Prishtina day, converted to MT for the query)

  - Completed calls owned by the intern: count (dials), by Call Result, and duration.
  - Connects: results Not interested, Requested more info, Requested call back, Interested, Meeting booked, Do not call.
  - Conversations: completed calls of 120 seconds or more.
  - Voicemails: Left voicemail.
  - Meetings: Leads moved to Pre-Qualified today.
  - Leads created and Leads enrolled today; claims still waiting.
  - Overdue calls at end of day.
  - Emails sent today (Emails module, if readable).

## Check, and name every one that trips

  - Fewer dials than the floor in the playbook.
  - Overdue calls above 20.
  - Completed calls with no Call Result, or results logged with no Lead Status change.
  - Clusters of 1 to 5 second "No answer" results logged in the same minute (looks like closing tasks, not dialing). Ask, do not accuse.
  - Any call to a Lead with a DNC Note or DNC registry flag.
  - Claims from the last two lists still not enrolled.
  - The playbook scorecard red flags (connect rate, conversations, LinkedIn accept rate, bounce rate).

## Write and hand back

  - Fill today's scorecard section in interns/<name>/daily-log.md. Commit and push.
  - Update accounts/claims.md for any status change today.
  - Slack post for #phase-2-ai-academy: dials, connects, conversations, voicemails, meetings, enrolled, overdue, win, blocker, red flags. One line each.
