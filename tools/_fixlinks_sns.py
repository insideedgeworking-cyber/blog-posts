# -*- coding: utf-8 -*-
"""SNSクラスタ公開後: 空?p=を実IDへ・wp_post_id記録・status=published。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")
IDS = {"post_030":98, "post_026":100, "post_027":102, "post_028":104}
# 空?p=行のキーワード -> 実ID（順に判定。先に「まとめ」=ピラー）
RULES = [("（まとめ）",98), ("X(旧Twitter)集客",102), ("スレッズ集客のやり方",100), ("インスタ集客のやり方",104)]

for pid, wpid in IDS.items():
    fp=os.path.join(PD,f"{pid}.json"); d=json.load(open(fp,encoding="utf-8-sig"))
    d["wp_post_id"]=wpid; d["status"]="published"
    out=[]
    for ln in d["body"].split("\n"):
        if "workstartedge.com/?p=)" in ln:
            for kw,rid in RULES:
                if kw in ln:
                    ln=ln.replace("?p=)",f"?p={rid})"); print(f"  {pid}: ?p={rid} ({kw})"); break
            else:
                print(f"  [!] {pid} 未解決:",ln[:55])
        out.append(ln)
    d["body"]="\n".join(out); d["char_count"]=len(d["body"])
    json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"{pid}: wp={wpid} published")
print("done")
