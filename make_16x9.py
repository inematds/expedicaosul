"""Gera a variante 16:9 de um projeto de rota (motor genérico) trocando só os blocos de layout marcados.
Uso: python3 make_16x9.py <projeto_9x16> <projeto_16x9>   (assets entram por link simbólico)"""
import os, re, sys, shutil, json

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
html = open(os.path.join(src, 'index.html')).read()

CSS = """/*LAYOUT-CSS-START 16x9*/
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: var(--bg); }
      .bg-glow { width: 1300px; height: 1300px; left: 920px; top: -80px; }
      #topbar { left: 40px; right: 40px; top: 24px; height: 60px; }
      #frame { left: 40px; top: 100px; width: 1160px; height: 940px; }
      #intro-title, #end-title { width: 1080px; }
      #rail { left: 1240px; top: 100px; width: 640px; height: 110px; }
      .card { left: 1240px; top: 236px; width: 640px; height: 804px; }
      .ph { width: 640px; height: 360px; }
      .inset { right: 18px; top: 206px; width: 240px; height: 160px; }
      .txt { top: 384px; width: 640px; }
      .body { font-size: 26px; width: 630px; }
      .databox .big { font-size: 118px; }
      .databox .lab { left: 300px; top: 40px; font-size: 19px; } .databox .lab.b { top: 74px; }
      .databox svg { left: 30px; top: 160px; width: 580px; height: 130px; }
      .databox .ax { top: 316px; font-size: 16px; }
      .stats { width: 640px; height: 360px; }
      .stat .v { font-size: 78px; } .stat .v small { font-size: 34px; }
      #intro-card .vimg { top: 50px; width: 640px; height: 230px; } #intro-card .vimg img { width: 480px; }
      #intro-card .floor { left: 80px; top: 280px; width: 480px; }
      #intro-card .nm { top: 300px; width: 640px; font-size: 66px; } #intro-card .sub { top: 376px; width: 640px; }
      #intro-card .chips { top: 640px; width: 640px; }
      .chip .v { font-size: 54px; } .chip .v small { font-size: 26px; }
      .chip .l { font-size: 14px; }
      #credits p { font-size: 21px; } #credits .col { width: 640px; }
      /*LAYOUT-CSS-END*/"""
JS = '/*LAYOUT-JS-START*/ const LAYOUT = { FW: 1160, FH: 940, RW: 640, TTL: 92, TTLMIN: 56, TXTW: 640, DSVG: [580, 130], stampX: 260, stampY: 320 }; /*LAYOUT-JS-END*/'

html = re.sub(r'/\*LAYOUT-CSS-START 9x16\*/.*?/\*LAYOUT-CSS-END\*/', CSS, html, flags=re.S)
html = re.sub(r'/\*LAYOUT-JS-START\*/.*?/\*LAYOUT-JS-END\*/', JS, html, flags=re.S)
html = re.sub(r'<!--VIEWPORT-->.*?<!--/VIEWPORT-->', '<!--VIEWPORT--><meta name="viewport" content="width=1920, height=1080" /><!--/VIEWPORT-->', html, flags=re.S)
html = html.replace('data-width="1080" data-height="1920"', 'data-width="1920" data-height="1080"')
assert 'LAYOUT-CSS-START 16x9' in html and 'FW: 1160' in html and 'data-width="1920"' in html
open(os.path.join(dst, 'index.html'), 'w').write(html)

for f in ['hyperframes.json', 'package.json', 'CLAUDE.md', 'AGENTS.md']:
    if os.path.exists(os.path.join(src, f)):
        shutil.copy(os.path.join(src, f), os.path.join(dst, f))
meta = json.load(open(os.path.join(src, 'meta.json')))
meta['id'] = meta['name'] = os.path.basename(os.path.abspath(dst))
json.dump(meta, open(os.path.join(dst, 'meta.json'), 'w'), indent=2)
link = os.path.join(dst, 'assets')
if not os.path.exists(link):
    os.symlink(os.path.relpath(os.path.join(src, 'assets'), dst), link)
print('ok', dst)
