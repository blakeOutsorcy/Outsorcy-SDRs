# Job signals: from new job posts to hot leads

The goal: interns sit down at 12:00 Prishtina on Monday and Thursday with new companies, each with an open role we can fill and an attack plan already written. Twice a week since Nov 3, 2026 (Travis runs it; Blake has left):

| When | What | Who |
|---|---|---|
| Sun and Wed 21:47 Prishtina (12:47 PT, 15:47 ET) | **Gather.** New postings at Living Account List companies since the last run, matched to target titles, placeability rules applied, HQ and role region added. Commits `lists/YYYY-MM-DD.csv` and `lists/YYYY-MM-DD-review.md`, dated for the next build (the day the interns work it), then Slack DMs Travis. | scheduled task (Travis) |
| Sun and Wed afternoon PT | **Review.** Travis ticks the companies worth working in the review file and marks it reviewed. Optional: a file not marked reviewed by the build is auto-approved. | Travis |
| Mon and Thu 07:47 Prishtina (Sun and Wed 22:47 PT, 01:47 ET) | **Build.** Approved companies: attack plan with outsorcy-account-attack-plan (Plan mode, up to 40 a run, leftovers first next run), then split-list round-robins them within each region. Commits `accounts/claims.md` and `lists/<today>-split.md`, Slack DMs Travis. Then **sheet upkeep**: monthly refresh of planned rows that are due, then plans for unplanned rows, up to 20 in total. | scheduled task (Travis) |
| Mon and Thu 12:00 Prishtina | Interns say "what are my hot leads today" (hot-leads skill). Tue, Wed and Fri they work the cadence and anything still to enroll. | interns |

A review not marked reviewed by the build is auto-approved: every company except suppressed or closed ones, logged as "auto-approved" in `review-log.csv`. A review older than 7 days is dropped. Interns never plan or split.

## Gather: what it keeps

1. Reads the Living Account List (Google Sheet `1xaVHsEaLbnMeZRzF9-ppMimbVvRIsFUWw92iqO8XPb8`, all tabs) through the Google Sheets connector.
2. Pulls every company's LinkedIn job page through treg (`blitzapi.jobs.company`). Companies with no LinkedIn page go through Crustdata by domain. Nothing touches anyone's own LinkedIn account. About $0.20 a run.
3. **EU discovery.** The Account List has few European companies (204 of 1,588, under 30 in DACH), so the gather also searches treg's job index (`blitzapi.jobs.search`) for target-title postings at companies headquartered in high-cost European countries that are not on the list yet:
   - Countries, in salary tiers: CH, LU, NO, DK, IS; then DE, AT, NL, IE, BE; then SE, FI, GB.
   - 11 to 500 staff and a B2B tech or services industry (software, IT, internet, financial services, consulting, marketing, telecoms and similar), checked on the company record (`crustdata.companies.identify`, free). Staffing and outsourcing firms are skipped.
   - Every fit new company is added to the "EU job signals" tab of the Living Account List by the gather (728 seeded from a 14-day backfill on Nov 2). From then on the daily gather checks it like any other account.
   - The review file gets the best 20 new companies per run (top salary tier first, then ease score, then smaller), so a day's review stays around 40 companies with the Account List. The run log counts the rest.
   - German and Dutch title keywords (Buchhalter, Kundenservice, Teamassistenz, Vertriebsinnendienst, Kreditoren, klantenservice and more) are in `target-titles.csv`, so they also match at German companies already on the list.
   - About $0.25 to $1 a run. `--no-eu` skips it; `--eu-days 14` backfills.
4. Window: since the last ok run in `run-log.csv`, so Sunday covers Wednesday to Sunday and Wednesday covers Sunday to Wednesday. Never more than 7 days back.
5. Keeps a posting only if:
   - The title matches an active row in `target-titles.csv`.
   - Any title containing "manager" is at a company with under 50 staff.
   - It is not senior level (Senior, Sr, Director, VP, Head of, Lead, Principal, Staff engineer, Architect, Controller).
   - It is not hard to place remotely (on-site, field, licensed, clinical, warehouse, driver, and similar).
   - Its URL is not already in an earlier `lists/*.csv`.
   - The company's HQ is not in ANZ (skipped for now; the review file names them).
6. Regions:
   - hq_region: the sheet's Region column (US, Europe, ANZ). Europe means Kosovo-like time zones, worked on the EU cadence; Canada counts as US. Blank Region: worked out from Country and HQ, else Unknown (worked as US unless Travis says otherwise).
   - role_region: where the seat is. US, Europe, ANZ, Offshore (a lower-cost country), Other, or blank when the posting gives no location. A US company hiring in Brazil shows up as Offshore: they already hire offshore, quality angle only.
