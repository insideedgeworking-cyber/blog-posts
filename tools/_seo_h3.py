# -*- coding: utf-8 -*-
"""SEO: フラットなH2群を、H2グループ＋H3子に再構成（内容は保持・並べ替えのみ）。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")

def parse(body):
    lines = body.split("\n")
    intro=[]; sections=[]; cur=None
    for ln in lines:
        if ln.startswith("## "):
            if cur: sections.append(cur)
            cur=[ln]
        elif cur is not None:
            cur.append(ln)
        else:
            intro.append(ln)
    if cur: sections.append(cur)
    return "\n".join(intro).rstrip(), [( s[0], "\n".join(s).rstrip() ) for s in sections]

def restructure(pid, plan, group_intros):
    fp=os.path.join(PD,f"{pid}.json"); d=json.load(open(fp,encoding="utf-8-sig"))
    intro, sections = parse(d["body"])
    used=set()
    def find(key):
        hits=[i for i,(h,_) in enumerate(sections) if key in h and i not in used]
        if not hits: raise SystemExit(f"[!] {pid}: 不一致キー '{key}'")
        used.add(hits[0]); return sections[hits[0]]
    out=[intro,""]
    for item in plan:
        kind=item[0]
        if kind=="G":
            out.append("## "+item[1])
            gi=group_intros.get(item[1])
            if gi: out.append(gi)
            out.append("")
        elif kind=="H2":
            h,full=find(item[1]); out.append(full); out.append("")
        elif kind=="H3":
            h,full=find(item[1])
            full="###"+full[2:]   # "## " -> "### "
            out.append(full); out.append("")
    # 未使用チェック
    un=[sections[i][0] for i in range(len(sections)) if i not in used]
    if un:
        print(f"[!] {pid}: 未配置セクション:",un); raise SystemExit(1)
    body="\n".join(out).rstrip()+"\n"
    d["body"]=body; d["char_count"]=len(body)
    json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    h2=body.count("\n## ")+ (1 if body.startswith("## ") else 0); h3=body.count("\n### ")
    print(f"{pid}: 再構成OK H2={h2} H3={h3} char={d['char_count']}")

# ===== post_026 Threads =====
restructure("post_026",[
 ("H2","どれから始める"),
 ("G","Threadsが伸びる仕組み"),
   ("H3","2つのフィードとAIランキング"),("H3","Xとの違い"),("H3","実例：少フォロワー"),("H3","アルゴリズムを上げる"),
 ("G","伸ばす投稿の作り方"),
   ("H3","バズらせ方の手順"),("H3","500文字の"),("H3","滞在時間を伸ばす2つの小ワザ"),("H3","フォロワーを増やす手順"),("H3","そのまま使える投稿"),("H3","AIの活かし方"),
 ("G","収益化につなげる"),
   ("H3","スレッズ→インスタ転用"),("H3","さらに効く2つの裏ワザ"),("H3","収益化の現実的な始め方"),("H3","集客・副業への動線"),
 ("H2","注意点"),("H2","よくある質問"),("H2","まとめ"),("H2","あわせて読みたい"),
],{
 "Threadsが伸びる仕組み":"まずは「なぜ伸びるのか」を押さえましょう。",
 "伸ばす投稿の作り方":"仕組みが分かったら、実際に伸びる投稿を作ります。",
 "収益化につなげる":"集めたフォロワーを“お金”に変える流れです。",
})

# ===== post_027 X =====
restructure("post_027",[
 ("H2","どれから始める"),
 ("G","Xが伸びる仕組み"),
   ("H3","2026年・Grokアルゴとクラスター"),("H3","クラスターに“所属”する"),
 ("G","伸ばす投稿の作り方"),
   ("H3","伸びるポストの作り方"),("H3","フォロワーを増やす“具体手順”"),("H3","滞在時間を稼ぐ"),("H3","ポストの“種類”"),("H3","AIの活かし方"),("H3","やってはいけないNG"),
 ("G","収益化につなげる"),
   ("H3","フォロワー数より"),("H3","集めたフォロワーを"),("H3","Xそのもので稼ぐ"),("H3","ブログ・副業への集客動線"),
 ("H2","注意点"),("H2","よくある質問"),("H2","まとめ"),("H2","あわせて読みたい"),
],{
 "Xが伸びる仕組み":"まずは2026年のアルゴリズムの考え方から。",
 "伸ばす投稿の作り方":"仕組みを踏まえて、反応されるポストを作ります。",
 "収益化につなげる":"フォロワーを売上に変える方法です。",
})

# ===== post_028 Instagram =====
restructure("post_028",[
 ("H2","どれから始める"),
 ("G","インスタが伸びる仕組み（2026年版）"),
   ("H3","インスタが副業に強い理由"),("H3","リール × ストーリー"),("H3","2026年の新常識"),("H3","初心者が今いちばん有利"),
 ("G","ジャンルとプロフィールを決める"),
   ("H3","ジャンルの選び方"),("H3","ジャンルの“決め方”4ステップ"),("H3","プロフィールの作り方"),
 ("G","投稿の作り方（リール・ストーリー）"),
   ("H3","リール動画を伸ばすコツ"),("H3","型をAIで分析"),("H3","リールの撮影とカバー画像"),("H3","ストーリーを"),("H3","そのまま使える投稿"),("H3","Manus等）でインスタ運用を半自動化"),("H3","AIの活かし方（2026年の武器）"),
 ("G","見つけてもらう・伸ばす"),
   ("H3","検索（Google・AI）"),("H3","伸ばす運用のコツ"),
 ("G","収益化につなげる"),
   ("H3","マネタイズ：アフィリエイト"),("H3","集客・収益への動線"),
 ("H2","注意点"),("H2","やめた方がいいこと"),("H2","よくある質問"),("H2","まとめ"),("H2","あわせて読みたい"),
],{
 "インスタが伸びる仕組み（2026年版）":"まずは伸びる土台＝仕組みから押さえます。",
 "ジャンルとプロフィールを決める":"伸びるかどうかは、ここでほぼ決まります。",
 "投稿の作り方（リール・ストーリー）":"実際に投稿を作っていきます。",
 "見つけてもらう・伸ばす":"投稿を“発見”してもらう工夫です。",
 "収益化につなげる":"フォロワーを売上に変える流れです。",
})
print("ALL done")
