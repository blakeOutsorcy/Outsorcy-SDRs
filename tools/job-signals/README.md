# Job signals: from new job posts to hot leads

The goal: interns sit down at 12:00 Prishtina with that day's companies, each with an open role we can fill and an attack plan already written. Three steps a weekday:

| When | What | Who |
|---|---|---|
| 14:00 MT (22:00 Prishtina) | **Gather.** New postings at Living Account List companies, matched to target titles, placeability rules applied, HQ and role region added. Commits `lists/YYYY-MM-DD.csv` and `lists/YYYY-MM-DD-review.md`, dated for the next morning's build (the day the interns work it), then Slack DMs Blake. | cloud routine |
| evening MT | **Review.** Blake ticks the companies worth working in the review file and marks it reviewed. | Blake |
| 08:00 Prishtina (00:00 MT) | **Build.** Approved companies only: attack plan with outsorcy-account-attack-plan (Plan mode), then split-list round-robins them within each region. Commits `accounts/claims.md` and `lists/<today>-split.md`, then Slack DMs Blake. | cloud routine |
| 12:00 Prishtina | Interns say "what are my hot leads today" (hot-leads skill). | interns |

A review not done by 08:00 Prishtina waits for the next morning's build. A review older than 7 days is dropped. Interns never plan or split.

## Gather: what it keeps

1. Reads the Living Account List (Google Sheet `1xaVHsEaLbnMeZRzF9-ppMimbVvRIsFUWw92iqO8XPb8`, all tabs) through the Google Sheets connector.
2. Pulls every company's LinkedIn job page through treg (`blitzapi.jobs.company`). Companies with no LinkedIn page go through Crustdata by domain. Nothing touches anyone's own LinkedIn account. About $0.20 a run.
3. Window: since the last ok run in `run-log.csv`, so Monday covers the weekend. Never more than 7 days back.
4. Keeps a posting only if:
   - The title matches an active row in `target-titles.csv`.
   - Any title containing "manager" is at a company with under 50 staff.
   - It is not senior level (Senior, Sr, Director, VP, Head of, Lead, Principal, Staff engineer, Architect, Controller).
   - It is not hard to place remotely (on-site, field, licensed, clinical, warehouse, driver, and similar).
   - Its URL is not already in an earlier `lists/*.csv`.
   - The company's HQ is not in ANZ (skipped for now; the review file names them).
5. Regions:
   - hq_region: the sheet's Region column (US, Europe, ANZ). Europe means Kosovo-like time zones, worked on the EU cadence; Canada counts as US. Blank Region: worked out from Country and HQ, else Unknown (worked as US unless Blake says otherwise).
   - role_region: where the seat is. US, Europe, ANZ, Offshore (a lower-cost country), Other, or blank when the posting gives no location. A US company hiring in Brazil shows up as Offshore: they already hire offshore, quality angle only.
6. Flags in the note column: large company (over 200 staff), outsourcing competitor, already hiring offshore, same role listed on an earlier date, HQ region unknown.
7. Ease score 1 to 10: the title's base_score, plus 1 at 200 staff or fewer, plus 1 if the posting mentions remote, minus 1 for a repeat. Competitors always 1.
8. Writes `lists/<build date>.csv` (columns in `lists/README.md`) and `lists/<build date>-review.md`, where the build date is the next weekday 08:00 Prishtina. A second gather before that build adds to the same files; if Blake had already marked the file reviewed, it is set back to not reviewed so he sees the new companies. No matches means neither file. Appends one row to `run-log.csv`: window, pages pulled, errors, matches, rows kept, cost, treg balance (warns under $3).

## Review file (Blake)

`lists/<date>-review.md`, one line per company under US, Europe and Unknown, each posting underneath with its link and flags. Edit it on GitHub (pencil icon):
  - `[ ]` to `[x]` for each company to work. Leave `[ ]` to skip it; a few words after `why:` help.
  - `Reviewed: [ ]` to `Reviewed: [x]`, then commit to main.
  - The owner tag (`new`, `re-post, Diar's (active)`, `suppressed`) comes from claims.md and suppression.md. Zoho owners are checked at the build.

`review.py log` copies every decision and reason into `review-log.csv` at the build. That log is what we use to automate the review later.

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

- Rows with `active` set to no are switched off: customer support, customer success, recruiting, payroll and account executive. Set one to yes to start pulling it.
- Change the file, commit and push. The next run uses it.
- The under-50 Manager rule, the senior and remote rules and the ANZ skip are at the top of `signals.py`.

## Gather runbook (what the 14:00 MT routine does)

You are running the automated job-signals gather for Blake Danielson (blake@outsorcy.com). This satisfies the CLAUDE.md "who am I working with" check. There is no intern in this session.

