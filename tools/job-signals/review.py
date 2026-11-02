#!/usr/bin/env python3
"""Blake's evening review of the daily job-signals list.

signals.py calls write_review() to write lists/YYYY-MM-DD-review.md next to the day's CSV:
one line per company, grouped by HQ region, with every posting under it. Blake ticks the
companies to work and marks the file reviewed. The morning build reads it back with:

  python3 tools/job-signals/review.py pending
      Reviewed files from the last 7 days that have no split yet, as JSON: approved companies
      (with their postings) and skipped ones (with Blake's reason). Read only.

  python3 tools/job-signals/review.py log YYYY-MM-DD
      Appends that day's decisions to review-log.csv (once per date). This log is what we
      learn from to automate the review later.
"""
import csv, json, os, re, sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LISTS = os.path.join(REPO, "lists")
CLAIMS = os.path.join(REPO, "accounts", "claims.md")
SUPPRESSION = os.path.join(REPO, "accounts", "suppression.md")
REVIEW_LOG = os.path.join(HERE, "review-log.csv")
MT = ZoneInfo("America/Denver")
ET = ZoneInfo("America/New_York")
PRISHTINA = ZoneInfo("Europe/Belgrade")
MAX_AGE_DAYS = 7
REGIONS = ["US", "Europe", "Europe new", "Unknown"]
GROUP_HEAD = {"Europe new": "Europe, new companies not on the Account List"}
LOG_COLS = ["list_date", "company", "domain", "hq_region", "decision", "reason", "best_ease", "departments",
            "titles", "employees", "tab", "owner", "flags"]

COMPANY_RX = re.compile(r"^- \[([ xX])\] \*\*(.+?)\*\* · (.+?) · ")
WHY_RX = re.compile(r"^\s+- why:(.*)$")
REVIEWED_RX = re.compile(r"^Reviewed: \[([ xX])\]", re.M)


def norm(name):
    n = re.sub(r"[^a-z0-9 ]", " ", (name or "").lower())
    n = re.sub(r"\b(inc|llc|ltd|limited|corp|corporation|co|company|gmbh|plc|the)\b", " ", n)
    return " ".join(n.split())


def load_claims():
    """norm(company) -> (intern, status) from accounts/claims.md."""
    out, who = {}, None
    if not os.path.exists(CLAIMS):
        return out
    for line in open(CLAIMS, encoding="utf-8"):
        m = re.match(r"^## (\w+)", line)
        if m:
            who = m.group(1)
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if who and line.startswith("|") and len(cells) >= 2 and cells[0] not in ("Company", "---", ""):
            out[norm(cells[0])] = (who, cells[1])
    return out


