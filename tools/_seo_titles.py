# -*- coding: utf-8 -*-
"""SEO: タイトル短縮(KW前方/32字目安)・メタ120字・英語スラッグ・キーワード分離(カニバリ回避)。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")

# (title, slug, keywords, excerpt<=120字)
S = {
 "post_026": dict(
   title="スレッズ集客のやり方｜フォロワーの増やし方【2026】",
   slug="threads-shukyaku",
   keywords=["スレッズ集客","Threads","フォロワーの増やし方","スレッズ 伸ばし方","アルゴリズム","副業"],
   excerpt="スレッズ(Threads)のフォロワーの増やし方を2026年最新で解説。24時間法則・初速・保存重視のアルゴリズム、冒頭1行10パターン、Xリサーチ術、note収益化まで。少フォロワーで伸ばす実例つき。"),
 "post_027": dict(
   title="X(旧Twitter)集客のやり方｜フォロワーの増やし方【2026】",
   slug="x-twitter-shukyaku",
   keywords=["X集客","Twitter","フォロワーの増やし方","X 伸ばし方","アルゴリズム","クラスター"],
   excerpt="X(旧Twitter)のフォロワーの増やし方を2026年最新で解説。Grokアルゴとクラスター、交流・初速・滞在時間の伸ばし方、冒頭フック集、やってはいけないNG、収益化まで未経験向けに。"),
 "post_028": dict(
   title="インスタ集客のやり方｜リールでフォロワーを増やす【2026】",
   slug="instagram-shukyaku",
   keywords=["インスタ集客","リール","フォロワーの増やし方","インスタ 伸ばし方","アルゴリズム","副業"],
   excerpt="インスタ(Instagram)のフォロワーの増やし方を2026年最新で解説。リール×ストーリーの伸ばし方、2026新常識、ジャンル選び、検索流入、収益化まで。リール台本のAI分析術つき。"),
}
for pid, s in S.items():
    fp = os.path.join(PD, f"{pid}.json")
    d = json.load(open(fp, encoding="utf-8-sig"))
    d["title"]=s["title"]; d["slug"]=s["slug"]; d["keywords"]=s["keywords"]; d["excerpt"]=s["excerpt"]
    # body内の見出し直後の旧タイトル参照は無いのでbodyはそのまま
    json.dump(d, open(fp,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{pid}: title({len(s['title'])}字) excerpt({len(s['excerpt'])}字) slug={s['slug']}")
print("done")
