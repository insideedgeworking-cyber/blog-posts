# -*- coding: utf-8 -*-
"""post_011用：Claude Code と Codex の比較カード図を生成。
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
BLUE="#2f6fb3"; DARK="#1d4778"; ORANGE="#ff7a3d"; GREEN="#2e8b6f"; INK="#27313a"; GREY="#6b7682"

fig, ax = plt.subplots(figsize=(11.2, 6.6), dpi=160); ax.axis("off")
ax.set_xlim(0, 12); ax.set_ylim(0, 7.4)

ax.text(0.15, 7.05, "Claude Code と Codex の違い（2026年・副業の自動化目線）",
        fontproperties=fp(17, True), color=INK, va="center")

# 共通点バンド
ax.add_patch(FancyBboxPatch((0.15, 6.0), 11.7, 0.72, boxstyle="round,pad=0.02,rounding_size=0.1",
             fc="#eef4fb", ec="#cfe0fa", lw=1.2))
ax.text(6.0, 6.36, "共通：どちらも“ターミナルで動くAIエージェント”／日本語で指示OK／プログラミング未経験でも使える",
        ha="center", va="center", fontproperties=fp(11.5, True), color=DARK)

def card(x, name, maker, accent, rows, who):
    w = 5.7
    ax.add_patch(FancyBboxPatch((x, 0.5), w, 5.25, boxstyle="round,pad=0.02,rounding_size=0.14",
                 fc="white", ec=accent, lw=2.2))
    ax.add_patch(FancyBboxPatch((x, 5.05), w, 0.7, boxstyle="round,pad=0.02,rounding_size=0.14",
                 fc=accent, ec=accent, lw=2.2))
    ax.text(x+w/2, 5.4, name, ha="center", va="center", fontproperties=fp(16, True), color="white")
    ax.text(x+w/2, 4.78, maker, ha="center", va="center", fontproperties=fp(10.5), color=GREY)
    y = 4.30
    for label, val in rows:
        ax.text(x+0.30, y, label, fontproperties=fp(11, True), color=accent, va="top")
        ax.text(x+0.30, y-0.34, val, fontproperties=fp(11), color=INK, va="top", wrap=True)
        y -= 1.04
    ax.add_patch(FancyBboxPatch((x+0.22, 0.66), w-0.44, 0.74, boxstyle="round,pad=0.02,rounding_size=0.1",
                 fc="#f6f8fa", ec="#e3e8ee", lw=1.0))
    ax.text(x+w/2, 1.03, who, ha="center", va="center", fontproperties=fp(10.5, True), color=GREEN)

card(0.15, "Claude Code", "Anthropic", BLUE, [
    ("料金", "Claude Pro 月20ドル〜（重い人はMax）"),
    ("得意", "文章・調査・作業全般の自動化の作り込み"),
    ("使い勝手", "Proは5時間ごとの利用枠／文脈が広い"),
], "こんな人に：書き味重視・作業全般を自動化したい")

card(6.15, "Codex", "OpenAI", ORANGE, [
    ("料金", "ChatGPT Plus 月20ドル〜に込み（無料枠も）"),
    ("得意", "コードを書く・直す・出荷する開発作業"),
    ("使い勝手", "2026年4月にトークン課金へ／無料で試せる"),
], "こんな人に：ChatGPT課金済み・開発が主目的")

fig.text(0.012, 0.015, "※料金・仕様は2026年時点の目安。両者とも2026年に課金体系を改定。最終的な金額は必ず公式で最新を確認。",
         fontproperties=fp(8.5), color=GREY)
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.05)
fig.savefig(os.path.join(IMG, "claude-codex-compare.png"), facecolor="white", bbox_inches="tight"); plt.close(fig)
print("saved claude-codex-compare.png")
