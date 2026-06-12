# -*- coding: utf-8 -*-
"""SNS集客クラスタ用：X / Threads / Instagram の使い分け比較図。images/sns-compare.png
注意: matplotlibのtextで $ は数式扱い→使わない。"""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
os.makedirs(IMG, exist_ok=True)
_fp=None
for c in (r"C:\Windows\Fonts\YuGothM.ttc", r"C:\Windows\Fonts\meiryo.ttc"):
    if os.path.exists(c): _fp=c; break
_fpb=r"C:\Windows\Fonts\YuGothB.ttc"
def fp(sz,bold=False):
    f=font_manager.FontProperties(fname=(_fpb if bold and os.path.exists(_fpb) else _fp)); f.set_size(sz); return f
INK="#27313a"; GREY="#6b7682"
X_C="#1d9bf0"; TH_C="#2b2b2b"; IG_C="#d6336c"

fig,ax=plt.subplots(figsize=(11.2,6.9),dpi=160); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.6)
ax.text(0.15,7.25,"X・Threads・Instagram｜SNS集客の使い分け（2026）",fontproperties=fp(17,True),color=INK,va="center")

def card(x,name,maker,accent,rows,who):
    w=3.7
    ax.add_patch(FancyBboxPatch((x,0.5),w,5.7,boxstyle="round,pad=0.02,rounding_size=0.14",fc="white",ec=accent,lw=2.2))
    ax.add_patch(FancyBboxPatch((x,5.5),w,0.7,boxstyle="round,pad=0.02,rounding_size=0.14",fc=accent,ec=accent,lw=2.2))
    ax.text(x+w/2,5.85,name,ha="center",va="center",fontproperties=fp(15,True),color="white")
    ax.text(x+w/2,5.18,maker,ha="center",va="center",fontproperties=fp(9.5),color=GREY)
    y=4.66
    for label,val in rows:
        ax.text(x+0.25,y,label,fontproperties=fp(10.5,True),color=accent,va="top")
        ax.text(x+0.25,y-0.32,val,fontproperties=fp(9.8),color=INK,va="top")
        y-=1.0
    ax.add_patch(FancyBboxPatch((x+0.18,0.66),w-0.36,0.66,boxstyle="round,pad=0.02,rounding_size=0.1",fc="#f6f8fa",ec="#e3e8ee",lw=1.0))
    ax.text(x+w/2,0.99,who,ha="center",va="center",fontproperties=fp(9.3,True),color=accent)

card(0.15,"X（旧Twitter）","拡散 × 会話",X_C,[
 ("強み","テキストで瞬発的に拡散"),
 ("カギ","会話・初速・クラスター"),
 ("収益","集客→アフィリ／note"),
 ("向く人","文章が得意・最新発信"),
],"こんな人に：発信・最新情報")
card(4.15,"Threads（スレッズ）","先行者 × 共感",TH_C,[
 ("強み","今いちばん0→1で伸びる"),
 ("カギ","共感・24時間法則・初速"),
 ("収益","リンク直貼り→アフィリ"),
 ("向く人","ライバルが少ない今に"),
],"こんな人に：今すぐ0→1")
card(8.15,"Instagram","拡散 × ファン化",IG_C,[
 ("強み","リールで発見→ファン化"),
 ("カギ","リール・保存/シェア"),
 ("収益","物販・アフィリと好相性"),
 ("向く人","ビジュアルが得意"),
],"こんな人に：物販・ファン化")

fig.text(0.012,0.015,"※2026年時点の目安。まず1つに絞るのが伸びる近道。ThreadsとInstagramはMeta連携で同時に育てやすい。",fontproperties=fp(8.5),color=GREY)
fig.subplots_adjust(left=0.01,right=0.99,top=0.99,bottom=0.05)
fig.savefig(os.path.join(IMG,"sns-compare.png"),facecolor="white",bbox_inches="tight"); plt.close(fig)
print("saved sns-compare.png")
