# -*- coding: utf-8 -*-
"""ブログ用の収入グラフを生成する。
1) 副業ジャンル別の月収レンジ（fukugyo-income.png）
2) 職業別の平均年収比較 飲食/全業種平均/IT・PC系/AI系（shokugyo-income.png）

参考ブログ(ヒトデ/副業コンパス/きつねコード等)に倣い、淡い同系色・余白多め・
グリッド控えめのクリーンなスタイル。出典は各図に注記。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
os.makedirs(IMG_DIR, exist_ok=True)

# 日本語フォント（Windows同梱の游ゴシック→なければメイリオ）
_font_path = None
for _cand in (r"C:\Windows\Fonts\YuGothM.ttc", r"C:\Windows\Fonts\meiryo.ttc",
              r"C:\Windows\Fonts\YuGothR.ttc", r"C:\Windows\Fonts\msgothic.ttc"):
    if os.path.exists(_cand):
        _font_path = _cand
        break
FP = font_manager.FontProperties(fname=_font_path)


def _fp(size, weight="normal"):
    f = FP.copy()
    f.set_size(size)
    f.set_weight(weight)
    return f


def make_chart(filename, title, rows, xlabel, xmax, note):
    """rows: list of (label, lo, hi, value_text, color)。
    lo==hi の場合は単一値の棒。余白広めで描画する。"""
    n = len(rows)
    # 余白を広めに：1項目あたり高さ0.9inを確保
    fig_h = 1.7 + n * 0.92
    fig, ax = plt.subplots(figsize=(9.2, fig_h), dpi=160)

    rows = rows[::-1]  # 上から順に並ぶように反転
    bar_h = 0.46       # 細めの棒＋広い隙間でスッキリ
    for i, (label, lo, hi, vtxt, color) in enumerate(rows):
        ax.barh(i, hi - lo, left=lo, height=bar_h, color=color,
                edgecolor="white", linewidth=1.2, zorder=3)
        ax.text(hi + xmax * 0.02, i, vtxt, va="center", ha="left",
                fontproperties=_fp(11.5), color="#444")

    ax.set_yticks(range(n))
    ax.set_yticklabels([r[0] for r in rows], fontproperties=_fp(12))
    ax.set_ylim(-0.7, n - 0.3)        # 上下に余白
    ax.set_xlim(0, xmax)
    ax.set_xlabel(xlabel, fontproperties=_fp(11.5), labelpad=10)
    ax.set_title(title, fontproperties=_fp(16.5, "bold"), pad=20, loc="left", x=0.0)

    ax.grid(axis="x", color="#eef1f4", linewidth=1, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#dfe3e8")
    ax.tick_params(axis="x", labelsize=9.5, colors="#888", length=0)
    ax.tick_params(axis="y", length=0)

    fig.text(0.013, 0.022, note, fontproperties=_fp(7.6), color="#9aa0a6")

    # 余白：左にラベル分、下に注記分を確保
    fig.subplots_adjust(left=0.235, right=0.965, top=0.84, bottom=0.16 + 0.015 * n)
    out = os.path.join(IMG_DIR, filename)
    fig.savefig(out, dpi=160, facecolor="white")
    plt.close(fig)
    print("saved:", out)


# 同系色パレット（淡いブルー基調＋ポイント色）
BLUE = "#6f9fd8"        # 標準
BLUE_LT = "#a9c6e6"     # 薄い
CORAL = "#e88a73"       # 低い側の強調（飲食）
GREEN = "#5cb389"       # 高い側の強調（AI）

# 1) 副業ジャンル別 月収レンジ ----------------------------------------
make_chart(
    "fukugyo-income.png",
    "副業ジャンル別 月収レンジの目安",
    [
        ("ブログ・\nアフィリエイト", 0, 100, "0〜100万円超", BLUE),
        ("コンテンツ販売\n(note・Booth)", 0, 50, "0〜50万円超", BLUE_LT),
        ("動画編集", 5, 30, "5〜30万円", BLUE_LT),
        ("せどり・物販", 3, 30, "3〜30万円", BLUE_LT),
        ("Webライター", 3, 20, "3〜20万円", BLUE_LT),
    ],
    "月収の目安（万円）",
    132,
    "※上限は成功者の水準。アフィリは月1,000円未満が約4割・1万円超えに半年ほどとも。"
    "／出典: アフィリエイトマーケティング協会2025・poten社調査ほか",
)

# 2) 職業別 平均年収の比較 --------------------------------------------
make_chart(
    "shokugyo-income.png",
    "職業別 平均年収の比較",
    [
        ("飲食業", 0, 358, "約358万円", CORAL),
        ("全業種の平均", 0, 458, "約458万円", BLUE_LT),
        ("IT・PC系\nエンジニア", 0, 550, "約550万円", BLUE),
        ("AI・機械学習\nエンジニア", 0, 650, "約650万円", GREEN),
    ],
    "平均年収（万円）",
    760,
    "※出典: 国税庁 民間給与実態統計(全業種平均)・厚労省 job tag・求人ボックス 給料ナビ"
    "・doda/パーソルキャリア(2024〜2025) を基に作成。金額は目安。",
)
