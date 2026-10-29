# How this project works (read this first)

Everyone in the intern SDR program works in this one GitHub repo, Outsorcy-SDRs, through Claude Code: Vullnet, Urese, Diar, Liza, and the managers Blake Danielson and Travis Bennett.

Updated Oct 29, 2026. The fixed account lists from week one are retired. Your work now comes from the daily job-post list, and Zoho is where your Leads, cadences and calls live. Claude reads Zoho for you, so you do not keep lists by hand.

## Opening a session

1. Go to claude.ai/code and start a new session on the Outsorcy-SDRs repo.
2. One time only: connect Zoho, Apollo and Slack with your own login at https://claude.ai/customize/connectors. Zoho records belong to whoever is connected, so it has to be you. Connect first, then open the session.
3. One session per day. Start a fresh one each morning.

Claude saves your docs to the repo after every change. If it says a save failed, tell a manager before you close the session.

## How a day works

1. **Blake posts the list.** A CSV of companies that just posted a job we can place, in #phase-2-ai-academy.
2. **Split it.** Anyone says "split today's list". Claude round-robins the companies across the four of you and writes them into accounts/claims.md. A company someone already worked goes back to them.
3. **Enroll your claims.** "enroll [company]". Claude picks 2 to 4 people (or asks you to), pulls email, phone and LinkedIn from Apollo, shows you the Leads, and on your yes creates them and puts them in the US or EU call cadence.
4. **Call.** "start my day" gives you a call sheet built from Zoho. Dial from the cadence step in Zoho, set the Call Result, then tell Claude what happened: "vm on Gil", "Gil picked up, wants info", "booked Gil for Tuesday". Claude updates the Lead, takes do-not-call people out at once, and tells you what to send next.
5. **Wrap.** "wrap my day". Claude pulls your numbers from Zoho and gives you the scorecard and the Slack post.

When a cadence ends without a meeting, the company is parked. It comes back to you when it posts a new job.

## What you say

| You say | What happens |
| --- | --- |
| start my day | latest coaching line, call sheet from Zoho, 10:00 Slack post |
| split today's list | today's CSV split across the four of you |
| enroll [company] | Leads created and enrolled, after checks |
| vm on X / X picked up / booked X | Zoho updated, next touch drafted |
| what do I send after this call | LinkedIn request, Email 1 or 2, break-up |
| prep me for X | ten-line pre-call brief |
| research [company] | attack plan |
| what are my accounts | your claims, with live numbers |
| wrap my day | scorecard from Zoho, 19:00 Slack post |

## The rules that matter

  - **Claims.** If a company is in your section of accounts/claims.md, it is yours. First claim wins. Found a company yourself? "enroll [company]" checks it and flags it for the 16:00 standup.
  - **Capacity.** At most 45 Leads in a cadence at once, at most 15 new Leads a day, and no new enrollments while you have more than 20 overdue calls. Over the line, Claude will tell you what to clear first.
  - **Do not call.** A number on the DNC registry is email and LinkedIn only. Someone who says "don't call me" is out the same day. Dialing a DNC number is a red flag.
  - **Set the Call Result on every call.** Dial from the cadence step, not the Lead page. If it is not in Zoho, it did not happen.
  - **Never** create Deals, delete records, touch someone else's records, discuss pricing, or send on a manager's behalf. A booked meeting goes to Blake and Travis as a Note and a Slack post.

## What is where

  - accounts/claims.md: who owns which company.
  - accounts/suppression.md: companies nobody touches.
  - lists/: the daily CSVs and each day's split.
  - claude/intern-sdr-playbook.md: pitch, rhythm, scorecard and red flags, meeting definition, Zoho rules.
  - claude/zoho-reference.md: cadences, Call Result rules, DNC and capacity rules.
  - interns/<your name>/: daily-log.md (plan and scorecard), prospect-notes.md (per-company touches), coaching.md (feedback from Blake and Travis).
  - archive/: the old October lists. History only.

## Rules of the room

  - Write only in your own folder and your own section of claims.md. Claude will refuse anything else, and the repo history shows every edit.
  - Do not edit the playbook, suppression or zoho-reference. If something is wrong, say so in #phase-2-ai-academy.
  - Everyone can read everyone's folder. Steal good openers, learn from each other's objections.

## Slack

Two posts a day in #phase-2-ai-academy: the 10:00 plan and the 19:00 scorecard. Claude writes them, you post them.
