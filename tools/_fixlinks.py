# -*- coding: utf-8 -*-
"""公開後: 相互リンクの空 ?p= を実WP IDに差し替え、各JSONに wp_post_id を記録。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")

IDS = {"post_020": 86, "post_021": 77, "post_022": 78}
# 空 ?p= の行に含まれるキーワード -> 実ID
RULES = [
    ("ChatGPT vs Claude", 86),
    ("AI用語", 77),
    ("AIツール事典", 77),
    ("AIを使った副業の種類", 78),
]

for pid, wpid in IDS.items():
    fp = os.path.join(PD, f"{pid}.json")
    d = json.load(open(fp, encoding="utf-8-sig"))
    d["wp_post_id"] = wpid
    lines = d["body"].split("\n")
    out = []
    for ln in lines:
        if "https://workstartedge.com/?p=)" in ln:
            for kw, rid in RULES:
                if kw in ln:
                    ln = ln.replace("?p=)", f"?p={rid})")
                    print(f"  {pid}: -> ?p={rid}  ({kw})")
                    break
            else:
                print(f"  [!] {pid}: 未解決の空?p= -> {ln[:50]}")
        out.append(ln)
    d["body"] = "\n".join(out)
    d["char_count"] = len(d["body"])
    json.dump(d, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{pid}: wp_post_id={wpid}, char={d['char_count']}")
print("done")
