# -*- coding: utf-8 -*-
"""「おすすめツール」固定ページを作成/更新する（まとめ記事級・SEO資産＋収益ハブ）。
体験ベースの選び方・一言評価を載せ、各比較/解説記事へ導線。ツールが増えたら追記する。
make_base_pages.py と同じ upsert 方式。status は下記で切替。
"""
import os, json, base64, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRED = os.path.join(os.path.dirname(ROOT), "wp-credentials.local.json")
c = json.load(open(CRED, encoding="utf-8-sig"))
TOK = base64.b64encode((c["username"] + ":" + c["application_password"].replace(" ", "")).encode()).decode()
B = c["site_url"].rstrip("/") + "/wp-json/wp/v2"
STATUS = os.environ.get("PAGE_STATUS", "draft")  # PAGE_STATUS=publish で公開

def api(path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(B + path, data=data, method=method,
        headers={"Authorization": "Basic " + TOK, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit("HTTPError %d: %s" % (e.code, e.read().decode()[:400]))

def find_page(slug):
    r = api("/pages?slug=%s&status=publish,draft,pending,private" % slug)
    return r[0] if r else None

def A(wp, text):
    return '<a href="https://workstartedge.com/?p=%d">%s</a>' % (wp, text)

CONTENT = """
<p>このページは、未経験・パソコンが苦手だった私が、<strong>低スペックの古いノートPCとスマホ・AIを相棒に副業を続けるなかで、実際に使ってきた／おすすめできるツール</strong>を用途別にまとめたものです。「結局どれを選べばいい？」で止まらないよう、<strong>無料か有料か・料金の目安・どんな人向きか</strong>まで正直に整理しました。</p>
<p>各ツールの詳しい比較・使い方は、リンク先の記事で深掘りしています。<strong>ツールが増えたら、このページも随時更新</strong>していきます。</p>
<p><em>※紹介の一部に広告（アフィリエイト）を含みます。実際に使った・調べた一次情報をもとに、メリットだけでなくデメリットも正直に書いています。「必ず稼げる」と保証するものではありません。</em></p>

<h2>ツール選びの基本（最初に読んでください）</h2>
<p>道具をそろえる前に、これだけ知っておくと失敗しません。</p>
<ul>
<li><strong>まずは無料から</strong>：ほとんどのジャンルは無料ツールで始められます。続けられそうなら有料へ。</li>
<li><strong>増やしすぎない</strong>：多機能なものを1つ使い込むほうが、あれこれ手を出すより伸びます。</li>
<li><strong>「時間を買う」発想で有料を選ぶ</strong>：有料は“作業時間を減らす投資”。収益が出てから検討で十分です。</li>
</ul>

<h2>ブログを始める・運営する</h2>
<h3>レンタルサーバー（土台）</h3>
<p><strong>無料/有料：有料（必須）｜料金の目安：月1,000円前後</strong>。ブログを置く「土地」で、ここだけはケチらない方がいい部分。迷ったら<strong>ConoHa WING</strong>（速くて管理画面が分かりやすい）か<strong>エックスサーバー</strong>（実績・情報量が多くて安心）。私は管理のしやすさ重視で選びました。→ %s</p>
<h3>WordPressテーマ（見た目と機能）</h3>
<p><strong>無料/有料：両方あり</strong>。無料なら高機能な<strong>Cocoon</strong>（当ブログもこれ）、有料なら書きやすさNo.1クラスの<strong>SWELL</strong>（17,600円）。まず無料で始めて、収益が出たら有料へ、がムダなし。→ %s</p>
<h3>アクセス解析（無料・必須）</h3>
<p><strong>無料</strong>。検索の状況を見る<strong>サーチコンソール</strong>と、来た人の動きを見る<strong>GA4</strong>はセットで導入を。最初は怖く感じますが、入れるほど改善が早くなります。→ %s ／ %s</p>

<h2>AI・AIライティング</h2>
<h3>ChatGPT と Claude（文章AIの二大巨頭）</h3>
<p><strong>無料/有料：無料でも使える（本格利用は月20ドル前後）</strong>。副業の相棒にするならこの2つが中心。用途で得意が分かれるので、比較して自分に合う方を。→ %s</p>
<h3>AIツール全体の比較・使い分け</h3>
<p>「どのAIを何に使う？」で迷ったら、副業向けの選び方をまとめた比較記事を。→ %s ／ %s</p>
<h3>AIエージェント（自動化）</h3>
<p><strong>中〜上級者向け</strong>。Manus・Gensparkなどで記事制作を自動化する一歩進んだ使い方。→ %s</p>

<h2>アフィリエイト・収益化</h2>
<h3>ASP（広告の入口・無料）</h3>
<p><strong>無料</strong>。アフィリエイトの入口。まず<strong>A8.net</strong>と<strong>もしもアフィリエイト</strong>の2つに登録すればOK。慣れたらafb等を追加。→ %s</p>
<h3>物販（Amazon・楽天）</h3>
<p>商品レビュー記事と相性◎。もしも経由だと審査・管理がラク。→ %s</p>
<h3>Googleアドセンス（クリック型広告）</h3>
<p>審査に通れば、記事に広告を貼って収益化できます。通し方のコツはこちら。→ %s</p>

<h2>AI音楽で稼ぐ</h2>
<h3>作曲AI（Suno・Udio）</h3>
<p><strong>無料から試せる</strong>。文章を入れるだけでプロ級の曲ができるAI。使い方とコツ、商用利用の注意は記事で。→ %s</p>
<h3>音楽配信（DistroKid など）</h3>
<p>作った曲をSpotify等へ世界配信して収益化する仕組み。配信サービスの選び方も。→ %s ／ %s</p>

<h2>動画・SNS・ライター</h2>
<h3>動画編集ソフト（無料から）</h3>
<p><strong>無料</strong>。<strong>CapCut</strong>・<strong>Vrew</strong>なら無料でショート動画が作れて、スマホだけでも完結。→ %s</p>
<h3>クラウドソーシング（案件を取る）</h3>
<p>Webライター等の案件を受注する場所。未経験が案件を取る手順はこちら。→ %s</p>
<h3>SNS集客（無料・全副業の土台）</h3>
<p><strong>無料</strong>。X・スレッズ・インスタは、検索が育つまでの初速をくれる大事なチャネル。→ %s</p>

<h2>まず揃える「最低限」はこれだけ</h2>
<p>あれこれ迷うより、ブログ副業ならまずこの3つで十分スタートできます。</p>
<ul>
<li><strong>レンタルサーバー</strong>（土台）＋<strong>WordPressテーマはCocoon（無料）</strong></li>
<li><strong>サーチコンソール＋GA4</strong>（無料の解析）</li>
<li><strong>ChatGPT か Claude</strong>（執筆の相棒・無料から）</li>
</ul>
<p>まだ副業の方向性が決まっていない方は、先に %s で自分に合うものを見つけて、ブログなら %s から進めるのがおすすめです。</p>
<p>このページは、私が新しいツールを使うたびに更新していきます。ブックマークしておくと便利です。</p>
""" % (
    A(281, "レンタルサーバーの選び方・比較"),
    A(283, "WordPressテーマの選び方・比較"),
    A(358, "サーチコンソールの使い方"), A(360, "GA4の導入方法"),
    A(86,  "ChatGPT vs Claude の比較"),
    A(46,  "AIツール比較2026"), A(166, "AIライティングツール＆モデルの使い分け"),
    A(167, "AIエージェントで記事制作を自動化"),
    A(287, "おすすめASPの比較"),
    A(136, "Amazon・楽天アフィリエイトの始め方"),
    A(137, "Googleアドセンス審査の通し方"),
    A(114, "Suno・Udioの使い方と比較"),
    A(112, "DistroKidの使い方"), A(116, "音楽配信サービス比較"),
    A(253, "動画編集ソフトの使い方"),
    A(161, "クラウドソーシングの使い方"),
    A(98,  "SNS集客のやり方"),
    A(56,  "副業の選び方"), A(129, "ブログの始め方"),
)

if __name__ == "__main__":
    slug, title = "tools", "おすすめツール｜副業・ブログで実際に使っている道具まとめ"
    p = find_page(slug)
    payload = {"title": title, "content": CONTENT.strip(), "status": STATUS, "slug": slug}
    res = api("/pages/%d" % p["id"], "POST", payload) if p else api("/pages", "POST", payload)
    print("page:", slug, "id", res["id"], res["status"], "len", len(CONTENT))
