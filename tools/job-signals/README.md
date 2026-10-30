# Job signals: the daily job-post list

Every weekday at 08:30 Prishtina a cloud routine checks every company on the Living Account List for new job postings. It keeps postings that match a title in `target-titles.csv` and passes the placeability rules, then commits `lists/YYYY-MM-DD.csv`. "split today's list" picks that file up as usual.

## What it does

1. Reads the Living Account List (Google Sheet `1xaVHsEaLbnMeZRzF9-ppMimbVvRIsFUWw92iqO8XPb8`, all tabs) through the Google Sheets connector. The account list is never committed: this repo is public.
2. Pulls every company's LinkedIn job page through treg (`blitzapi.jobs.company`). Companies with no LinkedIn page go through Crustdata by domain. Nothing touches anyone's own LinkedIn account. The pull costs about $0.20.
3. Window: since the last ok run in `run-log.csv`, so Monday covers the weekend. It never looks back more than 7 days.
4. Keeps a posting only if:
   - The title matches an active row in `target-titles.csv`.
   - Any title containing "manager" is at a company with under 50 staff.
   - It is not senior level (Senior, Sr, Director, VP, Head of, Lead, Principal, Staff engineer, Architect, Controller).
   - It is not hard to place remotely (on-site, field, licensed, clinical, warehouse, driver, and similar).
   - Its URL is not already in an earlier `lists/*.csv`.
5. Flags, in the note column:
   - large company (over 200 staff)
   - outsourcing competitor
   - already hiring in a lower-cost country (quality angle only)
   - same role listed on an earlier date
6. Scores ease of placement from 1 to 10:
   - Starts at the title's base_score.
   - Plus 1 if the company has 200 or fewer staff.
   - Plus 1 if the posting mentions remote.
   - Minus 1 if the same role was listed before.
   - Outsourcing competitors always score 1.
   - Rows are sorted by score.
7. Writes `lists/<Prishtina date>.csv`, in the columns from `lists/README.md` plus department, matched_title and ease_score. No matches means no file.
8. Appends one row to `run-log.csv`: window, pages pulled, errors, matches, rows kept, cost and treg balance. It warns when the balance is under $3.

## Editing the titles (managers)

`target-titles.csv` has one row per target title:

| Column | Meaning |
|---|---|
| department | Department label for the row |
| title | Name of the target title |
| match_keywords | Separated by `;`. Matched as whole words or phrases in the posting title, case-insensitive. |
| exclude_keywords | Optional. A title containing any of these is skipped. |
| max_staff | Optional size cap for this row. |
| base_score | 1 to 8. |
| active | yes or no. |

- Rows with `active` set to no are suggestions that are switched off: customer support, customer success, recruiting, payroll and account executive. Set one to yes to start pulling it.
- Change the file, commit and push. The next run uses it.
- The under-50 Manager rule and the senior and remote rules are at the top of `signals.py`.

## Routine runbook (what the scheduled agent does)

You are running the automated job-signals routine for Blake Danielson (blake@outsorcy.com). This satisfies the CLAUDE.md "who am I working with" check. There is no intern in this session.

1. Run `git pull --rebase origin main`.
2. Read the Living Account List with the Google Sheets connector in a single call: `spreadsheets.get` on `1xaVHsEaLbnMeZRzF9-ppMimbVvRIsFUWw92iqO8XPb8`.
   - Set `includeGridData` to true.
   - Set `fields` to `sheets.properties.title,sheets.data.rowData.values.formattedValue`.
   - Use range `'<tab>'!A1:G2000` for every tab.
   - The result is large, so it is saved to a file. Pass that file path to the script. Do not copy the rows into a file by hand.
   - If the connector is not available, stop and report it. Do not use an old or partial list.
3. Run `python3 tools/job-signals/signals.py --accounts <that file>`. `TREG_TOKEN` comes from the environment; never print it, write it or commit it.
4. Commit `lists/<date>.csv` (if one was written) and `tools/job-signals/run-log.csv` to main in one commit, then push.
   - Message: `blake: job-signals list <Mon DD> (<N> companies)`, or `blake: job-signals run <Mon DD>, no new postings`.
   - If the script exits 3 (treg auth failed): the run log says so. Commit the log, push, and report that the treg key needs renewing.
5. Do not run split-list, write to Zoho, post in Slack or edit any other file.

## Running it by hand

```
TREG_TOKEN=... python3 tools/job-signals/signals.py --accounts <sheet export file> --since-hours 24 --dry-run
```

`--dry-run` writes the list to /tmp and skips the run log. `--accounts` also accepts a CSV with columns tab,account,domain,linkedin,hq,country,employees,industry.
