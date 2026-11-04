#!/usr/bin/env python3
"""Mallangable-AI Design Space Calculator

Enumerates every combination of the 11 design axes and filters them with 3 kinds of constraints.
  - L (logical)   : combinations that cannot hold logically or contractually, or redundant encodings of the same meaning (normalization)
  - N (normative) : combinations that can hold but are forbidden by Mallangable-AI norms (safety principles)
  - S (soft)      : combinations that are allowed but not recommended (warnings)

Usage:
  python3 tools/design_space.py            # summary (JSON)
  python3 tools/design_space.py --markdown # tables for the docs
  python3 tools/design_space.py --check P1  # check a reference profile
  python3 tools/design_space.py --profile '{"A1":"D3", ...}'  # check an arbitrary combination
  python3 tools/design_space.py --profile my-profile.json     # check from a file (commit it to a design review or ADR)

Change the axes or constraints to recompute the design space for your own product.
Uses the standard library only.
"""
import argparse
import collections
import itertools
import json
import os
import sys

AXES = collections.OrderedDict([
    ("A1", ("Maximum change depth", ["D1", "D2", "D3", "D4", "D5"])),
    ("A2", ("Artifact representation", ["decl", "sandboxed", "native"])),
    ("A3", ("Agent location", ["client", "server", "hybrid"])),
    ("A4", ("Execution isolation", ["none", "lang", "frame", "proc"])),
    ("A5", ("Code visibility", ["open", "own", "hidden"])),
    ("A6", ("Version topology", ["snapshot", "fork", "lineage", "crdt"])),
    ("A7", ("Baseline propagation", ["none", "manual", "proposed", "auto"])),
    ("A8", ("Sharing scope", ["none", "tenant", "public"])),
    ("A9", ("Model sourcing", ["sub", "byok", "credits", "tenant_cloud", "on_device"])),
    ("A10", ("Management visibility", ["none", "V0", "V1", "V2", "V3"])),
    ("A11", ("Activation mode", ["live", "preview", "gated"])),
])
STRUCTURAL = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"]
ECONOMIC = ["A9", "A10", "A11"]
DEPTH_RANK = {"D1": 1, "D2": 2, "D3": 3, "D4": 4, "D5": 5}


# Logical constraints. Order defines the 'first violation' counts, so do not reorder (--independent is order-free).
LOGICAL_RULES = [
    ("L1", lambda c: c["A5"] == "hidden" and c["A3"] != "server"),  # if the agent that touches code runs on the user's side, code cannot be hidden
    ("L2", lambda c: c["A9"] in ("sub", "on_device") and c["A3"] == "server"),  # personal subscriptions and on-device models cannot serve server jobs (terms of service, physical location)
    ("L3", lambda c: c["A1"] in ("D1", "D2", "D3") and c["A2"] != "decl"),  # 2.6: D1~D3 are declarative. A code artifact means D4 or higher
    ("L4", lambda c: (c["A1"] == "D4" and c["A2"] != "sandboxed")  # 2.6: D4 is sandboxed code
                     or (c["A1"] == "D5" and c["A2"] != "native")),  # a core change is a native code modification
    ("L5", lambda c: c["A2"] == "decl" and c["A4"] != "none"),  # normalization: without executable code the execution isolation axis is meaningless
    ("L6", lambda c: c["A2"] == "sandboxed" and c["A4"] == "none"),  # a sandboxed artifact needs a sandbox
    ("L7", lambda c: c["A2"] == "native" and c["A4"] in ("lang", "frame")),  # native code cannot hold 'host privileges' inside language or frame isolation
    ("L8", lambda c: c["A6"] == "snapshot" and c["A7"] != "none"),  # without tracking the relation to a baseline there is nothing to propagate
    ("L9", lambda c: c["A6"] == "crdt" and c["A7"] == "manual"),  # CRDT merges automatically, so there is no manual merge step
    ("L10", lambda c: c["A5"] == "own" and c["A6"] not in ("fork", "lineage")),  # 'see only my own' holds only in topologies with separated layers
    ("L11", lambda c: c["A5"] == "hidden" and c["A6"] == "crdt"),  # CRDT replicas live on the client, so code cannot be hidden
]


