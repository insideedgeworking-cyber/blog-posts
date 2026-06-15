# -*- coding: utf-8 -*-
"""post_013(ブログの始め方)の図解を生成(matplotlibをWindowsのpythonで実行)。images/に保存。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm
import os

for cand in ["Yu Gothic", "Meiryo", "MS Gothic", "Yu Gothic UI"]:
    if any(cand.lower() in f.name.lower() for f in fm.fontManager.ttflist):
        plt.rcParams["font.family"] = cand
        print("font:", cand)
        break
plt.rcParams["axes.unicode_minus"] = False

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
os.makedirs(IMG, exist_ok=True)
NAVY = "#1f2a44"; BLUE = "#2f6fb3"; ORANGE = "#ff7a3d"; GRAY = "#5b6472"; LIGHT = "#e7edf5"


def box(ax, x, y, w, h, text, fc, tc="white", fs=13, bold=True, r=0.05):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.01,rounding_size={r}", fc=fc, ec="none"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            color=tc, fontsize=fs, fontweight="bold" if bold else "normal", wrap=True)


fig, ax = plt.subplots(figsize=(10, 5.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.4); ax.axis("off")

ax.text(5, 5.05, "WordPressブログの始め方 7ステップ（最短10分）",
        ha="center", va="center", fontsize=17, fontweight="bold", color=NAVY)

steps = [
    ("① サーバー申込", "クイックスタートを選択", BLUE),
    ("② ドメイン決定", "「.com」でOK・無料", BLUE),
    ("③ WordPress設置", "サイト名・情報を入力", BLUE),
    ("④ SSL(https)確認", "ほぼ自動・少し待つ", ORANGE),
    ("⑤ テーマ有効化", "Cocoonの子テーマ", ORANGE),
    ("⑥ プラグイン", "最低限だけ入れる", GRAY),
    ("⑦ 記事を公開", "下手でもまず1本", "#1faf6a"),
]

# 2行レイアウト(4 + 3)
positions = [(0.3, 3.2), (2.7, 3.2), (5.1, 3.2), (7.5, 3.2),
             (1.5, 1.2), (3.9, 1.2), (6.3, 1.2)]
w, h = 2.2, 1.3
for (title, sub, c), (x, y) in zip(steps, positions):
    box(ax, x, y, w, h, "", c)
    ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center",
            color="white", fontsize=12.5, fontweight="bold")
    ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center",
            color="white", fontsize=9.5)

# 矢印(上段右へ→折返し→下段右へ)
def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                 mutation_scale=18, lw=2, color=NAVY))


for i in range(3):
    x = positions[i][0] + w
    arrow(x + 0.02, 3.85, x + 0.18, 3.85)
# 折返し(④→⑤)
arrow(7.5 + w / 2, 3.1, 1.5 + w / 2, 2.55)
for i in range(4, 6):
    x = positions[i][0] + w
    arrow(x + 0.02, 1.85, x + 0.18, 1.85)

ax.text(5, 0.35, "費用は月1,000円ほど（年1万円ほど）／初期費用は無料",
        ha="center", va="center", fontsize=11.5, color=GRAY)

out = os.path.join(IMG, "blog-start-flow.png")
fig.savefig(out, dpi=130, bbox_inches="tight", facecolor="white")
print("saved:", out)
