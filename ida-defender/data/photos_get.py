"""Baixa fotos escolhidas (1920px padrão -> 1600px) e grava créditos. Uso: python3 photos_get.py picks.json <assets_dir>
picks.json: {"chave_saida": ["pasta_cand", "categoria", indice], ...}"""
import json, sys, os, re, time
from geo_util import get
from PIL import Image
P=json.load(open(sys.argv[1])); A=sys.argv[2]; os.makedirs(f'{A}/photos',exist_ok=True)
cred={}
cache={}
for out,(d,cat,i) in P.items():
    if d not in cache: cache[d]=json.load(open(f'{d}/candidates.json'))
    r=cache[d][cat][i]; u=re.sub(r'/(\d+)px-',r'/1920px-',r['thumb'])
    data=None
    for a in range(6):
        try: data=get(u); break
        except Exception as e:
            u2=re.sub(r'/(\d+)px-',r'/1280px-',r['thumb'])
            try: data=get(u2); break
            except Exception: time.sleep(6)
    fn=f'{A}/photos/{out}.jpg'; open(fn,'wb').write(data)
    im=Image.open(fn).convert('RGB'); im.thumbnail((1600,1600)); im.save(fn,quality=88)
    cred[out]=dict(file=r['title'].replace('File:',''),author=r['artist'] or 'Wikimedia Commons',license=r['lic'],page=r['page'])
    print(out,im.size,r['lic'],'|',cred[out]['author'][:40],flush=True); time.sleep(1.5)
json.dump(cred,open(f'{A}/../data/photo_credits.json','w'),ensure_ascii=False,indent=1)