7. Flags in the note column: large company (over 200 staff), outsourcing competitor, already hiring offshore, same role listed on an earlier date, HQ region unknown, new company not on the Account List (with its industry).
8. Ease score 1 to 10: the title's base_score, plus 1 at 200 staff or fewer, plus 1 if the posting mentions remote, minus 1 for a repeat. Competitors always 1.
9. Writes `lists/<build date>.csv` (columns in `lists/README.md`) and `lists/<build date>-review.md`, where the build date is the next Monday or Thursday 08:00 Prishtina (`BUILD_DAYS` in `review.py`). A second gather before that build adds to the same files; if Travis had already marked the file reviewed, it is set back to not reviewed so he sees the new companies. No matches means neither file. Appends one row to `run-log.csv`: window, pages pulled, errors, matches, rows kept, cost, treg balance (warns under $3).

## Review file (Travis)

`lists/<date>-review.md`, one line per company under US, Europe, "Europe, new companies not on the Account List" and Unknown, each posting underneath with its link and flags. Edit it on GitHub (pencil icon):
  - `[ ]` to `[x]` for each company to work. Leave `[ ]` to skip it; a few words after `why:` help.
  - `Reviewed: [ ]` to `Reviewed: [x]`, then commit to main.
  - Skipping the review is fine: a file not marked reviewed by its build is auto-approved, every company except suppressed or closed ones. Ticks on a file not marked reviewed are ignored, so mark it reviewed if you ticked.
  - The owner tag (`new`, `re-post, Diar's (active)`, `suppressed`) comes from claims.md and suppression.md. Zoho owners are checked at the build.
  - New EU companies are already on the "EU job signals" tab (the gather adds them); ticked ones are planned and split like the rest.

`review.py log` copies every decision and reason into `review-log.csv` at the build (reason "auto-approved: not reviewed by the build" when nobody reviewed). That log is what we use to automate the review later.

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

- Rows with `active` set to no are switched off: recruiting, payroll and account executive (Nov 2: no AE). Set one to yes to start pulling it.
- Change the file, commit and push. The next run uses it.
- The under-50 Manager rule (Account Manager and Activation Manager are exempt: not people managers), the senior and remote rules and the ANZ skip are at the top of `signals.py`.

## Gather runbook (what the Sunday and Wednesday 21:47 Prishtina task does)

You are running the automated job-signals gather for Travis Bennett (travis@outsorcy.com), a manager. This satisfies the CLAUDE.md "who am I working with" check. There is no intern in this session. Travis's Slack user id is U0BTEKB679V; every DM below goes there (`slack_send_message` with that id as the channel).

1. `git checkout main && git pull --rebase origin main`.
2. treg auth comes from the Outsorcy environment's network secret for `treg.to` (the agent proxy adds it; the session never sees the key). Nothing to export. If `TREG_TOKEN` happens to be set it is sent too. Never print, write or commit a token.
3. Read the Living Account List with the Google Sheets connector. First `get_spreadsheet` with `fields` `["sheets.properties.title"]` for the tab names, then one call: `get_spreadsheet` on `1xaVHsEaLbnMeZRzF9-ppMimbVvRIsFUWw92iqO8XPb8`, `includeGridData` true, `fields` `["sheets.properties.title", "sheets.data.rowData.values.formattedValue"]`, range `'<tab>'!A1:U2000` for every tab, including "EU job signals" once it exists (A to U covers every tab's Region column). The result is saved to a file; pass that path to the script, never retype rows. Connector unavailable or the call fails: stop, run nothing, DM Travis "Gather failed: Google Sheets connector unavailable."
4. `python3 tools/job-signals/signals.py --accounts <that file> --eu-companies-out /tmp/eu_new_companies.csv`. The last line is a JSON summary. The CSV (never committed: company list) holds every fit new EU company found.
4b. Append the CSV's rows (header excluded) to the "EU job signals" tab: read `'EU job signals'!A:C` for the next empty row and the Domains and LinkedIn URLs already there, drop rows already on the tab, then write the rest with one `update_values` call (columns Account to Added, in the CSV's order). Re-read the range to check. Write nothing else on the sheet.
5. Commit `lists/<date>.csv` and `lists/<date>-review.md` (if written) and `tools/job-signals/run-log.csv` in one commit, then push. Message: `travis: job-signals gather <Mon DD> (<N> companies to review)` or `travis: job-signals gather <Mon DD>, no new postings`.
6. Slack DM Travis, plain text, no emoji:
   - With a list: "Job review ready: <N> companies (<a> US, <b> Europe, <e> new EU, <c> unknown) for the <build_day from the summary> morning build (22:47 PT tonight). Not reviewed by then, all are approved except suppressed or closed. Review: https://github.com/blakeOutsorcy/Outsorcy-SDRs/edit/main/lists/<date>-review.md". Add one line for any earlier review that `python3 tools/job-signals/review.py pending` shows as still waiting.
   - No new postings: "No new job posts since <window start, PT>. Nothing to review."
   - Exit code 3 (treg auth failed): commit the run log, push, and DM "Gather failed: treg rejected the key. Check the treg.to network secret on the Outsorcy cloud environment (host must be exactly treg.to)."
