"""Build the dashboard's value-chain, Fulton and glossary datasets, plus readable markdown copies.

Usage: python3 -I build_value_chain.py <workflow_result.json> <out_dir> <markdown_dir>
Reads the research workflow's result (network, glossary, fulton_research, fulton_plan) and writes
value_chain_nodes, value_chain_edges, glossary, fulton_plan, fulton_portfolio and fulton_plays JSON
files to out_dir, and value-chain.md, fulton-summary.md and glossary.md to markdown_dir.
"""
import json
import os
import re
import sys
from urllib.parse import urlparse

LAYERS = ["S3", "S2", "S1", "B", "C1", "C2", "C3"]
LAYER_TITLES = {"S3": "Raw materials", "S2": "Processed materials", "S1": "Parts and services", "B": "Transformer builders",
                "C1": "Direct buyers", "C2": "Their customers", "C3": "End demand"}
ID_BRACKETS = re.compile(r"\s*\[(?:[a-z0-9]+(?:-[a-z0-9]+)+)(?:,\s*[a-z0-9]+(?:-[a-z0-9]+)*)*(?:,\s*[PSW](?:/[PSW])?)?\]")
IMPACT_RANK = {"High": 0, "Medium": 1, "Low": 2, "None": 3}
# Glossary aliases that would underline ordinary words or the wrong thing, and terms not worth a definition.
DROP_ALIASES = {"EO", "CT", "CC", "shelter", "fluids", "Wesco", "Irby", "Border States", "Annex readings", "Baseline P", "Baseline S",
                "tagged W", "W-grade", "W summary", "Municipal", "municipal", "Reclamation", "EDGE", "ACA", "MDA", "EDO", "breaker", "breakers"}
DROP_TERMS = {"computed"}


