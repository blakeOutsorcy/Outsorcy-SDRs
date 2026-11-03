---
name: hot-leads
description: Show an intern the companies the morning build gave them today, each open role, and a short attack-plan brief per company. Use for "what are my hot leads today", "my hot leads", "what did I get today", "new leads", "today's companies", "what's new for me".
---

# What are my hot leads today

Read only. No commits, no research, no credits. Identify the intern first (CLAUDE.md). Use Prishtina time.

The morning build (Monday and Thursday, 08:00 Prishtina) plans each approved company with outsorcy-account-attack-plan and splits them in lists/<today>-split.md. This skill shows the intern their part of it. Interns never plan a company themselves.

## 1. Find today's leads

  - Read lists/<today>-split.md (Prishtina date). Take only the intern's table.
  - Tuesday, Wednesday or Friday: there is no build today. Say new companies come Monday and Thursday, show the intern's table from the latest split if it is from this week, and go to the leftovers below.
  - Monday or Thursday, no file yet: before 10:00, say the morning build is still running and to ask again shortly. After 10:00, say nothing was split today (no new postings, or the build failed; Travis has been told) and go to the leftovers below.
  - Leftovers: grep the intern's section of accounts/claims.md for status claimed with Leads 0 from earlier days. List them under "Still to enroll", one line each, oldest first.

## 2. One block per company

Order: Europe HQ first (dial 12:00 to 15:00), then US (dial 15:00 to 19:00, after 9:00 ET). Within each, the order in the split.

For each company:
  - **Company** (domain), HQ region and cadence (High-Touch EU Calls or High-Touch US Calls), staff count.
  - **Roles:** each title, city and country, how many days ago it was posted, the posting link. A role outside the US and Europe means they already hire offshore: say "quality angle, not cost".
  - **Re-post:** if the split says it came back to them, say so and point to their own notes in prospect-notes.md (grep, then read only that section).
  - **Brief, three lines,** read from the company's row on the Living Account List the way outsorcy-account-attack-plan Read mode does it (read row 1 and the Domain column of each tab, find the row, read that one row; never a whole tab):
    - What they do: one sentence.
    - Why us, now: the Lead angle in plain words, one or two sentences.
    - Watch out: the main line from Don't say or Objection & counter.
  - Plan date empty, or the split says "plan pending": "Plan comes with the next morning build. Start with the roles." Do not research the company yourself.
  - The sheet cannot be read (no Google Sheets connector, or no access): give the roles only and say once, at the end, "Ask Travis for view access to the Living Account List and the Google Sheets connector to see the briefs."

## 3. Hand off

End with the next step, one line: "Say 'research [company]' for the full brief, find 2 to 4 people on LinkedIn, then 'enroll [company]'." If the capacity rules in claude/zoho-reference.md block enrolling today (45 live Leads or more than 20 overdue calls), say so first: today is clean-up, these wait.

Never quote role counts to a prospect, never discuss pricing beyond the percentage in the row, and never copy the brief into a repo file.
