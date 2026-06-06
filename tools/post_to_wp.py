# -*- coding: utf-8 -*-
"""指定した post_xxx.json を WordPress の下書きとして作成する。
- 本文マークダウンを HTML に変換（##/###, **, `code`, > 引用, - 箇条書き, ![]() 画像）
- アフィリ差し込み枠の <!-- ... --> コメントはHTMLにそのまま残す（WP編集画面で目印になり読者には見えない）
- カテゴリは名前から検索、なければ作成
使い方: python post_to_wp.py post_001 [--status draft|publish]
"""
import os, sys, re, json, base64, html, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))            # blog-posts
CRED = os.path.join(os.path.dirname(ROOT), "wp-credentials.local.json")       # 親フォルダ

def load_cred():
    c = json.load(open(CRED, encoding="utf-8-sig"))
    pw = c["application_password"].replace(" ", "")
    c["_token"] = base64.b64encode(f"{c['username']}:{pw}".encode()).decode()
    c["_base"] = c["site_url"].rstrip("/") + "/wp-json/wp/v2"
    return c

def api(cred, path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(cred["_base"] + path, data=data, method=method,
        headers={"Authorization": "Basic " + cred["_token"], "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTPError {e.code}: {e.read().decode()[:500]}")

def get_or_create_category(cred, name):
    found = api(cred, f"/categories?search={urllib.parse.quote(name)}&per_page=100")
    for c in found:
        if c["name"] == name:
            return c["id"]
    created = api(cred, "/categories", "POST", {"name": name})
    return created["id"]

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)",
               r'<img src="\2" alt="\1" style="max-width:100%;height:auto;" />', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s

GLOSSARY_PATH = os.path.join(ROOT, "posts", "_glossary.json")

def load_glossary():
    try:
        return json.load(open(GLOSSARY_PATH, encoding="utf-8-sig"))
    except Exception:
        return None

def save_glossary_url(url):
    g = load_glossary()
    if g is not None and g.get("url") != url:
        g["url"] = url
        json.dump(g, open(GLOSSARY_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def add_anchor_ids(html, gloss):
    """用語解説記事の見出しに id を付ける（他記事からの飛び先アンカー）。"""
    for e in gloss["terms"]:
        m = e.get("match")
        if not m:
            continue
        # <h3>CPU（…）</h3> → <h3 id="g-cpu">CPU（…）</h3>（最初の一致のみ）
        pat = re.compile(r'(<h[23])>(' + re.escape(m) + r')')
        html, n = pat.subn(r'\1 id="g-' + e["slug"] + r'">\2', html, count=1)
    return html

def autolink_terms(body, gloss, url):
    """本文(マークダウン)中、各用語の最初の1回だけを用語解説へリンクする。"""
    pairs = []
    for e in gloss["terms"]:
        for a in e.get("aliases", []):
            pairs.append((a, e["slug"]))
    pairs.sort(key=lambda x: -len(x[0]))      # 長い語を優先（部分一致の誤リンク防止）
    used = set()
    lines = body.split("\n")
    for i, line in enumerate(lines):
        s = line.lstrip()
        if s.startswith(("#", "!", "<!--", ">", "|")) or "](" in line:
            continue                          # 見出し/画像/コメント/引用/既存リンク行は対象外
        for a, slug in pairs:
            if slug in used:
                continue
            idx = line.find(a)
            if idx < 0:
                continue
            lines[i] = line[:idx] + f"[{a}]({url}#g-{slug})" + line[idx + len(a):]
            line = lines[i]
            used.add(slug)
    return "\n".join(lines)

RAW_IMG_RE = re.compile(r'https://raw\.githubusercontent\.com/[^)\s]+/images/[A-Za-z0-9._-]+')

def media_find(cred, slug):
    """同じslugのメディアが既にあれば、そのURLを返す（再アップロード防止）。"""
    try:
        res = api(cred, f"/media?slug={slug}&per_page=20")
        for m in res:
            if m.get("slug") == slug:
                return m.get("source_url")
    except SystemExit:
        pass
    return None

def media_upload(cred, path, filename):
    data = open(path, "rb").read()
    req = urllib.request.Request(cred["_base"] + "/media", data=data, method="POST",
        headers={"Authorization": "Basic " + cred["_token"], "Content-Type": "image/png",
                 "Content-Disposition": f'attachment; filename="{filename}"'})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["source_url"]

def media_ensure_id(cred, path, filename, slug):
    """slugで既存メディアを探し、無ければアップロード。media idを返す（アイキャッチ用）。"""
    try:
        res = api(cred, f"/media?slug={slug}&per_page=20")
        for m in res:
            if m.get("slug") == slug:
                return m["id"]
    except SystemExit:
        pass
    data = open(path, "rb").read()
    req = urllib.request.Request(cred["_base"] + "/media", data=data, method="POST",
        headers={"Authorization": "Basic " + cred["_token"], "Content-Type": "image/png",
                 "Content-Disposition": f'attachment; filename="{filename}"'})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["id"]

def localize_images(cred, body):
    """本文中のGitHub画像URLを、WordPressメディアにアップした自前URLへ置き換える。"""
    for url in sorted(set(RAW_IMG_RE.findall(body))):
        fname = url.split("/images/")[-1]
        slug = re.sub(r"\.[A-Za-z0-9]+$", "", fname).lower()
        local = os.path.join(ROOT, "images", fname)
        wp_url = media_find(cred, slug)
        if not wp_url:
            if not os.path.exists(local):
                print("  ! 画像が見つからずスキップ:", fname); continue
            wp_url = media_upload(cred, local, fname)
            print("  upload:", fname, "->", wp_url)
        else:
            print("  reuse :", fname, "->", wp_url)
        body = body.replace(url, wp_url)
    return body

def md_to_html(md):
    out, in_ul = [], False
    def close():
        nonlocal in_ul
        if in_ul: out.append("</ul>"); in_ul = False
    for raw in md.split("\n"):
        line = raw.rstrip()
        if re.match(r"^<!--.*-->\s*$", line):                 # アフィリ枠コメントは温存
            close(); out.append(line); continue
        if re.match(r"^!\[[^\]]*\]\([^)]+\)\s*$", line):       # 画像単独行 → 中央寄せ
            close(); out.append('<p style="text-align:center">' + inline(line) + "</p>"); continue
        if re.match(r"^###\s+", line):
            close(); out.append("<h3>" + inline(re.sub(r"^###\s+", "", line)) + "</h3>")
        elif re.match(r"^##\s+", line):
            close(); out.append("<h2>" + inline(re.sub(r"^##\s+", "", line)) + "</h2>")
        elif re.match(r"^#\s+", line):
            close(); out.append("<h1>" + inline(re.sub(r"^#\s+", "", line)) + "</h1>")
        elif re.match(r"^>\s+", line):
            close(); out.append("<blockquote>" + inline(re.sub(r"^>\s+", "", line)) + "</blockquote>")
        elif re.match(r"^\s*[-*]\s+", line):
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append("<li>" + inline(re.sub(r"^\s*[-*]\s+", "", line)) + "</li>")
        elif line.strip() == "":
            close()
        else:
            close(); out.append("<p>" + inline(line) + "</p>")
    close()
    return "\n".join(out)

def main():
    import urllib.parse
    globals()["urllib"].parse = urllib.parse
    post_id = sys.argv[1] if len(sys.argv) > 1 else "post_001"
    status = "draft"
    if "--status" in sys.argv:
        status = sys.argv[sys.argv.index("--status") + 1]

    dry = "--dry" in sys.argv
    post = json.load(open(os.path.join(ROOT, "posts", f"{post_id}.json"), encoding="utf-8-sig"))
    cred = load_cred()

    gloss = load_glossary()
    is_glossary = bool(gloss) and post_id == gloss.get("glossary_post_id")

    body = post["body"] if dry else localize_images(cred, post["body"])   # 画像をWPメディアへ
    # 用語の自動リンク（用語解説記事そのものは対象外。URL未確定ならスキップ）
    if gloss and gloss.get("url") and not is_glossary:
        body = autolink_terms(body, gloss, gloss["url"])
        print("  用語リンク:", body.count(gloss["url"] + "#g-"), "件")
    content = md_to_html(body)
    if is_glossary and gloss:
        content = add_anchor_ids(content, gloss)
        print("  用語アンカー付与:", content.count('id="g-'), "件")

    if dry:
        print("--- DRY RUN（投稿しません）。本文HTML先頭600字 ---")
        print(content[:600]); return

    cat_id = get_or_create_category(cred, post["category"])
    # アイキャッチ（表紙）: images/cover-<id>.png があれば featured_media に設定
    # ファイル名はアンダースコア無し（post_017 -> cover-post017.png）
    featured_id = None
    cid = post_id.replace("_", "")
    cover_path = os.path.join(ROOT, "images", f"cover-{cid}.png")
    if os.path.exists(cover_path):
        featured_id = media_ensure_id(cred, cover_path, f"cover-{cid}.png", f"cover-{cid}")
        print("  アイキャッチ:", f"cover-{cid}.png", "-> media", featured_id)
    payload = {"title": post["title"], "content": content,
               "status": status, "categories": [cat_id]}
    if featured_id:
        payload["featured_media"] = featured_id
    if post.get("excerpt"):                              # メタ説明（検索スニペット用）
        payload["excerpt"] = post["excerpt"]
    if post.get("wp_post_id"):                                 # 既存があれば更新
        res = api(cred, f"/posts/{post['wp_post_id']}", "POST", payload)
    else:
        res = api(cred, "/posts", "POST", payload)
    if is_glossary:                                            # 用語解説のURLを記録（他記事のリンク先）
        save_glossary_url(res.get("link", ""))

    print("OK id=", res["id"], "status=", res["status"], "category=", post["category"], f"(id {cat_id})")
    print("edit:", cred["site_url"].rstrip("/") + f"/wp-admin/post.php?post={res['id']}&action=edit")
    print("link:", res.get("link"))

if __name__ == "__main__":
    import urllib.parse  # noqa
    main()
