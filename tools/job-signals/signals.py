#!/usr/bin/env python3
"""Daily job-signals list for the intern SDR program.

Finds new job postings at the companies on the Living Account List that match the
target titles in target-titles.csv, drops senior and hard-to-place roles, scores the
rest for ease of placement, and writes lists/YYYY-MM-DD.csv (Prishtina date) in the
format split-list expects. Appends one row to run-log.csv per run.

Usage (from the repo root):
  TREG_TOKEN=... python3 tools/job-signals/signals.py --accounts <file> [--accounts <file> ...]
      [--since-hours N] [--dry-run]

--accounts takes the Living Account List as either a CSV with columns
tab,account,domain,linkedin,hq,country,employees,industry, or the JSON a Google Sheets
connector returns (spreadsheets.get with grid data, or values.get). The account list is
never written into the repo.

Exit codes: 0 ok, 2 bad input, 3 treg auth failed (logged), 4 other pull failure (logged).
"""
import argparse, csv, json, math, os, re, sys, time, threading, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LISTS = os.path.join(REPO, "lists")
TITLES = os.path.join(HERE, "target-titles.csv")
RUN_LOG = os.path.join(HERE, "run-log.csv")
ET = ZoneInfo("America/New_York")
PRISHTINA = ZoneInfo("Europe/Belgrade")  # Kosovo time
TOKEN = os.environ.get("TREG_TOKEN", "").strip()

MANAGER_MAX_STAFF = 49          # titles containing "manager" only at companies under 50 staff
LARGE_COMPANY = 200             # flagged, not dropped (split-list decides)
MAX_WINDOW_DAYS = 7             # never look back further than this
LOW_BALANCE_USD = 3.0

# Columns split-list reads (lists/README.md), then the three job-signals columns.
LIST_COLS = ["posted_et", "hours_ago", "tab", "company", "domain", "employees", "hq_country", "title", "category",
             "job_city", "job_country", "url", "source", "job_id", "note", "same_role_posted_in_n_locations",
             "ai_summary", "department", "matched_title", "ease_score"]
LOG_COLS = ["run_utc", "window_start_utc", "window_end_utc", "companies", "pages_pulled", "pull_errors",
            "postings_in_window", "title_matches", "kept", "new_rows", "list_file", "cost_usd", "balance_usd",
            "status", "message"]

TAB_SHORT = [("PE/Debt Backed", "PE 6+"), ("PE/Debt, no raise 5", "PE 5+"), ("VC Seed-B", "VC Seed-B"),
             ("Digital health", "Digital health"), ("Travis 300", "Travis 300+"), ("Using competitors", "Using competitors"),
             ("Remote only", "Remote only")]

# Placeability rules (built up over the Oct 27-28 manual checks).
SENIOR = r"\b(senior|sr\.?|snr|starszy|director|directeur|vp|svp|evp|vice president|head of|chief|cfo|cto|coo|ceo|cmo|principal|staff (software|data|product|site|content|machine|security|backend|frontend|full)|member of technical staff|lead(?! generation)|leader|team lead|leiter|controller|president|superintendent|general manager|branch manager|architect|arquitecto|tax manager|reporting officer|expert partner)\b"
SENIOR_OK = r"(associate\s*/\s*sr\.? associate|senior associate|sr\.? associate(?! scientist|,? research)|semi-senior)"
HARD_TITLE = r"\b(physician|md/do|nurse|rn|lpn|therapist|psychiatrist|psychologist|counsel+or|clinician|chiropractor|medical expert|consultor emocional|clinical (investigator|social worker|qa|stewardship|practice)|pharmacist|dentist|histology|lab professionals|technician|installer|installation|cleaning|warehouse(?! management system)(?!\))|driver|cdl|field|außendienst|estimator|community liaison|in-person|on-?site|insurance agent|financial advisor|caregiver|home care|manufacturing|supervisor|showroom|on-camera|research associate|scientist, fpd|attorney|area prevention specialist|operations manager|teacher|forward deployed|medical assistant|licensed|loan officer|outside sales|sales representative - branch|clets|gd-rdc|entretien)\b"
HARD_SUMMARY = r"\b(in-person|in person|on-site|onsite|in-office|on site|field-based|in the field|travel to (client|customer) sites|experiments|cgmp|territory plans|store and warehouse|branch business plan|construction (activities|operations|teams)|site personnel|marine construction|through construction|conducting visits|customer visits|field monitoring|community outreach and meetings|showings)\b"
KEEP_ALWAYS = ["warehouse management system"]
COMPETITORS = {"accelone", "keyideas infotech private limited", "listo global", "ontop", "frontier",
               "growmotely", "isotalent", "bruntwork", "cloudstaff", "virtual latinos", "tribe wellness sales"}
