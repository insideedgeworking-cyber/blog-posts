# -*- coding: utf-8 -*-
"""最新情報との照合で修正(2026-06-15):DistroKid値上げ($22.99→$24.99)・Suno最新v5.5・
Apple/Spotify単価の精度・訴訟(Warnerは Suno/Udio 両方和解)・TuneCoreのAI例外(Udioは可)。"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")
def load(n): fp=os.path.join(PD,f"post_{n}.json"); return fp,json.load(open(fp,encoding="utf-8-sig"))
def R(b,old,new,tag,all=False):
    if old not in b: print(f"  [!!] {tag} 不一致: {old[:34]}"); sys.exit(1)
    print(f"  [ok] {tag}"+(" (all)" if all else "")); return b.replace(old,new) if all else b.replace(old,new,1)

# ===== 136 =====
fp,d=load("136"); b=d["body"]; print("post_136:")
b=R(b,"## 元になる曲の作り方｜Suno V5でプロ級にするコツ","## 元になる曲の作り方｜Suno（v5.5）でプロ級にするコツ","heading V5")
b=R(b,"Sunoの最新モデル（V5）は、**最大8分のフル尺**","Sunoの最新モデル（v5.5）は、**最大8分のフル尺**","本文V5")
b=R(b,"さらにV5には、曲の雰囲気を保ったまま音を磨く","さらにv5.5には、曲の雰囲気を保ったまま音を磨く","本文V5-2")
b=R(b,"いちばん安い「Musician」プランは**年$22.99（約3,500円）**","いちばん安い「Musician」プランは**年$24.99（約3,800円）**","特徴price")
b=R(b,"- **Musician（年$22.99・約3,500円）**：1名義で配信し放題。","- **Musician（年$24.99・約3,800円）**：1名義で配信し放題。","Musician price")
b=R(b,"- **Musician Plus（上位）**：複数のアーティスト名義を使いたい人向け。歌詞表示などの機能も追加","- **Musician Plus（年$44.99・約6,800円）**：複数のアーティスト名義を使いたい人向け。歌詞表示などの機能も追加","MusicianPlus price")
b=R(b,"年3,500円ということは、**1か月あたり約300円**。","年3,800円ということは、**1か月あたり約320円**（2026年に$22.99から値上げ）。","月額換算+値上げ注記")
d["body"]=b; d["char_count"]=len(b)
d["notes"]=(d.get("notes") or "")+" ファクト更新(2026-06-15):DistroKid Musician $22.99→$24.99(約3,800円)・Plus $44.99追記/Suno最新V5→v5.5。"
json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2); print("  char=",d["char_count"])

# ===== 137 =====
fp,d=load("137"); b=d["body"]; print("post_137:")
b=R(b,"（DistroKidは年約3,500円）","（DistroKidは年約3,800円）","FAQ price")
b=R(b,"（Spotifyの数倍という試算も）","（Spotifyの約2倍。1再生あたり約1円前後）","Apple単価精度")
b=R(b,"約0.3〜0.5円","約0.4〜0.7円","Spotify単価精度",all=True)
d["body"]=b; d["char_count"]=len(b)
d["notes"]=(d.get("notes") or "")+" ファクト更新(2026-06-15):DistroKid年約3,800円/Spotify単価0.4〜0.7円・Appleは約2倍(1再生約1円・2026実数$0.003-0.005 vs $0.007-0.01)。"
json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2); print("  char=",d["char_count"])

# ===== 138 =====
fp,d=load("138"); b=d["body"]; print("post_138:")
b=R(b,"**ワーナーはSunoと和解（2025年11月）**、**UMGはUdioと和解（2025年10月）**してライセンス契約へ。和解した曲は“クリーン”に使えるようになりつつあります",
      "**ワーナーはSuno・Udioの両方と和解（2025年11月）**、**UMGはUdioと和解（2025年10月）**してライセンス契約へ。和解した曲は“クリーン”に使えるようになりつつあり、**Udioはライセンス済みプラットフォーム扱い**に（後述のTuneCoreでもUdio製なら配信できるケースが出てきました）","訴訟Warner両方+Udio扱い")
b=R(b,"## 最新モデル（V5）でできること\nSunoの最新モデルは、これまでの音楽AIのハードルをほぼ取り払いました。\n\n",
      "## 最新モデル（v5.5）でできること\nSunoの最新モデルは**v5.5**（2026年3月〜）。これまでの音楽AIのハードルをほぼ取り払い、さらに“あなた専用”に寄せる機能が増えました。\n\n","V5節 heading+intro")
b=R(b,"- **プロンプト制御が細かく**：より具体的な指示が通る\n",
      "- **プロンプト制御が細かく**：より具体的な指示が通る\n- **Voices（自分の声）**：自分の声を録音・アップロードして歌わせられる（ベータ・1曲4クレジット）\n- **Custom Models／My Taste**：自分の曲を6曲以上学習させた“自分専用Suno”を作れる・好みも学習\n","v5.5新機能bullet")
d["body"]=b; d["char_count"]=len(b)
d["notes"]=(d.get("notes") or "")+" ファクト更新(2026-06-15):Suno最新v5.5(2026/3・Voices/Custom Models/My Taste追加・最大8分は据置)/訴訟はWarnerがSuno・Udio両方と和解・Udioはライセンス済扱い。"
json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2); print("  char=",d["char_count"])

# ===== 139 =====
fp,d=load("139"); b=d["body"]; print("post_139:")
b=R(b,"**料金**：年$22.99（約3,500円）〜の**年定額で出し放題**","**料金**：年$24.99（約3,800円）〜の**年定額で出し放題**","DistroKid price")
b=R(b,"- **DistroKid**：出し放題なので**年約3,500円ぽっきり**","- **DistroKid**：出し放題なので**年約3,800円ぽっきり**","cost例")
b=R(b,"約0.3〜0.5円","約0.4〜0.7円","Spotify単価",all=True)
b=R(b,"- **ひとこと**：日本語サポートは魅力だが、**AI量産とは相性が悪い**",
      "- **ひとこと**：日本語サポートは魅力だが、**AI量産とは相性が悪い**（※“人の手が入った曲”や、ライセンス契約済みの**Udio製**なら配信できる場合あり）","TuneCore例外")
d["body"]=b; d["char_count"]=len(b)
d["notes"]=(d.get("notes") or "")+" ファクト更新(2026-06-15):DistroKid年$24.99(約3,800円)/Spotify単価0.4〜0.7円/TuneCoreは人手入り・ライセンス済Udio製なら配信可の例外を追記。"
json.dump(d,open(fp,"w",encoding="utf-8"),ensure_ascii=False,indent=2); print("  char=",d["char_count"])
print("DONE")
