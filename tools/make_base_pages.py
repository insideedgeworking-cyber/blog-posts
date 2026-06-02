# -*- coding: utf-8 -*-
"""サイトの土台ページを作成/更新する。
- プライバシーポリシー（既存の自動下書き id を slug で探して更新→公開）
- プロフィール（無ければ作成→公開）
- 著者プロフィール文(description)を設定（Cocoonのプロフィール欄に表示）
出力はASCIIのみ（Windowsコンソールの文字化け回避）。
"""
import os, json, base64, urllib.request, urllib.error, urllib.parse

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
        raise SystemExit(f"HTTPError {e.code}: {e.read().decode()[:400]}")

def find_page(slug):
    r = api(f"/pages?slug={slug}&status=publish,draft,pending,private")
    return r[0] if r else None

def upsert_page(slug, title, content):
    p = find_page(slug)
    payload = {"title": title, "content": content, "status": "publish", "slug": slug}
    if p:
        res = api(f"/pages/{p['id']}", "POST", payload)
    else:
        res = api("/pages", "POST", payload)
    print("page:", slug, "id", res["id"], res["status"])
    return res

PRIVACY = """
<p>WorkStartEdge（以下「当サイト」）における個人情報の取り扱いについて、以下のとおりプライバシーポリシーを定めます。</p>

<h2>個人情報の利用目的</h2>
<p>当サイトでは、お問い合わせの際に、お名前やメールアドレス等の個人情報を入力いただく場合があります。取得した個人情報は、お問い合わせへの回答や必要な情報を返信する目的のみに利用し、それ以外の目的では利用しません。</p>

<h2>アクセス解析ツールについて</h2>
<p>当サイトでは、サイトの利用状況を把握するためにGoogleアナリティクス等のアクセス解析ツールを利用する場合があります。これらのツールはトラフィックデータの収集のためにCookie（クッキー）を使用しますが、このデータは匿名で収集されており、個人を特定するものではありません。Cookieはブラウザの設定で無効にすることができます。</p>

<h2>広告について</h2>
<p>当サイトでは、第三者配信の広告サービス（A8.net、もしもアフィリエイト、Amazonアソシエイト、楽天アフィリエイト、Googleアドセンス等）を利用する場合があります。これらの広告配信事業者は、利用者の興味に応じた広告を表示するためにCookieを使用することがあります。Cookieを無効にする方法や、広告配信事業者のプライバシーポリシーについては、各事業者の案内をご確認ください。</p>
<p>また、当サイトは各種アフィリエイトプログラムに参加しており、商品・サービスの紹介を通じて紹介料を得ることがあります。</p>

<h2>免責事項</h2>
<p>当サイトの情報は、できる限り正確な情報を掲載するよう努めていますが、その内容の正確性や安全性を保証するものではありません。当サイトの情報を用いて行う一切の行為について、いかなる責任も負いかねます。各種サービスの利用やご購入は、ご自身の判断と責任において行ってください。</p>

<h2>著作権について</h2>
<p>当サイトに掲載されている文章・画像等の著作権は、運営者または各権利者に帰属します。無断での転載・複製を禁じます。引用される場合は、出典として当サイトへのリンクを明記してください。</p>

<h2>プライバシーポリシーの変更</h2>
<p>当サイトは、必要に応じて本ポリシーの内容を変更することがあります。変更後の内容は、当ページに掲載した時点から効力を生じるものとします。</p>

<p>制定日：2026年6月3日</p>
"""

PROFILE = """
<p>はじめまして。<strong>WorkStartEdge｜未経験から始める副業ログ</strong>を運営している管理人です。当ブログを読んでくださり、ありがとうございます。</p>

<h2>ずっと飲食業で働いてきました</h2>
<p>私はもともと、パソコンもまともに触ったことがないまま、ずっと飲食業で働いてきました。仕事に大きな不満があったわけではありませんが、「このまま続けても、収入はそんなに変わらないかもしれない」という、ぼんやりとした不安を抱えていました。</p>

<h2>未経験・低スペックPCから副業を始めました</h2>
<p>そんな私が、AIとゲーム用パソコンをきっかけに副業に興味を持ち、今は<strong>スマホとGPUもない古いノートPC</strong>で副業に挑戦しています。特別なスキルも、高性能なパソコンも持っていません。分からないことはAIに聞きながら、一歩ずつ進めている最中です。</p>

<h2>このブログで発信していること</h2>
<p>当ブログは「副業もPCもやったことがない人」に向けた、副業のリアルな記録です。私自身が実際に取り組んでいる<strong>ブログ・YouTube・X（旧Twitter）・Threads、そしてそれらを支えるAI活用</strong>を軸に、ひとつに絞らず複数を組み合わせて稼ぐ方法を、数字も失敗も正直に書いていきます。</p>

<h2>同じ立場のあなたへ</h2>
<p>「未経験だから」「PCに詳しくないから」と一歩を踏み出せずにいる方に、「それ、始めない理由にはならないよ」と伝えたくてこのブログを書いています。一緒に、少しずつ前に進んでいきましょう。</p>
"""

if __name__ == "__main__":
    upsert_page("privacy-policy", "プライバシーポリシー", PRIVACY.strip())
    upsert_page("profile", "プロフィール", PROFILE.strip())
    bio = ("飲食業出身。未経験・低スペックPC・スマホからAIを活用して副業に挑戦中。"
           "ブログ/YouTube/X/Threadsを掛け合わせて稼ぐ方法を、数字も失敗も正直に発信しています。")
    res = api("/users/me", "POST", {"description": bio})
    print("bio set for user id", res["id"])
