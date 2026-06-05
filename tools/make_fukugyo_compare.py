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

# ── 現実：稼げている人の割合（楽に月100万は嘘） ──
make_table("fukugyo-reality.png", "副業で稼げている人の割合（現実・ピンキリ）",
    ["副業", "稼げている人の割合の現実", "出典・補足"],
    [
        ["副業全体(平均的な実態)", "月1万未満が最多(約48%)／10万超は約14%", "Job総研2025ほか"],
        ["ブログ・アフィリエイト", "大半が月1万未満(約6割)／100万超も13.3%", "アフィリ協会2025"],
        ["YouTube", "収益化(登録1000人)到達は上位15〜17%だけ", "各種統計"],
        ["せどり・物販", "月の利益1万円以下が約63%", "実践者調査"],
        ["コンテンツ販売(note)", "月1万超は上位ごく一部(数千人規模)", "note公表データ"],
        ["Webライター・動画編集", "即金で月数万が中心／20〜30万は一部", "各種相場"],
        ["X・Threads", "広告収益は月数百〜数千円が大半", "各種"],
    ],
    [0.24, 0.50, 0.26],
    "※調査ごとに対象・基準が異なるため傾向の目安。共通するのは『大半は最初そんなに稼げない』こと。だから“楽に一発”の宣伝に騙されないで。",
    figh=4.6)

# ── 始めやすさ × 稼ぎやすさ のポジショニングマップ ──
ORANGE = "#ff7a3d"
# 軸は「進むほど難しい」向き：x=始めにくさ(右ほど始めにくい), y=稼ぎにくさ(上ほど稼ぎにくい)
# name, x(始めにくさ), y(稼ぎにくさ), タイプ, ラベル位置(dx,dy,ha)
POINTS = [
    ("ブログ・アフィリ", 1.5, 4.0, "asset", (0,  0.30, "center")),
    ("YouTube",          3.2, 4.5, "asset", (0,  0.30, "center")),
    ("X・Threads",       1.0, 3.5, "asset", (0.16, 0.0, "left")),
    ("note販売",         2.0, 3.3, "asset", (0, -0.32, "center")),
    ("Webライター",      2.0, 1.2, "labor", (0,  0.30, "center")),
    ("動画編集",         3.5, 1.6, "labor", (0,  0.30, "center")),
    ("せどり・物販",     4.6, 1.9, "labor", (-0.12,-0.32,"right")),
]
def make_map(fname):
    fig, ax = plt.subplots(figsize=(9.6, 7.2), dpi=160)
    # 四分割の補助線
    ax.axvline(3, color="#dfe5ec", lw=1, zorder=1); ax.axhline(3, color="#dfe5ec", lw=1, zorder=1)
    quad = [(0.65,2.55,"手軽＆早く稼ぎやすい","left"),(5.6,1.0,"手間・資金だが即金","right"),
            (0.65,5.05,"手軽だが時間がかかる(資産)","left"),(5.6,5.05,"ハードル高め","right")]
    for x,y,t,ha in quad:
        ax.text(x,y,t,fontproperties=fp(9.5,"bold"),color="#c2c8d0",ha=ha,va="center",zorder=1)
    for name,x,y,typ,(dx,dy,ha) in POINTS:
        col = BLUE if typ=="asset" else ORANGE
        ax.scatter([x],[y],s=420,color=col,edgecolor="white",linewidth=1.5,zorder=3)
        ax.text(x+dx,y+dy,name,fontproperties=fp(11.5,"bold"),color="#333",ha=ha,va="center",zorder=4)
    ax.set_xlim(0.5,5.7); ax.set_ylim(0.7,5.2)
    ax.set_xlabel("始めやすさ →（右に進むほど始めにくい）", fontproperties=fp(12,"bold"), color=BLUE)
    ax.set_ylabel("稼ぎやすさ →（上に進むほど稼ぎにくい）", fontproperties=fp(12,"bold"), color=BLUE)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_color("#c2c8d0")
    # 凡例
    ax.scatter([],[],s=200,color=BLUE,label="資産型（育てば収入の天井が高い）")
    ax.scatter([],[],s=200,color=ORANGE,label="労働型（即金だが作業＝収入）")
    leg = ax.legend(loc="lower left", prop=fp(10), frameon=True, edgecolor="#e3e9f0")
    ax.set_title("副業の「始めやすさ × 稼ぎやすさ」マップ", fontproperties=fp(15,"bold"), loc="left", x=0, pad=12)
    fig.text(0.012,0.015,"※目安。左下ほど手軽で早く稼げる。青(資産型)は今は上(稼ぎにくい側)でも、続ければ収入の天井が高い。",
             fontproperties=fp(8), color="#9aa0a6")
    fig.subplots_adjust(left=0.07, right=0.97, top=0.9, bottom=0.1)
    fig.savefig(os.path.join(IMG, fname), facecolor="white", bbox_inches="tight"); plt.close(fig)
    print("saved", fname)

make_map("fukugyo-map.png")
