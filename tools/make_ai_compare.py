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
    ["Cowork", "デスクトップアプリ", "Claude(約3,000円)に込み", "ノーコード寄り。ファイル/Office作業を自動化"],
    ["OpenAI Codex", "ターミナル/クラウド", "ChatGPT(無料〜)に込み", "任せて待つ“おまかせ”型。大きな作業向き"],
    ["GitHub Copilot", "エディタの中", "月10ドル〜", "書きながら補完・相談。二人三脚で"],
    ["Cursor", "AI専用エディタ", "月20ドル〜", "VS Code型。エディタごとAI化"],
]
fig, ax = plt.subplots(figsize=(10.8, 3.6), dpi=160); ax.axis("off")
tbl = ax.table(cellText=data3, colLabels=header3, cellLoc="center", loc="center",
               colWidths=[0.19, 0.2, 0.26, 0.35])
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
fig.text(0.012, 0.04, "※Coworkはノーコード寄りで初心者にも。料金はチャット版の契約に含まれることが多い。改定あり。", fontproperties=fp(7.5), color="#9aa0a6")
fig.subplots_adjust(left=0.02, right=0.98, top=0.84, bottom=0.1)
fig.savefig(os.path.join(IMG,"ai-coding.png"), facecolor="white", bbox_inches="tight"); plt.close(fig)
print("saved ai-coding.png")

# 4) プラン×機能の早見表（どのプランに何が含まれるか） ----------------
def make_matrix(fname, title, header, rows, note):
    fig, ax = plt.subplots(figsize=(10.4, 0.7 + 0.62*(len(rows)+1)), dpi=160); ax.axis("off")
    tbl = ax.table(cellText=rows, colLabels=header, cellLoc="center", loc="center",
                   colWidths=[0.28, 0.18, 0.18, 0.18, 0.18])
    tbl.auto_set_font_size(False); tbl.scale(1, 2.1)
    for (r,c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#e3e9f0"); t = cell.get_text()
        if r == 0:
            cell.set_facecolor(BLUE); t.set_color("white"); t.set_fontproperties(fp(10.5,"bold"))
        elif c == 0:
            cell.set_facecolor("#eef3f9"); t.set_color("#1d3a5f"); t.set_fontproperties(fp(10.5,"bold")); t.set_ha("left")
            cell.PAD = 0.04
        else:
            cell.set_facecolor("#ffffff" if r%2 else "#f7fafd"); t.set_fontproperties(fp(10.5))
            s = t.get_text()
            if s == "○": t.set_color("#2e9e5b")
            elif s == "×": t.set_color("#c64b3c")
    ax.set_title(title, fontproperties=fp(14.5,"bold"), loc="left", x=0, pad=12)
    fig.text(0.012, 0.03, note, fontproperties=fp(7.5), color="#9aa0a6")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.12)
    fig.savefig(os.path.join(IMG, fname), facecolor="white", bbox_inches="tight"); plt.close(fig)
    print("saved", fname)

make_matrix("chatgpt-plans.png", "ChatGPT プラン×機能（2026年6月）",
    ["機能 ＼ プラン", "Free", "Go\n約1,500円", "Plus\n約3,000円", "Pro\n約32,000円"],
    [
        ["使えるAIモデル", "標準(制限)", "多め", "最新・高性能", "最上位"],
        ["メッセージ量", "少", "中", "多", "最大"],
        ["Deep Research(深い調査)", "×", "△", "○", "○"],
        ["画像生成", "△制限", "○", "○", "○"],
        ["Codex(コーディング)", "△お試し", "△", "○", "○"],
        ["広告", "あり", "あり", "なし", "なし"],
    ],
    "※Codexは単体契約ではなくChatGPTの契約に“含まれる”。実用はPlus以上が目安。動画生成Soraは2026年に終了。20ドル≒約3,000円換算。改定あり。")

make_matrix("claude-plans.png", "Claude プラン×機能（2026年6月）",
    ["機能 ＼ プラン", "Free", "Pro\n約3,000円", "Max 5x\n約16,000円", "Max 20x\n約32,000円"],
    [
        ["最新モデル(Opus)", "×", "○", "○", "○"],
        ["Claude Code(自動作業)", "×", "○", "○", "○"],
        ["Cowork(ノーコード自動化)", "×", "○", "○", "○"],
        ["Projects/リサーチ", "△", "○", "○", "○"],
        ["使える量の目安", "少", "基準", "5倍", "20倍"],
    ],
    "※Claude Code・CoworkはPro以上に“含まれる”(追加料金なし)。Max 5x/20xは機能は同じで使用量の差。20ドル≒約3,000円換算。改定あり。")