def logical_all(c):
    return [r for r, f in LOGICAL_RULES if f(c)]


def logical(c):
    """Logical constraints. Returns the id of the first violated rule (None if none)."""
    return next((r for r, f in LOGICAL_RULES if f(c)), None)


def normative(c):
    """Normative constraints (Mallangable-AI safety principles)."""
    code = c["A2"] != "decl"
    if code and c["A8"] == "public" and c["A4"] not in ("frame", "proc"):
        return "N1"  # publicly shared executable code requires frame or process isolation
    if c["A2"] == "native" and c["A8"] != "none" and c["A4"] != "proc":
        return "N2"  # shared native code requires a separate process
    if c["A9"] == "credits" and c["A10"] == "none":
        return "N3"  # resale billing requires metering (at least V0)
    if c["A8"] == "public" and c["A10"] == "none":
        return "N4"  # a public market requires an audit trail
    if DEPTH_RANK[c["A1"]] >= 4 and c["A11"] == "live":
        return "N5"  # behavior and core changes must not activate immediately without preview or approval
    if c["A1"] == "D5" and (c["A8"] != "none" or c["A6"] == "snapshot"):
        return "N6"  # D5 is a core fork, not a user layer (I1, 2.6): no sharing, baseline tracking required
    return None


def soft(c):
    """Combinations that are not recommended (list of warnings)."""
    w = []
    code = c["A2"] != "decl"
    if code and c["A8"] == "public" and c["A11"] == "live":
        w.append("S1")  # immediate install of publicly shared code
    if c["A2"] == "native" and c["A4"] == "none":
        w.append("S2")  # native code without isolation (recommended for personal use only)
    if c["A6"] == "lineage" and c["A7"] in ("none", "manual"):
        w.append("S3")  # lineage exists but no propagation assistance, so drift accumulates
    if c["A1"] == "D5" and c["A6"] in ("fork", "lineage"):
        w.append("S4")  # per-user core forks make merge cost explode
    if c["A3"] == "hybrid" and c["A9"] == "sub":
        w.append("S5")  # no LLM at the server stage, so semantic conflicts are sent back to the client
    if c["A9"] == "on_device" and DEPTH_RANK[c["A1"]] >= 4:
        w.append("S6")  # generating behavior code with an on-device model raises the failure rate
    if c["A6"] == "crdt" and DEPTH_RANK[c["A1"]] >= 4:
        w.append("S7")  # concurrent editing of executable code in a real-time synced document
    return w


PROFILES = {
    "P1": ("Personal workshop", {"A1": "D4", "A2": "sandboxed", "A3": "client", "A4": "frame", "A5": "open",
                         "A6": "fork", "A7": "proposed", "A8": "none", "A9": "sub", "A10": "none", "A11": "preview"}),
    "P2": ("Team-curated", {"A1": "D3", "A2": "decl", "A3": "hybrid", "A4": "none", "A5": "own",
                          "A6": "lineage", "A7": "proposed", "A8": "tenant", "A9": "byok", "A10": "V2", "A11": "preview"}),
    "P3": ("Enterprise confidential", {"A1": "D4", "A2": "sandboxed", "A3": "server", "A4": "proc", "A5": "hidden",
                         "A6": "lineage", "A7": "proposed", "A8": "tenant", "A9": "tenant_cloud", "A10": "V2", "A11": "gated"}),
    "P4": ("Mass consumer", {"A1": "D2", "A2": "decl", "A3": "server", "A4": "none", "A5": "open",
                          "A6": "snapshot", "A7": "none", "A8": "public", "A9": "credits", "A10": "V1", "A11": "live"}),
    "P5": ("Local-first collaborative", {"A1": "D3", "A2": "decl", "A3": "client", "A4": "none", "A5": "open",
                              "A6": "crdt", "A7": "auto", "A8": "tenant", "A9": "byok", "A10": "none", "A11": "preview"}),
    "P6": ("Marketplace platform", {"A1": "D4", "A2": "sandboxed", "A3": "hybrid", "A4": "frame", "A5": "own",
                          "A6": "lineage", "A7": "proposed", "A8": "public", "A9": "credits", "A10": "V1", "A11": "gated"}),
    "P7": ("Air-gapped public sector", {"A1": "D3", "A2": "decl", "A3": "server", "A4": "none", "A5": "hidden",
                          "A6": "lineage", "A7": "proposed", "A8": "tenant", "A9": "tenant_cloud", "A10": "V3", "A11": "gated"}),
}


