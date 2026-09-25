"""Gera ../huahum-real[-<lang>]-16x9/index.html a partir do index.html 9:16 (arg opcional: en|es) (mesmo conteúdo, layout 1920×1080).

Layout 16:9: topo com NOSSO PLANO / NOSSA AVENTURA grande · esquerda: mapa detalhado 1100×910 ·
direita: mapa geral 710×270, fotos 710×400, texto. Rodar de novo a cada mudança no 9:16.
"""
import os, re

import sys
HERE = os.path.dirname(os.path.abspath(__file__))
LANG = sys.argv[1] if len(sys.argv) > 1 else ''  # '' = PT; 'en'/'es' = saída de make_lang.py
NAME = 'huahum-real' + (f'-{LANG}' if LANG else '')
OUT = os.path.join(os.path.dirname(HERE), NAME + '-16x9')
s = open(os.path.join(os.path.dirname(HERE), NAME, 'index.html'), encoding='utf-8').read()

def rep(a, b, count=1):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, count)

rep('<meta name="viewport" content="width=1080, height=1920" />', '<meta name="viewport" content="width=1920, height=1080" />')
rep('data-width="1080" data-height="1920"', 'data-width="1920" data-height="1080"')
rep('const FW = 1000, FH = 570,', 'const FW = 1100, FH = 910,')
rep('const MW = 1000, MH = 320;', 'const MW = 710, MH = 270;')
rep('PHW = 1000, PHH = 440;', 'PHW = 710, PHH = 400;')
rep('<svg id="ov" viewBox="0 0 1000 570">', '<svg id="ov" viewBox="0 0 1100 910">')
rep('<svg id="mov" viewBox="0 0 1000 320">', '<svg id="mov" viewBox="0 0 710 270">')
rep("mEl('<div class=\"mlbl cty\">CHILE</div>', 34, 262)", "mEl('<div class=\"mlbl cty\">CHILE</div>', 20, 214)")

css = '''
      /* ===== LAYOUT 16:9 (make_16x9.py) ===== */
      html, body { width: 1920px; height: 1080px; }
      .bg-glow { left: 700px; top: -300px; }
      .bg-ghost { display: none; }
      #topbar { left: 40px; right: 40px; top: 12px; height: 108px; }
      #sec { font-size: 96px; }
      #frame { left: 40px; top: 130px; width: 1100px; height: 910px; }
      #ov { width: 1100px; height: 910px; }
      #scrim-top, #scrim-bot { width: 100%; }
      .stamp { left: 160px; top: 305px; }
      #mini { left: 1170px; top: 130px; width: 710px; height: 270px; }
      #mov { width: 710px; height: 270px; }
      #photos { left: 1170px; top: 416px; width: 710px; height: 400px; }
      .card { left: 1170px; top: 416px; width: 710px; height: 644px; }
      .kick { top: 422px; font-size: 20px; }
      .ttl { top: 454px; width: 710px; font-size: 64px; }
      .body { top: 530px; width: 710px; font-size: 22px; }
      .card .body.lo { top: 596px; font-size: 18px; }
      .schips { top: 454px; width: 710px; gap: 10px; }
      .schip { padding: 10px 12px; }
      .schip .v { font-size: 48px; } .schip .v small { font-size: 22px; } .schip .l { font-size: 13px; }
      #convoy .cars { top: 40px; width: 710px; height: 300px; }
      .cv { width: 340px; height: 300px; }
      #convoy .cv:nth-child(2) { left: 370px !important; }
      .cv .imgwrap { width: 340px; height: 180px; top: 20px; }
      .cv img { width: 310px; }
      .cv .floor { left: 20px; width: 300px; top: 200px; }
      .cv .nm { width: 340px; top: 214px; font-size: 46px; }
      .cv .sub { width: 340px; top: 266px; font-size: 15px; }
      #convoy .chips { top: 360px; width: 710px; }
      .chip .v { font-size: 52px; } .chip .v small { font-size: 26px; } .chip .l { font-size: 15px; }
      #credits .col { width: 710px; }
      #credits h3 { font-size: 48px; } #credits p { font-size: 16px; }
      .big .bgimg { width: 1920px; height: 1080px; }
      .big .k { top: 205px; }
      #mini-cap { left: auto; right: 14px; top: 12px; }
      .big h1 { top: 300px; font-size: 240px; }
      .big .rule { left: 760px; top: 800px; }
      .big .sub { top: 830px; }
'''
s = s.replace('    </style>', css + '    </style>', 1)
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(s)
for f in ('package.json', 'hyperframes.json', 'meta.json'):
    t = open(os.path.join(HERE, f), encoding='utf-8').read().replace('"huahum-real"', f'"{NAME}-16x9"')
    open(os.path.join(OUT, f), 'w', encoding='utf-8').write(t)
link = os.path.join(OUT, 'assets')
if not os.path.islink(link):
    os.symlink('../huahum-real/assets', link)
print('ok', OUT)