make_matrix("gemini-plans.png", "Gemini プラン×機能（2026年6月）",
    ["機能 ＼ プラン", "無料", "AI Plus\n1,200円", "AI Pro\n2,900円", "AI Ultra\n14,500円〜"],
    [
        ["Deep Research(深い調査)", "月5回", "○", "1日20回", "1日120回"],
        ["Veo(動画生成)", "×", "△", "○(高速)", "○(音声付)"],
        ["AIクレジット(画像/動画量)", "少", "200", "1,000", "25,000"],
        ["Googleストレージ", "15GB", "200GB", "2TB", "20TB〜"],
        ["NotebookLM上位機能", "基本のみ", "○", "○(拡大)", "○(最大)"],
        ["Deep Think(高度な推論)", "×", "×", "×", "○"],
    ],
    "※NotebookLMの上位機能はAI Plus以上に“含まれる”。AI Plusは最初の2か月600円、AI Proは初月無料。Ultraは20TB/30TBの2段階。改定あり。")

# 5) 汎用テーブル（画像生成・動画生成の比較用） ----------------------
def make_table(fname, title, header, rows, widths, note, figh=3.0):
    fig, ax = plt.subplots(figsize=(10.6, figh), dpi=160); ax.axis("off")
    tbl = ax.table(cellText=rows, colLabels=header, cellLoc="center", loc="center", colWidths=widths)
    tbl.auto_set_font_size(False); tbl.scale(1, 2.0)
    for (r,c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#e3e9f0"); t = cell.get_text()
        if r == 0:
            cell.set_facecolor(BLUE); t.set_color("white"); t.set_fontproperties(fp(10.5,"bold"))
        else:
            cell.set_facecolor("#ffffff" if r%2 else "#f5f8fc")
            t.set_fontproperties(fp(10.5 if c>0 else 11, "bold" if c==0 else "normal"))
            if c==0: t.set_color(BLUE)
            s = t.get_text()
            if s.startswith("○"): t.set_color("#2e9e5b")
            elif s == "×": t.set_color("#c64b3c")
    ax.set_title(title, fontproperties=fp(14.5,"bold"), loc="left", x=0, pad=12)
    fig.text(0.012, 0.04, note, fontproperties=fp(7.5), color="#9aa0a6")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.84, bottom=0.1)
    fig.savefig(os.path.join(IMG, fname), facecolor="white", bbox_inches="tight"); plt.close(fig)
    print("saved", fname)

make_table("image-gen.png", "画像生成AIの比較（2026年6月）",
    ["ツール", "無料", "料金の目安", "特徴・向いてる用途"],
    [
        ["ChatGPT(画像)", "△制限", "Plus 約3,000円", "会話で指示・部分修正が得意。万能型"],
        ["Gemini(Nano Banana)", "○ 1日約100回", "無料〜2,900円", "日本語の文字入れに強い。無料枠が多い"],
        ["Midjourney", "×", "月10ドル〜", "アート/イラストが最高品質。商用OK(有料)"],
        ["Adobe Firefly", "△", "Adobe契約", "商用利用が安心。Photoshop等と連携"],
        ["Canva", "○", "無料〜", "デザインと一体。SNS・バナー作成向き"],
    ],
    [0.2, 0.16, 0.2, 0.44],
    "※商用利用の可否は各サービスの規約を必ず確認。料金・仕様は改定あり。", figh=3.4)

make_table("video-gen.png", "動画生成AIの比較（2026年6月）",
    ["ツール", "料金の目安", "特徴"],
    [
        ["Google Veo (Gemini)", "AI Pro 2,900円〜", "現在の本命。高品質。Ultraで音声付き"],
        ["Grok Imagine (Grok)", "Lite 980円〜", "安く動画も作れる。Xと相性がよい"],
        ["Runway", "月12ドル〜", "プロ向け。映像品質が最高峰"],
        ["Kling", "無料枠あり", "無料枠が充実。音声も同時に生成"],
        ["Pika", "低価格", "高速・手軽に短い動画を作れる"],
    ],
    [0.26, 0.24, 0.5],
    "※OpenAIのSoraは2026年に終了し、現在ChatGPTでは動画生成は使えません。料金・仕様は改定あり。", figh=3.4)

make_table("research-compare.png", "リサーチに強いAIの比較（2026年6月）",
    ["ツール", "無料", "料金の目安", "得意なこと"],
    [
        ["Perplexity", "○", "Pro 約3,000円", "出典つきでネット全体を調べる"],
        ["NotebookLM", "○", "Google AIに込み", "自分の資料だけから回答・音声化"],
        ["Gemini Deep Research", "月5回", "Geminiに含まれる", "テーマを自動で深掘り調査"],
    ],
    [0.26, 0.13, 0.24, 0.37],
    "※リサーチ＝ネット全体はPerplexity、自分の資料はNotebookLMが得意。料金・仕様は改定あり。", figh=2.7)
