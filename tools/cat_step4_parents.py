# -*- coding: utf-8 -*-
"""カテゴリ再編 STEP4：各記事に親カテゴリ(AI副業/副業ツール)を追加。
→ 親カテゴリのページでも子の記事が一覧表示されるようにする。"""
import os, json, base64, glob, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(os.path.dirname(ROOT), "wp-credentials.local.json"), encoding="utf-8-sig"))
TOK = base64.b64encode((c["username"] + ":" + c["application_password"].replace(" ", "")).encode()).decode()
B = c["site_url"].rstrip("/") + "/wp-json/wp/v2"
ids = json.load(open(os.path.join(ROOT, "tools", "_catids.json"), encoding="utf-8"))

AIF = ids["AI副業"]; TOOL = ids["副業ツール"]
AIF_CHILDREN = {ids[k] for k in ["ブログ・note","YouTube・動画","AIライティング","AI音楽","Webライター","スマホ・スキマ副業"]}
TOOL_CHILDREN = {ids[k] for k in ["ブログツール","AIツール","動画ツール","音楽ツール"]}

def api(path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(B + path, data=data, method=method,
        headers={"Authorization": "Basic " + TOK, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

n = 0
for f in sorted(glob.glob(os.path.join(ROOT, "posts", "post_*.json"))):
    d = json.load(open(f, encoding="utf-8-sig"))
    w = d.get("wp_post_id")
    if not w:
        continue
    cur = set(api("/posts/%d?_fields=categories" % w)["categories"])
    add = set()
    if cur & AIF_CHILDREN:
        add.add(AIF)
    if cur & TOOL_CHILDREN:
        add.add(TOOL)
    new = cur | add
    if new != cur:
        api("/posts/%d" % w, "POST", {"categories": sorted(new)})
        n += 1
print("親カテゴリ追加: %d本に反映" % n)
