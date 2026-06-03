# -*- coding: utf-8 -*-
"""post_006用：主要AIツールの比較図を生成。
1) ai-price.png  個人向け有料プランの月額（最安）の横棒
2) ai-compare.png 無料/有料/得意分野の比較表
料金は2026年6月時点の目安（$20≒約3,000円換算）。"""
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

BLUE="#2f6fb3"; BLUE_LT="#a9c6e6"; ORANGE="#ff8a3d"; GREEN="#5cb389"

# 1) 料金バー（最安有料/月・円） -----------------------------------
rows = [
    ("ChatGPT (Plus)", 3000, "約3,000円"),
    ("Claude (Pro)", 3000, "約3,000円"),
    ("Perplexity (Pro)", 3200, "約3,200円"),
    ("Gemini (AI Plus)", 1200, "1,200円"),
    ("Grok (SuperGrok Lite)", 980, "980円"),
]
rows = rows[::-1]
fig, ax = plt.subplots(figsize=(9.0, 4.4), dpi=160)
colors = [GREEN, GREEN, BLUE, BLUE, BLUE][::-1]
for i,(name,val,lab) in enumerate(rows):
    ax.barh(i, val, height=0.5, color=colors[i], edgecolor="white", zorder=3)
    ax.text(val+60, i, lab, va="center", ha="left", fontproperties=fp(11.5), color="#444")
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows], fontproperties=fp(11.5))
ax.set_ylim(-0.7, len(rows)-0.3); ax.set_xlim(0, 3900)
ax.set_xlabel("個人向け有料プランの月額（最安・円）", fontproperties=fp(11), labelpad=8)
ax.set_title("主要AIツール 有料プラン月額の目安（2026年6月）", fontproperties=fp(15.5,"bold"), loc="left", x=0, pad=16)
ax.grid(axis="x", color="#eef1f4", zorder=0); ax.set_axisbelow(True)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#dfe3e8"); ax.tick_params(length=0, labelsize=9, colors="#888")
fig.text(0.012, 0.02, "※全サービス無料プランあり。海外サービスは20ドル≒約3,000円で換算した目安。為替・改定で変動。", fontproperties=fp(7.5), color="#9aa0a6")
fig.subplots_adjust(left=0.27, right=0.96, top=0.82, bottom=0.2)
fig.savefig(os.path.join(IMG,"ai-price.png"), facecolor="white"); plt.close(fig)
print("saved ai-price.png")

# 2) 比較表 -------------------------------------------------------
header = ["サービス", "無料プラン", "有料(最安/月)", "得意なこと"]
data = [
    ["ChatGPT", "あり", "約3,000円", "万能・文章・相談全般"],
    ["Claude", "あり", "約3,000円", "長文・自然な文章・コード"],
    ["Gemini", "あり", "1,200円〜", "Google連携・リサーチ"],
    ["Grok", "あり", "980円〜", "X連携・最新情報"],
    ["Perplexity", "あり", "約3,000円", "出典付きリサーチ"],
]
fig, ax = plt.subplots(figsize=(9.0, 3.3), dpi=160); ax.axis("off")
tbl = ax.table(cellText=data, colLabels=header, cellLoc="center", loc="center",
               colWidths=[0.17,0.16,0.2,0.47])
tbl.auto_set_font_size(False); tbl.scale(1, 2.0)
for (r,c), cell in tbl.get_celld().items():
    cell.set_edgecolor("#e3e9f0")
    txt = cell.get_text()
    if r == 0:
        cell.set_facecolor(BLUE); txt.set_color("white"); txt.set_fontproperties(fp(11.5,"bold"))
    else:
        cell.set_facecolor("#ffffff" if r%2 else "#f5f8fc")
        txt.set_fontproperties(fp(11 if c>0 else 11.5, "bold" if c==0 else "normal"))
        if c==0: txt.set_color(BLUE)
ax.set_title("主要AIツールの特徴くらべ（2026年6月時点）", fontproperties=fp(15,"bold"), loc="left", x=0, pad=14)
fig.text(0.012, 0.04, "※無料でも試せる。料金は代表的な個人向けプランの目安で、改定により変わる。", fontproperties=fp(7.5), color="#9aa0a6")
fig.subplots_adjust(left=0.02, right=0.98, top=0.84, bottom=0.1)
fig.savefig(os.path.join(IMG,"ai-compare.png"), facecolor="white", bbox_inches="tight"); plt.close(fig)
print("saved ai-compare.png")

# 3) 開発・自動化系（コーディングエージェント）比較表 ----------------
header3 = ["ツール", "使う場所", "料金の目安", "特徴・こんな人向け"]
data3 = [
    ["Claude Code", "ターミナル", "Claude Pro(約3,000円)に込み", "自律的に複数ファイルを編集。実装向き"],
    ["OpenAI Codex", "ターミナル/クラウド", "ChatGPT(無料〜)に込み", "任せて待つ“おまかせ”型。大きな作業向き"],
    ["GitHub Copilot", "エディタの中", "月10ドル〜", "書きながら補完・相談。二人三脚で"],
    ["Cursor", "AI専用エディタ", "月20ドル〜", "VS Code型。エディタごとAI化"],
]
fig, ax = plt.subplots(figsize=(10.6, 3.0), dpi=160); ax.axis("off")
tbl = ax.table(cellText=data3, colLabels=header3, cellLoc="center", loc="center",
               colWidths=[0.2, 0.18, 0.27, 0.35])
tbl.auto_set_font_size(False); tbl.scale(1, 2.0)
for (r,c), cell in tbl.get_celld().items():
    cell.set_edgecolor("#e3e9f0"); txt = cell.get_text()
    if r == 0:
        cell.set_facecolor(BLUE); txt.set_color("white"); txt.set_fontproperties(fp(11,"bold"))
    else:
        cell.set_facecolor("#ffffff" if r%2 else "#f5f8fc")
        txt.set_fontproperties(fp(10.5 if c>0 else 11, "bold" if c==0 else "normal"))
        if c==0: txt.set_color(BLUE)
ax.set_title("AIにPC作業を任せる「開発・自動化系」ツール（2026年6月時点）", fontproperties=fp(14.5,"bold"), loc="left", x=0, pad=14)
fig.text(0.012, 0.04, "※やや上級者向け。料金はチャット版の契約に含まれることが多い。改定により変わる。", fontproperties=fp(7.5), color="#9aa0a6")
fig.subplots_adjust(left=0.02, right=0.98, top=0.84, bottom=0.1)
fig.savefig(os.path.join(IMG,"ai-coding.png"), facecolor="white", bbox_inches="tight"); plt.close(fig)
print("saved ai-coding.png")
