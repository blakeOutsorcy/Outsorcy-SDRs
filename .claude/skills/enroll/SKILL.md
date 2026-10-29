---
name: enroll
description: Put a claimed company's people into Zoho and into the right call cadence, or re-enroll a parked company that re-posted a job. Use for "enroll [company]", "put [people] in Zoho", "add [company] to Zoho", "work [company]", "re-enroll [company]".
---

# Enroll a company

The intern is the rep and the record owner. Use the outsorcy-zoho-crm skill conventions if it is available; otherwise call the Zoho tools directly with the same rules. Every write needs the intern's approval, in one approval line per batch.

## 1. Gates (stop at the first failure and say why)

  1. Claim: the company is in this intern's section of accounts/claims.md. If it is not there at all, run the split-list checks for this one company (suppression, claims, Zoho owners) and, if clear, add it as a claim with Source "self-claimed" and flag it for the 16:00 standup. If another intern or a manager has it, stop and name them.
  2. Fresh post: a parked company only goes back into a cadence if it appears in a job-post list dated in the last 7 days. Otherwise stop: it waits.
  3. Capacity: read the intern's open calls and live Leads from Zoho. More than 20 overdue calls, or 45 Leads already in a cadence, or 15 Leads already enrolled today: stop, show the numbers, and say what to clear first.

## 2. People

  - Parked company that re-posted: reuse the intern's existing Leads there. Skip anyone Not Qualified, Junk, Lost or on the DNC registry for calling. Do not create duplicates.
  - New company: 2 to 4 people. Use the buyer for the role posted (hiring manager for the role, the head of that function, and one exec: COO, CRO, VP Sales, Head of Support, CFO for finance roles). If the intern has not named people, propose them from Apollo or Clay and let the intern pick. Use outsorcy-account-attack-plan if the intern asks for research.

## 3. Dedup and enrich

  - Search Leads (including converted), Contacts, Accounts and Deals by company, domain and each email. Someone else owns a person: drop that person and say who.
  - Apollo people match (bulk when more than one) with waterfall email and phone. State the Apollo credit cost before running it.
  - Each Lead needs Email, Phone or Mobile, and LinkedIn_URL. Name any that are still empty in the approval line, create anyway, and add a "chase on LinkedIn today" line under the company in prospect-notes.md. Never guess one.
  - If Apollo flags a phone on the DNC registry: create the Lead without enrolling it in a call cadence, add a Note "DNC registry: email and LinkedIn only".

## 4. Show, then write on one approval

Show the exact Lead fields (First_Name, Last_Name, Designation, Company, Email, Phone or Mobile, LinkedIn_URL, Lead_Source = Apollo, Lead_Status = Not Contacted, Owner = the intern), the cadence (US Calls or EU Calls by the company's or job's country, ids in claude/zoho-reference.md) and the enroll time. On approval: create, add a one-paragraph Note per Lead (role posted, posting link, angle, ask), enroll.

## 5. Record

  - accounts/claims.md: status active, Leads = count.
  - prospect-notes.md under the company: date, Lead ids, cadence, the posting that triggered it.
  - Commit and push.
  - Offer the day-one touches (LinkedIn request, Email 1) from outsorcy-high-touch-3day, built on the job posting: plain ask, "open to a remote hire for this seat?", no role counts, no pricing.
