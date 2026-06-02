# -*- coding: utf-8 -*-
"""副業ジャンル別 月収レンジの横棒グラフを生成する。
出典: アフィリエイトマーケティング協会(2025) / poten社 副業平均収入調査(2025) ほか。
上限値は成功者の水準であり、多くの人は初期は低水準である点を注記する。"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 日本語フォント（Windows同梱の游ゴシック→なければメイリオ）
font_path = None
for cand in (r"C:\Windows\Fonts\YuGothM.ttc", r"C:\Windows\Fonts\meiryo.ttc",
             r"C:\Windows\Fonts\YuGothR.ttc", r"C:\Windows\Fonts\msgothic.ttc"):
    if os.path.exists(cand):
        font_path = cand
        break
fp = font_manager.FontProperties(fname=font_path)

# (ラベル, 下限, 上限, 上限表記)
data = [
    ("ブログ・アフィリエイト", 0, 100, "100万円超"),
    ("コンテンツ販売\n(note・Booth)", 0, 50, "50万円超"),
    ("動画編集", 5, 30, "30万円"),
    ("せどり・物販", 3, 30, "30万円"),
    ("Webライター", 3, 20, "20万円"),
]
# 上から見やすいよう逆順で描画
data = data[::-1]

labels = [d[0] for d in data]
lows = [d[1] for d in data]
highs = [d[2] for d in data]
caps = [d[3] for d in data]

fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
y = range(len(data))
colors = ["#4f8cff", "#5aa9e6", "#5fb878", "#f0a93b", "#e8694f"]

for i, (lo, hi) in enumerate(zip(lows, highs)):
    ax.barh(i, hi - lo, left=lo, height=0.55, color=colors[i % len(colors)],
            edgecolor="white", zorder=3)
    # 右端にレンジ表記（下限〜上限）
    range_label = f"{lo}〜{caps[i]}"
    ax.text(hi + 2.0, i, range_label, va="center", ha="left",
            fontproperties=fp, fontsize=10.5, color="#333")

ax.set_yticks(list(y))
ax.set_yticklabels(labels, fontproperties=fp, fontsize=11)
ax.set_xlim(0, 132)
ax.set_xlabel("月収の目安（万円）", fontproperties=fp, fontsize=11)
ax.set_title("副業ジャンル別 月収レンジの目安", fontproperties=fp,
             fontsize=15, fontweight="bold", pad=14)
ax.grid(axis="x", color="#e6e6e6", zorder=0)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="x", labelsize=9)

# 注記
fig.text(0.012, 0.015,
         "※上限は成功者の水準。アフィリは月1,000円未満が約4割・1万円超えに半年ほどとも。"
         "／出典:アフィリエイトマーケティング協会2025・poten社調査ほか",
         fontproperties=fp, fontsize=7.3, color="#888")

plt.tight_layout(rect=(0, 0.04, 1, 1))
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "images", "fukugyo-income.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=150, facecolor="white", bbox_inches="tight")
print("saved:", out)
