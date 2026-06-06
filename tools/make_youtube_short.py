# -*- coding: utf-8 -*-
"""YouTube記事(post_008/009)用：ショートフィードの仕組み図を生成。
最初は少人数に表示→反応が良ければ段階的に拡大、を可視化。
注意: matplotlibのtextで $ は数式扱いになるため使わない。"""
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
def fp(sz, w="normal"):
    f = font_manager.FontProperties(fname=_fp); f.set_size(sz); f.set_weight(w); return f
BLUE = "#2f6fb3"; DARK = "#1d4778"; ORANGE = "#ff7a3d"; RED = "#e05a5a"

fig, ax = plt.subplots(figsize=(11.2, 4.6), dpi=160); ax.axis("off")
ax.set_xlim(0, 12); ax.set_ylim(0, 5)

stages = [
    (1.5, "投稿直後", "まず最初の\n数十人に表示"),
    (4.4, "反応◎なら", "数百人へ\n拡大"),
    (7.3, "さらに◎なら", "数千人へ"),
    (10.2, "伸び続ければ", "数万人〜\nバズ"),
]
colors = ["#e8f0fe", "#cfe0fa", "#a9c7f3", BLUE]
tcols  = [DARK, DARK, DARK, "white"]
bw, bh, y = 2.1, 1.5, 3.1
for i, (x, head, body) in enumerate(stages):
    ax.add_patch(FancyBboxPatch((x-bw/2, y-bh/2), bw, bh, boxstyle="round,pad=0.02,rounding_size=0.12",
                 fc=colors[i], ec="#c3d3ea", lw=1.2))
    ax.text(x, y+0.38, head, ha="center", va="center", fontproperties=fp(11.5, "bold"), color=tcols[i])
    ax.text(x, y-0.28, body, ha="center", va="center", fontproperties=fp(11, "bold"), color=tcols[i])
    if i < 3:
        ax.annotate("", xy=(stages[i+1][0]-bw/2-0.05, y), xytext=(x+bw/2+0.05, y),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.4))
        ax.text((x+stages[i+1][0])/2, y+0.5, "視聴維持・\nエンゲージ◎", ha="center", va="center",
                fontproperties=fp(8.5), color=BLUE)

# 反応が悪いと止まる（赤の注意）
ax.annotate("", xy=(2.9, 1.15), xytext=(1.5, y-bh/2-0.05),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2, linestyle=(0,(4,2))))
ax.add_patch(FancyBboxPatch((3.0, 0.55), 6.2, 1.15, boxstyle="round,pad=0.02,rounding_size=0.1",
             fc="#fff0f0", ec="#f3c2c2", lw=1.2))
ax.text(6.1, 1.12, "反応が悪い（最後まで見られない・エンゲージ低い）と…",
        ha="center", va="center", fontproperties=fp(10.5, "bold"), color=RED)
ax.text(6.1, 0.8, "ここで拡散ストップ。おすすめに乗らず再生が伸びない",
        ha="center", va="center", fontproperties=fp(9.5), color="#a05a5a")

ax.set_title("YouTubeショートが広がる仕組み（ショートフィード）", fontproperties=fp(15, "bold"), loc="left", x=0.01, pad=12)
fig.text(0.012, 0.02, "※勝負は“量”より「最初の数十人に刺さるか」。冒頭2秒・視聴維持が次の拡大を呼ぶ。",
         fontproperties=fp(8.5), color="#9aa0a6")
fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.10)
fig.savefig(os.path.join(IMG, "youtube-shortfeed.png"), facecolor="white", bbox_inches="tight"); plt.close(fig)
print("saved youtube-shortfeed.png")
