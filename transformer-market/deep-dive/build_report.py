"""Render a deep-dive synthesis JSON into the markdown report.

Usage: python3 -I build_report.py <synthesis.json> <out.md> <as_of>
"""
import json
import sys


def cell(text):
    return str(text if text is not None else "").replace("|", "\\|").replace("\n", " ")


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def main(src, dst, as_of):
    s = json.load(open(src))
    md = [f"# North American Transformer Market: Deep Dive ({as_of})", ""]
    md += [
        "*Two rounds of multi-agent research on government data, permits, incentive filings, dockets, company filings, "
        "trade statistics and utility procurement, with independent checks of the key claims. "
        "Confidence tags: P primary, S secondary, W weak. Bracketed ids point to findings in `findings.json`.*",
        "",
        "## Answer",
        "",
        s["executive_summary"],
        "",
    ]
    if s.get("what_changed_from_round1"):
        md += ["## What changed after the second research round", ""]
        md += ["- " + x for x in s["what_changed_from_round1"]] + [""]
    md += ["## Thesis scorecard", ""]
    md += [table(["Question", "Answer", "Confidence", "Key evidence"],
                 [[q["question"], q["answer"], q["confidence"], "; ".join(q["key_evidence"])] for q in s["thesis_scorecard"]]), ""]
    md += ["## Segments ranked for a new builder", ""]
    md += [table(["Segment", "Attractiveness", "Why"],
                 [[x["segment"], x["attractiveness"], x["why"]] for x in s["segment_ranking"]]), ""]
    md += ["## Supply and demand balance", "", s["supply_demand_balance"], ""]
    if s.get("plant_status"):
        md += ["## Plant status check", ""]
        md += [table(["Plant", "Announced online", "Verdict", "Evidence", "Source"],
                     [[p["plant"], p.get("announced_online", ""), p["verdict"], p["evidence_status"], p.get("source", "")]
                      for p in s["plant_status"]]), ""]
    if s.get("price_points"):
        md += ["## Buyer-level price and lead-time datapoints", ""]
        md += [table(["Date", "Buyer", "Item", "Vendor", "Unit price", "Lead time", "Source"],
                     [[p["date"], p["buyer"], p["item"], p.get("vendor", ""), p.get("unit_price", ""), p.get("lead_time", ""), p["source"]]
                      for p in s["price_points"]]), ""]
    for sec in s["sections"]:
        title = sec["title"]
        md += ["## " + title.split(". ", 1)[-1] if title[:2].strip(". ").isdigit() else "## " + title, "", sec["markdown"], ""]
    md += ["## Implications", ""]
    md += [f"- **{x['stance']}: {x['heading']}.** {x['body']}" for x in s["revised_implications"]] + [""]
    md += ["## Watchlist", ""]
    md += [table(["When", "What", "Why"], [[w["when"], w["item"], w["why"]] for w in s["watch_items"]]), ""]
    md += ["## Open questions", ""] + ["- " + q for q in s["open_questions"]] + [""]
    md += ["## Data coverage", ""]
    md += [table(["Source", "Status", "Takeaway"],
                 [[d["source"], d["status"].replace("_", " "), d["takeaway"]] for d in s["data_inventory"]]), ""]
    md += [
        "## Method and limits",
        "",
        "- Research agents could only read pages through web search. This environment's network policy blocks direct "
        "access to census.gov, bls.gov, sec.gov, regulations.gov and state permit portals, so long PDFs and data "
        "tables were read through search summaries.",
        "- Web search is capped at 200 calls per turn across all agents. The first round ran out early, so a second "
        "round re-ran the domains that had no data, with fixed allowances per agent.",
        "- Plant online dates are company guidance unless the plant-status table cites a permit or incentive record.",
        "",
    ]
    open(dst, "w").write("\n".join(md))


if __name__ == "__main__":
    main(*sys.argv[1:4])
