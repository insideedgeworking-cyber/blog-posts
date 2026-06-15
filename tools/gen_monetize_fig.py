# -*- coding: utf-8 -*-
"""post_140(収益化ロードマップ)の5STEPフロー図を生成。images/に保存。WindowsのpythonでYu Gothic。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm
import os

for cand in ["Yu Gothic", "Meiryo", "MS Gothic", "Yu Gothic UI"]:
    if any(cand.lower() in f.name.lower() for f in fm.fontManager.ttflist):
        plt.rcParams["font.family"] = cand; print("font:", cand); break
plt.rcParams["axes.unicode_minus"] = False

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
os.makedirs(IMG, exist_ok=True)
NAVY = "#1f2a44"; BLUE = "#2f6fb3"; ORANGE = "#ff7a3d"; GRAY = "#5b6472"; GREEN = "#1faf6a"

fig, ax = plt.subplots(figsize=(10, 5.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.2); ax.axis("off")
ax.text(5, 4.9, "ブログ収益化ロードマップ（月5万円までの5STEP）",
        ha="center", va="center", fontsize=17, fontweight="bold", color=NAVY)

steps = [
    ("STEP1", "ジャンルと案件を選ぶ", "※ここで9割決まる", BLUE),
    ("STEP2", "キーワードを選ぶ", "弱者の戦略", BLUE),
    ("STEP3", "読まれて売れる記事", "体験を足す", ORANGE),
    ("STEP4", "集客（検索＋SNS）", "育つのを待つ", GRAY),
    ("STEP5", "分析して改善", "リライト", GREEN),
]
x0, w, h, gap = 0.35, 1.78, 1.5, 0.13
y = 2.5
for i, (tag, main, sub, c) in enumerate(steps):
    x = x0 + i * (w + gap)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                 fc=c, ec="none"))
    ax.text(x + w / 2, y + h * 0.72, tag, ha="center", va="center", color="white", fontsize=12, fontweight="bold")
    ax.text(x + w / 2, y + h * 0.44, main, ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")
    ax.text(x + w / 2, y + h * 0.17, sub, ha="center", va="center", color="white", fontsize=9)
    if i < len(steps) - 1:
        ax.add_patch(FancyArrowPatch((x + w + 0.005, y + h / 2), (x + w + gap - 0.005, y + h / 2),
                     arrowstyle="-|>", mutation_scale=15, lw=2, color=NAVY))

ax.text(5, 1.4, "目安：初報酬まで30〜50記事/約半年　・　月5万円まで50〜100記事/1〜2年",
        ha="center", va="center", fontsize=11, color=GRAY)
ax.text(5, 0.7, "大原則＝「役立つ記事」より先に「売れる商品がある場所」を選ぶ（商品から逆算）",
        ha="center", va="center", fontsize=11, color=ORANGE, fontweight="bold")

out = os.path.join(IMG, "monetize-roadmap-flow.png")
fig.savefig(out, dpi=130, bbox_inches="tight", facecolor="white")
print("saved:", out)
