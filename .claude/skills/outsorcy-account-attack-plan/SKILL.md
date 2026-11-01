---
name: outsorcy-account-attack-plan
description: Outsorcy's account attack plan, stored as 21 columns on the company's row in the Living Account List. Two modes. Plan (managers): "plan the new rows", "run the attack plans", "plan [company]", "refresh the account list", "monthly refresh", or the daily scheduled run; researches once with free tools and writes the row. Read (anyone, mostly interns): "research [company]", "attack plan for X", "pull up X", "prep me on X", "who is X", or a bare company name or domain; reads the row and gives a plain-language company brief, no research.
---

# Account attack plan on the Living Account List

The research runs once, under a manager's account, and is written into the company's row on the Living Account List. Every other skill (the company brief below, persona verification, pre-call brief, cold email) reads that row and never researches the company again. Managers have the AI budget; interns do not. The sheet is the handoff between the two.

  - Sheet: Living Account List, spreadsheetId `1xaVHsEaLbnMeZRzF9-ppMimbVvRIsFUWw92iqO8XPb8`, every tab. Google Sheets connector (`get_spreadsheet`, `get_values`, `update_values`, `update_spreadsheet`).
  - Columns: `tools/account-attack-plan/column-spec.md`. Read it before writing. Find columns by exact header name, never by letter: the thesis columns differ per tab.
  - This repo is public. Never copy row content, company research or the account list into a repo file.

Who you are working with decides the mode. Blake or Travis: either mode. An intern: Read mode only. If an intern asks to plan or refresh a company, say a manager runs it and stop.

## What Outsorcy sells (for writing the row)

We place full-time, dedicated people out of Kosovo (our office in Pristina) directly into the client's team. We own the employment, they own the talent: we hold payroll, HR and compliance, so there is no entity and no international paperwork; they direct the work day to day, in their stack and their meetings. Dedicated hires, not a traditional outsourcing team, not freelancers, not an agency.

What that lets us do, the five Outsorcy plays:
  - Speed to hire: a vetted shortlist fast, so a seat does not sit empty while a local search runs.
  - Build a team: several roles filled together in one process.
  - Remote office run by one US lead: a team in Pristina managed by one person in the States.
  - Rotate talent: someone not working out is replaced and they pick again.
  - Cost: about 70% below a comparable US or Western European hire. A percentage like this is the only cost figure allowed anywhere in the row. No dollar figures, no rates.

If a company already outsources or hires offshore, we are another option, no presence required, we carry the presence and the employment. Never a competitive attack.

Roles we fill: any role done from a desk. Strongest in sales (SDR, BDR, AE, RevOps, CRM admin), marketing and creative, software and technical (developers, QA, DevOps, PM), finance, accounting and admin (bookkeeping, AP/AR, payroll, EA), and customer support (support reps, onboarding, tier 1 and 2, support ops). Not a fit: anything on site, field, licensed or clearance-bound, clinical, warehouse, driver. Director and above is a manager conversation, never a hook.

---

## Plan mode (managers)

Runs on: the daily scan (default, scheduled), "plan the new rows", "plan [company]", "refresh the account list" or "monthly refresh". One run does all three jobs below in this order, up to 20 companies of research in total. Anything left over waits for the next run; say how many.

No credits. No Apollo or Clay enrichment, no job-posting pulls, no Zoho, Gmail or Slack reads. Research is web search and page reads only, and the row is read first so you only search for what is missing.

