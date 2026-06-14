# -*- coding: utf-8 -*-
"""公開Pass2準備:wp_post_id記録／本文画像を相対→raw URL化(localize_imagesが拾える形)／?p=リンクを実IDへ解決。"""
import json, os, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")
RAW = "https://raw.githubusercontent.com/insideedgeworking-cyber/blog-posts/main/images/"
SITE = "https://workstartedge.com/?p="
WPID = {'023':118,'136':112,'137':110,'138':114,'139':116}

def target(text):
    if '確定申告' in text or '税金' in text: return 'EXT'
    if '配信サービス' in text: return WPID['139']
    if 'Suno' in text or 'Udio' in text: return WPID['138']
    if '稼ぐ方法' in text:                 return WPID['137']
    if 'DistroKid' in text:               return WPID['136']
    if 'BGM' in text:                     return WPID['023']
    return None

for n,wid in WPID.items():
    fp=os.path.join(PD,f'post_{n}.json'); d=json.load(open(fp,encoding='utf-8-sig'))
    b=d['body']
    # 1) wp_post_id
    d['wp_post_id']=wid
    # 2) 画像 相対→raw
    b=b.replace('](images/', f']({RAW}')
    # 3) ?p= リンク解決
    def repl(m):
        txt=m.group(1); t=target(txt)
        if t=='EXT':  # 未公開の外部記事→リンク解除(太字テキスト化)
            return f'**{txt}**'
        if t is None:
            print(f'  [!!] post_{n} 未解決リンク: {txt}'); sys.exit(1)
        return f'[{txt}]({SITE}{t})'
    b=re.sub(r'\[([^\]]+)\]\(\?p=\)', repl, b)
    left=b.count('(?p=)')
    d['body']=b; d['char_count']=len(b)
    json.dump(d,open(fp,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(f"post_{n}: wp_id={wid} 画像raw化✓ ?p=残り{left} 画像数={b.count(RAW)}")
print("PREP DONE")
