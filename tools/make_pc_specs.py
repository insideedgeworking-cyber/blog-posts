# -*- coding: utf-8 -*-
"""PC用語記事(post_002)用：ゲーム快適度別のグラボ目安の図を生成。
2026年6月時点の目安。価格・型番は変動するため要更新。"""
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

def make_table(fname, title, header, rows, widths, note, figh=3.2):
    fig, ax = plt.subplots(figsize=(10.8, figh), dpi=160); ax.axis("off")
    tbl = ax.table(cellText=rows, colLabels=header, cellLoc="center", loc="center", colWidths=widths)
    tbl.auto_set_font_size(False); tbl.scale(1, 2.1)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#e3e9f0"); t = cell.get_text()
        if r == 0:
            cell.set_facecolor(BLUE); t.set_color("white"); t.set_fontproperties(fp(11, "bold"))
        else:
            cell.set_facecolor("#ffffff" if r % 2 else "#f5f8fc")
            t.set_fontproperties(fp(10.5 if c > 0 else 10.5, "bold" if c == 0 else "normal"))
            if c == 0: t.set_color(BLUE)
    ax.set_title(title, fontproperties=fp(14.5, "bold"), loc="left", x=0, pad=12)
    fig.text(0.012, 0.04, note, fontproperties=fp(7.5), color="#9aa0a6")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.84, bottom=0.12)
    fig.savefig(os.path.join(IMG, fname), facecolor="white", bbox_inches="tight"); plt.close(fig)
    print("saved", fname)

make_table("gpu-gaming.png", "ゲームを快適に遊ぶグラボ（GPU）の目安（2026年6月）",
    ["遊び方の目安", "おすすめグラボ", "VRAM", "グラボ価格の目安"],
    [
        ["フルHD・60fps（PS5並み）", "RTX 5060", "8GB", "約4〜5万円"],
        ["フルHD・144fpsでヌルヌル／WQHD", "RTX 5060 Ti 16GB ／ RX 9060 XT", "16GB", "約7万円台"],
        ["4K・最高画質をガチで", "RTX 4070 Ti SUPER 以上", "16GB〜", "約15万円〜"],
    ],
    [0.32, 0.31, 0.11, 0.26],
    "※グラボ単体の目安。PC全体だと約15〜30万円。fps=1秒間のコマ数で大きいほど滑らか。価格は変動大なので最新を確認。",
    figh=2.7)
