# Daily job-post lists

Every weekday at 22:00 Prishtina (14:00 MT) the gather routine (tools/job-signals/README.md) commits lists/YYYY-MM-DD.csv here, dated for the next morning's build (the day the interns work it): postings since the last run (Monday covers the weekend) at companies on the Living Account List, for titles in tools/job-signals/target-titles.csv, with senior and hard-to-place roles removed. No file that day means no new matching postings; the reason is in tools/job-signals/run-log.csv.

Next to it, lists/YYYY-MM-DD-review.md is Travis's review: he ticks the companies to work. The Monday and Thursday 08:00 Prishtina morning build plans and splits those (everything except suppressed or closed companies if the file was not marked reviewed), and writes lists/<build date>-split.md.

A manager can still post a hand-built CSV in #phase-2-ai-academy (older names look like job-check-last24h-placeable.csv).

## Getting a list into the repo

Either works:
  - A manager saves the CSV here as lists/YYYY-MM-DD.csv and pushes it.
  - A manager says "split today's list". Claude finds the newest job-check CSV in #phase-2-ai-academy, saves it here under that date and splits it.

## Columns

posted_et, hours_ago, tab, company, domain, employees, hq_country, title, category, job_city, job_country, url, source, job_id, note, same_role_posted_in_n_locations, ai_summary, department, matched_title, ease_score, hq_region, role_region, company_linkedin, industry

  - One row per job posting. A company can appear several times (same role in several cities, or several roles).
  - tab is the segment the company's search came from (PE 6+, PE 5+, Digital health, Using competitors, VC Seed-B, Travis 300+).
  - note flags "large company (N staff)" and "already hiring in a lower-cost country". The second one means quality angle only, never price.
  - department and matched_title say which target title the posting matched. ease_score (1 to 10) ranks how easy the seat is to fill; rows come sorted by it. Routine files only.
  - hq_region (US, Europe, Unknown) decides the cadence and the split bucket. role_region (US, Europe, ANZ, Offshore, Other, blank) is where the seat is; Offshore means they already hire offshore, quality angle only. Routine files from Nov 2, 2026.
  - tab "EU discovery" marks a company found by the EU discovery search, not on the Account List yet; company_linkedin and industry come from its company record. Routine files from Nov 3, 2026.

## After the split

Each split adds rows to accounts/claims.md (status claimed) and writes lists/YYYY-MM-DD-split.md with who got what and why; its first line names the review file or CSV it came from. Interns see their part with "what are my hot leads today", then enroll with "enroll [company]".
