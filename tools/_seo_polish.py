# -*- coding: utf-8 -*-
"""SEO仕上げ:タイトル短縮(023/136/138)・137のH3階層化と税金節整理とキーワード調整・138のH3階層化。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")

def load(n):
    fp=os.path.join(PD,f"post_{n}.json"); return fp, json.load(open(fp,encoding="utf-8-sig"))
def repl(b, old, new, tag):
    if old not in b: print(f"  [!!] {tag} 不一致: {old[:30]}"); sys.exit(1)
    print(f"  [ok] {tag}"); return b.replace(old,new,1)
def demote(b, h2line, tag):
    if h2line not in b: print(f"  [!!] demote不一致: {h2line}"); sys.exit(1)
    print(f"  [demote] {tag}"); return b.replace(h2line, "###"+h2line[2:], 1)

# ---- タイトル短縮 ----
for n,newt in [
 ("023","YouTubeのBGM収益｜登録者0でも稼げる仕組みと始め方【2026】"),
 ("136","DistroKidの使い方｜AI音楽を世界配信して稼ぐ【2026年最新】"),
 ("138","Suno・Udioの使い方と比較｜AIでプロ級の曲を作るコツ【2026】"),
]:
    fp,d=load(n); d["title"]=newt
    json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"post_{n} title→{newt}({len(newt)}字)")

# ============ 137: 集客のH2を1つの親にまとめてH3化 + 税金節整理 + キーワード ============
fp,d=load("137"); b=d["body"]
print("post_137:")
# 集客グルーピング: TikTok/LoFi の2H2の前に親H2を挿入し、両者をH3へ
b = repl(b,
 "## TikTokで“拡散”して再生を集める",
 "## 再生を伸ばす“集客”の方法（ここが本番）\n曲を出しても、聞かれなければ収益は始まりません。Spotifyの1,000再生の壁を越えるためにも、**自分から拡散する**動きが欠かせません。代表的な2つを紹介します。\n\n### TikTokで“拡散”して再生を集める",
 "集客親+TikTok→H3")
b = demote(b, "## YouTubeの“作業用BGM”で稼ぐ（Lo-Fi長尺戦略）", "LoFi→H3")
# 税金節を短縮＋リンク化
old_tax = """## 副業の税金（ざっくりだけ知っておく）
稼ぎ始めたら、税金の基本も頭の片隅に。

- 会社員の場合、**副業の所得（売上−経費）が年20万円を超えたら確定申告**が必要（住民税は20万円以下でも申告対象）
- Sunoや配信サービスの**利用料・機材費は経費**にできる。領収書・明細は残しておく
- 会社に知られたくない人は、住民税を**「自分で納付（普通徴収）」**にするのが基本

最初から気にしすぎる必要はありませんが、**収益と経費の記録だけはつけておく**と後でラクです。

"""
new_tax = """## 稼げてきたら“税金”も少しだけ
副業の所得（売上−経費）が**年20万円を超えたら確定申告**が必要です（住民税は20万円以下でも申告対象）。Sunoや配信の利用料・機材費は**経費**にできるので、**収益と経費の記録だけ**は最初からつけておきましょう。詳しい手順は[副業の確定申告・税金の基本](?p=)で解説します。

"""
b = repl(b, old_tax, new_tax, "税金節を短縮＋リンク化")
d["body"]=b; d["char_count"]=len(b)
d["keywords"]=["AI音楽","稼ぐ","Suno","音楽配信","副業"]  # BGM収益を外し023とのカニバリ回避
d["notes"]=(d.get("notes") or "")+" SEO仕上げ(2026-06-13):集客2節を親H2+H3に階層化・税金節を短縮しリンク化・キーワードからBGM収益を外す(023とカニバリ回避)。"
json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("  post_137 char=",d["char_count"],"H2=",sum(1 for l in b.split(chr(10)) if l.startswith('## ')))

# ============ 138: 補足的なH2をH3へ降格（フラット解消） ============
fp,d=load("138"); b=d["body"]
print("post_138:")
for h2,tag in [
 ("## クレジットの仕組み（何曲作れる？）","クレジット"),
 ("## 歌詞修正の“落とし穴”","歌詞修正"),
 ("## 仕上げの“マスタリング”で市販クオリティに","マスタリング"),
 ("## Suno・Udio以外の作曲AIも知っておく","他作曲AI"),
 ("## ダウンロード・書き出しで注意すること","DL注意"),
 ("## つまずきやすいポイント（先回り）","つまずき"),
]:
    b = demote(b, h2, tag)
d["body"]=b; d["char_count"]=len(b)
d["notes"]=(d.get("notes") or "")+" SEO仕上げ(2026-06-13):補足6節をH3に降格しH2フラットを解消(H2過多を整理)。"
json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("  post_138 H2=",sum(1 for l in b.split(chr(10)) if l.startswith('## ')),"H3=",sum(1 for l in b.split(chr(10)) if l.startswith('### ')))
print("DONE")
