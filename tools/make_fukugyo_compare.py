# -*- coding: utf-8 -*-
"""副業選び記事(post_017)用：主要7副業の早見表（収入・期間・初期費用・タイプ）を生成。
各種調査(2025〜2026)＋運営者の実感をもとにした目安。数字は変動するため要更新。
注意: matplotlibのtextで $ は数式扱いになるため使わない。"""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
os.makedirs(IMG, exist_ok=True)
_fp = None
for cand in (r"C:\Windows\Fonts\YuGothM.ttc", r"C:\Windows\Fonts\meiryo.ttc"):
    if os.path.exists(cand): _fp = cand; break
def fp(sz, w="normal"):
    f = font_manager.FontProperties(fname=_fp); f.set_size(sz); f.set_weight(w); return f
BLUE = "#2f6fb3"

def make_table(fname, title, header, rows, widths, note, figh=4.6):
    fig, ax = plt.subplots(figsize=(11.2, figh), dpi=160); ax.axis("off")
    tbl = ax.table(cellText=rows, colLabels=header, cellLoc="center", loc="center", colWidths=widths)
    tbl.auto_set_font_size(False); tbl.scale(1, 2.0)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#e3e9f0"); t = cell.get_text()
        if r == 0:
            cell.set_facecolor(BLUE); t.set_color("white"); t.set_fontproperties(fp(10.5, "bold"))
        else:
            cell.set_facecolor("#ffffff" if r % 2 else "#f5f8fc")
            t.set_fontproperties(fp(9.5, "bold" if c == 0 else "normal"))
            if c == 0: t.set_color(BLUE)
    ax.set_title(title, fontproperties=fp(14.5, "bold"), loc="left", x=0, pad=12)
    fig.text(0.012, 0.03, note, fontproperties=fp(7.5), color="#9aa0a6")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.10)
    fig.savefig(os.path.join(IMG, fname), facecolor="white", bbox_inches="tight"); plt.close(fig)
    print("saved", fname)

make_table("fukugyo-compare.png", "副業7種類の早見表（収入・期間・初期費用・タイプ）",
    ["副業", "収入の目安", "稼げるまで", "初期費用", "タイプ"],
    [
        ["ブログ・アフィリ", "大半が月1万未満/上位は100万超", "半年〜1年", "月1,000円〜", "資産型"],
        ["YouTube", "1万人で月5千〜1.5万円", "半年〜1年+", "スマホ0円〜", "資産型"],
        ["X・Threads", "月数百〜数千円＋送客に強い", "数ヶ月", "0円(収益化に980円)", "資産/入口"],
        ["Webライター", "月3〜10万(慣れれば20万)", "初月〜(即金)", "ほぼ0円", "労働型"],
        ["動画編集", "月6〜10万(数こなせば30万)", "学習数週間〜", "ソフト月数千円", "労働型"],
        ["せどり・物販", "大半が月1万以下/利益率20-30%", "その月〜(即金)", "仕入れ等30万前後", "労働型寄り"],
        ["コンテンツ販売(note)", "1本500〜1842円/手元は8割", "3〜6ヶ月", "0円", "資産型"],
    ],
    [0.18, 0.30, 0.16, 0.20, 0.16],
    "※各種調査(2025〜2026)と運営者の実感をもとにした目安。収入・期間は人ややり方で大きく変わる。即金=作業した分すぐ収入／資産型=育つと継続収入。",
    figh=4.6)
