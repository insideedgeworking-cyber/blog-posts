# -*- coding: utf-8 -*-
"""post_023: AI音楽規制の現状＋AIっぽすぎると落ちる＋著者のギターBGM体験を新設、
配信サービスにDistroKid追加・TuneCoreのフルAI禁止を明記。出典=Web調査(2025-2026)。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")
fp = os.path.join(PD, "post_023.json")
d = json.load(open(fp, encoding="utf-8-sig"))
b = d["body"]

# ① AI規制セクションを「## 配信サービスの選び方（重要）」の前に挿入
airegs = """## AI曲は“そのまま出すと弾かれる”時代に（重要）
ここ最近で大きな変化があります。**配信プラットフォーム側のAI規制が、2025年から一気に厳しくなりました。**

- **Spotify**は2025年9月、スパム的な**AI量産曲を約7,500万曲も削除**し、AI使用の表示義務とスパムフィルターを導入
- **Deezer**には**1日3万曲ものフルAI曲**が届いており、検出してタグ付け・おすすめから除外・収益化停止を実施
- 流れは「2025年＝見つけたら消す」→「2026年＝禁止ではなく“開示義務＋規制”」へ。**どの配信会社も“入口”でAIをチェック**するようになりました

そして重要なのが、**いかにもAIな曲は検出されやすい**ということ。AI生成音には信号上の“指紋”（ステレオ感の不自然さ・高音域の不自然なカット・メタデータに残るAIツール名など）が残るため、**「AIっぽすぎる曲」は審査で弾かれたり、後から削除されたりしやすい**のです。

> 💡 **私の体験**：私は**いかにもAIっぽくない、ギター中心のBGM**で申請したら、問題なく通りました。生楽器っぽい音・人間の演奏に近い曲はAIの“指紋”が出にくく、審査を通りやすい印象です。逆に、ピコピコした典型的な“AIっぽい曲”ほど弾かれやすいと感じます。

だから、AIで作るとしても次を意識してください。

- **AIっぽさが強すぎる曲は避ける**：生楽器系（ギター・ピアノなど）や、人間が手を加えた“自然な”曲にする
- **AIを使ったら正直に「開示」する**：多くの配信会社はアップロード時に**AI使用のチェック項目**があり、隠すと規約違反になります
- **権利が100%自分にあることを確認**：他人の声やフレーズの模倣はNG。AIツールの**商用利用条件**も必ず確認

"""
anchor = "## 配信サービスの選び方（重要）"
if "AI曲は“そのまま出すと弾かれる”時代" in b:
    print("AI規制セクション 既存 → skip")
elif anchor in b:
    b = b.replace(anchor, airegs + anchor, 1); print("AI規制セクション 挿入 OK")
else:
    print("[!] anchor(配信サービス)不一致 → 中止"); sys.exit(1)

# ② 配信サービスの3バレット→5バレット（DistroKid追加・TuneCoreフルAI禁止・CD Baby）
old_bul = """- **AnyMind Music**：分配率は実績次第で50〜80%。**収益剥奪の事例が少なく、リスクが低い**のが強み。初心者はまずここが無難
- **TuneCore（チューンコア）**：分配率80%。利用者がいちばん多い定番。ただし**2024年8月に大規模な収益剥奪**が起き、その後も規制が強化されています。リスクは中〜高め
- **Shorts Music（韓国系）**：かつては単価が高めとされましたが、**2024年12月に振り込み保留**が起きるなどリスクが高く、中抜き率も高いと言われます"""
new_bul = """- **AnyMind Music**：分配率は実績次第で50〜80%。**収益剥奪の事例が少なく、リスクが低い**のが強み。初心者はまずここが無難
- **DistroKid（ディストロキッド）**：世界的な定番。主要各社の中で**AIにいちばん寛容**で、Suno／Udio製の曲も配信実績があります。ただし**アップロード時にAI使用の開示が必須**・権利は100%自分のものが条件で、**ポリシーは後から遡って適用**（過去に通った曲も現行ルール違反なら削除されうる）。料金は年額制
- **TuneCore（チューンコア）**：分配率80%・利用者最多の定番。ただし**100%AIで作った曲の配信は禁止**（人間が意味のある形で関わった曲のみ可）で、AI関与は開示が必要。2024年8月の大規模剥奪など規制も強化。**AI主体で作るなら相性は良くありません**
- **Shorts Music（韓国系）**：かつては単価が高めとされましたが、**2024年12月に振り込み保留**が起きるなどリスクが高く、中抜き率も高いと言われます
- **CD Baby**：参考までに、**AIで作った曲を全面的に受け付けない**最も厳格なタイプの会社もあります"""
if "DistroKid（ディストロキッド）" in b:
    print("配信サービス 既に更新済 → skip")
elif old_bul in b:
    b = b.replace(old_bul, new_bul, 1); print("配信サービス バレット更新 OK")
else:
    print("[!] 配信サービス バレット不一致 → 中止"); sys.exit(1)

# ③ 優先順位の一文をAI考慮版に
old_lead = "優先順位の目安は **①AnyMind Music → ②TuneCore → ③Shorts Music**。"
new_lead = "BGM収益（YouTube）目線での無難さは **AnyMind Music ＞ TuneCore ＞ Shorts Music**。ただし**AIで作った曲を出すなら、AIに寛容なDistroKidや、剥奪リスクの低いAnyMindが安全**です。TuneCoreはフルAI不可なので、AI主体の人は“人間の関与”を足すか別を選ぶのが無難。"
if old_lead in b:
    b = b.replace(old_lead, new_lead, 1); print("優先順位リード更新 OK")
elif "BGM収益（YouTube）目線での無難さは" in b:
    print("優先順位リード 既に更新済 → skip")
else:
    print("[!] 優先順位リード不一致（要確認）")

d["body"] = b
d["char_count"] = len(b)
d["excerpt"] = "YouTubeのBGM収益とは？登録者0でも即日始められる仕組み(コンテンツID)と始め方を解説。楽曲の用意(Suno/Udio等のAI作曲)、配信サービスの選び方(AnyMind/DistroKid/TuneCore等)。2025年以降のAI音楽規制強化(Spotify7500万曲削除・TuneCoreはフルAI禁止)、AIっぽすぎると審査落ちする理由、著者がギター系BGMで通った実体験まで正直にまとめます。"
json.dump(d, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("post_023 char=", d["char_count"])
