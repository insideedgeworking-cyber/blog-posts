# -*- coding: utf-8 -*-
"""カテゴリ再編 STEP1：新カテゴリ（親＋新しい子）を作成し、ID一覧を保存。"""
import os, json, base64, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(os.path.dirname(ROOT), "wp-credentials.local.json"), encoding="utf-8-sig"))
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
        raise SystemExit("HTTPError %d: %s" % (e.code, e.read().decode()[:300]))

def get_by_slug(slug):
    r = api("/categories?slug=%s" % slug)
    return r[0] if r else None

def upsert_cat(name, slug, parent_id):
    ex = get_by_slug(slug)
    if ex:
        # 親・名前を合わせる
        api("/categories/%d" % ex["id"], "POST", {"name": name, "parent": parent_id})
        print("  exists/upd:", name, "id", ex["id"])
        return ex["id"]
    res = api("/categories", "POST", {"name": name, "slug": slug, "parent": parent_id})
    print("  created   :", name, "id", res["id"])
    return res["id"]

ids = {}
# 親カテゴリ
ids["AI副業"]   = upsert_cat("AI副業", "ai-fukugyo", 0)
ids["副業ツール"] = upsert_cat("副業ツール", "fukugyo-tools", 0)
# AI副業 配下の新しい子
ids["Webライター"]       = upsert_cat("Webライター", "web-writer", ids["AI副業"])
ids["スマホ・スキマ副業"] = upsert_cat("スマホ・スキマ副業", "smartphone-fukugyo", ids["AI副業"])
# 副業ツール 配下の子
ids["ブログツール"] = upsert_cat("ブログツール", "blog-tools", ids["副業ツール"])
ids["AIツール"]    = upsert_cat("AIツール", "ai-tools", ids["副業ツール"])
ids["動画ツール"]  = upsert_cat("動画ツール", "video-tools", ids["副業ツール"])
ids["音楽ツール"]  = upsert_cat("音楽ツール", "music-tools", ids["副業ツール"])

json.dump(ids, open(os.path.join(ROOT, "tools", "_catids.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("保存:", ids)
