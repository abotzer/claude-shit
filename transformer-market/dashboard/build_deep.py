"""Build the dashboard's deep-dive datasets from the deep-dive synthesis.

Usage: python3 -I build_deep.py <round2_synthesis.json> <round2_research.json> <out_dir>
Writes deep_segments, deep_scorecard, plant_status, price_points, margins,
demand_units, ppi_monthly, takeaways and watchlist JSON files.
"""
import json
import os
import re
import sys

ID_BRACKETS = re.compile(r"\s*\[(?:[a-z0-9]+(?:-[a-z0-9]+)+)(?:,\s*[a-z0-9]+(?:-[a-z0-9]+)*)*(?:,\s*[PSW](?:/[PSW])?)?\]")


def clean(text):
    """Markdown-ish synthesis text -> plain text with bullet lines (rendered with white-space: pre-line)."""
    t = str(text or "").replace("**", "")
    t = ID_BRACKETS.sub("", t)
    t = re.sub(r"(^|\n)\s*-\s+", r"\1• ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def slug(text, i):
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")[:40]
    return f"{i:02d}-{s}"


def main(syn_path, research_path, out):
    s = json.load(open(syn_path))
    research = {d["key"]: d["result"] for d in json.load(open(research_path))["domains"]}

    def w(name, rows):
        with open(os.path.join(out, name), "w") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
        print(name, len(rows))

    rank = {"high": 0, "medium": 1, "low": 2}
    w("deep_segments.json", [
        dict(id=slug(x["segment"], i), order=i, segment=x["segment"], attractiveness=x["attractiveness"].capitalize(),
             rank=rank[x["attractiveness"]], why=clean(x["why"]))
        for i, x in enumerate(s["segment_ranking"])
    ])
    w("deep_scorecard.json", [
        dict(id=slug(q["question"], i), order=i, question=q["question"], answer=clean(q["answer"]), confidence=q["confidence"].capitalize())
        for i, q in enumerate(s["thesis_scorecard"])
    ])

    verdict_label = {"on_track": "On track", "operating": "Operating", "slipped": "Slipped", "at_risk": "At risk",
                     "cancelled": "Cancelled", "unverified": "Unverified"}
    w("plant_status.json", [
        dict(id=slug(p["plant"], i), plant=p["plant"], announced_online=p.get("announced_online", ""),
             verdict=p["verdict"], verdict_label=verdict_label[p["verdict"]], evidence=clean(p["evidence_status"]),
             source_url=p.get("source", "") if str(p.get("source", "")).startswith("https://") else "")
        for i, p in enumerate(s["plant_status"])
    ])

    def src_url(x):
        m = re.search(r"https://\S+", str(x))
        return m.group(0).rstrip(").,;") if m else ""

    w("price_points.json", [
        dict(id=f"pp{i:02d}", date=p["date"], buyer=p["buyer"], item=p["item"], vendor=p.get("vendor", ""),
             unit_price=p.get("unit_price", ""), lead_time=p.get("lead_time", ""), source_url=src_url(p.get("source", "")),
             source=p.get("source", ""))
        for i, p in enumerate(s["price_points"])
    ])

    # Margins now vs a year ago (EBITDA or operating), from the filings research table.
    margins = [
        dict(id="forgent", company="Forgent Power Solutions", period="Q4 FY26 (Jun 2026)", metric="Adj. EBITDA", now_pct=24.4, prior_pct=18.0,
             gross="FY26 ~35.1% (computed) vs ~36.9%", note="Revenue +94% in Q4; backlog $3.0B; book-to-bill 3.3x", confidence="P",
             source_url="https://www.sec.gov/"),
        dict(id="hdhe", company="HD Hyundai Electric", period="Q2 2026", metric="Operating", now_pct=25.1, prior_pct=23.1,
             gross="n/a", note="North America revenue +10%; gain from price and mix", confidence="S", source_url="https://www.mt.co.kr/"),
        dict(id="hubbell", company="Hubbell Utility Solutions", period="Q2 2026", metric="Adj. operating", now_pct=25.6, prior_pct=25.5,
             gross="n/a", note="Low-single-digit price; inflation and tariffs offset", confidence="P", source_url="https://www.sec.gov/"),
        dict(id="gev", company="GE Vernova Electrification", period="Q2 2026", metric="Segment EBITDA", now_pct=18.4, prior_pct=14.5,
             gross="n/a", note="+700 bp organic; includes Prolec from Feb 2", confidence="P",
             source_url="https://www.sec.gov/Archives/edgar/data/1996810/000199681026000147/gevpressrelease2q26.htm"),
        dict(id="hammond", company="Hammond Power Solutions", period="Q2 2026", metric="Adj. EBITDA", now_pct=16.4, prior_pct=14.9,
             gross="31.5% (flat)", note="Backlog -6.9% QoQ; Canada pricing competitive", confidence="P", source_url="https://tedmag.com/hammond-power-solutions-reports-2q-2026-results/"),
        dict(id="hyosung", company="Hyosung Heavy Industries", period="Q2 2026", metric="Operating (consolidated)", now_pct=15.7, prior_pct=10.8,
             gross="n/a", note="Higher-margin US EHV transformer and breaker sales", confidence="S", source_url="https://www.bloter.net/"),
    ]
    w("margins.json", margins)

    demand_rows = []
    for t in research.get("demand_counts", {}).get("tables", []):
        if t["title"].startswith("Demand drivers converted"):
            for i, r in enumerate(t["rows"]):
                driver, qty, units, timing, src = (r + [""] * 5)[:5]
                demand_rows.append(dict(id=f"d{i:02d}", driver=driver, quantity=qty, units_implied=units, timing=timing,
                                        source_url=src if src.startswith("https://") else ""))
    w("demand_units.json", demand_rows)

    ppi = []
    for m, v in [("2025-06", 350.532), ("2025-07", 351.192), ("2025-08", 351.192), ("2025-09", 351.192), ("2026-01", 362.638),
                 ("2026-02", 362.638), ("2026-03", 362.638), ("2026-04", 364.861), ("2026-05", 364.861), ("2026-06", 364.861), ("2026-07", 381.783)]:
        ppi.append(dict(month=m, series="Power and distribution transformers (WPU117409)", value=v,
                        source_url="https://fred.stlouisfed.org/series/WPU117409"))
    for m, v in [("2025-05", 438.942), ("2025-06", 438.942), ("2025-07", 440.550), ("2025-08", 440.550), ("2025-09", 440.550), ("2025-10", 458.356),
                 ("2026-04", 454.338), ("2026-05", 456.602), ("2026-06", 456.602), ("2026-07", 474.831), ("2026-08", 475.065)]:
        ppi.append(dict(month=m, series="Transformer manufacturing (PCU335311)", value=v,
                        source_url="https://fred.stlouisfed.org/series/PCU335311335311"))
    w("ppi_monthly.json", ppi)

    take = [dict(id="headline", order=0, kind="headline", stance="Neutral", heading="Headline",
                 body="Build, but aim one size class up: 10-60 MVA substation transformers with 69-138 kV primaries, entered by buying or converting a plant that already has a test bay, with 3-phase pad-mounts as the fast first product. Commit after DOE's EO 14421 rules (around Dec 24) and the Q3 margin reports.")]
    for i, x in enumerate(s["revised_implications"], start=1):
        take.append(dict(id=slug(x["heading"], i), order=i, kind="implication", stance=x["stance"], heading=x["heading"], body=clean(x["body"])))
    n = len(take)
    take.append(dict(id="bottom_line", order=n, kind="bottom_line", stance="Neutral", heading="Bottom line",
                     body="The shortage is real but splitting by segment. Substation and power units still quote about 130 weeks and carry rising margins; pad-mounts are filling fast with new US, Chinese-owned and Korean supply, and get no protection from the EO. A newcomer wins by owning a qualified 69-138 kV line by 2028, buying cores from two suppliers, siting away from the Southeast hiring wave, and walking away if DOE's rules, bid lead times or margins break the thresholds in the deep dive."))
    caveats = [
        ("cav_sources", "How the numbers were gathered", "Two rounds of multi-agent research read government, permit, filing, docket and procurement sources through web search; direct access to those sites is blocked here. Each figure links to its source and carries a P, S or W tag."),
        ("cav_conflicts", "Where sources disagree", "The duty on imported cores reads as 25% or 50% depending on the annex reading. The >100 MVA import counts come from a vendor compilation that could not be verified. Korea's Jan-Jul 2026 export figure has one source."),
        ("cav_gaps", "What is still missing", "Census HS-10 import units by country, QCEW plant employment, and any state permit record: permit portals are not indexed by search, so plant dates rest on groundbreakings, incentive filings and job postings."),
    ]
    for j, (cid, h, b) in enumerate(caveats):
        take.append(dict(id=cid, order=n + 1 + j, kind="caveat", stance="Neutral", heading=h, body=b))
    w("takeaways.json", take)

    sort_dates = ["2026-10-15", "2026-10-12", "2026-10-18", "2026-10-19", "2026-10-20", "2026-10-21", "2026-10-25", "2026-10-28",
                  "2026-11-05", "2026-11-06", "2026-11-15", "2026-11-16", "2026-11-24", "2026-12-01", "2026-12-10", "2026-12-20",
                  "2026-12-24", "2026-12-31", "2027-02-22", "2027-02-15", "2027-04-15", "2027-06-30", "2027-07-15", "2027-08-31",
                  "2027-12-31", "2028-06-30", "2028-07-01", "2029-06-30"]
    watch = s["watch_items"]
    assert len(watch) == len(sort_dates), (len(watch), len(sort_dates))
    w("watchlist.json", [
        dict(id=f"w{i:02d}", sort_date=sort_dates[i], when=x["when"], item=clean(x["item"]), why=clean(x["why"]))
        for i, x in enumerate(watch)
    ])


if __name__ == "__main__":
    main(*sys.argv[1:4])
