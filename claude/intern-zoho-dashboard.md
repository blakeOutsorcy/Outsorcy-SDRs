# Intern SDR Activity dashboard (Zoho CRM)

Built Oct 12, 2026 by Blake. Lives in Zoho CRM > Analytics > "Intern SDR Activity" (dashboard id 6673507000006257025, <https://crm.zoho.com/crm/tab/Analytics/6673507000006257025>). Public, read_write. Every component is filtered to the four intern users: Liza Xhaferi, Urese Bytyci, Diar Bllaca, Vullnet Polloshka. Managers read it at the 16:00 standup and before the 19:00 scorecard; interns can open it to check their own numbers.

## How each scorecard line maps to Zoho

  - Dials = Calls where Call Type is Outbound and Outgoing Call Status is Completed. Scheduled and Overdue calls are cadence steps that have not been made yet and do not count.
  - Connects = Completed calls with a Call Result of Not interested, Requested more info, Requested call back, Interested, Meeting booked or Do not call. Gatekeeper is not a connect. If you do not set a Call Result on a pickup, it does not count as a connect. (Dashboard components still use the old four-value list until updated.)
  - Conversations = Completed calls with duration of 120 seconds or more.
  - Voicemails = Call Result "Left voicemail".
  - Meetings booked = Leads at Lead Status "Pre-Qualified". That is the stage for a booked meeting. Move the Lead to Pre-Qualified the moment the invite is accepted, same day, with the handoff Note from the playbook. The all-time chart is the running count; the this-week chart uses Modified Time as the proxy for when it was booked.
  - Cadence backlog = calls with Outgoing Call Status Overdue. This is the red flag chart. Un-enroll or work the list, do not let it stack.
  - Leads created = Leads owned by the intern, by Created Time.
  - Lead status mix = all intern-owned leads by Lead Status. Movement from Not Contacted to Attempted to Contact or Contacted is what we want to see.
  - LinkedIn and email steps = Tasks owned by the intern, Completed (by Closed Time) and Open.
  - Emails sent = Emails module, intern as owner, by Sent On.

## Call Result picklist (org wide, changed Oct 12, 2026)

Eleven values on the Calls module. Pick one on every completed call before moving on.

| Result | Use it when | Lead Status it will set (once the workflow is live) |
| --- | --- | --- |
| No answer | Rang out, no voicemail left | Attempted to Contact |
| Left voicemail | No answer, voicemail left | Attempted to Contact |
| Busy | Busy signal or dropped | Attempted to Contact |
| Gatekeeper | Reception or assistant, not the decision maker | Attempted to Contact |
| Wrong number | Number is wrong or disconnected | No change, flag for data fix |
| Not interested | Decision maker said no | Contacted |
| Requested more info | Asked for an email or material | Contacted |
| Requested call back | Asked for a specific later time. Stay in the cadence, add a Note with the day and time | Attempted to Contact |
| Interested | Engaged, no meeting yet | Contacted |
| Meeting booked | Meeting on the calendar | Pre-Qualified |
| Do not call | Asked not to be contacted | Not Qualified, un-enroll |

"No answer" and "Wrong number" are relabels of the old "No response/Busy" and "Invalid number" (same underlying values, old records still work). The dropdown order could not be set through the API; the four original values show first.

## How calls get logged (found Oct 12)

Two records get created per dial when an intern dials from the lead page and then marks the cadence step done: the dialer auto-log ("Outgoing call to Name", has duration and recording, no result) and the cadence call ("Name Company | EU Day 1 - Call 1", has the result). Dials double count and the result sits on the record without the recording. Rule going forward: dial from the scheduled call inside the cadence step, never from the lead page or a list view, and set the Call Result before the next dial. Then there is one record per dial with duration, recording and result on it. Confirm with one intern's first call of the day before rolling to all four.

The Lead link on a call is What_Id with $se_module = Leads, not Who_Id.

## Planned workflow (not built yet, Blake to say go)

Calls workflow rule on outgoing call logged or modified, action is a Deluge function that reads Call_Result and What_Id and moves the related Lead's status per the table above, never backwards. Native Field Update can target Leads from a Calls rule but cannot check the current Lead Status, which is why the function is needed. Requested call back stays at Attempted to Contact so the lead stays in the cadence. Cadence change to pair with it: trim the result-based un-enroll in High-Touch EU and US to Wrong number and Do not call only, and attach it to all eight calls (today it is on calls 1, 2, 3, 5 and 7 only). Optional: a validation rule on Calls that blocks saving a Completed call without a Call Result (browser only).

## Components (top to bottom)

1.  Dials Today by Intern (count and talk seconds)
2.  Connects Today by Intern (by call result)
3.  Conversations Today (2+ min) by Intern
4.  Overdue Cadence Calls by Intern (backlog, red flag)
5.  Dials This Week by Day and Intern
6.  Call Results This Week by Intern
7.  Conversations This Week (2+ min) by Intern
8.  Leads Created This Week by Intern
9.  Lead Status Mix by Intern
10. Cadence Tasks Completed This Week by Intern
11. Open Cadence Tasks by Intern
12. Emails Sent This Week by Intern
13. Dials Last 30 Days by Day and Intern (trend)
14. Weekly Scorecard: Dials This Week by Intern
15. Meetings Booked: Leads at Pre-Qualified by Intern (all time)
16. Meetings Booked This Week: Pre-Qualified Leads by Intern (by last modified)

## Not in Zoho (still reported in the 19:00 Slack post)

Mock call counts and scores, LinkedIn requests sent and accept rate (HeyReach).

## Baseline on day one of week two (Mon Oct 12, Prishtina)

Completed dials: Urese 20, Diar 16, Liza 13, Vullnet 10 (includes duplicates from the two-record logging above). Overdue cadence calls: Liza 110, Urese 74, Vullnet 64, Diar 41 (289 total). Call Results set on 9 of 72 completed calls since Oct 5, 8 of them Diar's. No intern leads at Pre-Qualified yet. Durations: 29 calls at 0 seconds, 22 in the 30 to 50 second voicemail band, 5 real conversations of 2 to 3 minutes.
