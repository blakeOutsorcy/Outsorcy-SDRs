# Daily job-post lists

Blake builds a CSV of companies that posted a job we can place in the last 24 hours (sometimes a 2 to 3 day window after a weekend) and posts it in #phase-2-ai-academy. File names look like job-check-last24h-placeable.csv or job-check-fri-mon-placeable.csv.

## Getting a list into the repo

Either works:
  - A manager saves the CSV here as lists/YYYY-MM-DD.csv and pushes it.
  - Anyone says "split today's list". Claude finds the newest job-check CSV in #phase-2-ai-academy, saves it here under that date and splits it.

## Columns

posted_et, hours_ago, tab, company, domain, employees, hq_country, title, category, job_city, job_country, url, source, job_id, note, same_role_posted_in_n_locations, ai_summary

  - One row per job posting. A company can appear several times (same role in several cities, or several roles).
  - tab is the segment Blake's search came from (PE 6+, PE 5+, Digital health, Using competitors, VC Seed-B, Travis 300+).
  - note flags "large company (N staff)" and "already hiring in a lower-cost country". The second one means quality angle only, never price.

## After the split

Each split adds rows to accounts/claims.md (status claimed) and writes lists/YYYY-MM-DD-split.md with who got what and why. Interns then enroll their claims with "enroll [company]".
