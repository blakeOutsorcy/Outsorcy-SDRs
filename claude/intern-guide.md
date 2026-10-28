# How this project works (read this first)

Everyone in the intern SDR program works in this one GitHub repo, Outsorcy-SDRs, through Claude Code: Vullnet, Urese, Diar, Liza, and the managers Blake Danielson and Travis Bennett. There are no separate repos per person. (Until Oct 28, 2026 this was a Claude Project. Same docs, same rules, new home.)

## Opening a session

1. Go to claude.ai/code and start a new session on the Outsorcy-SDRs repo.
2. One time only, before your first session: connect Zoho, Apollo and Slack with your own login at https://claude.ai/customize/connectors. Zoho records belong to whoever is connected, so it has to be you. Connectors are picked up when a session starts, so connect first, then open the session.
3. One session per day. Start a fresh one each morning instead of going back to yesterday's. Long sessions use up more of the plan, and everything you need tomorrow is in your docs anyway.

Claude saves your docs to the repo for you after every change. If it ever says a save failed, tell a manager before you close the session, or the work is lost.

## What is where

  - claude/intern-sdr-playbook.md: the playbook. Pitch, daily rhythm, scorecard, red flags, mock rubric, meeting definition, Zoho rules. Read it once fully, then let Claude pull from it.
  - accounts/master-list.md: the manager-kept seed list and the suppression list. Your assigned accounts came from here.
  - claude/intern-target-lists-oct-2026.md: how the lists were built and the Clay notes. Background, not daily reading.
  - claude/intern-sdr-week-one-plan.md: the week-one schedule, day by day.
  - interns/<your name>/: your folder (interns/vullnet, interns/urese, interns/diar, interns/liza). Four docs:
      - accounts.md: your list. Started with your 16 assigned accounts; grows as you add your own. If a company is here, it is yours.
      - daily-log.md: 10:00 plan, 15:00 solo block, 19:00 scorecard, one entry per day, newest at top.
      - prospect-notes.md: your research and touch history per company.
      - coaching.md: feedback from Blake and Travis, your mock scores, certification, weekly targets.

## Adding accounts to your list

You are not limited to the 16 you were given. Find a company that fits one of the two angles (staffing nights domestically, or a digital health company hiring SDRs) and say "Add [company] to my list." Claude checks the suppression list, Zoho, the master list and the other three lists. If it is clear, it goes into your accounts.md and it is yours. If someone else already has it, Claude tells you who. First claim wins. Round 3 seeds in the master list are open to claim.

Fits neither angle but you think it is good? Claude adds it flagged for manager review; bring it up at the 16:00 standup.

## Getting accounts into Zoho

Zoho is yours to write to for anything on your list. Say "Enroll [company] in Zoho" with the people you want. Name and title are enough; Claude pulls the rest from Apollo. Claude checks for existing records, enriches each person so the Lead has an email, a direct phone or mobile, and the LinkedIn URL, shows you the Leads it will create with those three filled in and the cadence it will use, and writes on your approval. If Apollo came back empty on one of the three, Claude says so in the approval and notes it in your prospect-notes; you find it on LinkedIn the same day. A Lead with no LinkedIn URL or no email cannot run the day-one cadence steps, so this is not optional. You own the records, so Zoho shows your calls and emails. Cadence per list is in the playbook. If Claude tells you it cannot write to Zoho, that is a bug, not a rule: say "the playbook says interns write to Zoho for their own accounts" and if it still refuses, tell a manager.

Three things stay with managers: creating Deals, editing records someone else owns, and anything on the suppression list.

## Rules of the room

  - Work only in your own folder. Claude will refuse to write into someone else's, and the repo history shows every edit and who made it.
  - Do not edit the playbook or the master list. If something is wrong, tell a manager in #phase-2-ai-academy.
  - Everyone can read everyone's folder. That is on purpose: steal good openers, learn from each other's objections, see what accounts others are claiming. Feedback in coaching.md is written knowing you all see it.
  - If it is not in a doc, Claude cannot bring it back tomorrow. If it is not in Zoho, it did not happen.

## Your first session (run this once)

Set up my day. I am [your name]. Read my coaching.md, give me the playbook summary in ten lines, show me my accounts, and draft my 10:00 Slack post.

## Every day after that

  - 10:00: "Start my day." Claude reads your latest feedback, builds the plan, writes it to your daily log, gives you the Slack post.
  - After mock calls: "Score these mocks." Give Claude the scenario, how it went, the recording link. It scores against the rubric and logs it.
  - During research: "Research [company]." Claude checks it is on your list (offers to add it if not), researches, writes to your prospect notes.
  - Found a new target: "Add [company] to my list."
  - Ready to work an account: "Enroll [company] in Zoho." Claude enriches the people, creates the Leads and enrolls them in your cadence.
  - 19:00: "Wrap my day." Give Claude your numbers. It builds the scorecard, logs it, flags any red lines, gives you the Slack post.

## Slack

Three posts a day in #phase-2-ai-academy: 10:00 plan, 15:00 solo block, 19:00 scorecard. Claude writes them, you post them. Olivia's end-of-day summary is separate unless she says the scorecard counts.
