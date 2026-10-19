#!/usr/bin/env python3
"""Generate the appendix of KEYWORD_MAP.md from the clustered harvest."""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    d = json.load(open(os.path.join(HERE, "kw_clustered.json")))
    lines = []
    for name, items in sorted(d["clusters"].items(), key=lambda x: -len(x[1])):
        lines.append(f"### {name} — {len(items)} queries\n")
        lines.append("| score | seeds | best rank | query |")
        lines.append("|---|---|---|---|")
        for r in items[:15]:
            lines.append(f"| {r['score']} | {r['seeds']} | {r['best_rank']} | {r['keyword']} |")
        lines.append("")
    table = "\n".join(lines)
    p = os.path.join(HERE, "KEYWORD_MAP.md")
    s = io.open(p, encoding="utf-8").read()
    assert "<!--GENERATED-->" in s, "marker missing"
    io.open(p, "w", encoding="utf-8").write(s.replace("<!--GENERATED-->", table))
    print(f"appendix written: {len(d['clusters'])} clusters, kept={d['kept']}, dropped={d['dropped']}")


if __name__ == "__main__":
    main()