LOWCOST = {"PH", "IN", "CO", "AR", "MX", "BR", "PK", "BD", "VN", "ID", "EG", "NG", "KE", "ZA", "RS", "BA", "AL",
           "MK", "XK", "UA", "RO", "BG", "PE", "CL", "EC", "DO", "GT", "HN", "SV", "NI", "CR", "JO", "NP", "LK", "MY"}

_cost = {"micro": 0}
_cost_lock = threading.Lock()


class AuthError(Exception):
    pass


# ---------------------------------------------------------------- treg
def treg_call(endpoint, body, retries=4):
    req_body = json.dumps(body).encode()
    for attempt in range(retries):
        req = urllib.request.Request(f"https://treg.to/call/{endpoint}", data=req_body, method="POST",
                                     headers={"X-Treg-Token": TOKEN, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                c = r.headers.get("X-Treg-Cost-Micro")
                if c:
                    with _cost_lock:
                        _cost["micro"] += int(float(c))
                return json.loads(r.read().decode()), None
        except urllib.error.HTTPError as e:
            txt = e.read().decode(errors="replace")[:400]
            if e.code in (401, 403) or "invalid or expired" in txt:
                raise AuthError(f"treg HTTP {e.code}: {txt}")
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 * (attempt + 1)); continue
            return None, f"HTTP {e.code}: {txt}"
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1)); continue
            return None, f"ERR {e}"
    return None, "retries exhausted"