def load_suppressed():
    out = set()
    if not os.path.exists(SUPPRESSION):
        return out
    for line in open(SUPPRESSION, encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and cells and cells[0] not in ("Company", "---", ""):
            out.add(norm(cells[0]))
    return out


def owner_text(company, claims, suppressed):
    k = norm(company)
    if k in suppressed:
        return "suppressed"
    if k in claims:
        who, status = claims[k]
        return f"closed ({who})" if status == "closed" else f"re-post, {who}'s ({status})"
    return "new"


def _companies(rows):
    by = {}
    for r in rows:
        k = (r.get("domain") or "").lower() or norm(r["company"])
        by.setdefault(k, []).append(r)
    return by


def next_build(now):
    """The first weekday 08:00 Prishtina after now: when this list gets planned and split."""
    t = now.astimezone(PRISHTINA)
    b = t.replace(hour=8, minute=0, second=0, microsecond=0)
    if b <= t:
        b += timedelta(days=1)
    while b.weekday() >= 5:
        b += timedelta(days=1)
    return b


def split_done(date):
    """True once a lists/*-split.md names this day's review file."""
    tag = f"lists/{date}-review.md"
    for fn in os.listdir(LISTS):
        if fn.endswith("-split.md") and tag in open(os.path.join(LISTS, fn), encoding="utf-8").read():
            return True
    return False


def write_review(path, rows, now, skipped_anz=()):
    """Write (or extend) the review file for one day's list."""
    claims, suppressed = load_claims(), load_suppressed()
    groups = {reg: [] for reg in REGIONS}
    for posts in _companies(rows).values():
        reg = posts[0].get("hq_region") or "Unknown"
        if posts[0].get("tab") == "EU discovery":
            reg = "Europe new"
        groups.setdefault(reg, []).append(posts)
    stamp = now.astimezone(MT).strftime("%H:%M MT")
    lines = []
    exists = os.path.exists(path)
    if exists:
        text = open(path, encoding="utf-8").read()
        if REVIEWED_RX.search(text) and REVIEWED_RX.search(text).group(1).lower() == "x":
            # New companies after Blake reviewed: hold the file until he looks again.
            text = REVIEWED_RX.sub("Reviewed: [ ]", text, count=1)
            open(path, "w", encoding="utf-8").write(text)
            lines += [f"New companies added at {stamp} after the review. Tick them, then mark the file reviewed again.", ""]
    if not exists:
        b, g = next_build(now), now.astimezone(MT)
        lines += [f"# Review: jobs for the {b.strftime('%a %b')} {b.day} morning build", "",
                  f"Gathered {g.strftime('%a %b')} {g.day}, {g.strftime('%H:%M')} MT "
                  f"({now.astimezone(PRISHTINA).strftime('%H:%M')} Prishtina). "
                  f"Built {b.strftime('%a %b')} {b.day}, 08:00 Prishtina ({b.astimezone(MT).strftime('%a %H:%M')} MT).", "",
                  "How to review (edit this file on GitHub, pencil icon):",
                  "  - Change `[ ]` to `[x]` for each company the interns should work.",
                  "  - Leave `[ ]` to skip it. A few words after `why:` help us learn your rules.",
                  "  - Then change the line below to `Reviewed: [x]` and commit to main.",
                  "  - The 08:00 Prishtina build (midnight MT) plans and splits only reviewed files. "
                  "Not reviewed by then: it waits for the next morning.",
                  "  - Owner `new` or `re-post` comes from accounts/claims.md. Zoho owners are checked at the build.",
                  "  - \"Europe, new companies\" are not on the Account List yet. Ticked ones are added to its "
                  "\"EU job signals\" tab at the build, then planned and split like the rest.", "",
                  "Reviewed: [ ]", ""]
        if skipped_anz:
            lines += [f"Skipped (ANZ, for later): {', '.join(sorted(skipped_anz))}", ""]
    for reg in REGIONS + [r for r in groups if r not in REGIONS]:
        comps = groups.get(reg) or []
        if not comps:
            continue
        comps.sort(key=lambda ps: (-max(int(p["ease_score"]) for p in ps), ps[0]["company"].lower()))
        name = GROUP_HEAD.get(reg, reg)
        head = f"## {name} ({len(comps)})" if not exists else f"## {name} (added {stamp})"
        lines += [head, ""]
        for ps in comps:
            p0 = ps[0]
            best = max(int(p["ease_score"]) for p in ps)
            emp = f"{p0['employees']} staff" if p0.get("employees") else "staff unknown"
            lines.append(f"- [ ] **{p0['company']}** · {p0.get('domain') or 'no domain'} · {emp} · {p0['tab']} · "
                         f"ease {best} · {owner_text(p0['company'], claims, suppressed)}")
            flags = set()
            for p in sorted(ps, key=lambda p: -int(p["ease_score"])):
                where = ", ".join(x for x in (p.get("job_city"), p.get("job_country")) if x) or "location not given"
                rr = f" ({p['role_region']})" if p.get("role_region") else ""
                lines.append(f"  - {p['title']} · {where}{rr} · posted {p['posted_et']} ET · {p['url']}")
                flags.update(n.strip() for n in (p.get("note") or "").split(";") if n.strip())
            if flags:
                lines.append(f"  - flags: {'; '.join(sorted(flags))}")
            lines.append("  - why:")
        lines.append("")
    with open(path, "a" if exists else "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def parse_review(path):
    """(reviewed, [{company, domain, hq_region, approved, reason}])."""
    text = open(path, encoding="utf-8").read()
    m = REVIEWED_RX.search(text)
    reviewed = bool(m and m.group(1).lower() == "x")
    out, reg = [], "Unknown"
    for line in text.splitlines():
        h = re.match(r"^## (\w+)", line)
        if h:
            reg = h.group(1)
            continue
        c = COMPANY_RX.match(line)
        if c:
            dom = c.group(3).strip()
            out.append({"company": c.group(2).strip(), "domain": "" if dom == "no domain" else dom.lower(),
                        "hq_region": reg, "approved": c.group(1).lower() == "x", "reason": ""})
            continue
        w = WHY_RX.match(line)
        if w and out:
            out[-1]["reason"] = w.group(1).strip()
    return reviewed, out


def _list_rows(date):
    p = os.path.join(LISTS, f"{date}.csv")
    if not os.path.exists(p):
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _match(entry, rows):
    k = entry["domain"] or None
    return [r for r in rows if (k and (r.get("domain") or "").lower() == k) or
            (not k and norm(r["company"]) == norm(entry["company"]))]


def pending():
    today = datetime.now(timezone.utc).astimezone(PRISHTINA).date()
    out = []
    for fn in sorted(os.listdir(LISTS)):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-review\.md$", fn)
        if not m:
            continue
        date = m.group(1)
        if split_done(date):
            continue
        age = (today - datetime.strptime(date, "%Y-%m-%d").date()).days
        reviewed, entries = parse_review(os.path.join(LISTS, fn))
        item = {"list_date": date, "review_file": f"lists/{fn}", "reviewed": reviewed, "age_days": age}
        if age > MAX_AGE_DAYS:
            item["status"] = "expired (older than 7 days, not split)"
        elif not reviewed:
            item["status"] = "waiting for Blake's review"
        else:
            rows = _list_rows(date)
            item["status"] = "ready"
            item["approved"] = []
            for e in entries:
                if not e["approved"]:
                    continue
                ps = _match(e, rows)
                a = {**e, "postings": [{k: r.get(k, "") for k in ("title", "job_city", "job_country", "role_region",
                                        "url", "posted_et", "ease_score", "matched_title", "note")} for r in ps]}
                new = next((r for r in ps if r.get("tab") == "EU discovery"), None)
                if new:   # the build adds this row to the EU job signals tab before planning
                    a["new_company"] = {"Account": new["company"], "Domain": new.get("domain", ""),
                                        "LinkedIn": new.get("company_linkedin", ""), "HQ": "",
                                        "Country": new.get("hq_country", ""), "Employees": new.get("employees", ""),
                                        "Industry": new.get("industry", ""), "Region": "Europe",
                                        "Source": f"job-signals EU discovery, {date}"}
                item["approved"].append(a)
            item["skipped"] = [{"company": e["company"], "reason": e["reason"]} for e in entries if not e["approved"]]
        out.append(item)
    print(json.dumps(out, indent=1))


def log(date):
    if os.path.exists(REVIEW_LOG):
        with open(REVIEW_LOG, newline="", encoding="utf-8") as f:
            if any(r["list_date"] == date for r in csv.DictReader(f)):
                print(f"{date} already logged")
                return 0
    reviewed, entries = parse_review(os.path.join(LISTS, f"{date}-review.md"))
    if not reviewed:
        print(f"{date} is not reviewed yet", file=sys.stderr)
        return 1
    rows = _list_rows(date)
    claims, suppressed = load_claims(), load_suppressed()
    new = not os.path.exists(REVIEW_LOG)
    with open(REVIEW_LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LOG_COLS)
        if new:
            w.writeheader()
        for e in entries:
            ps = _match(e, rows)
            notes = sorted({n.strip() for p in ps for n in (p.get("note") or "").split(";") if n.strip()})
            w.writerow({"list_date": date, "company": e["company"], "domain": e["domain"], "hq_region": e["hq_region"],
                        "decision": "approved" if e["approved"] else "skipped", "reason": e["reason"],
                        "best_ease": max((int(p["ease_score"]) for p in ps), default=""),
                        "departments": "; ".join(sorted({p.get("department", "") for p in ps})),
                        "titles": "; ".join(p["title"] for p in ps),
                        "employees": ps[0].get("employees", "") if ps else "", "tab": ps[0].get("tab", "") if ps else "",
                        "owner": owner_text(e["company"], claims, suppressed), "flags": "; ".join(notes)})
    print(f"logged {len(entries)} decisions for {date}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "pending":
        pending()
    elif len(sys.argv) == 3 and sys.argv[1] == "log":
        sys.exit(log(sys.argv[2]))
    else:
        print(__doc__)
        sys.exit(2)