1. `git checkout main && git pull --rebase origin main`.
2. `TREG_TOKEN` must be in the environment. If it is not set, find another environment variable whose name contains TREG (`env | cut -d= -f1 | grep -i treg`, names only) and export its value as TREG_TOKEN. Never print, write or commit the token.
3. Read the Living Account List with the Google Sheets connector in one call: `get_spreadsheet` on `1xaVHsEaLbnMeZRzF9-ppMimbVvRIsFUWw92iqO8XPb8`, `includeGridData` true, `fields` `["sheets.properties.title", "sheets.data.rowData.values.formattedValue"]`, range `'<tab>'!A1:U2000` for every tab (A to U covers every tab's Region column). If a tab name changed, first get the tab names with `fields` `["sheets.properties.title"]`. The result is saved to a file; pass that path to the script, never retype rows. Connector unavailable or the call fails: stop, run nothing, DM Blake "Gather failed: Google Sheets connector unavailable."
4. `python3 tools/job-signals/signals.py --accounts <that file>`. The last line is a JSON summary.
5. Commit `lists/<date>.csv` and `lists/<date>-review.md` (if written) and `tools/job-signals/run-log.csv` in one commit, then push. Message: `blake: job-signals gather <Mon DD> (<N> companies to review)` or `blake: job-signals gather <Mon DD>, no new postings`.
6. Slack DM Blake (user U0A0N4BR7SP, `slack_send_message` with that id as the channel), plain text, no emoji:
   - With a list: "Job review ready: <N> companies (<a> US, <b> Europe, <c> unknown) for the <build_day from the summary> 08:00 Prishtina build (midnight MT). Review: https://github.com/blakeOutsorcy/Outsorcy-SDRs/edit/main/lists/<date>-review.md". Add one line for any earlier review that `python3 tools/job-signals/review.py pending` shows as still waiting.
   - No new postings: "No new job posts since <window start, MT>. Nothing to review."
   - Exit code 3 (treg auth failed): commit the run log, push, and DM "Gather failed: the treg key needs renewing in the Outsorcy cloud environment."
7. Do not run split-list, plan any company, write to Zoho or edit any other file.

## Build runbook (what the 08:00 Prishtina routine does)

You are running the automated morning build for Blake Danielson (blake@outsorcy.com), a manager. This satisfies the CLAUDE.md "who am I working with" check; there is no intern in this session. Prishtina time throughout.

1. `git checkout main && git pull --rebase origin main`.
2. `python3 tools/job-signals/review.py pending`. Each item has a status:
   - `ready`: Blake reviewed it. Its approved companies are today's work.
   - `waiting for Blake's review`: leave it for tomorrow; mention it in the DM.
   - `expired`: mention it in the DM, nothing else.
   No ready items: DM Blake only if something is waiting or expired ("Morning build: nothing reviewed, so no new leads today. Waiting: lists/<date>-review.md"), then stop. No commit.
3. Decide the split first, without writing: follow `.claude/skills/split-list/SKILL.md` steps 2 to 4 for the approved companies of every ready item together, oldest list first. Zoho is read only here (owner search and the capacity check).
4. Plan the companies that are going to an intern (new or re-post), following `.claude/skills/outsorcy-account-attack-plan/SKILL.md` Plan mode as "plan [company]", matched by domain:
   - Plan date empty: full plan (its section 3).
   - Already planned: role-driven update from the new postings (its section 4).
   - Not on the sheet: no plan, mark it "plan pending: not on the Living Account List".
   - At most 20 full plans; past that, highest ease first, and mark the rest "plan pending". They are planned on a later run.
   - Do not run the skill's general daily scan (new rows, monthly refresh) here. That stays with Travis until he folds it into this run.
5. Write the split: split-list step 5. The split file is `lists/<today>-split.md`, first line(s) `From: lists/<date>-review.md`, each company marked "plan ready" or "plan pending".
6. `python3 tools/job-signals/review.py log <date>` for each ready item.
7. Commit `accounts/claims.md`, `lists/<today>-split.md` and `tools/job-signals/review-log.csv` in one commit and push. Message: `blake: morning build <Mon DD> (<N> companies, <M> plans)`. If the push conflicts on claims.md, rebase and keep both sides' rows.
8. Slack DM Blake (user U0A0N4BR7SP): one line per intern with their companies, plans written and pending, skipped companies with the reason (owner in Zoho, suppression), anything waiting or expired. Plain text, no emoji.
9. Never write to Zoho, enroll anyone, message a prospect or post in a channel. The only sheet writes are the attack-plan columns the plan skill writes.

## Running it by hand

```
TREG_TOKEN=... python3 tools/job-signals/signals.py --accounts <sheet export file> --since-hours 24 --dry-run
```

`--dry-run` writes the list and review file to /tmp and skips the run log. `--accounts` also accepts a CSV with columns tab,account,domain,linkedin,hq,country,employees,industry,region.
