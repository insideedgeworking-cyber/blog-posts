# -*- coding: utf-8 -*-
"""カテゴリ再編 STEP3：全公開記事を新カテゴリへ振り分け（メイン＋兼任）。
ルール：旧カテゴリ→新メイン（副業/比較はタイトルで分割）＋ ツール記事は兼任。
各記事の old->new を表示。--apply で実際に反映、無しなら確認のみ(dry)。
ローカルJSONのcategoryも新メイン名に更新（再公開時の維持のため）。
"""
import os, json, base64, glob, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(os.path.dirname(ROOT), "wp-credentials.local.json"), encoding="utf-8-sig"))
TOK = base64.b64encode((c["username"] + ":" + c["application_password"].replace(" ", "")).encode()).decode()
B = c["site_url"].rstrip("/") + "/wp-json/wp/v2"
ids = json.load(open(os.path.join(ROOT, "tools", "_catids.json"), encoding="utf-8"))
APPLY = "--apply" in sys.argv

def api(path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(B + path, data=data, method=method,
        headers={"Authorization": "Basic " + TOK, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def main_cat(old, title):
    if old in ("ブログ", "ブログ・note", "アフィリエイト", "ノウハウ"):
        return "ブログ・note"
    if old in ("YouTube", "YouTube・動画"):
        return "YouTube・動画"
    if old in ("AI活用", "AIライティング"):
        return "AIライティング"
    if old in ("AI音楽",):
        return "AI音楽"
    if old in ("用語", "用語辞典"):
        return "用語辞典"
    if old == "体験談":
        return "体験談"
    if old == "SNS集客":
        return "SNS集客"
    if old == "比較":
        if "AIツール" in title or "ChatGPT" in title:
            return "AIツール"
        if "Webライター" in title:
            return "Webライター"
        return "ブログ・note"  # note vs ブログ 等
    if old in ("副業", "副業の基礎・お金"):
        if "選び方" in title or "バレない" in title or "確定申告" in title:
            return "副業の基礎・お金"
        if "AIを使った副業" in title:
            return "AIライティング"
        if "Webライター" in title or "クラウドソーシング" in title:
            return "Webライター"
        if "スマホ副業" in title or "運用代行" in title or "動画編集" in title or "ポイ活" in title:
            return "スマホ・スキマ副業"
        return "副業の基礎・お金"
    return None  # 不明（要確認）

def kenms(title):
    out = []
    if any(k in title for k in ["レンタルサーバー", "WordPressテーマ", "サーチコンソール", "GA4"]):
        out.append("ブログツール")
    if "AIライティングツール" in title:
        out.append("AIツール")
    if "動画編集ソフト" in title:
        out.append("動画ツール")
    if any(k in title for k in ["Suno", "Udio", "DistroKid", "音楽配信サービス"]):
        out.append("音楽ツール")
    return out

rows, unknown = [], []
for f in sorted(glob.glob(os.path.join(ROOT, "posts", "post_*.json"))):
    d = json.load(open(f, encoding="utf-8-sig"))
    w = d.get("wp_post_id")
    if not w:
        continue
    title = d.get("title", "")
    m = main_cat(d.get("category", ""), title)
    if not m:
        unknown.append((d.get("id"), d.get("category"), title[:30]))
        continue
    names = [m] + (kenms(title) if m != "用語辞典" else [])
    cat_ids = [ids[n] for n in names]
    rows.append((f, d, w, names, cat_ids))

print("=== 振り分け結果（%d本）%s ===" % (len(rows), "[APPLY]" if APPLY else "[DRY]"))
for f, d, w, names, cat_ids in rows:
    print("  wp%-4s %-22s -> %s" % (w, (d.get("title","")[:22]), "／".join(names)))
    if APPLY:
        api("/posts/%d" % w, "POST", {"categories": cat_ids})
        d["category"] = names[0]
        json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if unknown:
    print("\n★要確認（未割当）:", unknown)
print("\n%s" % ("反映しました" if APPLY else "確認のみ（--apply で反映）"))
