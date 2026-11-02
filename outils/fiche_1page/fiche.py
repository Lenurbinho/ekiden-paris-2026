"""Fiche speaker une page (A4 paysage) : favoris + équipes et athlètes repérés, dans l'ordre des dossards.
Usage : python outils/fiche_1page/fiche.py 5.9 182mm 70 80   puis   node outils/fiche_1page/rendu.js
(taille du texte, hauteur des colonnes, longueur max des textes athlète / équipe).
À ADAPTER à chaque course : le bandeau TOP (titre, date, format, favoris) et FAV (dossards encadrés en rouge).
Si rendu.js affiche sw > cw, le contenu déborde : baisser la taille ou raccourcir les textes.
"""
import json, re, html, subprocess, sys
AT=int(sys.argv[3]) if len(sys.argv)>3 else 100
TN=int(sys.argv[4]) if len(sys.argv)>4 else 120
import os
B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','data')+'/'
ICI=os.path.dirname(os.path.abspath(__file__))
R=json.load(open(B+'reperes.json'));F=json.load(open(B+'ffa.json'));S=json.load(open(B+'startlist.json'))
T={t['d']:t for t in S['teams']}
CAT={'GP':'Grand public','EC':'Entreprise classique','EP':'Entreprise privilège','FFA':'Club FFA'}
DIST=['5','10','5','10','5','7,2']
E={int(e['dossard']):e for e in R['equipes']}
C={c['dossard']:c for c in R['coureurs']}
PAL={k:v for k,v in F['a'].items() if v.get('int') or v.get('nat') or v.get('rec')}
REMP={}
for r in R.get('remplacants',[]):REMP.setdefault(int(r['equipe']),[]).append(('rep',r))
for r in F.get('remplacants',[]):
    if r.get('int') or r.get('nat'):
        if not any(x[1]['nom'].split()[-1].upper() in r['nom'].upper() for x in REMP.get(int(r['equipe']),[])):REMP.setdefault(int(r['equipe']),[]).append(('ffa',r))
e=html.escape
def cap(s):return re.sub(r"(^|[\s\-'])(\w)",lambda m:m.group(1)+m.group(2).upper(),s.lower())
def short(t,n=150):
    t=t.strip()
    if len(t)<=n:return t
    cut=t[:n];i=max(cut.rfind('. '),cut.rfind(' ; '))
    return (cut[:i+1] if i>60 else cut.rsplit(' ',1)[0]+'…')
def best_pb(v):
    df=v.get('df','')
    for want in ('10 km route','semi-marathon','5000m','5 km route','1500m','marathon'):
        for x in df.split(' · '):
            lib,_,rest=x.partition('\t')
            if lib==want:
                m=re.search(r"/ (\S+)",rest) or re.search(r"^(\S+)",rest)
                if m and m.group(1)!='-':return f"{lib.replace('semi-marathon','semi').replace(' km route','k').replace('m','') if lib.endswith('route') else lib.replace('semi-marathon','semi')} {m.group(1)}"
    return ''
def palshort(v):
    items=[x for x in (v.get('int','')+' / '+v.get('nat','')).split(' / ') if x.strip() and x.strip()!='…']
    return ' · '.join(items[:3])
SKIP={1607,1608,1668}
E[1356]=dict(E[1356],titre='France Télévisions',texte='3 équipes : 1356, 1607, 1608.')
E[1666]=dict(E[1666],titre='Ville de Paris',texte='Espaces verts (1666) et Jeunesse et sports (1668).')
teams=sorted(set(E)|{int(k.split('.')[0]) for k in C}|{int(k.split('.')[0]) for k in PAL}|set(REMP))
FAV={1,2,3,4,5,159,1384,1609,1613}
blocks=[]
for d in teams:
    t=T.get(d)
    if not t or d in SKIP:continue
    h=f'<div class="tm{" fav" if d in FAV else ""}"><div class="th"><b class="n">{d}</b> <b>{e(t["e"])}</b> <i>{CAT.get(t["c"],"")}</i></div>'
    if d in E:
        ee=E[d];h+=f'<div class="tn"><b>{e(ee["titre"])}</b>{(" — "+e(short(ee["texte"],TN))) if ee["texte"] and not any(k.startswith(f"{d}.") for k in list(C)+list(PAL)) else ""}</div>'
    for o in range(1,7):
        k=f'{d}.{o}';r=t['r'][o-1];c=C.get(k);p=PAL.get(k)
        if not c and not p:continue
        ver=c and re.search('VÉRIFIER|HOMONYME',c['titre'])
        nm=f'{cap(r[0])} {r[1].upper()}'+(f' ({r[3]})' if r[3] else '')
        h+=f'<div class="at{" v" if ver else ""}"><span class="k">R{o}<small>{DIST[o-1]}</small></span><span><b>{e(nm)}</b> '
        if c:h+=f'<u>{e(c["titre"].replace("À VÉRIFIER · ","⚠ "))}</u> {e(short(c["texte"],AT))}'
        else:h+=f'<u>Palmarès FFA</u> {e(palshort(p))}'
        pb=best_pb(F['a'].get(k,{}))
        if pb and (not c or pb.split()[-1] not in c['texte']):h+=f' <em>{e(pb)}</em>'
        h+='</span></div>'
    for kind,r in REMP.get(d,[]):
        if kind=='rep':h+=f'<div class="at"><span class="k">Rempl.</span><span><b>{e(r["nom"])}</b> <u>{e(r["titre"].split(" (")[0])}</u> {e(short(r["texte"],AT))}</span></div>'
        else:h+=f'<div class="at"><span class="k">Rempl.</span><span><b>{e(cap(r["nom"]))}</b> <u>Palmarès FFA</u> {e(palshort(r))}</span></div>'
    h+='</div>';blocks.append(h)
