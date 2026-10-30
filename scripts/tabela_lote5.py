#!/usr/bin/env python3
"""Gera data/remix/curadoria_lote5_tabela.md a partir dos CSVs filtrados + curadoria/lote5/*/meta.json (rode de novo quando a transcrição terminar)."""
import csv,json,glob,os,re
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(R)
meta={}
for p in glob.glob('curadoria/lote5/*/meta.json'):
    d=json.load(open(p)); d['dir']=os.path.dirname(p); meta[d['id']]=d
BUY=re.compile(r'onde (compr|encontr|acho|tem|vende)|aonde|donde|dónde|dond |where|link|how much|how do i order|quanto|cuánto|precio|dove|où |como compr|nome d|does it work|funciona|valor|quero link|qual o',re.I)
# produto -> (produto, termo busca Shopee, vendas, preço)
P={'b02':('mochila de transporte pet (inferido pelos comentários)','mochila transporte cachorro','1mil+','R$ 64,33'),
'b03':('casinha/toca de pano p/ gato (inferido pelo título)','casinha cama gato barraca','3mil+','R$ 37,90'),
'b06':('bota/sapato de silicone p/ patas','sapato cachorro verao','2mil+','R$ 22,99'),
'b07':('túnel de brinquedo p/ gato (inferido pelos comentários)','tunel gato brinquedo','3mil+','R$ 24,90'),
'b10':('escova/dedeira dental pet','dedeira escova dente cachorro','10mil+','R$ 10,00'),
'b17':('bebedouro portátil p/ cães','bebedouro cachorro portatil','9mil+','R$ 28,88'),
'b20':('camisa de time p/ pet','camisa time futebol pet cachorro','1mil+','R$ 25,00'),
'b25':('bebedouro portátil p/ cães','bebedouro cachorro portatil','9mil+','R$ 28,88'),
'b26':('rampa p/ cachorro subir na cama','rampa cachorro cama','3mil+','R$ 78,99'),
'b27':('protetor de ouvido (abafador) p/ cão','protetor ouvido cachorro','50mil+','R$ 15,88'),
'b29':('brinquedo/escova dental p/ cão','dedeira escova dente cachorro','10mil+','R$ 10,00'),
'b31':('fonte/bebedouro automático p/ gato','fonte bebedouro gato automatico','30mil+','R$ 37,98'),
'b32':('escova secadora pet','escova secadora pet cachorro','10mil+','R$ 42,99'),
'b39':('comedouro lento/elevado','comedouro elevado cachorro lento','2mil+','R$ 35,99')}
SHFAIL={'b05':'item 4: colete/boia pet 334 vendas (<1 mil)','b09':'item 4: capa/bolsa de secagem 919 vendas (<1 mil)','b18':'item 4: puff-rampa R$ 179 (>R$ 100), 4 vendas','b21':'item 4: bolsa de banho p/ gato 330 vendas (<1 mil)','b23':'item 4: chuveiro/ducha pet 752 vendas (<1 mil)','b38':'item 4: tapete gelado 895 vendas (<1 mil)','b08':'item 4: produto ≈ US$ 80 (>R$ 100)','b12':'item 5: perfil de marca vendendo, "link na bio"'}
EX=json.load(open('data/remix/lote5_B_verificacao_extra.json'))
for _i,_v in EX['passaram'].items(): P[_v['cid']]=(_v['produto'],_v['busca'],_v['vendas'],_v['preco'])
def sh(kw): return 'https://shopee.com.br/search?keyword='+kw.replace(' ','%20')
def load(f):
    return list(csv.DictReader(open(f,encoding='utf-8')))
out=['# Curadoria lote 5 — tabela única (30/10/2026) · régua v5','',
'Gerada por `scripts/tabela_lote5.py`. Passou = pré-requisitos NUMÉRICOS da v5 + (B) sinal de compra nos 10 comentários + Shopee. Julgar humor (riso) e "produto visível em uso" é com o Fable, assistindo com áudio; nada aqui é opinião.','']
def k(n):
    n=float(n or 0); return f'{n/1e6:.1f} mi' if n>=1e6 else f'{n/1e3:.0f} mil'