def treg_balance():
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "balance", "arguments": {}}}).encode()
    req = urllib.request.Request("https://treg.to/mcp/", data=body, headers={
        "Authorization": "Bearer " + TOKEN, "Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            txt = r.read().decode()
        if not txt.lstrip().startswith("{"):
            txt = "\n".join(l[5:].strip() for l in txt.splitlines() if l.startswith("data:"))
        res = json.loads(txt).get("result", {})
        for c in res.get("content", []):
            d = json.loads(c.get("text", "{}"))
            if "balance_usd" in d:
                return float(d["balance_usd"])
            if "error" in d:
                raise AuthError(d.get("error"))
    except AuthError:
        raise
    except Exception:
        return None
    return None


def pull_blitz(company, days):
    url = company["linkedin"].strip().rstrip("/")
    jobs, cursor, pages, res = [], None, 0, {}
    while True:
        body = {"company_linkedin_url": url, "job": {"date_posted": {"last_days": days}}, "max_results": 50}
        if cursor:
            body["cursor"] = cursor
        res, err = treg_call("blitzapi.jobs.company", body)
        pages += 1
        if err:
            return company, jobs, err
        for j in res.get("results") or []:
            j["_src"] = "blitz"
            jobs.append(j)
        cursor = res.get("cursor")
        if not cursor or pages >= 6:
            return company, jobs, None


def pull_crustdata(companies, since_utc):
    domains = [c["domain"] for c in companies if c["domain"]]
    if not domains:
        return [], None
    filters = {"op": "and", "conditions": [
        {"field": "company.basic_info.primary_domain", "type": "in", "value": domains},
        {"field": "metadata.date_added", "type": "=>", "value": since_utc.strftime("%Y-%m-%d")}]}
    count, err = treg_call("crustdata.companies.jobs.search", {"filters": filters, "limit": 0, "aggregations": [{"type": "count"}]})
    if err:
        return [], f"crustdata count: {err}"
    n = count.get("total_count") or ((count.get("aggregations") or [{}])[0].get("value")) or 0
    if not n:
        return [], None
    fields = ["job_details.title", "job_details.url", "location.raw", "location.country", "metadata.date_added",
              "company.basic_info.name", "company.basic_info.primary_domain", "content.description"]
    res, err = treg_call("crustdata.companies.jobs.search", {"filters": filters, "fields": fields, "limit": min(int(n), 300)})
    if err:
        return [], f"crustdata rows: {err}"
    bydom = {c["domain"]: c for c in companies}
    out = []
    for row in res.get("job_listings") or []:
        jd, md = row.get("job_details", {}), row.get("metadata", {})
        co, loc = row.get("company", {}).get("basic_info", {}), row.get("location", {})
        comp = bydom.get((co.get("primary_domain") or "").lower())
        if not comp:
            continue
        out.append({"_src": "crustdata", "_company": comp, "title": jd.get("title"), "url": jd.get("url"),
                    "date_posted": md.get("date_added"), "company_name": co.get("name"),
                    "location": {"city": loc.get("raw"), "country_code": loc.get("country")},
                    "ai_summary": (row.get("content", {}).get("description") or "")[:400]})
    return out, None


# ---------------------------------------------------------------- inputs
def short_tab(title):
    for prefix, short in TAB_SHORT:
        if title.startswith(prefix):
            return short
    return title


def _rows_to_companies(tab, values, out):
    if not values:
        return
    hdr = [h.strip().lower() for h in values[0]]
    idx = {k: hdr.index(k) for k in ("account", "domain", "linkedin", "hq", "country", "employees", "industry") if k in hdr}
    if "account" not in idx:
        return
    for v in values[1:]:
        g = lambda k: (v[idx[k]].strip() if k in idx and idx[k] < len(v) else "")
        if not g("account"):
            continue
        out.append({"tab": tab, "account": g("account"), "domain": g("domain").lower(), "linkedin": g("linkedin"),
                    "hq": g("hq"), "country": g("country"), "employees": g("employees"), "industry": g("industry")})


def load_accounts(paths):
    rows = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            head = f.read(1).strip()
            f.seek(0)
            if head in ("{", "["):
                d = json.load(f)
                if isinstance(d, dict) and "sheets" in d:          # spreadsheets.get with grid data
                    for sh in d["sheets"]:
                        tab = short_tab(sh["properties"]["title"])
                        for block in sh.get("data", []):
                            vals = [[c.get("formattedValue", "") for c in rd.get("values", [])] for rd in block.get("rowData", [])]
                            _rows_to_companies(tab, vals, rows)
                elif isinstance(d, dict) and "values" in d:        # values.get
                    tab = short_tab(d.get("range", "").split("!")[0].strip("'"))
                    _rows_to_companies(tab, d["values"], rows)
                elif isinstance(d, dict) and "valueRanges" in d:   # values.batchGet
                    for vr in d["valueRanges"]:
                        _rows_to_companies(short_tab(vr.get("range", "").split("!")[0].strip("'")), vr.get("values", []), rows)
                else:
                    raise ValueError(f"{p}: unrecognized JSON shape")
            else:
                for r in csv.DictReader(f):
                    rows.append({k: (r.get(k) or "").strip() for k in ("tab", "account", "domain", "linkedin", "hq", "country", "employees", "industry")})
                    rows[-1]["domain"] = rows[-1]["domain"].lower()
    seen, out = {}, []
    for r in rows:
        k = r["domain"] or r["account"].lower()
        if k in seen:
            if r["tab"] not in seen[k]["tab"]:
                seen[k]["tab"] += " | " + r["tab"]
            continue
        seen[k] = r
        out.append(r)
    return out


def load_titles():
    titles = []
    with open(TITLES, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("active") or "yes").strip().lower() not in ("yes", "y", "true", "1"):
                continue
            kws = [k.strip().lower() for k in (r.get("match_keywords") or "").split(";") if k.strip()]
            exc = [k.strip().lower() for k in (r.get("exclude_keywords") or "").split(";") if k.strip()]
            if not kws:
                continue
            titles.append({"department": r["department"].strip(), "title": r["title"].strip(),
                           "rx": re.compile(r"(?<![a-z0-9])(" + "|".join(re.escape(k) for k in kws) + r")(?![a-z0-9])"),
                           "exc": exc, "max_staff": int(r["max_staff"]) if (r.get("max_staff") or "").strip() else None,
                           "base": int(r.get("base_score") or 5)})
    return titles


def previous_lists():
    """URLs and company+title pairs already in earlier lists/*.csv."""
    urls, pairs = set(), {}
    if not os.path.isdir(LISTS):
        return urls, pairs
    for fn in sorted(os.listdir(LISTS)):
        if not re.match(r"\d{4}-\d{2}-\d{2}.*\.csv$", fn):
            continue
        with open(os.path.join(LISTS, fn), newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("url"):
                    urls.add(r["url"].split("?")[0])
                pairs.setdefault(((r.get("company") or "").lower(), (r.get("title") or "").strip().lower()), fn[:10])
    return urls, pairs


def last_run_end():
    if not os.path.exists(RUN_LOG):
        return None
    last = None
    with open(RUN_LOG, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("status") == "ok" and r.get("window_end_utc"):
                last = r["window_end_utc"]
    return datetime.fromisoformat(last) if last else None


# ---------------------------------------------------------------- logic
def parse_ts(s):
    if not s:
        return None
    s = s.strip().replace(" ", "T", 1)
    if re.search(r"[+-]\d{2}$", s):
        s += ":00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def staff(c):
    nums = [int(x) for x in re.findall(r"\d+", (c.get("employees") or "").replace(",", ""))]
    return max(nums) if nums else 0


def match_title(title, n_staff, titles):
    t = (title or "").lower()
    for tt in titles:
        if not tt["rx"].search(t) or any(e in t for e in tt["exc"]):
            continue
        if tt["max_staff"] and n_staff and n_staff > tt["max_staff"]:
            return None, f"over {tt['max_staff']} staff for {tt['title']}"
        if re.search(r"\bmanager\b", t) and (not n_staff or n_staff > MANAGER_MAX_STAFF):
            return None, f"manager title at {n_staff or 'unknown'} staff"
        return tt, None
    return None, "not a target title"


def placeability(title, summary):
    t, s = (title or "").lower(), (summary or "").lower()
    if any(k in t for k in KEEP_ALWAYS):
        return None
    if re.search(SENIOR, t) and not re.search(SENIOR_OK, t):
        return "senior level"
    m = re.search(HARD_TITLE, t)
    if m:
        return f"hard to place remotely ({m.group(0)})"
    m = re.search(HARD_SUMMARY, s)
    if m:
        return f"hard to place remotely (posting says {m.group(0)})"
    return None


def job_id(url):
    m = re.search(r"/jobs/view/(?:[^/]*-)?(\d{6,})", url or "")
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--accounts", action="append", required=True)
    ap.add_argument("--since-hours", type=float, help="override the window (default: since the last ok run, else 24h)")
    ap.add_argument("--dry-run", action="store_true", help="write the list to stdout path in /tmp, not lists/, and skip the run log")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    now = datetime.now(timezone.utc).replace(microsecond=0)
    log = {"run_utc": now.isoformat(), "status": "ok", "message": ""}

    def write_log(**kw):
        log.update(kw)
        log["cost_usd"] = f"{_cost['micro'] / 1e6:.2f}"
        if a.dry_run:
            print("RUN LOG (dry run, not written):", json.dumps(log))
            return
        new = not os.path.exists(RUN_LOG)
        with open(RUN_LOG, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=LOG_COLS)
            if new:
                w.writeheader()
            w.writerow({k: log.get(k, "") for k in LOG_COLS})

    if not TOKEN:
        write_log(status="error", message="TREG_TOKEN is not set")
        print("TREG_TOKEN is not set", file=sys.stderr); return 3
    try:
        companies = load_accounts(a.accounts)
    except Exception as e:
        write_log(status="error", message=f"could not read accounts: {e}")
        print(f"could not read accounts: {e}", file=sys.stderr); return 2
    if len(companies) < 100:
        write_log(status="error", message=f"only {len(companies)} accounts loaded; expected the full Living Account List")
        print("too few accounts loaded", file=sys.stderr); return 2
    titles = load_titles()

    start = now - timedelta(hours=a.since_hours) if a.since_hours else (last_run_end() or now - timedelta(hours=24))
    start = max(start, now - timedelta(days=MAX_WINDOW_DAYS))
    days = min(MAX_WINDOW_DAYS, math.ceil((now - start).total_seconds() / 86400) + 1)
    log.update(window_start_utc=start.isoformat(), window_end_utc=now.isoformat(), companies=len(companies))

    try:
        bal_before = treg_balance()
    except AuthError as e:
        write_log(status="auth_error", message=str(e)[:300])
        print(f"treg auth failed: {e}", file=sys.stderr); return 3

    with_li = [c for c in companies if "linkedin.com/company" in c["linkedin"]]
    without = [c for c in companies if c not in with_li]
    raw, errors = [], []
    try:
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            futs = [ex.submit(pull_blitz, c, days) for c in with_li]
            for fut in as_completed(futs):
                comp, jobs, err = fut.result()
                if err:
                    errors.append(f"{comp['account']}: {err}")
                for j in jobs:
                    j["_company"] = comp
                    raw.append(j)
        cj, err = pull_crustdata(without, start)
        if err:
            errors.append(err)
        raw.extend(cj)
    except AuthError as e:
        write_log(status="auth_error", message=str(e)[:300], pages_pulled=len(with_li))
        print(f"treg auth failed: {e}", file=sys.stderr); return 3
    log.update(pages_pulled=len(with_li), pull_errors=len(errors))
    if with_li and len(errors) > len(with_li) * 0.2:
        write_log(status="error", message=f"{len(errors)} pull errors, e.g. {errors[0][:200]}")
        print("too many pull errors", file=sys.stderr); return 4

    prev_urls, prev_pairs = previous_lists()
    in_window, matched, kept_rows, seen = 0, 0, [], set()
    for j in raw:
        dt = parse_ts(j.get("date_posted"))
        if not dt or dt < start or dt > now + timedelta(hours=1):
            continue
        url = (j.get("url") or "").split("?")[0]
        if url in seen:
            continue
        seen.add(url)
        in_window += 1
        c = j["_company"]
        n_staff = staff(c)
        tt, _why = match_title(j.get("title"), n_staff, titles)
        if not tt:
            continue
        matched += 1
        if placeability(j.get("title"), j.get("ai_summary")):
            continue
        if url and url in prev_urls:
            continue
        loc = j.get("location") or {}
        country = (loc.get("country_code") or "").upper()
        notes, score = [], tt["base"]
        if n_staff > LARGE_COMPANY:
            notes.append(f"large company ({n_staff} staff)")
        else:
            score += 1
        competitor = c["account"].lower() in COMPETITORS
        if competitor:
            notes.append("outsourcing competitor: skip")
        if country in LOWCOST:
            notes.append("already hiring in a lower-cost country")
        if "remote" in (j.get("title") or "").lower() or "remote" in (j.get("ai_summary") or "").lower():
            score += 1
        prev = prev_pairs.get((c["account"].lower(), (j.get("title") or "").strip().lower()))
        if prev:
            notes.append(f"same role listed {prev}")
            score -= 1
        kept_rows.append({
            "posted_et": dt.astimezone(ET).strftime("%Y-%m-%d %H:%M"),
            "hours_ago": round((now - dt).total_seconds() / 3600, 1),
            "tab": c["tab"], "company": c["account"], "domain": c["domain"], "employees": c["employees"],
            "hq_country": c["country"], "title": (j.get("title") or "").strip(), "category": tt["department"],
            "job_city": loc.get("city") or "", "job_country": loc.get("country_code") or "", "url": j.get("url") or "",
            "source": j.get("_src"), "job_id": job_id(j.get("url")), "note": "; ".join(notes),
            "ai_summary": (j.get("ai_summary") or "").replace("\n", " ").strip(),
            "department": tt["department"], "matched_title": tt["title"], "ease_score": 1 if competitor else max(1, min(10, score))})

    counts = {}
    for r in kept_rows:
        k = (r["company"], r["title"].lower())
        counts[k] = counts.get(k, 0) + 1
    for r in kept_rows:
        r["same_role_posted_in_n_locations"] = counts[(r["company"], r["title"].lower())]
    kept_rows.sort(key=lambda r: (-int(r["ease_score"]), r["note"] != "", r["company"], r["posted_et"]))
    log.update(postings_in_window=in_window, title_matches=matched, kept=len(kept_rows), new_rows=len(kept_rows))

    list_file = ""
    if kept_rows:
        date = now.astimezone(PRISHTINA).strftime("%Y-%m-%d")
        path = os.path.join("/tmp" if a.dry_run else LISTS, f"{date}.csv")
        exists = os.path.exists(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a" if exists else "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=LIST_COLS, extrasaction="ignore")
            if not exists:
                w.writeheader()
            w.writerows(kept_rows)
        list_file = os.path.relpath(path, REPO) if not a.dry_run else path

    bal = None
    try:
        bal = treg_balance()
    except AuthError:
        pass
    msg = []
    if errors:
        msg.append(f"{len(errors)} pull errors")
    if bal is not None and bal < LOW_BALANCE_USD:
        msg.append(f"LOW TREG BALANCE ${bal:.2f}: top up")
    if not kept_rows:
        msg.append("no new matching postings; no list file written")
    write_log(list_file=list_file, balance_usd=f"{bal:.2f}" if bal is not None else "", message="; ".join(msg))

    companies_n = len({r["company"] for r in kept_rows})
    print(json.dumps({"status": "ok", "list_file": list_file, "companies": companies_n, "rows": len(kept_rows),
                      "window_start_utc": start.isoformat(), "window_end_utc": now.isoformat(),
                      "postings_in_window": in_window, "title_matches": matched, "pull_errors": len(errors),
                      "cost_usd": round(_cost["micro"] / 1e6, 2), "balance_usd": bal}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
