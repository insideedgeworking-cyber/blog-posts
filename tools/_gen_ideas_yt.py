# -*- coding: utf-8 -*-
"""参考動画(おさむ/中の人/abemutsuki)由来のYouTube記事アイデアを idea スタブで大量作成(post_053〜)。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")

IDEAS = [
 ("YouTubeショートが伸びない原因と対策","おさむ『伸びない7つ/9つの原因』。冒頭/ジャンル/量産/設定。post_008(失敗談)と差別化し原因→対策の実用記事に。",["YouTubeショート","伸びない","原因","対策","初心者"]),
 ("YouTubeショートで再生数を伸ばす方法（100万再生の型）","おさむ『100万再生連発の伸ばし方』。冒頭2秒/ループ/テンポ/ジャンル選定。",["YouTubeショート","伸ばし方","再生数","100万再生","バズ"]),
 ("YouTube収益化の条件と達成までの道のり（フェーズ別）","おさむ『収益化条件達成までの壁(1〜4ヶ月目)』。登録者1000人/4000時間/ショート要件。",["YouTube収益化","条件","達成","フェーズ","初心者"]),
 ("YouTube収益化ポリシー｜NGコンテンツとAIの扱い","おさむ『7/15ポリシー変更・7つの誤解』。合成音声/AI動画はどこまでOKか・量産NG。",["YouTube収益化","ポリシー","NG","AI","規約"]),
 ("YouTube収益化停止から復活する方法（再審査請求）","おさむ『再審査請求で復活100%』。停止の原因と再審査の書き方。",["YouTube","収益化停止","復活","再審査請求","対処"]),
 ("顔出しなしYouTubeの作り方（AI活用）","台本→AI音声→編集で顔出しなし。雑学/解説/骸骨ショート等のジャンル。",["顔出しなし","YouTube","作り方","AI","ショート"]),
 ("AIでYouTubeショートを量産する方法（Vrew×ChatGPT）","おさむ『Vrew×ChatGPTで1日10本』。台本→自動編集の手順。ただし量産だけはNGの注意も。",["YouTubeショート","量産","Vrew","ChatGPT","AI"]),
 ("ショートをインスタ・Facebookに使い回して稼ぐ","おさむ『リール流用で月3万/Facebookショート収益化』。1本を複数SNSで使い回す動線。",["YouTubeショート","使い回し","インスタリール","Facebook","収益化"]),
 ("TuneCoreの登録〜配信・審査のやり方（BGM収益）","おさむ『TuneCore完全保存版』。登録→配信→審査→レポートの見方。post_023(BGM)の実務深掘り。",["TuneCore","登録","配信","審査","BGM収益"]),
 ("BGM収益の単価が高いジャンル","おさむ『BGM単価が高いジャンルTOP13』。プレミアム視聴者が多いジャンルほど高い。",["BGM収益","単価","ジャンル","YouTubeショート","ランキング"]),
 ("YouTube動画編集ソフトの使い方（CapCut・Vrew）","おさむ/中の人『CapCut・VREWの使い方』。初心者向けカット/テロップ/BGM。無料・商用利用。",["動画編集","CapCut","Vrew","使い方","初心者"]),
 ("AI音声VOICEVOXの使い方（商用利用OK）","おさむ『VOICEVOX完全解説』。無料・商用利用可のAIナレーション。ショート/解説動画に。",["VOICEVOX","AI音声","使い方","商用利用","ナレーション"]),
 ("YouTubeショートが伸びるハッシュタグの付け方","おさむ『伸びるハッシュタグ』。付け方/個数/ジャンル認知。",["YouTubeショート","ハッシュタグ","付け方","伸びる","SEO"]),
 ("ショート投稿後に再生数を伸ばす設定・方法","おさむ『出した後に伸ばす5つ/爆伸びする設定』。エンゲージビュー/初速/概要欄。",["YouTubeショート","設定","再生数","伸ばす","投稿後"]),
 ("YouTube長尺チャンネルの育て方","中の人『100ch運営ノウハウ』。長尺の視聴維持/初動/ロードマップ。ショートとの両輪。",["YouTube","長尺","チャンネル","育て方","運営"]),
 ("YouTubeのサムネイル・タイトルの作り方","中の人『10万再生のサムネの型/プロの企画台本』。クリック率を上げる型。",["YouTube","サムネイル","タイトル","作り方","クリック率"]),
 ("YouTubeのジャンル・企画の選び方（ブルーオーシャン）","中の人『伸びる企画』。レッド/ブルーオーシャン、伸びてる隙間を狙う。",["YouTube","ジャンル","企画","選び方","ブルーオーシャン"]),
 ("VidIQの使い方（YouTube分析ツール）","YouTube対策『VidIQ完全ガイド』。キーワード/Outliers/競合分析。料金。",["VidIQ","YouTube","分析ツール","使い方","キーワード"]),
 ("AIショート量産は稼げない？正直な注意点","おさむ『AIショート副業で稼ぐのは無理』。誇大広告に注意・量産NG・独自性が必須。",["AIショート","量産","稼げない","注意","誇大広告"]),
 ("YouTubeショート初期の再生数の相場と伸びる前兆","おさむ『初期の再生回数相場/伸びる前兆5選』。最初は数十回が普通・伸びるサイン。",["YouTubeショート","初期","再生数","相場","前兆"]),
]

start = 53
for i,(theme,ideas,kw) in enumerate(IDEAS):
    pid = f"post_{start+i:03d}"
    fp = os.path.join(PD, f"{pid}.json")
    if os.path.exists(fp):
        print("既存→skip", pid); continue
    d = {"id":pid,"created_at":"2026-06-13","theme":theme,"ideas":ideas,
         "title":"","category":"YouTube","keywords":kw,"body":"","char_count":0,
         "status":"idea","wp_post_id":None,
         "notes":"参考動画(おさむ/中の人/abemutsuki・YouTube対策md)由来のYouTube記事アイデア(2026-06-13)。柱: YouTube。"}
    json.dump(d, open(fp,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"created {pid}: {theme}")
print("done")
