# -*- coding: utf-8 -*-
"""post_020用：ChatGPT と Claude の比較カード図を生成。
注意: matplotlibのtextで $ は数式扱いになるため使わない（ドルは「ドル」表記）。"""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
os.makedirs(IMG, exist_ok=True)
_fp = None
for cand in (r"C:\Windows\Fonts\YuGothM.ttc", r"C:\Windows\Fonts\meiryo.ttc"):
    if os.path.exists(cand): _fp = cand; break
_fpb = r"C:\Windows\Fonts\YuGothB.ttc"
def fp(sz, bold=False):
    f = font_manager.FontProperties(fname=(_fpb if bold and os.path.exists(_fpb) else _fp)); f.set_size(sz); return f
GREEN="#10a37f"; CORAL="#d97757"; INK="#27313a"; GREY="#6b7682"; OKBLUE="#2f6fb3"

fig, ax = plt.subplots(figsize=(11.2, 6.7), dpi=160); ax.axis("off")
ax.set_xlim(0, 12); ax.set_ylim(0, 7.5)

ax.text(0.15, 7.15, "ChatGPT と Claude の違い（2026年・副業目線）",
        fontproperties=fp(17, True), color=INK, va="center")

ax.add_patch(FancyBboxPatch((0.15, 6.05), 11.7, 0.72, boxstyle="round,pad=0.02,rounding_size=0.1",
             fc="#eef4fb", ec="#cfe0fa", lw=1.2))
ax.text(6.0, 6.41, "共通：どちらも月20ドルの対話型AI／無料版あり／総合性能はほぼ互角",
        ha="center", va="center", fontproperties=fp(11.5, True), color=OKBLUE)

def card(x, name, maker, accent, rows, who):
    w = 5.7
    ax.add_patch(FancyBboxPatch((x, 0.5), w, 5.3, boxstyle="round,pad=0.02,rounding_size=0.14",
                 fc="white", ec=accent, lw=2.2))
    ax.add_patch(FancyBboxPatch((x, 5.1), w, 0.7, boxstyle="round,pad=0.02,rounding_size=0.14",
                 fc=accent, ec=accent, lw=2.2))
    ax.text(x+w/2, 5.45, name, ha="center", va="center", fontproperties=fp(16, True), color="white")
    ax.text(x+w/2, 4.83, maker, ha="center", va="center", fontproperties=fp(10.5), color=GREY)
    y = 4.34
    for label, val in rows:
        ax.text(x+0.30, y, label, fontproperties=fp(11, True), color=accent, va="top")
        ax.text(x+0.30, y-0.34, val, fontproperties=fp(10.5), color=INK, va="top")
        y -= 1.06
    ax.add_patch(FancyBboxPatch((x+0.22, 0.66), w-0.44, 0.74, boxstyle="round,pad=0.02,rounding_size=0.1",
                 fc="#f6f8fa", ec="#e3e8ee", lw=1.0))
    ax.text(x+w/2, 1.03, who, ha="center", va="center", fontproperties=fp(10.5, True), color=accent)

card(0.15, "ChatGPT", "OpenAI", GREEN, [
    ("料金", "無料／Plus 月20ドル（Pro 200ドル）"),
    ("得意", "画像生成・音声会話、Web検索、連携(GPTs)が最多"),
    ("ひとことで", "多機能の“王道”。迷ったらコレ"),
], "こんな人に：画像も使う・最新検索・とにかく無難に")

card(6.15, "Claude", "Anthropic", CORAL, [
    ("料金", "無料／Pro 月20ドル（Max 100ドル）"),
    ("得意", "文章の質・超長文・コーディング・Artifacts"),
    ("ひとことで", "文章と“作業をやり切る”力が強い"),
], "こんな人に：ブログ/長文資料・自動化の作り込み重視")

fig.text(0.012, 0.015, "※料金・性能は2026年時点の目安。Claudeは画像生成は不可（画像はChatGPT等で）。最新は必ず公式で確認。",
         fontproperties=fp(8.5), color=GREY)
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.05)
fig.savefig(os.path.join(IMG, "chatgpt-claude-compare.png"), facecolor="white", bbox_inches="tight"); plt.close(fig)
print("saved chatgpt-claude-compare.png")
