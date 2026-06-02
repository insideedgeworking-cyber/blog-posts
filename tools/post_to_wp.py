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

    post = json.load(open(os.path.join(ROOT, "posts", f"{post_id}.json"), encoding="utf-8-sig"))
    cred = load_cred()
    cat_id = get_or_create_category(cred, post["category"])
    content = md_to_html(post["body"])

    payload = {"title": post["title"], "content": content,
               "status": status, "categories": [cat_id]}
    if post.get("wp_post_id"):                                 # 既存があれば更新
        res = api(cred, f"/posts/{post['wp_post_id']}", "POST", payload)
    else:
        res = api(cred, "/posts", "POST", payload)

    print("OK id=", res["id"], "status=", res["status"], "category=", post["category"], f"(id {cat_id})")
    print("edit:", cred["site_url"].rstrip("/") + f"/wp-admin/post.php?post={res['id']}&action=edit")
    print("link:", res.get("link"))

if __name__ == "__main__":
    import urllib.parse  # noqa
    main()
