# -*- coding: utf-8 -*-
"""AI音楽クラスタの図解を生成(matplotlibはWindowsのpythonで実行)。images/に保存。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm
import os

# 日本語フォント
for cand in ["Yu Gothic","Meiryo","MS Gothic","Yu Gothic UI"]:
    if any(cand.lower() in f.name.lower() for f in fm.fontManager.ttflist):
        plt.rcParams["font.family"]=cand; print("font:",cand); break
plt.rcParams["axes.unicode_minus"]=False

IMG=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"images")
os.makedirs(IMG,exist_ok=True)
NAVY="#1f2a44"; BLUE="#2f6fed"; GREEN="#1faf6a"; ORANGE="#f08a24"; PINK="#e2447a"; GRAY="#5b6472"; LIGHT="#eef2f9"

def box(ax,x,y,w,h,text,fc,tc="white",fs=15,bold=True,r=0.04):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0.01,rounding_size={r}",
                fc=fc,ec="none"))
    ax.text(x+w/2,y+h/2,text,ha="center",va="center",color=tc,fontsize=fs,
            fontweight="bold" if bold else "normal",wrap=True)

def arrow(ax,x1,y1,x2,y2,c=GRAY):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=22,lw=3,color=c))

# ---------- 1) 137: 作る→配信→稼ぐ フロー ----------
fig,ax=plt.subplots(figsize=(12,6.75)); ax.set_xlim(0,12); ax.set_ylim(0,6.75); ax.axis("off")
ax.text(6,6.3,"AIで作った音楽で稼ぐ 3ステップ",ha="center",fontsize=24,fontweight="bold",color=NAVY)
steps=[("① 作る","Suno / Udio で\n文章から1曲",BLUE),
       ("② 配信する","DistroKid等で\nSpotify・YouTubeへ",GREEN),
       ("③ 稼ぐ","再生・販売・案件で\n収益化",ORANGE)]
for i,(t,s,c) in enumerate(steps):
    x=0.6+i*3.9
    box(ax,x,4.2,3.0,1.5,t,c,fs=20)
    ax.text(x+1.5,3.75,s,ha="center",va="top",fontsize=13,color=NAVY)
    if i<2: arrow(ax,x+3.0,4.95,x+3.9,4.95)
ax.text(6,2.85,"稼ぐ“4つの出口”",ha="center",fontsize=17,fontweight="bold",color=NAVY)
outs=[("ストリーミング","Spotify等で再生"),("ストック販売","BGMを何度も販売"),
      ("YouTube広告","作業用BGMで収益"),("クラウド案件","即金・1件3千〜")]
for i,(t,s) in enumerate(outs):
    x=0.5+i*2.95
    box(ax,x,1.0,2.6,1.4,"",LIGHT,r=0.05)
    ax.text(x+1.3,1.95,t,ha="center",fontsize=14,fontweight="bold",color=BLUE)
    ax.text(x+1.3,1.35,s,ha="center",fontsize=11.5,color=GRAY)
plt.savefig(os.path.join(IMG,"ai-music-flow.png"),dpi=100,bbox_inches="tight",facecolor="white"); plt.close()

# ---------- 2) 139: 配信サービス比較表 ----------
fig,ax=plt.subplots(figsize=(12,7.2)); ax.set_xlim(0,12); ax.set_ylim(0,7.2); ax.axis("off")
ax.text(6,6.85,"音楽配信サービス比較（AI可否で選ぶ）",ha="center",fontsize=22,fontweight="bold",color=NAVY)
cols=["サービス","AI音楽","料金タイプ","還元率","ひとこと"]
cw=[2.5,1.7,2.5,1.5,3.3]; x0=0.15; rowh=0.62; ytop=6.1
rows=[
 ("DistroKid","◎ 可","年定額・出し放題","100%","AI量産の本命",GREEN),
 ("SoundOn","◎ 可","無料","初年100%","TikTok狙い",GREEN),
 ("ドワンゴ","○ 可","無料・1曲〜","約60%","まず試す入口",BLUE),
 ("BIG UP!","○ 可","無料/有料","70〜100%","国内・無料枠",BLUE),
 ("Amuse","△ 要確認","無料/1曲課金","100%","スカウト機能",GRAY),
 ("CD Baby","△ 要確認","1曲買い切り","高め","たまに出す人",GRAY),
 ("TuneCore","× 100%AIは不可","1曲課金","約80%","日本語◎/人作り向き",PINK),
 ("LANDR","× 厳しい","定額(月12曲上限)","—","AIには不向き",PINK),
]
# header
xx=x0
for j,c in enumerate(cols):
    box(ax,xx,ytop,cw[j],rowh,c,NAVY,fs=13)
    xx+=cw[j]
for i,r in enumerate(rows):
    y=ytop-(i+1)*rowh
    xx=x0
    fc=LIGHT if i%2==0 else "#e3e9f4"
    vals=[r[0],r[1],r[2],r[3],r[4]]
    for j,v in enumerate(vals):
        box(ax,xx,y,cw[j],rowh,"",fc,r=0.02)
        tc=r[5] if j in(0,1) else NAVY
        ax.text(xx+cw[j]/2,y+rowh/2,v,ha="center",va="center",fontsize=11.5,
                fontweight="bold" if j in(0,1) else "normal",color=tc)
        xx+=cw[j]
ax.text(6,0.18,"※2026年時点。各社の最新規約は登録前に確認を。",ha="center",fontsize=10,color=GRAY)
plt.savefig(os.path.join(IMG,"music-distribution-compare.png"),dpi=100,bbox_inches="tight",facecolor="white"); plt.close()

# ---------- 3) 136: DistroKid vs TuneCore ----------
fig,ax=plt.subplots(figsize=(12,6.6)); ax.set_xlim(0,12); ax.set_ylim(0,6.6); ax.axis("off")
ax.text(6,6.2,"DistroKid と TuneCore どっち？",ha="center",fontsize=23,fontweight="bold",color=NAVY)
box(ax,0.5,5.1,5.3,0.8,"DistroKid",GREEN,fs=19)
box(ax,6.2,5.1,5.3,0.8,"TuneCore",PINK,fs=19)
d=["AI音楽：◎ 条件つきOK","料金：年定額で出し放題","還元率：100%","LINE MUSIC：× 非対応","向く人：AIで量産する人"]
t=["AI音楽：× 100%AIは不可","料金：1曲ごと課金","還元率：約80%","LINE MUSIC：○ 対応","向く人：人の手で少数精鋭"]
for i,(a,bb) in enumerate(zip(d,t)):
    y=4.4-i*0.78
    box(ax,0.5,y,5.3,0.64,"",LIGHT,r=0.03); ax.text(0.8,y+0.32,a,ha="left",va="center",fontsize=13,color=NAVY)
    box(ax,6.2,y,5.3,0.64,"",LIGHT,r=0.03); ax.text(6.5,y+0.32,bb,ha="left",va="center",fontsize=13,color=NAVY)
ax.text(6,0.25,"AIで量産するなら DistroKid／LINE MUSIC重視なら TuneCore",ha="center",fontsize=13,fontweight="bold",color=BLUE)
plt.savefig(os.path.join(IMG,"distrokid-vs-tunecore.png"),dpi=100,bbox_inches="tight",facecolor="white"); plt.close()

# ---------- 4) 138: Suno vs Udio ----------
fig,ax=plt.subplots(figsize=(12,6.2)); ax.set_xlim(0,12); ax.set_ylim(0,6.2); ax.axis("off")
ax.text(6,5.8,"Suno と Udio どっちを使う？",ha="center",fontsize=23,fontweight="bold",color=NAVY)
box(ax,0.5,4.7,5.3,0.8,"Suno",BLUE,fs=19)
box(ax,6.2,4.7,5.3,0.8,"Udio",ORANGE,fs=19)
s=["歌もの・万能型に強い","情報が多く初心者向き","日本語プロンプトOK","V5は最大8分・高音質","まずはコレ"]
u=["音質・作り込みがきれい","“produced”寄りの音","UMGと和解→権利クリーン","音にこだわる人向け","中〜上級者に"]
for i,(a,bb) in enumerate(zip(s,u)):
    y=4.0-i*0.72
    box(ax,0.5,y,5.3,0.58,"",LIGHT,r=0.03); ax.text(0.8,y+0.29,a,ha="left",va="center",fontsize=13,color=NAVY)
    box(ax,6.2,y,5.3,0.58,"",LIGHT,r=0.03); ax.text(6.5,y+0.29,bb,ha="left",va="center",fontsize=13,color=NAVY)
ax.text(6,0.2,"※どちらも商用利用は有料プラン。登録前に最新規約を確認。",ha="center",fontsize=10.5,color=GRAY)
plt.savefig(os.path.join(IMG,"suno-udio-compare.png"),dpi=100,bbox_inches="tight",facecolor="white"); plt.close()

# ---------- 5) 023: BGM収益の流れ ----------
fig,ax=plt.subplots(figsize=(12,6.0)); ax.set_xlim(0,12); ax.set_ylim(0,6.0); ax.axis("off")
ax.text(6,5.6,"登録者0でも稼げる BGM収益の仕組み",ha="center",fontsize=22,fontweight="bold",color=NAVY)
flow=[("楽曲を用意","Suno等で作る/外注",BLUE),("配信会社に登録","TuneCore等",GREEN),
      ("各SNSへ配信","YouTube/TikTok/Insta",ORANGE),("誰かが使う","動画のBGMに",PINK),("収益が発生","コンテンツID",NAVY)]
for i,(t,s,c) in enumerate(flow):
    x=0.3+i*2.35
    box(ax,x,3.3,2.05,1.2,t,c,fs=14)
    ax.text(x+1.02,2.95,s,ha="center",va="top",fontsize=10.5,color=GRAY)
    if i<4: arrow(ax,x+2.05,3.9,x+2.35,3.9)
ax.text(6,1.7,"原盤収益（平均RPM約4）＋ 著作権収益（RPM約30）の二重取りも",ha="center",fontsize=14,fontweight="bold",color=BLUE)
ax.text(6,1.05,"登録者・フォロワー0人でも、曲を出した時点でスタートできる",ha="center",fontsize=13,color=NAVY)
plt.savefig(os.path.join(IMG,"bgm-income-flow.png"),dpi=100,bbox_inches="tight",facecolor="white"); plt.close()

print("生成完了:",os.listdir(IMG))
