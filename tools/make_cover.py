# -*- coding: utf-8 -*-
"""記事のアイキャッチ（表紙）画像を生成する。青基調＋オレンジ差し色。
使い方: python make_cover.py 出力名 "メインタイトル" "サブ1" "サブ2" "ラベル"
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
os.makedirs(IMG_DIR, exist_ok=True)

BOLD = r"C:\Windows\Fonts\YuGothB.ttc"
MED  = r"C:\Windows\Fonts\YuGothM.ttc"
def font(path, size): return ImageFont.truetype(path, size, index=0)

W, H = 1200, 630
TOP    = (47, 111, 179)    # #2f6fb3 ブルー
BOTTOM = (29, 71, 120)     # 濃いブルー
ORANGE = (255, 138, 61)    # 差し色
WHITE  = (255, 255, 255)
SOFT   = (214, 228, 244)   # 薄い水色（サブ文字）

def make(out, title, sub1, sub2, label):
    img = Image.new("RGB", (W, H), TOP)
    d = ImageDraw.Draw(img)
    # 縦グラデーション
    for y in range(H):
        t = y / H
        c = tuple(int(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    # 装飾の円（うっすら）
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([W-260, -120, W+120, 260], fill=(255, 255, 255, 18))
    od.ellipse([W-160, 360, W+200, 720], fill=(255, 255, 255, 14))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    M = 80  # 左マージン
    # ラベル（オレンジのピル）
    lf = font(BOLD, 30)
    lb = d.textbbox((0, 0), label, font=lf)
    lw, lh = lb[2]-lb[0], lb[3]-lb[1]
    pad_x, pad_y = 24, 14
    d.rounded_rectangle([M, 70, M+lw+pad_x*2, 70+lh+pad_y*2+8], radius=10, fill=ORANGE)
    d.text((M+pad_x, 70+pad_y), label, font=lf, fill=WHITE)

    # メインタイトル（大）
    tf = font(BOLD, 92)
    d.text((M, 170), title, font=tf, fill=WHITE)
    # オレンジの下線バー
    tb = d.textbbox((0, 0), title, font=tf)
    d.rounded_rectangle([M, 170+ (tb[3]-tb[1]) + 36, M+200, 170+(tb[3]-tb[1])+48], radius=6, fill=ORANGE)

    # サブタイトル（2行）
    sf = font(MED, 40)
    y = 360
    for s in (sub1, sub2):
        if s:
            d.text((M, y), s, font=sf, fill=SOFT)
            y += 58

    # サイト名（下部）
    nf = font(MED, 30)
    d.text((M, H-72), "WorkStartEdge｜未経験から始める副業ログ", font=nf, fill=(180, 200, 222))

    path = os.path.join(IMG_DIR, out)
    img.save(path, quality=95)
    print("saved:", path)

if __name__ == "__main__":
    out   = sys.argv[1] if len(sys.argv) > 1 else "cover-post001.png"
    title = sys.argv[2] if len(sys.argv) > 2 else "飲食からの一歩"
    sub1  = sys.argv[3] if len(sys.argv) > 3 else "未経験の私が AI × ゲーム用PC で"
    sub2  = sys.argv[4] if len(sys.argv) > 4 else "副業を始めた話"
    label = sys.argv[5] if len(sys.argv) > 5 else "体験談"
    make(out, title, sub1, sub2, label)
