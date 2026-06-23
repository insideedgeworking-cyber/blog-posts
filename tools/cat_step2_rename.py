# -*- coding: utf-8 -*-
"""カテゴリ再編 STEP2：既存カテゴリを改名＆親付け。"""
import os, json, base64, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(os.path.dirname(ROOT), "wp-credentials.local.json"), encoding="utf-8-sig"))
TOK = base64.b64encode((c["username"] + ":" + c["application_password"].replace(" ", "")).encode()).decode()
B = c["site_url"].rstrip("/") + "/wp-json/wp/v2"
ids = json.load(open(os.path.join(ROOT, "tools", "_catids.json"), encoding="utf-8"))

def api(path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(B + path, data=data, method=method,
        headers={"Authorization": "Basic " + TOK, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit("HTTPError %d: %s" % (e.code, e.read().decode()[:300]))

AI = ids["AI副業"]
# (既存カテゴリid, 新名前, 新スラッグ, 親id)
UPD = [
    (13, "ブログ・note", "blog-note", AI),     # 旧ブログ
    (10, "YouTube・動画", "youtube", AI),       # 旧YouTube（slug据え置き）
    (15, "AIライティング", "ai-writing", AI),    # 旧AI活用
    (12, "AI音楽", "ai-music", AI),             # 旧AI音楽
    (7,  "用語辞典", "yougo", 0),               # 旧用語
    (9,  "副業の基礎・お金", "fukugyo-kiso", 0), # 旧副業（記事は次STEPで振り分け）
]
for cid, name, slug, parent in UPD:
    api("/categories/%d" % cid, "POST", {"name": name, "slug": slug, "parent": parent})
    print("  更新:", cid, "->", name, "(slug:%s, parent:%s)" % (slug, parent))
ids["ブログ・note"] = 13; ids["YouTube・動画"] = 10; ids["AIライティング"] = 15
ids["AI音楽"] = 12; ids["用語辞典"] = 7; ids["副業の基礎・お金"] = 9
ids["SNS集客"] = 11; ids["体験談"] = 3
# 解体予定（記事移動後に削除）: アフィリエイト8 / 比較6 / ノウハウ14
ids["_dissolve"] = {"アフィリエイト": 8, "比較": 6, "ノウハウ": 14}
json.dump(ids, open(os.path.join(ROOT, "tools", "_catids.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("保存OK")