for V,f in (('A','data/remix/lote5_filtro_A.csv'),('B','data/remix/lote5_filtro_B.csv')):
    rows=load(f)
    rows.sort(key=lambda r:(r['passou']!='s',-float(r['compart_pct'] or 0)))
    out+=[f'## Vertente {V} — todos os medidos ({len(rows)})','','| # | id | conta | fonte | link | views | curtidas | coment. | compart. % | idade d | dur s | passou? | cid |','|-|-|-|-|-|-|-|-|-|-|-|-|-|']
    npass=0
    for i,r in enumerate(rows,1):
        m=meta.get(r['id']); cid=m['cid'] if m else ''
        ok=r['passou']=='s'
        if V=='B' and m:
            cid=m['cid']
            c=open(m['dir']+'/comentarios.txt').read().splitlines()[:10] if os.path.exists(m['dir']+'/comentarios.txt') else []
            buy=any(BUY.search(l) for l in c) and cid not in ('b19','b22','b33','b36','b34','b01','b04','b05','b11','b13','b14','b15','b16','b24','b30','b35','b37','b40')
            if cid in SHFAIL: ok=False; mot=SHFAIL[cid]
            elif not buy: ok=False; mot='item 3: nenhum "onde compro/link/nome/funciona?" nos 10 comentários mais curtidos'
            elif cid not in P: ok=False; mot='Shopee não conferida (produto não identificado)'
            else: mot='—'
            r['motivo']=mot; r['passou']='s' if ok else 'n'
            if ok: npass+=1
        elif V=='B' and ok and r['id'] in EX['verificados_sem_passar']: ok=False; r['motivo']=EX['verificados_sem_passar'][r['id']]['motivo']
        elif V=='B' and ok: ok=False; r['motivo']='numérico ok, mas itens 1/3/4 NÃO verificados (fora dos 40 pré-selecionados por título/comentários)'
        elif ok: npass+=1
        out.append(f"| {i} | {r['id']} | {r['conta']} | {r['fonte'][:40]} | {r['link']} | {k(r['views'])} | {k(r['curtidas'])} | {r['coment']} | {r['compart_pct']} | {r['idade_d']} | {r['dur']} | {'s' if ok else 'n — '+r['motivo']} | {cid} |")
    out+=['',f'**Passaram: {npass} de {len(rows)}** (mínimo da piscina: {"30" if V=="A" else "20"}).','']
    if V=='A': passA=npass
    else: passB=npass
out+=['## Detalhe dos baixados','','| cid | conta | link | views | compart. % | dur | folha | transcrição | 10 comentários | produto · busca Shopee · vendas · preço |','|-|-|-|-|-|-|-|-|-|-|']
for m in sorted(meta.values(),key=lambda d:d['cid']):
    d=m['dir']; cid=m['cid']
    tr='sim' if os.path.exists(d+'/transcricao.txt') else 'pendente'
    fo='sim' if os.path.exists(d+'/folha.jpg') else 'não'
    co='sim' if os.path.exists(d+'/comentarios.txt') else 'não'
    pr=''
    if cid in P: p=P[cid]; pr=f"{p[0]} · [busca]({sh(p[1])}) · {p[2]} · {p[3]}"
    elif cid.startswith('b'): pr=SHFAIL.get(cid,'—')
    out.append(f"| {cid} | {m['conta']} | {m['link']} | {k(m['views'])} | {m['compart_pct']} | {m['dur']} | {fo} | {tr} | {co} | {pr} |")
open('data/remix/curadoria_lote5_tabela.md','w',encoding='utf-8').write('\n'.join(out)+'\n')
print('A passou',passA,'B passou',passB)