# Business model (BM) coupling verdicts.  ●=possible as is, ◐=conditional (needs an operating practice or external contract), ○=structurally impossible
F, C, X = "●", "◐", "○"
GOV_RICH = ("V1", "V2", "V3")
PROPAGATES = ("proposed", "auto")
BMS = collections.OrderedDict([
    ("B1", ("License sales", lambda c: F)),
    ("B2", ("Seat subscription", lambda c: F)),
    ("B3", ("Inference credit margin", lambda c: F if c["A9"] == "credits" else X)),
    ("B4", ("BYOK platform fee", lambda c: (F if c["A3"] != "client" else C) if c["A9"] in ("byok", "tenant_cloud") else X)),
    ("B5", ("Sharing market commission", lambda c: F if c["A8"] == "public" else (C if c["A8"] == "tenant" else X))),
    ("B6", ("Governance add-on", lambda c: F if c["A10"] in GOV_RICH else (C if c["A10"] == "V0" else X))),
    ("B7", ("Confidential execution premium", lambda c: F if (c["A3"] == "server" and c["A5"] == "hidden") else (C if c["A3"] == "server" else X))),
    ("B8", ("Baseline support contract", lambda c: (F if c["A6"] == "lineage" else (C if c["A6"] == "fork" else X)) if c["A7"] in PROPAGATES else X)),
    ("B9", ("Upgrade survival guarantee", lambda c: F if (c["A6"] in ("fork", "lineage") and c["A7"] in PROPAGATES) else X)),
    ("B10", ("Promotion revenue sharing", lambda c: (F if (c["A8"] != "none" and c["A10"] in GOV_RICH) else C) if c["A6"] == "lineage" else X)),
    ("B11", ("Local developer matching", lambda c: F if (c["A5"] != "hidden" and c["A8"] != "none") else C)),
    ("B12", ("Demand signal reports", lambda c: F if c["A10"] != "none" else X)),
    ("B13", ("Lexicon and domain packs", lambda c: F)),
    ("B14", ("Model provider partnership", lambda c: X if c["A9"] == "on_device" else C)),
    ("B15", ("Quality tier differentiation", lambda c: F if c["A9"] == "credits" else (C if (c["A9"] in ("byok", "tenant_cloud") and c["A3"] != "client") else X))),
    ("B16", ("Outcome-based billing", lambda c: X if c["A10"] == "none" else (F if c["A9"] == "credits" else (C if c["A9"] in ("byok", "tenant_cloud") else X)))),
    ("B17", ("Runtime OEM license", lambda c: F)),
    ("B18", ("Resolution recipe subscription", lambda c: F if (c["A6"] in ("fork", "lineage") and c["A7"] in PROPAGATES) else X)),
    ("B19", ("Revenue sharing for productized features", lambda c: F if c["A8"] == "public" else (C if c["A8"] == "tenant" else X))),
    ("B20", ("Sponsored default slot", lambda c: C if c["A8"] == "public" else X)),
])


def bm_row(c):
    return {b: fn(c) for b, (_, fn) in BMS.items()}


def bm_markdown():
    lines = ["| BM | Name | " + " | ".join(PROFILES) + " |",
             "| --- | --- | " + " | ".join(":-:" for _ in PROFILES) + " |"]
    rows = {p: bm_row(PROFILES[p][1]) for p in PROFILES}
    for b, (name, _) in BMS.items():
        lines.append(f"| {b} | {name} | " + " | ".join(rows[p][b] for p in PROFILES) + " |")
    return "\n".join(lines)


