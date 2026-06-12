# -*- coding: utf-8 -*-
"""AIライティングの記事アイデアを idea スタブで大量作成。参考動画+YouTube検索由来。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")

IDEAS = [
 ("AIライティングとは？メリット・デメリット","初心者向けに概要。時短/アイデア出しが強み、ハルシネーション/独自性不足が弱み。",["AIライティング","とは","メリット","デメリット","初心者"]),
 ("ブログ記事をAIで書く手順（ChatGPT/Claude）","キーワード→構成→本文→リライトの実手順。10分で下書きを作る流れ。",["AIライティング","ブログ記事","書き方","ChatGPT","手順"]),
 ("AIライティングのプロンプト集（構成・見出し・本文）","そのまま使えるプロンプト。構成案/見出し/リード/本文/リライト/FAQ生成。",["AIライティング","プロンプト","テンプレート","ChatGPT","SEO"]),
 ("AIで書いた記事はSEOで評価される？Googleの見解","AI記事はOKだが「誰が・何のため」が大事。E-E-A-Tと一次情報で差別化。",["AI記事","SEO","Google","評価","E-E-A-T"]),
 ("AI記事を“人間らしく”仕上げるリライトのコツ","AIっぽさの消し方。体験/数字/口調/具体例を足す。冗長表現カット。",["AIライティング","リライト","人間らしく","コツ","AI感"]),
 ("AIライティングツール比較（ChatGPT/Claude/Gemini）","汎用AIの比較。文章の質/長文/リサーチ/料金。用途別おすすめ。",["AIライティング","ツール","比較","ChatGPT","Claude"]),
 ("AI専用ライティングツール比較（ラクリン/Catchy等）","SEO特化の専用ツール(ラクリン/Catchy/SAKUBUN/Transcope/value AI Writer)を比較。",["AIライティングツール","ラクリン","Catchy","比較","SEO"]),
 ("AIで記事を量産する方法と注意点（ペナルティ回避）","量産の手順と、薄い量産がGoogleに嫌われる理由。独自性の担保。",["AI記事","量産","SEO","ペナルティ","注意"]),
 ("AIライティングで稼ぐ方法（記事作成代行・Webライター）","クラウドソーシングで記事作成を受注。AIで高速化→仕上げて納品。単価。",["AIライティング","稼ぐ","Webライター","記事作成代行","副業"]),
 ("AIに正確な情報を書かせる（ハルシネーション対策）","嘘を書かせない指示/ディープリサーチ/参考URLでファクトチェック。",["AIライティング","ハルシネーション","ファクトチェック","正確","対策"]),
 ("ChatGPTのモデル使い分け（4o/o3/o1）でライティング","用途別の最適モデル。軽い文章は4o、深い記事はo3/o1 pro。アウトライン→編集。",["ChatGPT","モデル","使い分け","ライティング","o3"]),
 ("AIで記事の構成（アウトライン）を作る方法","読者の検索意図→見出し構成をAIで。アウトラインはAI・編集は人間。",["AIライティング","構成","アウトライン","見出し","作り方"]),
 ("AIライティング×WordPress（下書き→投稿の効率化）","AIの下書きをWordPressへ。装飾/表/画像/内部リンクの仕上げ。",["AIライティング","WordPress","効率化","下書き","投稿"]),
 ("AIライティングの始め方（未経験向けロードマップ）","必要なAI/最初の1記事/上達の流れ。未経験が今日から始める手順。",["AIライティング","始め方","未経験","ロードマップ","初心者"]),
 ("無料で使えるAIライティングツール","無料で試せるAI(ChatGPT無料/Gemini/Copilot等)と無料枠の限界。",["AIライティング","無料","ツール","おすすめ","初心者"]),
 ("AIライティングは稼げる？仕事の取り方","稼げるかの現実。案件の取り方/ポートフォリオ/単価の上げ方。",["AIライティング","稼げる","仕事","取り方","副業"]),
 ("AIと人間の役割分担（どこをAI・どこを人間）","リサーチ/構成/下書き=AI、体験/事実確認/編集/独自性=人間。",["AIライティング","役割分担","AIと人間","編集","コツ"]),
 ("AI記事がGoogleペナルティを受けないために","スパム的量産を避ける/一次情報/E-E-A-T/開示。安全な運用。",["AI記事","ペナルティ","Google","回避","E-E-A-T"]),
 ("AIライティングのコピペ・著作権の注意点","コピペチェック/既存記事との類似/学習データの著作権。安全に使う。",["AIライティング","コピペ","著作権","注意","チェック"]),
 ("AIで魅力的なタイトル・リード文を書くプロンプト","クリックされるタイトル/離脱させないリード文の生成プロンプト。",["AIライティング","タイトル","リード文","プロンプト","クリック率"]),
]

# 既存の最大番号の次から（既存ファイルはskip）
existing = set(int(os.path.basename(f)[5:8]) for f in __import__('glob').glob(os.path.join(PD,'post_*.json')))
n = max(existing)+1
created=0
for theme,ideas,kw in IDEAS:
    while f"post_{n:03d}" in {f"post_{e:03d}" for e in existing}: n+=1
    pid=f"post_{n:03d}"; existing.add(n)
    fp=os.path.join(PD,f"{pid}.json")
    d={"id":pid,"created_at":"2026-06-13","theme":theme,"ideas":ideas,
       "title":"","category":"AIライティング","keywords":kw,"body":"","char_count":0,
       "status":"idea","wp_post_id":None,
       "notes":"AIライティング記事アイデア。参考動画+YouTube検索(GPTモデル比較/ブログ記事作成/専用ツール等)由来(2026-06-13)。"}
    json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"created {pid}: {theme}"); created+=1; n+=1
# 既存 post_032(AIライティング) もカテゴリ統一
fp32=os.path.join(PD,"post_032.json")
if os.path.exists(fp32):
    d=json.load(open(fp32,encoding="utf-8-sig")); d["category"]="AIライティング"
    json.dump(d,open(fp32,"w",encoding="utf-8"),ensure_ascii=False,indent=2); print("post_032 -> AIライティング(カテゴリ統一)")
print("done created:",created)
