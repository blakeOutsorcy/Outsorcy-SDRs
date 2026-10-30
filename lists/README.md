# Daily job-post lists

Every weekday at 08:30 Prishtina the job-signals routine (tools/job-signals/README.md) commits lists/YYYY-MM-DD.csv here: postings since the last run (Monday covers the weekend) at companies on the Living Account List, for titles in tools/job-signals/target-titles.csv, with senior and hard-to-place roles removed. No file that day means no new matching postings; the reason is in tools/job-signals/run-log.csv.

Blake can still post a hand-built CSV in #phase-2-ai-academy (older names look like job-check-last24h-placeable.csv).

## Getting a list into the repo

Either works:
  - A manager saves the CSV here as lists/YYYY-MM-DD.csv and pushes it.
  - Anyone says "split today's list". Claude finds the newest job-check CSV in #phase-2-ai-academy, saves it here under that date and splits it.

## Columns

posted_et, hours_ago, tab, company, domain, employees, hq_country, title, category, job_city, job_country, url, source, job_id, note, same_role_posted_in_n_locations, ai_summary, department, matched_title, ease_score

  - One row per job posting. A company can appear several times (same role in several cities, or several roles).
  - tab is the segment Blake's search came from (PE 6+, PE 5+, Digital health, Using competitors, VC Seed-B, Travis 300+).
  - note flags "large company (N staff)" and "already hiring in a lower-cost country". The second one means quality angle only, never price.
  - department and matched_title say which target title the posting matched. ease_score (1 to 10) ranks how easy the seat is to fill; rows come sorted by it. Routine files only.

## After the split

Each split adds rows to accounts/claims.md (status claimed) and writes lists/YYYY-MM-DD-split.md with who got what and why. Interns then enroll their claims with "enroll [company]".