def bm_stats():
    """Share of all recommended combinations in which each BM is possible (●) / conditional (◐)."""
    keys = list(AXES)
    tot = 0
    cnt = {b: collections.Counter() for b in BMS}
    for combo in itertools.product(*[AXES[k][1] for k in keys]):
        c = dict(zip(keys, combo))
        if classify(c)[0] != "clean":
            continue
        tot += 1
        for b, v in bm_row(c).items():
            cnt[b][v] += 1
    lines = ["| BM | Name | ● possible | ◐ conditional | ○ impossible |", "| --- | --- | ---: | ---: | ---: |"]
    for b, (name, _) in BMS.items():
        f = cnt[b]
        lines.append(f"| {b} | {name} | {f[F] / tot * 100:.1f}% | {f[C] / tot * 100:.1f}% | {f[X] / tot * 100:.1f}% |")
    return "\n".join(lines)


def classify(c):
    l = logical(c)
    if l:
        return "logical", l, []
    n = normative(c)
    if n:
        return "normative", n, []
    w = soft(c)
    return ("warned" if w else "clean"), None, w


def enumerate_space():
    keys = list(AXES)
    stats = {
        "raw": 0, "logical_ok": 0, "normative_ok": 0, "clean": 0,
        "logical_reason": collections.Counter(), "normative_reason": collections.Counter(),
        "logical_independent": collections.Counter(), "logical_unique": collections.Counter(),
        "soft_hits": collections.Counter(),
        "clean_marginals": {k: collections.Counter() for k in keys},
    }
    families = collections.defaultdict(int)  # structural combination -> number of clean economic and policy completions
    for combo in itertools.product(*[AXES[k][1] for k in keys]):
        stats["raw"] += 1
        c = dict(zip(keys, combo))
        hits = logical_all(c)
        stats["logical_independent"].update(hits)
        if len(hits) == 1:
            stats["logical_unique"][hits[0]] += 1
        kind, rule, warns = classify(c)
        if kind == "logical":
            stats["logical_reason"][rule] += 1
            continue
        stats["logical_ok"] += 1
        if kind == "normative":
            stats["normative_reason"][rule] += 1
            continue
        stats["normative_ok"] += 1
        for w in warns:
            stats["soft_hits"][w] += 1
        if kind == "clean":
            stats["clean"] += 1
            for k in keys:
                stats["clean_marginals"][k][c[k]] += 1
            families[tuple(c[k] for k in STRUCTURAL)] += 1
    full = 1
    for k in ECONOMIC:
        full *= len(AXES[k][1])
    dist = collections.Counter(families.values())
    stats["structural_families"] = len(families)
    stats["economic_full"] = full
    stats["completion_distribution"] = dict(sorted(dist.items(), reverse=True))
    stats["mean_completion"] = round(sum(families.values()) / max(1, len(families)), 2)
    return stats


def as_jsonable(stats):
    out = {}
    for k, v in stats.items():
        if isinstance(v, collections.Counter):
            out[k] = dict(sorted(v.items()))
        elif isinstance(v, dict) and v and isinstance(next(iter(v.values())), collections.Counter):
            out[k] = {kk: dict(vv) for kk, vv in v.items()}
        else:
            out[k] = v
    return out


