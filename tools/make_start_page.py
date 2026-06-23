# -*- coding: utf-8 -*-
"""「はじめての方へ」スタートページを作成/更新する固定ページ。
訪問者を目的別に最適な入口記事へ案内する（回遊・直帰改善）。
make_base_pages.py と同じ upsert 方式。出力はASCIIのみ。
"""
import os, json, base64, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRED = os.path.join(os.path.dirname(ROOT), "wp-credentials.local.json")
c = json.load(open(CRED, encoding="utf-8-sig"))
TOK = base64.b64encode((c["username"] + ":" + c["application_password"].replace(" ", "")).encode()).decode()
B = c["site_url"].rstrip("/") + "/wp-json/wp/v2"

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

def L(wp, text):
    return '<a href="https://workstartedge.com/?p=%d">%s</a>' % (wp, text)

CONTENT = """
<p>はじめまして。<strong>WorkStartEdge｜未経験から始める副業ログ</strong>へようこそ。当ブログは、パソコンもまともに触ったことがなかった私が、<strong>低スペックの古いPCとスマホ・AIを相棒に</strong>、副業に挑戦している実録です。</p>
<p>「何から読めばいいか分からない」という方のために、目的別におすすめの記事をまとめました。気になるところから読んでみてください。</p>

<h2>まず迷ったら、この3つから</h2>
<ul>
<li>%s … 自分に合う副業の選び方が分かります（各副業の始め方リンク付き）</li>
<li>%s … ブログ・アフィリエイトで稼ぐ全体像</li>
<li>%s … 運営者がどんな人間かが分かる体験談</li>
</ul>

<h2>やりたいことから選ぶ</h2>
<p>「これをやってみたい」が決まっている方は、各ジャンルの入口記事へどうぞ。</p>

<h3>ブログ・アフィリエイトで稼ぎたい</h3>
<ul>
<li>%s</li>
<li>%s</li>
<li>%s ／ %s（最初に決めるもの）</li>
</ul>

<h3>AIで文章を書いて稼ぎたい</h3>
<ul>
<li>%s</li>
<li>%s</li>
</ul>

<h3>そのほかの副業</h3>
<ul>
<li>Webライター … %s</li>
<li>スマホ副業 … %s</li>
<li>YouTube … %s</li>
<li>note … %s</li>
<li>AI音楽 … %s</li>
<li>SNS集客 … %s</li>
</ul>

<h2>基礎を固める・用語を調べる</h2>
<ul>
<li>%s … 検索で読まれるための土台</li>
<li>用語が分からなくなったら … %s ／ %s ／ %s</li>
</ul>

<h2>運営者の歩み（体験談）</h2>
<p>うまくいったことも、つまずいたことも正直に記録しています。</p>
<ul>
<li>%s</li>
<li>%s</li>
<li>%s</li>
</ul>

<h2>運営者・お問い合わせ</h2>
<ul>
<li><a href="/profile/">プロフィール（どんな人が書いているか）</a></li>
<li><a href="/contact/">お問い合わせ</a></li>
</ul>
<p>一緒に、少しずつ前に進んでいきましょう。気になる記事から、ぜひ読んでみてください。</p>
""" % (
    L(56, "副業の選び方｜種類別に収入・メリット・デメリットを比較"),
    L(131, "ブログ収益化ロードマップ｜月5万円までにやること"),
    L(7,  "飲食からの一歩｜未経験の私が副業を始めた話"),
    L(129, "ブログの始め方｜無料と有料の違い・どっちで稼ぐ"),
    L(131, "ブログ収益化ロードマップ｜未経験が月5万円まで"),
    L(281, "レンタルサーバーの選び方"), L(283, "WordPressテーマの選び方"),
    L(165, "AIライティング完全ガイド｜AIで書いて稼ぐ全体像"),
    L(164, "AIライティング副業の始め方｜月5万円を目指す手順"),
    L(159, "未経験からWebライターを始める方法"),
    L(169, "スマホ副業の始め方｜スキマ時間で稼ぐ全種類"),
    L(71,  "YouTubeの始め方｜ショート＆ロングで収益化"),
    L(219, "noteで稼ぐ始め方｜収益化の全体像"),
    L(110, "AIで作った音楽で稼ぐ方法｜作る→配信→収益化"),
    L(98,  "SNS集客のやり方｜X・スレッズ・インスタ"),
    L(134, "ブログSEOの基本｜やるべきこと・やってはいけないこと"),
    L(67,  "ブログ用語まとめ"), L(63, "副業用語まとめ"), L(368, "アクセス解析用語辞典"),
    L(7,   "飲食からの一歩｜未経験の私が副業を始めた話"),
    L(217, "ブログを始めて2週間ちょい｜準備期間のリアルな記録"),
    L(366, "「クロール済み-インデックス未登録」で焦った話"),
)

if __name__ == "__main__":
    slug = "start"
    title = "はじめての方へ"
    status = "draft"  # まず下書きで作成 → 確認後に公開
    p = find_page(slug)
    payload = {"title": title, "content": CONTENT.strip(), "status": status, "slug": slug}
    if p:
        res = api("/pages/%d" % p["id"], "POST", payload)
    else:
        res = api("/pages", "POST", payload)
    print("page:", slug, "id", res["id"], res["status"])
    print("preview:", c["site_url"].rstrip("/") + "/?page_id=%d" % res["id"])