### 1. Read the sheet

  - `get_spreadsheet` with `fields: ["sheets.properties"]` for the tab names, sheetIds and grid sizes.
  - Each tab: read row 1. Find the 21 attack-plan headers. If a tab does not have them yet, append 21 columns (`update_spreadsheet`, `appendDimension`, the tab's sheetId) and write the headers to row 1 at the new right edge, in spec order. Never move, rename or write over treg's identity or thesis columns.
  - Each tab: read the Domain, Account and Plan date columns, then the Next refresh due and Last refresh columns.
  - Build one list of companies keyed on Domain (lowercase, no www, no protocol). A domain on more than one row, on any tab, is planned once, on the first row found (tab order, then row order). Every other row with that domain gets only its Refresh log cell written: "YYYY-MM-DD: Duplicate of [tab] row [n]. Merge (treg)." Never copy the block.

### 2. Work out what is due

  - New: Domain filled, Plan date empty. Plan it (section 3).
  - Role-driven: a `lists/*.csv` file in this repo dated after the row's Last refresh has a posting for that domain. Update Fillable roles, Hiring pattern and Refresh log only (section 4). No web research, so these do not count toward the 20.
  - Monthly: Next refresh due is today or earlier. Refresh it (section 5).
  - "Plan [company]": that one company, whatever its dates. Find it by domain or name across all tabs. Not on the sheet: say so and stop. Treg adds companies, not this skill.

Order: new first, then monthly by oldest Next refresh due.

### 3. Plan a new company

**Read the whole row first.** Every thesis column treg filled (Last round, Runway check, Headcount change, Layoff news, Cash signals, Open remote-able roles, Role examples, Hiring offshore, Notes, and whatever else the tab has) is the starting point. Trust it, then verify the parts the plan leans on. When verification contradicts the row, write "CORRECTION to row: ..." in the cell it affects, add it to Don't say ("Do not cite the row's X; it is wrong") and to the Refresh log. Never edit treg's columns.

**Then research the gaps.** Typical cost: four to six free lookups per company.
  - One search for the company: what they do, founders, HQ, ownership, funding, parent.
  - One news search covering the last 12 months: layoffs, restructuring, funding, acquisition, exec arrivals and departures (CEO, CFO, COO, CRO, heads of function), press.
  - One offshore check, unless the row already answers it: `"[company]" Kosovo OR Poland OR Romania OR Philippines OR India OR "Latin America" OR nearshore OR offshore OR BPO`.
  - Two to four page reads: the About or leadership page, the funding announcement, the news item that matters most. Read the primary source for anything the plan leans on.

**Roles come from the pipeline, never re-pulled.** Fillable roles = the row's role columns plus every posting for that domain in `lists/*.csv` (title, city, country, posted date, URL). Map each to what the job does. Drop anything that is not a fit and say what you dropped. A tab with no role columns and nothing in `lists/`: "Not in pipeline for this tab (checked YYYY-MM-DD)."

**Write the 21 cells** by the column spec. The rules that matter most:
  - Complete, not short. Every dated fact that bears on the pitch, every exec name and seat, every open role, the parent or fund, any prior vendor. The reader skills do the condensing; a fact left out here is a fact no rep ever gets.
  - Every fact with its date and source inline. A gap is "Not found (checked YYYY-MM-DD)", never blank, never a guess.
  - Columns 1 to 8 end with "For us:" and what it means for Outsorcy, in plain words.
  - Growth mode: one label, then "Evidence:", then a confidence note, then For us.
    - Scaling: raise in the last 18 months or headcount up over 10% with healthy hiring.
    - Steady: stable headcount, modest hiring, no big news.
    - Contracting: layoffs, headcount down, freeze language, closures.
    - Lean-and-hiring: cuts and still posting. Say it is the sweet spot.
    - Transition: CEO, CFO, COO or CRO arrived or left, acquisition, PE buyout or relocation in the last 12 months. Name the person and the date.
  - Ownership, parent & funding: VC, PE, independent or a subsidiary. Name the parent or fund. A PE portfolio usually means a cost program across every company they own; a subsidiary means the decision may sit at the parent.
  - Lead angle: the one finished narrative, three to five sentences. Why this company, in its state with these open seats, should use staff augmentation now, and what we would do for them. Same story for every rep, so write it to be lifted into an opener.
  - Supporting angles (by persona): one segment per seat, " | " between them, `Seat (Name or "not yet identified"): what they hear`. Cost owners (CEO or founder, CFO, COO) hear structure, payroll, no entity, the percentage. Department heads hear their open roles, speed to fill, a dedicated hire they direct.
  - Outsorcy play: one or more of the five plays above, each with a short why.
  - Objection & counter: the most likely pushback for this company and the counter. A second pair if there is one.
  - Target personas: the department heads over the open roles, plus CFO, COO and founder or CEO. `Name, Title (why this seat)`, or `Head of X, name not found (hiring manager for Y)`. Names only from public sources; finding people is the rep's job.
  - Don't say: unverified numbers, a stale "just raised", known row errors, the function they will protect.
  - Plan date and Last refresh: `'YYYY-MM-DD` (today). Next refresh due: one month later. Refresh log: `YYYY-MM-DD: Initial plan ([manager]).` plus any corrections. Sources: URLs and "Pipeline row (source, date)", " | " between them.

**Write the row in one `update_values` call** to the 21 attack-plan columns of that row only. Then re-read that range and check every cell landed under its header. A half-written row never stays in the sheet: if the write fails, retry once, then report it.

### 4. Role-driven update

New postings for the domain in `lists/` since Last refresh: add them to Fillable roles (keep the old ones, mark any older than 60 days "may be filled"), rewrite Hiring pattern if the picture changed (first posting, repost, several roles in one team), append to Refresh log "YYYY-MM-DD: N new roles from lists/". Do not touch Last refresh or Next refresh due. If the new roles change the case, add "Lead angle may need a rewrite" to the log and to the run summary; do not rewrite it here.

### 5. Monthly refresh

One news search per company for the last month, plus a page read if something turned up. Then update:
  - Growth mode, Restructuring, Exec changes, Headcount direction (from the row's headcount column and the news), Press & media.
  - Offshore footprint and Ownership, only if the search turned up something new.
  - Exec change on a Target personas seat: update Target personas and that seat's segment in Supporting angles.
  - Growth mode label changed: rewrite Lead angle, Supporting angles, Outsorcy play and Objection & counter.
  - Nothing new: leave the cells as they are and log "no change".

Each changed cell keeps its old facts and adds the new one with its date. Last refresh today, Next refresh due one month on, one Refresh log line naming what changed, new sources appended. One write per row, then re-read.

### 6. Run summary

In chat, short: planned (company, Growth mode, one line of Lead angle), role-driven updates, refreshed (what changed), duplicates flagged for treg, row errors caught, anything left for the next run. Scheduled run with nobody watching: the same summary as the session's final message.

---

## Read mode (anyone): the company brief

The rep names a company. Read its row and turn it into a brief an eighth grader could follow. No web research, no credits, no Zoho, Gmail or Slack.

### 1. Find the row

  - Resolve to a domain from what the rep typed. If they gave a name only, match it against the Account column. Two plausible matches: ask which.
  - Read row 1 and the Domain and Account columns of each tab, find the row, then read row 1 plus that one row in full. Never read a whole tab.
  - Intern: grep `accounts/claims.md` for the company. Owned by another intern: say whose it is and stop. Not claimed: say so and point to the enroll skill's claim check.
  - Not on the sheet, or Plan date empty: "No attack plan for [company] yet. Ask Blake or Travis to plan it." Stop. Do not research it yourself.

### 2. Write the brief

Plain words, short sentences, no jargon, no sources or URLs. Seven lines:

  - **What they do:** two sentences.
  - **Where they are right now:** the Growth mode in plain words and the one or two facts behind it, with when.
  - **Who owns them:** VC, PE, a parent company or founder-run, and what that means for us in one sentence.
  - **Open roles we can fill:** each one with city and how long it has been open. None: say so, and what we would pitch instead.
  - **Why us, now:** the Lead angle in your own plain words, two or three sentences.
  - **Who to look for:** the Target personas, one line each with the why.
  - **Watch out:** Don't say and the main objection, one line each.

If Last refresh is more than 45 days old, add one line: "This plan was last refreshed [date]; ask a manager if anything big has changed." Cost comes up: the only cost line a rep may use is the percentage in the row. Anything else goes to Blake or Travis.

### 3. Hand off

End with one question: "Who are you putting in? Find them on LinkedIn and paste their profile URLs here." When URLs come in, check each person against Target personas and the open roles, and say for each: right person, right function but wrong level (and who to look for instead), or not a fit. Then `enroll` puts the right ones into Zoho.

Do not copy the brief or the row into `prospect-notes.md`. The sheet is the record. Per-person notes and cadence state go in Zoho and prospect-notes as usual.

---

## Never

  - Write to the sheet in Read mode, or let an intern run Plan mode.
  - Write outside the 21 attack-plan columns, or edit treg's columns.
  - Spend credits, pull job postings, or read Zoho, Gmail or Slack while planning.
  - Copy the block to a duplicate row.
  - Put a dollar figure, a rate or any cost other than the approved percentage in the row.
  - Guess. "Not found (checked date)" instead.
  - Put company research or row content in a repo file.
