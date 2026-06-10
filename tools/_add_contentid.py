# -*- coding: utf-8 -*-
"""post_023: コンテンツID解説を新設＋TuneCore Creatorsを新規募集停止に更新。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")
fp = os.path.join(PD, "post_023.json")
d = json.load(open(fp, encoding="utf-8-sig"))
b = d["body"]

# ① コンテンツID セクションを「## BGM収益は2種類ある」の前に挿入
cid = """## その正体は「コンテンツID」という仕組み
BGM収益が登録者0人でも成り立つのは、YouTubeの**コンテンツID（Content ID）**という仕組みのおかげです。ここを理解しておくと、リスクの避け方まで腑に落ちます。

**コンテンツIDとは**、「**音源や映像の“指紋”を登録しておくと、それが使われた動画をYouTubeが自動で見つけて、権利者に収益を渡す**」自動の権利管理システムです。BGM収益はこの仕組みの上に成り立っています。

- あなたの曲を配信会社経由で登録すると、その曲が**コンテンツIDに“指紋”として登録**される
- 誰か（あなた自身を含む）がその曲をショートや動画で使うと、**コンテンツIDが自動で「これはあなたの曲だ」と検出**する
- 検出された再生数に応じて、**使用料があなたに自動で配分**される

だから自分のチャンネルを伸ばさなくても、**曲が使われた分だけ受け取れる**わけです。ただし、この仕組みには**必ず守るべきルール**があります。

- **登録できるのは「自分が権利を持つオリジナル曲」だけ**：AIで作った曲はOKですが、他人の曲・既存曲・フリー素材を自分のものとして登録するのは**虚偽の権利主張**にあたり、最悪アカウント停止などの重いペナルティになります
- **同じ曲を複数人が登録すると“衝突”する**：コンテンツIDは「1つの音源に権利者は1人」が原則。同じ曲が重複登録されると、重複申し立て・収益保留・剥奪が起きます。**これが“収益剥奪”の正体**です
- **個人で直接は使えない**：コンテンツIDの利用は審査が厳しく、基本は**配信会社（TuneCore・AnyMind等）が代行で登録**します。だから次の「配信会社選び」が重要になります

"""
anchor = "## BGM収益は2種類ある"
if "コンテンツID（Content ID）" in b:
    print("Content IDセクション 既存 → skip insert")
elif anchor in b:
    b = b.replace(anchor, cid + anchor, 1); print("コンテンツIDセクション 挿入 OK")
else:
    print("[!] anchor不一致(2種類) → 中止"); sys.exit(1)

# ② TuneCore Creators の一文を「新規募集停止」に更新
old_tc = """なお、TuneCoreには「**TuneCore Creators**」という、自分で作曲せず“他人の既存楽曲の分配金を受け取る”仕組みもありますが、**同じ楽曲を使う他ユーザー全体が剥奪対象になりうる**ためリスクが高め。基本は「自分のオリジナル曲を配信する」やり方が安全です。"""
new_tc = """なお、TuneCoreには「**TuneCore Creators**」という、自分で作曲せず“他人の既存楽曲の分配金を受け取る”仕組みもありました。ただし、前述したコンテンツIDの「同じ曲の権利者は1人」という原則とぶつかり、**同じ楽曲を使う他ユーザーごと収益が剥奪される**トラブルが起きやすかったため、**現在は新規の募集を停止しています**（2026年時点）。いずれにせよ安全なのは「**自分が権利を持つオリジナル曲を配信する**」やり方です。受付状況やルールは変わるので、登録前に必ず公式の最新情報を確認してください。"""
if "現在は新規の募集を停止" in b:
    print("TuneCore Creators 既に更新済 → skip")
elif old_tc in b:
    b = b.replace(old_tc, new_tc, 1); print("TuneCore Creators 更新 OK")
else:
    print("[!] TuneCore Creators 一文 不一致 → 中止"); sys.exit(1)

d["body"] = b
d["char_count"] = len(b)
json.dump(d, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("post_023 char=", d["char_count"])