TOP='''<div class="top"><div class="ti"><b>MAIF EKIDEN DE PARIS</b><span>Dimanche 1<sup>er</sup> novembre 2026 · 13<sup>e</sup> édition · départ 9h00 · 42,195 km en 6 relais (5 – 10 – 5 – 10 – 5 – 7,195 km)</span></div>
<div class="fv"><b>FAVORIS & RECORDS</b> Record de l'épreuve <b>1h58'05</b> · <b>3</b> Pays de Fontainebleau vise le record de France H (<b>2h02'43</b>, passages 14'32 / 29'05) · <b>5</b> USBW vise le record de Belgique H (<b>2h02'37</b>, aussi record d'Europe) · <b>2</b> Zoom Volt Runners, vainqueurs au scratch 2024 · <b>1</b> Faster Toget'her, 6 internationales, vise le record de France F (<b>2h22'53</b>, passages 16'56 / 33'52) · <b>4</b> USBW dames vise le record de Belgique F (<b>2h31'13</b>) · <b>159</b> SCO Sainte-Marguerite (Gilavert, Navarro remplaçant) · <b>1609 / 1613</b> Police nationale (Bourgoin, Périault, Rochat, Rayet) · <b>1384</b> Elite Athletes en entreprises.</div></div>'''
def page(fs):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@page{{size:A4 landscape;margin:5mm}}*{{box-sizing:border-box}}body{{margin:0;font-family:"DejaVu Sans Condensed","Liberation Sans Narrow",Arial,sans-serif;font-size:{fs}pt;line-height:1.18;color:#0b1b33}}
.top{{display:flex;gap:6px;margin-bottom:3px}}.ti{{background:#001d46;color:#fff;padding:3px 7px;border-radius:3px;min-width:58mm}}.ti b{{display:block;font-size:{fs*2.1}pt;letter-spacing:.02em;color:#fff}}.ti b::first-letter{{color:#ff3045}}.ti span{{font-size:{fs*.95}pt}}
.fv{{flex:1;background:#d8f0ec;border-left:4px solid #e3001b;padding:2px 6px;border-radius:3px;font-size:{fs*1.02}pt}}.fv>b:first-child{{color:#e3001b;margin-right:3px}}
.cols{{column-count:5;column-gap:5px;column-fill:auto;height:{{H}}}}
.tm{{break-inside:avoid;border:0.5px solid #b8c6d6;border-radius:3px;margin:0 0 2px;padding:1px 3px}}.tm.fav{{border:1px solid #e3001b;background:#fff7f8}}
.th{{border-bottom:0.5px solid #d5dee6;padding-bottom:1px;margin-bottom:1px}}.th .n{{color:#e3001b;font-size:{fs*1.35}pt}}.th i{{color:#5a6b80;font-size:{fs*.88}pt}}
.tn{{color:#4a3500;background:#fff4d6;padding:0 2px;margin:1px 0}}.tn b{{margin-right:2px}}
.at{{display:grid;grid-template-columns:{fs*3.2}pt 1fr;gap:2px;margin-top:1px}}.at .k{{font-weight:700;color:#12407f}}.at .k small{{display:block;font-weight:400;color:#7a8799;font-size:{fs*.8}pt;line-height:1}}
.at u{{text-decoration:none;color:#12407f;font-weight:700}}.at.v u{{color:#e3001b}}.at em{{font-style:normal;background:#e8f0fb;padding:0 2px;border-radius:2px;white-space:nowrap}}
.foot{{font-size:{fs*.8}pt;color:#6b7a8c;margin-top:1px}}
</style></head><body>{TOP}<div class="cols">{''.join(blocks)}</div>
<div class="foot">⚠ = identité à confirmer sur place · encadré bleu = record personnel FFA · Encadrés rouges = favoris / équipes de tête · Sources : startlist du 31/10, athle.fr, World Athletics, Wikidata/presse · Site : lenurbinho.github.io/ekiden-paris-2026</div></body></html>'''
import sys
fs=float(sys.argv[1]);H=sys.argv[2]
open(os.path.join(ICI,'fiche.html'),'w').write(page(fs).replace('{H}',H))
print(len(blocks),'blocs')
