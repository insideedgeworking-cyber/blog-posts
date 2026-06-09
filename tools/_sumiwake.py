# -*- coding: utf-8 -*-
"""post_017(副業の選び方) と post_022(AI副業) のすみわけを明示。
役割を1行で示し、相互リンクを双方向にする。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")

def load(p): return json.load(open(os.path.join(PD, p), encoding="utf-8-sig"))
def save(p, d):
    d["char_count"] = len(d["body"])
    json.dump(d, open(os.path.join(PD, p), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(p, "char=", d["char_count"])

# --- post_022: 冒頭に「これはAIで“作る”前提に特化」位置づけ ---
d22 = load("post_022.json")
anchor22 = "私も未経験から、AIでブログやYouTubeの仕組みを自作しました。"
add22 = "\n\n> 📌 この記事は**AIで“作る”前提の副業**に特化しています。AIに限らず副業全般を「収入・期間・初期費用」で比べて選びたい人は、まず [副業の選び方｜種類別に収入・メリット・デメリットを比較](https://workstartedge.com/?p=56) を読むと、自分に向くタイプが先に分かります。"
if add22 not in d22["body"] and anchor22 in d22["body"]:
    d22["body"] = d22["body"].replace(anchor22, anchor22 + add22, 1)
    print("post_022: 位置づけ挿入 OK")
else:
    print("post_022: skip (既存 or anchor不一致)")
save("post_022.json", d22)

# --- post_017: 結論直後にAI特化記事への誘導 + あわせて読みたいに追加 ---
d17 = load("post_017.json")
anchor17 = "で選ぶ**のが失敗しないコツです。"
add17 = "\n\n（なお、**ChatGPTなどのAIで“作って”稼ぐ副業**——楽天ROOM・LINEスタンプ・無在庫販売・AIブログなど——の具体的な手順だけ知りたい人は、[AIを使った副業の種類と始め方｜未経験が稼ぐ具体例](https://workstartedge.com/?p=78) にまとめています。）"
if add17 not in d17["body"] and anchor17 in d17["body"]:
    d17["body"] = d17["body"].replace(anchor17, anchor17 + add17, 1)
    print("post_017: 誘導文 挿入 OK")
else:
    print("post_017: 誘導文 skip")

# あわせて読みたいに post_022 を追加（AIツール比較の行の後）
link_line = "- [AIツール比較2026｜副業向けの選び方とおすすめ](https://workstartedge.com/?p=46)"
new_link = "- [AIを使った副業の種類と始め方｜未経験が稼ぐ具体例【2026】](https://workstartedge.com/?p=78)"
if new_link not in d17["body"] and link_line in d17["body"]:
    d17["body"] = d17["body"].replace(link_line, link_line + "\n" + new_link, 1)
    print("post_017: あわせて読みたいに post_022 追加 OK")
else:
    print("post_017: あわせて読みたい skip")
save("post_017.json", d17)
print("done")