def clean(text):
    t = str(text or "").replace("**", "")
    t = ID_BRACKETS.sub("", t)
    t = re.sub(r"(^|\n)\s*-\s+", r"\1• ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def https(u):
    u = str(u or "").strip()
    return u if u.startswith("https://") else ""


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")[:48]


def source_label(url):
    host = urlparse(url).netloc.replace("www.", "")
    path = [p for p in urlparse(url).path.split("/") if p]
    tail = re.sub(r"[-_]+", " ", path[-1]) if path else ""
    tail = re.sub(r"\.(html?|php|aspx)$", "", tail)
    tail = re.sub(r"\b[0-9a-f]{8,}\b|\b\d{6,}\b", "", tail).strip()
    return host + (": " + tail[:70] if tail and not tail.isdigit() else "")


def write(out, name, rows):
    with open(os.path.join(out, name), "w") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print(name, len(rows))


def md_cell(x):
    return str(x if x is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def main(src, out, md_dir):
    r = json.load(open(src))
    net = r["network"]
    groups = net.get("builder_groups") or []

    # ---------- nodes ----------
    nodes, seen = [], set()
    for n in net["nodes"]:
        if n["id"] in seen or n["layer"] not in LAYERS:
            continue
        seen.add(n["id"])
        g = n.get("group") or ""
        nodes.append(dict(
            id=n["id"], name=n["name"].strip(), layer=n["layer"], layer_title=LAYER_TITLES[n["layer"]], group=g,
            group_order=groups.index(g) if n["layer"] == "B" and g in groups else None,
            kind=n.get("kind", "company"), description=clean(n.get("description")), size_label=clean(n.get("size_label")),
            ownership=clean(n.get("ownership")), source_url=https(n.get("source_url"))))
    ids = {n["id"] for n in nodes}

    # ---------- edges ----------
    edges, eids = [], set()
    for i, e in enumerate(net["edges"]):
        if e["source"] not in ids or e["target"] not in ids or e["source"] == e["target"]:
            continue
        eid = e.get("id") or f"e{i:03d}"
        while eid in eids:
            eid += "x"
        eids.add(eid)
        lo, hi = e.get("value_low_usd_m"), e.get("value_high_usd_m")
        edges.append(dict(
            id=eid, source=e["source"], target=e["target"], product=clean(e["product"]),
            value_low_usd_m=lo, value_high_usd_m=hi, value_label=clean(e.get("value_label")),
            estimated="Yes" if e.get("estimated", True) else "No", kind=e.get("kind", "flow"),
            basis=clean(e.get("basis")), source_url=https(e.get("source_url"))))
    used = {e["source"] for e in edges} | {e["target"] for e in edges}
    dropped = [n["id"] for n in nodes if n["id"] not in used]
    nodes = [n for n in nodes if n["id"] in used]
    if dropped:
        print("dropped unconnected nodes:", dropped)
    write(out, "value_chain_nodes.json", nodes)
    write(out, "value_chain_edges.json", edges)

    # ---------- glossary (research terms, then the hand-written extras in glossary_extra.json) ----------
    extra_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "glossary_extra.json")
    extra = json.load(open(extra_path)) if os.path.exists(extra_path) else []
    gl, gids, taken = [], set(), set()
    for t in list(r["glossary"]["terms"]) + extra:
        gid = slug(t.get("id") or t["term"])
        if gid in gids or gid in DROP_TERMS:
            continue
        gids.add(gid)
        aliases = []
        for a in [t["term"].split(" (")[0]] + list(t.get("aliases") or []):
            a = str(a).strip()
            key = a if t.get("case_sensitive") else a.lower()
            if len(a) > 1 and a not in aliases and a not in DROP_ALIASES and key not in taken:
                aliases.append(a)
                taken.add(key)
        gl.append(dict(id=gid, term=t["term"].strip(), aliases=" | ".join(aliases), case_sensitive=bool(t.get("case_sensitive")),
                       category=t["category"], definition=clean(t["definition"])))
    gl.sort(key=lambda x: x["term"].lower())
    write(out, "glossary.json", gl)

    # ---------- Fulton ----------
    plan, fr = r["fulton_plan"], r.get("fulton_research") or {}
    firm = fr.get("firm") or {}
    rows = [dict(id="headline", kind="headline", order=0, heading="Headline", body=clean(plan["headline"]), url=""),
            dict(id="summary", kind="summary", order=1, heading="Our recommendation", body=clean(plan["summary"]), url=""),
            dict(id="fit", kind="fit", order=2, heading="Fit with Fulton's style", body=clean(plan["fit_with_style"]), url=""),
            dict(id="firm", kind="firm", order=3, heading="Fulton at a glance", body=clean(firm.get("summary")), url="")]
    k = 10
    for i, u in enumerate(firm.get("sources") or []):
        if https(u):
            rows.append(dict(id=f"src{i:02d}", kind="source", order=k, heading=source_label(u), body="", url=https(u)))
            k += 1
    for i, x in enumerate(plan["next_90_days"]):
        rows.append(dict(id=f"next{i:02d}", kind="next", order=100 + i, heading=f"Step {i + 1}", body=clean(x), url=""))
    for i, x in enumerate(plan["triggers"]):
        rows.append(dict(id=f"trig{i:02d}", kind="trigger", order=200 + i, heading=clean(x["signal"]), body=clean(x["meaning"]), url=""))
    for i, x in enumerate(plan["avoid"]):
        rows.append(dict(id=f"avoid{i:02d}", kind="avoid", order=300 + i, heading="Avoid", body=clean(x), url=""))
    rows.append(dict(id="caveats", kind="caveat", order=400, heading="Caveats", body=clean(plan["caveats"]), url=""))
    write(out, "fulton_plan.json", rows)

    research_port = fr.get("portfolio") or []

    def port_url(company):
        key = company.lower().split(" (")[0][:14]
        for p in research_port:
            if p["company"].lower().startswith(key) or key in p["company"].lower():
                return https(p.get("source_url"))
        return ""

    port = []
    for i, p in enumerate(plan["portfolio_exposure"]):
        port.append(dict(id=f"p{i:02d}-{slug(p['company'])[:24]}", company=p["company"], what_it_does=clean(p["what_it_does"]),
                         link_to_trend=clean(p["link_to_trend"]), impact=p["impact"], impact_rank=IMPACT_RANK.get(p["impact"], 4),
                         action=clean(p["action"]), confidence=p.get("confidence", ""), source_url=port_url(p["company"])))
    write(out, "fulton_portfolio.json", port)
    plays = []
    for p in sorted(plan["plays"], key=lambda x: x["rank"]):
        plays.append(dict(id=f"play{p['rank']:02d}", rank=p["rank"], play=clean(p["play"]), chain_position=clean(p["chain_position"]),
                          why_fulton=clean(p["why_fulton"]), how=clean(p["how"]), check_size=clean(p["check_size"]),
                          example_targets=clean(p.get("example_targets")), timing=clean(p.get("timing")), risks=clean(p["risks"]),
                          conviction=p["conviction"]))
    write(out, "fulton_plays.json", plays)

    # ---------- markdown copies ----------
    os.makedirs(md_dir, exist_ok=True)
    name = {n["id"]: n["name"] for n in nodes}
    L = ["# NA transformer value chain", "",
         "Seller → buyer flows three layers up and down from the transformer builders. Values are annual US$; most are estimates (basis given). "
         "Dashed Fulton rows are addressable markets, not current sales.", ""]
    for lay in LAYERS:
        L += [f"## {LAYER_TITLES[lay]} ({lay})", "", "| Company | Group | Kind | Size | Description |", "|---|---|---|---|---|"]
        for n in [n for n in nodes if n["layer"] == lay]:
            L.append(f"| {md_cell(n['name'])} | {md_cell(n['group'])} | {n['kind']} | {md_cell(n['size_label'])} | {md_cell(n['description'])} |")
        L.append("")
    L += ["## Flows", "", "| Seller | Buyer | Product | Annual value | Est. | Kind | Basis | Source |", "|---|---|---|---|---|---|---|---|"]
    for e in edges:
        src = f"[link]({e['source_url']})" if e["source_url"] else ""
        L.append(f"| {md_cell(name[e['source']])} | {md_cell(name[e['target']])} | {md_cell(e['product'])} | {md_cell(e['value_label'])} | "
                 f"{e['estimated']} | {e['kind']} | {md_cell(e['basis'])} | {src} |")
    if net.get("notes"):
        L += ["", "## Assembly notes", "", clean(net["notes"])]
    open(os.path.join(md_dir, "value-chain.md"), "w").write("\n".join(L) + "\n")

    F = ["# The transformer build-out: what it means for Fulton Asset Management", "", f"**{clean(plan['headline'])}**", "",
         clean(plan["summary"]), "", "## Why this fits how Fulton invests", "", clean(plan["fit_with_style"]), "",
         "## Fulton at a glance", "", clean(firm.get("summary")), "", clean(firm.get("style")), "",
         "## Plays across the value chain, ranked", ""]
    for p in plays:
        F += [f"### {p['rank']}. {p['play']}", "", f"*{p['chain_position']} · conviction {p['conviction']}*", "",
              f"- **Why Fulton:** {p['why_fulton']}", f"- **How:** {p['how']}", f"- **Check size:** {p['check_size']}",
              f"- **Targets:** {p['example_targets']}", f"- **Timing:** {p['timing']}", f"- **Risks:** {p['risks']}", ""]
    F += ["## Portfolio exposure", "", "| Company | Exposure | Link to the build-out | Next step | Tag |", "|---|---|---|---|---|"]
    for p in sorted(port, key=lambda x: x["impact_rank"]):
        F.append(f"| {md_cell(p['company'])} | {p['impact']} | {md_cell(p['link_to_trend'])} | {md_cell(p['action'])} | {p['confidence']} |")
    F += ["", "## Next ninety days", ""] + [f"{i + 1}. {clean(x)}" for i, x in enumerate(plan["next_90_days"])]
    F += ["", "## Signals that would change the plan", ""] + [f"- **{clean(x['signal'])}:** {clean(x['meaning'])}" for x in plan["triggers"]]
    F += ["", "## What to avoid", ""] + [f"- {clean(x)}" for x in plan["avoid"]]
    F += ["", "## Caveats", "", clean(plan["caveats"]), "", "## Sources on Fulton", ""]
    F += [f"- [{source_label(u)}]({u})" for u in firm.get("sources") or [] if https(u)]
    open(os.path.join(md_dir, "fulton-summary.md"), "w").write("\n".join(F) + "\n")

    G = ["# Glossary", "", "| Term | Category | Definition |", "|---|---|---|"]
    G += [f"| {md_cell(t['term'])} | {t['category']} | {md_cell(t['definition'])} |" for t in gl]
    open(os.path.join(md_dir, "glossary.md"), "w").write("\n".join(G) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:4])