def markdown(stats):
    raw = stats["raw"]
    pct = lambda x: f"{x / raw * 100:.2f}%"
    lines = []
    lines.append("| Stage | Combinations | Share of total |")
    lines.append("| --- | ---: | ---: |")
    lines.append(f"| Raw combinations Ω | {raw:,} | 100% |")
    lines.append(f"| Logically consistent (passes L) | {stats['logical_ok']:,} | {pct(stats['logical_ok'])} |")
    lines.append(f"| Normatively consistent (passes L+N) | {stats['normative_ok']:,} | {pct(stats['normative_ok'])} |")
    lines.append(f"| Recommended (no warnings) | {stats['clean']:,} | {pct(stats['clean'])} |")
    lines.append("")
    lines.append(f"- Number of structural families (A1~A8) among recommended combinations: {stats['structural_families']:,}")
    lines.append(f"- Average economic and policy completions (A9~A11) per family: {stats['mean_completion']} / {stats['economic_full']}")
    lines.append(f"- Distribution of completion counts (completions: families): {stats['completion_distribution']}")
    lines.append("")
    lines.append("| Logical rule | First violation | Independent violation | Unique violation |")
    lines.append("| --- | ---: | ---: | ---: |")
    for r, n in sorted(stats["logical_independent"].items(), key=lambda x: -x[1]):
        lines.append(f"| {r} | {stats['logical_reason'][r]:,} | {n:,} | {stats['logical_unique'][r]:,} |")
    lines.append("")
    lines.append("| Normative rule | Combinations filtered |")
    lines.append("| --- | ---: |")
    for r, n in sorted(stats["normative_reason"].items(), key=lambda x: -x[1]):
        lines.append(f"| {r} | {n:,} |")
    lines.append("")
    lines.append("| Warning rule | Combinations affected (among normatively consistent) |")
    lines.append("| --- | ---: |")
    for r, n in sorted(stats["soft_hits"].items(), key=lambda x: -x[1]):
        lines.append(f"| {r} | {n:,} |")
    lines.append("")
    lines.append("| Axis | Occurrences of each option among recommended combinations |")
    lines.append("| --- | --- |")
    for k, (name, opts) in AXES.items():
        m = stats["clean_marginals"][k]
        lines.append(f"| {k} {name} | " + ", ".join(f"{o} {m.get(o, 0):,}" for o in opts) + " |")
    return "\n".join(lines)


def check(c):
    if not isinstance(c, dict):
        return {"error": "profile must be a JSON object"}
    unknown = [k for k in c if k not in AXES]
    if unknown:
        return {"error": f"unknown axes: {unknown}"}
    missing = [k for k in AXES if k not in c]
    if missing:
        return {"error": f"missing axes: {missing}"}
    bad = [k for k in AXES if c[k] not in AXES[k][1]]
    if bad:
        return {"error": f"options not allowed: {[(k, c[k]) for k in bad]}"}
    kind, rule, warns = classify(c)
    return {"result": kind, "violated": rule, "warnings": warns}


PASS = ("clean", "warned")

def no_dup_keys(pairs):
    keys = [k for k, _ in pairs]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        raise ValueError(f"duplicate keys: {dup}")
    return dict(pairs)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--check", help="reference profile id (P1~P7) or all")
    ap.add_argument("--profile", help="check an arbitrary combination given as a JSON string or JSON file path")
    ap.add_argument("--bm", action="store_true", help="reference profile × BM coupling matrix")
    ap.add_argument("--bm-stats", action="store_true", help="per-BM feasibility share over all recommended combinations")
    a = ap.parse_args()
    if a.bm:
        print(bm_markdown())
        return
    if a.bm_stats:
        print(bm_stats())
        return
    if a.check:
        ids = list(PROFILES) if a.check == "all" else [a.check]
        if not set(ids) <= set(PROFILES):
            sys.exit(f"unknown profile: {a.check} (P1~P7 or all)")
        res = {i: {"name": PROFILES[i][0], **check(PROFILES[i][1])} for i in ids}
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0 if all(r.get("result") in PASS for r in res.values()) else 1
    if a.profile:
        try:
            if os.path.isfile(a.profile):
                with open(a.profile, encoding="utf-8") as fh:
                    prof = json.load(fh, object_pairs_hook=no_dup_keys)
            else:
                prof = json.loads(a.profile, object_pairs_hook=no_dup_keys)
        except (json.JSONDecodeError, ValueError) as e:
            sys.exit(f"--profile JSON error: {e}")
        out = check(prof)
        if out.get("result") in PASS:
            out["business_models"] = {f"{b} {BMS[b][0]}": v for b, v in bm_row(prof).items()}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0 if out.get("result") in PASS else 1  # gate-safe: error·logical·normative → exit 1
    stats = enumerate_space()
    print(markdown(stats) if a.markdown else json.dumps(as_jsonable(stats), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
