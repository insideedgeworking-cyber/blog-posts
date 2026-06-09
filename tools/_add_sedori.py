# -*- coding: utf-8 -*-
"""post_022 に「せどり・物販 × AI」を追加（①グループの末尾、②-1の前に挿入）。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")
fp = os.path.join(PD, "post_022.json")
d = json.load(open(fp, encoding="utf-8-sig"))
b = d["body"]

sedori = """## ①-4 せどり・物販 × AI（“仕入れて売る”をAIで時短）
店舗やネットで安く仕入れ、フリマ・ECで高く売る昔ながらの物販。AIが直接モノを作るわけではありませんが、いちばん時間がかかる**「リサーチ」と「出品」をAIで大幅に短縮**できます。在庫を持つ分、即金性が高いのが魅力です。

- **AIで効率化できるところ**：
  - 利益計算：商品名・仕入れ値・販売相場・手数料をChatGPTに渡して、利益額・利益率・損益分岐点をその場で計算
  - 売れ筋・トレンドのリサーチ：「今需要が伸びているジャンル」「型落ちで値上がりしやすい商品」などの調べ物・壁打ち
  - 出品文の自動作成：メルカリ・Amazon・ヤフオク用のタイトル・商品説明をAIで量産
  - 写真の補正：背景除去や明るさ調整をAI画像ツールで
- **手順**：ジャンルを決める → AIと相場・利益をリサーチ → 仕入れ → AIで出品文を作って出品 → 売れたら梱包・発送
- **使うAI・ツール**：ChatGPT／Claude／（相場確認は各フリマ・ECの売却履歴やリサーチツール）
- **収益の目安**：1品数百～数千円の利益から。回転重視で積み上げる。即金性は高い
- **ここだけ注意（他の方法と違う点）**：この記事の他の無在庫系と違い、**仕入れ資金と在庫リスクがある**唯一のタイプです。AIで全自動にはならず（仕入れ・梱包・発送は手作業）、AIはあくまでリサーチと出品の“時短”。また、継続的に仕入れて売るなら**古物商許可**が必要になる場合があります

"""

anchor = "## ②-1 AIブログ × アフィリエイト"
if "①-4 せどり" in b:
    print("既に存在 → skip")
elif anchor in b:
    b = b.replace(anchor, sedori + anchor, 1)
    print("せどりセクション挿入 OK")
else:
    print("[!] anchor不一致 → 中止"); sys.exit(1)

# ①の説明bulletに「せどり（物販）」を追記
oldbul = "すぐ試せて小さく稼ぐ** … 楽天ROOM／無在庫販売（SUZURI）／LINEスタンプ"
newbul = oldbul + "／せどり（物販）"
if oldbul in b:
    b = b.replace(oldbul, newbul, 1); print("①bullet 更新 OK")
else:
    print("①bullet skip")

d["body"] = b
d["char_count"] = len(b)
d["excerpt"] = "AIを使った副業の種類を3タイプ（0→1／資産型／発信・スキル）で整理。楽天ROOM・無在庫(SUZURI)・LINEスタンプ・せどり・AIブログ・顔出しなしYouTube・AI絵本・インスタ・ライティング代行・動画編集代行・ココナラ出品を、手順・使うツール・収益の目安・注意点まで具体的に解説。誇大広告の見抜き方も。"
json.dump(d, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("post_022 char=", d["char_count"])
