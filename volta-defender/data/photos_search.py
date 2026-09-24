"""Busca candidatos no Wikimedia Commons e monta folhas de contato. Uso: python3 photos_search.py queries.json outdir"""
import json, sys, time, re, os, urllib.parse
from geo_util import get
from PIL import Image, ImageDraw, ImageFont
Q=json.load(open(sys.argv[1])); OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
allc={}
for key,qs in Q.items():
    seen=set(); rows=[]
    for q in qs:
        u="https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrlimit=10&gsrsearch="+urllib.parse.quote(q)+"&prop=imageinfo&iiprop=url|size|extmetadata|mime&iiurlwidth=330"
        d={}
        for a in range(4):
            try: d=json.loads(get(u)); break
            except Exception as e: time.sleep(6)
        for pid,p in d.get('query',{}).get('pages',{}).items():
            ii=p['imageinfo'][0]
            if ii['mime']!='image/jpeg' or p['title'] in seen or ii['width']<1400 or ii['width']<ii['height']: continue
            seen.add(p['title']); md=ii.get('extmetadata',{})
            rows.append(dict(title=p['title'],w=ii['width'],h=ii['height'],lic=md.get('LicenseShortName',{}).get('value',''),
                artist=re.sub('<[^>]+>','',md.get('Artist',{}).get('value','')).strip()[:80],thumb=ii['thumburl'],page=ii['descriptionurl']))
        time.sleep(1.5)
    rows=rows[:12]; allc[key]=rows
    tiles=[]
    for i,r in enumerate(rows):
        fn=f'{OUT}/{key}_{i:02d}.jpg'
        if not os.path.exists(fn):
            for a in range(4):
                try: open(fn,'wb').write(get(r['thumb'])); break
                except Exception: time.sleep(5)
            time.sleep(0.8)
        try: im=Image.open(fn).convert('RGB')
        except Exception: continue
        im.thumbnail((330,250)); t=Image.new('RGB',(330,275),'black'); t.paste(im,(0,0))
        ImageDraw.Draw(t).text((4,252),f"{i} {r['lic'][:14]}",fill='yellow',font=font); tiles.append(t)
    if tiles:
        s=Image.new('RGB',(330*4,275*((len(tiles)+3)//4)),'gray')
        for j,t in enumerate(tiles): s.paste(t,((j%4)*330,(j//4)*275))
        s.save(f'{OUT}/sheet_{key}.jpg',quality=80)
    print(key,len(rows),flush=True)
json.dump(allc,open(f'{OUT}/candidates.json','w'),ensure_ascii=False,indent=1)
