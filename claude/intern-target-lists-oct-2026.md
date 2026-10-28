# Intern target lists (Oct 4 2026)

Workbook: Intern_Target_Lists_Oct2026.xlsx (sent in the Intern SDR project chat). 204 accounts: Overnight coverage 105 (36 Tier A), Health lookalikes 99 (28 Tier A). Tabs: Summary, Overnight coverage, Health lookalikes, Clay filters used.

## List 1: Overnight / 24-7 coverage (105)

Pitch: Prishtina is 6 hrs ahead of Eastern and 9 ahead of Pacific, so a normal 8am-4pm Kosovo shift covers 11pm-7am Pacific. No night differential, no graveyard churn. Target companies staffing nights domestically (half-cost framing works); rows marked "already offshore" compete on price, lead with quality only.

Verticals that produced Tier A: freight brokerage/3PL and time-critical logistics (TRAFFIX, PRIMO, Allen Lund, Airspace), remote video and alarm monitoring (Pro-Vigil, ECAM, Deep Sentinel, DGA, ALERT 360, Guardian Protection, Becklar, Netwatch, DynaFire), emergency home services and warranty (PuroClean, Oncourse, Goettl, Hoffmann Brothers, Contractor Connection), flexible-stay and property operators (Blueground, Kasa, FirstService Residential NY, Rently), private aviation and regional airlines (JSX, Jet Linx, flyExclusive, Clay Lacy, XO), fiber ISPs (Vero, Blue Stream, Ezee, Vyve), always-on marketplaces/fintech/medtech (Rover, FalconX, Elife, Kestra, Cadence).

Buyer titles: VP/Director Customer Support or Customer Care, Head of CX, Support Ops, VP Ops, COO; Director of Monitoring, Dispatch or Operations Control for security, freight and aviation.

## List 2: Teladoc / Wondr / Virta lookalikes (99)

Pattern: virtual care or benefit sold B2B2C to employers and health plans with a real SDR motion. Tier A: Sword, Calibrate, Form Health, Found, FlyteHealth, Lark, Dario, Lantern, Pomelo Care, Cylinder, Sana, Ramp Health, Wellth, Fabric, apree health, Hello Heart, Firefly Health, Vori Health, Rightway, Tava Health, Goodpath, OncoHealth, Pelago, Aduro, Centivo, First Stop Health, Visana Health, EasyHealth.

Buyer titles: CRO, VP Sales, VP Employer Sales, Head of Growth, Head of Sales Development. Pitch is "we fill the SDR seat you are hiring for"; reference the Wondr SDR case study.

## Clay notes and gotchas

  - Working field names: company_size (enum buckets), locations.any(country_name = "United States"), industry in (...), description contains (...) (whole-token), products_and_services is_similar_to (...) (semantic), estimated_employee_count >= N.
  - locations.any matches foreign HQs with a US office; post-filter on the returned country field.
  - The 51-200 bucket is full of 3-30 person companies; add estimated_employee_count >= 40 or 60.
  - Semantic phrases like "24/7 customer support" return CX software and BPO vendors, not buyers. Describe the buyer's business instead (freight broker, alarm monitoring, fiber ISP).
  - "description contains 24/7" matches product uptime claims; useless alone.
  - Pages are 20 rows; semantic queries degrade after page 3. Run more vertical queries instead of paging deeper.
  - Dormant/acquired pages surface (Livongo, Ginger, ActiveHealth, Quartet, Pack Health). Current clients surface too (Wondr Health on page 4); dedupe against Zoho before loading.
  - Next: Open Jobs, Tech Stack, Latest Funding, Headcount Growth enrichments; save Open Jobs + funding as cadence merge fields.
  - Still unverified seeds for a round 3: Omada, Hinge Health, Vida, Twin Health, Noom for Work, Lyra, Spring Health, Carrot, Maven, Progyny, Transcarent, Accolade, 9amHealth, Oshi, Cecelia Health, Knownwell, Sequence.
