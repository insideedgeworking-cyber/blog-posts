# -*- coding: utf-8 -*-
"""post_023に「二重取り・振込の遅さ・SNS別単価・2025/10削除祭り」を追加(2026最新参考ch字幕)。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")
fp = os.path.join(PD, "post_023.json")
d = json.load(open(fp, encoding="utf-8-sig"))
b = d["body"]

sec = """## “二重取り”できて、振込は遅い（知っておくと得）
BGM収益のうまみは、**広告収益と二重取り**できること。あなたが①YouTuberとして動画を投稿し、②自分の楽曲の“アーティスト”としても登録すれば、**1本の動画から広告収益＋BGM収益の両方**が入ります（「広告23万円＋BGM約4.6万円＝月28万円」という発信者も）。

ただし**振込はかなり遅い**ので注意。
- **原盤収益**：再生の約2〜3か月後に振込
- **著作権収益**：なんと約9〜12か月後（ほぼ1年後）。忘れた頃に届く“ボーナス”で、12月に35万円が振り込まれた人も
- 著作権収益は原盤の約7.5倍（RPM約30）と大きいので、**両方を取りこぼさない**のが大事

各SNSでも取れます（1本を使い回す）。単価の目安（2025年末）は、**YouTubeショートが最も高く**（広告0.03円・原盤0.004円・著作権0.030円）、**TikTokは原盤が極小**（0.001円）、**インスタ・Facebookは原盤0.002円**ほど（インスタはリールが伸びれば原盤だけで月3〜4万も）。

> ⚠️ **2025年10月ごろから、YouTubeはショート用に作られたBGM楽曲の“削除”を強化**しています（切り抜き・無断転載の荒稼ぎ対策）。削除されるとその月は0円、TuneCoreでは新規登録まで弾かれることも。**人が作ったオリジナル曲を使い・規約を守る**のが安全策です（この削除はYouTubeのみで、インスタ/TikTok/Facebookでは今のところ起きていません）。

## 楽曲を用意してTuneCoreに登録する（費用の目安）
- **曲は外注でOK**：自分で作れなくても、クラウドワークスやココナラで**1曲3,000円ほど**から依頼できます（※著作権を自分に譲渡する契約にする）
- **配信会社に登録**：TuneCoreなどに登録すると、YouTube・Instagram・TikTok等へ配信してくれます。費用は**1曲・年1,000円ちょい＋収益から手数料20%**（＝80%が自分に）
- **AIで作った曲は“100%AI”だと否認**：TuneCoreのガイドラインで明記。バレると剥奪・0円なので、人の手が入った曲にする

"""
a = "## 正直な話：今でも稼げるの？"
if "“二重取り”できて、振込は遅い" in b:
    print("既存 → skip")
elif a in b:
    b = b.replace(a, sec + a, 1); print("二重取り＋登録 挿入 OK")
else:
    print("[!] anchor不一致"); sys.exit(1)

d["body"]=b; d["char_count"]=len(b)
d["notes"]=(d.get("notes") or "")+" 2026最新参考ch字幕で追加(2026-06-13):広告とBGMの二重取り(例月28万)・振込の遅さ(原盤2-3ヶ月/著作権9-12ヶ月)・SNS別単価・2025/10からの楽曲削除祭り・楽曲外注3000円+TuneCore年1000円+手数料20%・100%AI曲は否認。"
json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("post_023 char=",d["char_count"])
