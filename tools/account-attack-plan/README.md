# Account attack plan on the Living Account List

Status as of Oct 30, 2026 (Travis). Design agreed and tested on five rows. Not live: the skill file is not written yet. Moved here from a Claude Cowork session ("Account attack plan workflow", Oct 30) so the work carries on in this repo.

## Why

The per-account attack plan skill (outsorcy-account-attack-plan) re-researches every company each time a rep runs it. Managers have the AI budget; the interns do not. So the research runs once, under a manager's account, when a company lands on the Living Account List (Google Sheet `1xaVHsEaLbnMeZRzF9-ppMimbVvRIsFUWw92iqO8XPb8`, the same sheet job-signals reads). The plan is written into that company's row. The interns' skills only read the row.

## Decisions

  - The attack plan is a block of 21 columns at the right edge of every tab, same headers in the same order everywhere. Spec: `column-spec.md`. The thesis columns in the middle can differ per tab; skills find columns by header name.
  - One row per company. Keyed on Domain. A duplicate domain is planned once and the second row is flagged for treg to merge. Nothing is copied.
  - A new role is filed under the existing company. That is what recycles the company back into a rep's workflow.
  - Complete, not short. The row holds full context: every dated fact, source, exec name and seat, open role, parent, prior vendor. The reader skills do the condensing. "Not found, checked Oct 30, 2026" beats a blank.
  - Each state cell ends with a "For us:" clause. Lead angle is the one cell written as a finished narrative.
  - Angles are high level: why this company, in its state with these open seats, should use staff augmentation now. Persona, brief and email skills coattail off it. If they already outsource, we are another option: no presence needed, we carry the presence and the employment. Never a competitive attack.
  - Positioning: we own the employment, they own the talent. Dedicated hires, not an outsourcing team. Speed up hiring, build teams, a remote office run by one person in the States, rotate out talent that is not working.
  - Targets: department heads over the open roles, plus CFO, COO and founder.
  - "Not a fit" column dropped: the treg filter already decided fit. Scoring left out for now; add later.
  - No Apollo or Clay credits and no Zoho, Gmail or Slack reads at plan time. Read the row's thesis columns first, search only for gaps. Roles come from the pipeline, never re-pulled.
  - Per-person state (who the rep picked, which touch they are on) lives in Zoho via the existing cadence skills, not the sheet.

## How it runs

  - Default trigger: a daily scan of every tab for rows with a Domain and an empty Plan date. Plan them, write each row in one update. A manager can also name a company to plan or re-read it on demand.
  - Refresh groups:
    - Static: What they do, Ownership, parent & funding, Plan date.
    - Monthly: Growth mode, Restructuring, Exec changes, Headcount direction, Press & media. Lead angle is rewritten only if the Growth mode label changes. Travis picked Growth mode, Headcount changes and Exec changes as the must-refresh three.
    - Role-driven: Fillable roles and Hiring pattern, updated whenever the pipeline writes new roles to the row.
  - Trust the row, but flag it when verification contradicts it (in Refresh log and Don't say).

## Rep workflow it feeds

  1. Rep sees their accounts, hotter ones (open roles) first.
  2. Rep drops a company into chat and gets a plain-language (eighth grade) brief: what they do, where they are, who owns them, open roles. A read of the row, no research.
  3. Rep finds people and pastes LinkedIn URLs. Persona verification checks each against Target personas and the open roles.
  4. Pre-call brief (the new, condensed attack plan for reps): the person plus the row. What they own, care about, the persona cut of the angle, one objection, the ask.
  5. Email skill writes from the same row.
  6. Ghost cadence: call, voicemail, call, email, guided in chat.

The sheet is the only company context any of these skills touch.

## Test run, Oct 30

Five rows on the "VC Seed-B, last raise 18-36 mo..." tab (sheetId 1079290677), block in columns V to AP, rows 3, 5, 6, 9 and 11. The 21 headers were added to that tab only. Company data stays in the sheet, not this repo (the repo is public).

  - Cost: 4 to 6 free lookups per company, no credits. About 15 minutes for five, so a daily batch of 20 is realistic.
  - Growth modes: one Contracting, three Lean-and-hiring, one Steady.
  - The read-the-row-first rule caught two pipeline errors: a funding round under-reported from an Apollo band, and a "Hiring offshore: Yes" that came from a req for the company's own product, not their team.
  - CFO and department-head names are often "name not found". Expected: reps find people, persona verification checks them.

## Open, waiting on Travis

  1. Cell length: the test cells are long by design. Right?
  2. Supporting angles format: pipe-separated, one segment per persona. Does that work for the email skill?
  3. Pricing in the row: the test Lead angle quotes a percent saving and a CFO line has a cost comparison. Interns never discuss pricing (CLAUDE.md). Keep cost figures out of the row, or tell the reader skills to strip them?

## Next

  1. Write the skill and finalize `column-spec.md` to match the test rows exactly.
  2. Add the block to the other tabs (identity columns first, thesis, then the block). Travis 300+ and Remote only lack Country or Region.
  3. Then, in order: pre-call brief, email skill, persona verification skill.
