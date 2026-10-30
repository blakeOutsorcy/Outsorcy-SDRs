# Attack-plan column spec (draft, Oct 30, 2026)

The 21 headers, in this order, at the right edge of every tab of the Living Account List. Reader skills find columns by these exact header names. Change a header here first, then in the sheet and the skills.

Draft until Travis signs off on the open items in `README.md`.

## Cell rules

  - Complete, not short. Plain text. Every fact carries its date and source inline, e.g. "Mar 2026: cut ~30% of staff during AI pivot (Law360, Mar 20, 2026)".
  - State cells (1 to 8) end with "For us:" and what it means for Outsorcy.
  - A gap is written "Not found (checked <date>)". Never blank, never a guess.
  - Dates in housekeeping cells are written `'YYYY-MM-DD` (leading apostrophe so Sheets keeps text).
  - Multi-part cells use " | " between parts.
  - The whole row is written in one update.

## Columns

| # | Header | Holds | Refresh |
|---|---|---|---|
| 1 | What they do | Product, customers, scale, founding, HQ, headcount, and why their seats fit our catalogue. | Static |
| 2 | Ownership, parent & funding | VC, PE, independent, or a subsidiary of a larger group. Parent or fund, rounds with dates and amounts, runway read. A PE portfolio usually means a cost program; a subsidiary means the decision may sit at the parent. Corrections to the pipeline row go here. | Static |
| 3 | Growth mode | Label first, then "Evidence: ...", a confidence note, then For us. Labels: Scaling, Steady, Contracting, Lean-and-hiring, Transition. | Monthly |
| 4 | Restructuring | Layoffs, closures, reorgs, pivots, cost language, with dates and sources. | Monthly |
| 5 | Exec changes | Who, which seat, arrived or left, date. Name the current decision-makers. | Monthly |
| 6 | Headcount direction | Up, flat or down, with the numbers and the pipeline source. | Monthly |
| 7 | Press & media | Dated items, one line each. | Monthly |
| 8 | Offshore footprint | Offshore staff, nearshore vendors, BPO use, or not found. If they already outsource: we are another option, no presence needed. | Monthly |
| 9 | Fillable roles | Open roles from the pipeline that we can fill, with location and posting date. "Not in pipeline for this tab" where the tab has no roles. | Role-driven |
| 10 | Hiring pattern | What the hiring (or its absence) says. | Role-driven |
| 11 | Lead angle | Finished narrative, two to four sentences: why this company, now, should use staff augmentation. Same story for every rep. | Rewritten only if Growth mode label changes |
| 12 | Supporting angles (by persona) | One segment per seat, " \| " separated: `Seat (Name or "not yet identified"): what they hear`. | With Lead angle |
| 13 | Outsorcy play | One or more of: speed to hire, build a team, remote office run by one US lead, rotate out talent, cost. With a short why. | With Lead angle |
| 14 | Objection & counter | "Objection: ... Counter: ...". A secondary pair is fine. | With Lead angle |
| 15 | Target personas | " \| " separated. `Name, Title (why this seat)`, or `Head of X, name not found (hiring manager for Y)`. Department heads over the open roles plus CFO, COO, founder. | Monthly (exec changes) |
| 16 | Don't say | Landmines: unverified numbers, stale "just raised", known pipeline errors. | Any time |
| 17 | Plan date | `'YYYY-MM-DD`. Empty means not planned; the daily scan picks it up. | Static |
| 18 | Last refresh | `'YYYY-MM-DD` | Each refresh |
| 19 | Next refresh due | `'YYYY-MM-DD`, Last refresh plus one month. | Each refresh |
| 20 | Refresh log | `YYYY-MM-DD: what changed (who)`, newest last. | Each refresh |
| 21 | Sources | URLs and "Pipeline row (source, date)", " \| " separated. | Each refresh |
