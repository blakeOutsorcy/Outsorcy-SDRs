# Zoho reference for the intern program

IDs and rules the skills use. Managers keep this current.

## Users

| Person | Zoho user id |
| --- | --- |
| Diar Bllaca | 6673507000005798020 |
| Liza Xhaferi | 6673507000005798002 |
| Urese Bytyci | 6673507000005798011 |
| Vullnet Polloshka | 6673507000005798029 |
| Blake Danielson | 6673507000002568001 |
| Travis Bennett | 6673507000004721002 |

## Cadences interns use

| Cadence | Id | When |
| --- | --- | --- |
| High-Touch US Calls_10/2026 | 6673507000006475041 | Company or job is in the US (also Canada). Enroll 15:00 to 16:00 Prishtina. |
| High-Touch EU Calls_10/2026 | 6673507000006543001 | Company or job is in the UK or EU. Enroll by 12:00 Prishtina. |

Both are 8 calls: 2 a day on days 1 to 3, then day 5 and day 7. Email and LinkedIn touches between calls come from the outsorcy-high-touch-3day skill, not from the cadence.

Do not enroll interns in any other cadence. Not "High-Touch US Calls v2", not the deactivated "High-Touch EU_10/2026" or "High-Touch US_10/2026", not "Health tech hiring - 15 day" (it creates calls under Blake's name), not Hammer, Switchers, Inbound, Bundled services, Pre-seed, Growing teams or Solo expert. Anything outside the US, UK and EU (Australia, India, LatAm): ask a manager first.

## How the two cadences behave

  - US Calls creates every call on a timer, made or not. Missed days stack 2 to 3 calls per Lead. Dial each Lead once and set the result on the newest open call; cancel the older ones.
  - EU Calls creates the next call only after the last one is completed or cancelled. Missed days freeze the Lead. Close every call out the same day.

## Call Result picklist and what to do after each

Set the Call Result on the cadence call in the Zoho dialer before the next dial. Then Claude does the rest (log-call skill).

| Call Result | Lead Status to set | Cadence |
| --- | --- | --- |
| No answer | Attempted to Contact | stays |
| Left voicemail | Attempted to Contact | stays |
| Busy | Attempted to Contact | stays |
| Gatekeeper | Attempted to Contact | stays |
| Wrong number | no change, note the bad number | stays, fix the number |
| Requested call back | Attempted to Contact, Note with the day and time | stays |
| Requested more info | Contacted | stays; send the info today |
| Interested | Contacted | un-enroll; next step by hand |
| Not interested | Contacted, then Not Qualified if it is a firm no | un-enroll |
| Meeting booked | Pre-Qualified, handoff Note | un-enroll |
| Do not call | Not Qualified | un-enroll at once, cancel open calls |

Note: Zoho does not yet move Lead Status from the Call Result on its own. Until a manager adds that workflow, the log-call skill does it.

## Do-not-call rules

  - A Lead whose phone is on the national DNC registry (Apollo flags it, the attack-plan Note says so) is email and LinkedIn only. It never goes into a call cadence.
  - A person who says "do not call" is Not Qualified the same day, un-enrolled, and their open calls cancelled.
  - Check before every enroll and every call sheet. Dialing a DNC number is a red flag.

## Capacity rules (managers set these)

  - Live load: at most 45 Leads per intern in a cadence at once.
  - Backlog gate: no new enrollments while the intern has more than 20 overdue calls.
  - Daily intake: at most 15 new Leads enrolled per intern per day, 2 to 4 people per company.
  - Parked Leads stay out of cadences until the company shows up again in a daily job-post list.

## Useful COQL

  - Open calls: select Subject, Call_Start_Time, What_Id from Calls where (Owner = '<id>' and Outgoing_Call_Status in ('Overdue','Scheduled'))
  - Completed calls today: select Subject, Call_Result, Call_Duration_in_seconds, What_Id from Calls where (Owner = '<id>' and Outgoing_Call_Status = 'Completed') and Call_Start_Time >= '<today 00:00 Prishtina, as MT offset>'
  - Leads by company: select Company, Lead_Status, COUNT(id) from Leads where Owner = '<id>' group by Company, Lead_Status
  - Use COUNT(id) in capitals with group by. Wrap three or more conditions in brackets. Change Outgoing_Call_Status with a normal update, not mass update.