7. Do not run split-list, plan any company, write to Zoho or edit any other file. The only sheet write is step 4b.

## Build runbook (what the Monday and Thursday 07:47 Prishtina task does)

You are running the automated morning build for Travis Bennett (travis@outsorcy.com), a manager. This satisfies the CLAUDE.md "who am I working with" check; there is no intern in this session. Prishtina time throughout. Travis's Slack user id is U0BTEKB679V; every DM below goes there.

1. `git checkout main && git pull --rebase origin main`.
2. `python3 tools/job-signals/review.py pending`. Each item has a status:
   - `ready`: its approved companies are today's work. `auto_approved: true` means Travis did not mark it reviewed, so everything except suppressed or closed companies is approved; say so in the DM.
   - `waiting for Travis's review`: dated for a later build; leave it and mention it in the DM.
   - `expired`: mention it in the DM, nothing else.
   No ready items: skip to step 11 (sheet upkeep), and say in the DM there were no new companies.
3. Decide the split first, without writing: follow `.claude/skills/split-list/SKILL.md` steps 2 to 4 for the approved companies of every ready item together, oldest list first. Zoho is read only here (owner search and the capacity check).
4. New EU companies: every approved company with a `new_company` block in the pending JSON goes on the "EU job signals" tab of the Living Account List before planning.
   - No tab yet: create it (`update_spreadsheet`, addSheet, title "EU job signals") and write the header row: Account, Domain, LinkedIn, HQ, Country, Employees, Industry, Region, Source, Added.
   - Read the Domain and LinkedIn columns of every tab first. A company already on any tab is not added again.
   - Append one row per company to the next empty row with the `new_company` values and Added `'YYYY-MM-DD` (today), in one `update_values` call. Re-read the range to check it landed.
   - Write nothing else on that tab; the plan skill adds its own columns.
5. Plan the companies that are going to an intern (new or re-post), following `.claude/skills/outsorcy-account-attack-plan/SKILL.md` Plan mode as "plan [company]", matched by domain:
   - Plan date empty: full plan (its section 3).
   - Already planned: role-driven update from the new postings (its section 4).
   - Not on the sheet: no plan, mark it "plan pending: not on the Living Account List".
   - First, any company still marked "plan pending" in an earlier `lists/*-split.md` that an intern still holds (claims.md status claimed or active): plan it now and change it to "plan ready" in that split file. Interns have little usage, so every assigned company must end up planned.
   - Then today's companies. At most 40 full plans per run in total (catch-ups included); past that, highest ease first, and mark the rest "plan pending". The next run picks them up first.
   - The general scan (monthly refresh, unplanned rows) is step 11, after the split is pushed.
6. Write the split: split-list step 5. The split file is `lists/<today>-split.md`, first line(s) `From: lists/<date>-review.md`, each company marked "plan ready" or "plan pending".
7. `python3 tools/job-signals/review.py log <date>` for each ready item.
8. Commit `accounts/claims.md`, `lists/<today>-split.md` and `tools/job-signals/review-log.csv` in one commit and push. Message: `travis: morning build <Mon DD> (<N> companies, <M> plans)`. If the push conflicts on claims.md, rebase and keep both sides' rows. This must land before step 11 so the interns' noon start never waits on upkeep.
9. Slack DM Travis: reviewed or auto-approved, companies added to the EU job signals tab, then one line per intern with their companies, plans written and pending, skipped companies with the reason (owner in Zoho, suppression), anything waiting or expired. Plain text, no emoji.
10. Never write to Zoho, enroll anyone, message a prospect or post in a channel. The only sheet writes are new rows on the EU job signals tab (step 4) and the attack-plan columns the plan skill writes.
11. Sheet upkeep, every build, after step 8 is pushed. Follow `.claude/skills/outsorcy-account-attack-plan/SKILL.md` Plan mode sections 1, 2, 3, 5 and 6 for the whole Living Account List, at most 20 companies of research, counting nothing from step 5:
    - First, monthly refresh (its section 5): planned rows whose Next refresh due is today or earlier, oldest due first. Growth mode, Restructuring, Exec changes, Headcount direction and Press & media are the columns that must stay current.
    - Then, with whatever is left of the 20, new rows (its section 3): Domain filled, Plan date empty. Rows on a tab whose companies posted a role in `lists/` go first.
    - Role-driven updates for rows not planned today (its section 4) cost no research; do them all.
    - No repo commit: the sheet is the record. DM Travis one short message: refreshed (company, what changed), newly planned (company, Growth mode), still due, unplanned rows left on the sheet, row errors and duplicates for treg.

## Running it by hand

```
python3 tools/job-signals/signals.py --accounts <sheet export file> --since-hours 24 --dry-run
```

`--dry-run` writes the list and review file to /tmp and skips the run log. `--accounts` also accepts a CSV with columns tab,account,domain,linkedin,hq,country,employees,industry,region.
