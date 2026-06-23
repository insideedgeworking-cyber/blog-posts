# -*- coding: utf-8 -*-
import os,json,base64,urllib.request
c=json.load(open(os.path.join('..','wp-credentials.local.json'),encoding='utf-8-sig'))
TOK=base64.b64encode((c['username']+':'+c['application_password'].replace(' ','')).encode()).decode()
B=c['site_url'].rstrip('/')+'/wp-json/wp/v2'
def api(p,m='GET',payload=None):
    data=json.dumps(payload).encode() if payload is not None else None
    req=urllib.request.Request(B+p,data=data,method=m,headers={'Authorization':'Basic '+TOK,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(req,timeout=60))
sub=json.load(open('tools/_subcats.json'))
BLOG=sub['blog']; NOTE=sub['note']
ids=[17,18,13,10,15,12,19,20,21,22,23,24,11,7,3,9,BLOG,NOTE]
info={i:api('/categories/%d'%i) for i in ids}
L={i:info[i]['link'] for i in info}
N={i:info[i]['count'] for i in info}

# 大カテゴリ
big='display:block;padding:9px 12px;margin:5px 0;background:#f5f8fc;color:#1d3a5f;border-left:4px solid #2f6fb3;border-radius:0 6px 6px 0;cursor:pointer;font-weight:bold;list-style:none;text-decoration:none'
# 中カテゴリ（全部これで統一）
mid='display:block;padding:8px 12px;margin:4px 0;background:#fafcfe;color:#1d3a5f;border-left:3px solid #9bb4d8;border-radius:0 5px 5px 0;cursor:pointer;font-weight:bold;list-style:none;font-size:.95em;text-decoration:none'
# 小カテゴリ・すべて見る
small='display:block;padding:6px 10px;color:#2f6fb3;text-decoration:none;border-bottom:1px solid #eef0f4;font-size:.9em'

def smalllink(name,i,count=True):
    lab='%s（%d）'%(name,N[i]) if count else name
    return '<a href="%s" style="%s">%s</a>'%(L[i],small,lab)
def midbar(name,i):  # 子なしの中カテゴリ
    return '<a href="%s" style="%s">%s（%d）</a>'%(L[i],mid,name,N[i])
def midseeall(i):  # 「すべて見る」も中カテゴリと同じバー
    return '<a href="%s" style="%s">すべて見る（%d）</a>'%(L[i],mid,N[i])
def midacc(name,i,kids):  # 子ありの中カテゴリ（ブログ・note）
    return '<details style="margin:4px 0"><summary style="%s">%s（%d）</summary><div style="padding-left:14px">%s</div></details>'%(mid,name,N[i],kids)
def bigacc(name,i,inner):
    return '<details style="margin-bottom:2px"><summary style="%s">%s（%d）</summary><div style="padding-left:14px">%s</div></details>'%(big,name,N[i],inner)
def bigbar(name,i):
    return '<a href="%s" style="%s">%s（%d）</a>'%(L[i],big,name,N[i])

# ブログ・note（中・子あり）→ ブログ/note（小）
blognote=midacc('ブログ・note',13, smalllink('すべて見る',13,False)+smalllink('ブログ',BLOG)+smalllink('note',NOTE))

# AI副業（大）：ブログ・noteを一番上に＋中カテゴリ統一
ai_inner=(midseeall(17)+blognote+midbar('YouTube・動画',10)+midbar('AIライティング',15)
          +midbar('AI音楽',12)+midbar('Webライター',19)+midbar('スマホ・スキマ副業',20))
ai=bigacc('AI副業',17,ai_inner)

# 副業ツール（大）：中カテゴリ統一
tool_inner=(midseeall(18)+midbar('ブログツール',21)+midbar('AIツール',22)+midbar('動画ツール',23)+midbar('音楽ツール',24))
tool=bigacc('副業ツール',18,tool_inner)

html='<div><h3 class="wp-block-heading" style="margin-bottom:8px">カテゴリーから探す</h3>'+ai+tool+bigbar('SNS集客',11)+bigbar('用語辞典',7)+bigbar('体験談',3)+bigbar('副業の基礎・お金',9)+'</div>'
api('/widgets/block-7','POST',{'id_base':'block','instance':{'raw':{'content':'<!-- wp:html -->'+html+'<!-- /wp:html -->'}}})
print('更新OK（中カテゴリ統一・ブログnote最上部）')
