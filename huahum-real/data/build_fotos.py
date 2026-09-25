"""Monta assets/fotos.js a partir de data/fotos.txt.

Formato de cada linha (| separa):  segundo | arquivo | legenda
  - arquivo relativo a assets/ (ex.: fotos/IMG_1234.jpg); vazio = espaço "SUA FOTO"
  - fotos da viagem vão em assets/fotos/ (redimensionadas p/ no máx. 2000 px pelo lado maior)
Linhas começando com # são ignoradas. A foto fica na tela do seu segundo até o da próxima linha.
"""
import json, os
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
out = []
for ln in open(os.path.join(HERE, 'fotos.txt'), encoding='utf-8'):
    ln = ln.strip()
    if not ln or ln.startswith('#'):
        continue
    at, f, cap = [x.strip() for x in ln.split('|', 2)]
    d = {'at': float(at), 'cap': cap}
    if f:
        p = os.path.join(ROOT, 'assets', f)
        im = ImageOps.exif_transpose(Image.open(p))  # celular: respeita a rotação EXIF
        if max(im.size) > 2000 or im.mode != 'RGB':
            im.thumbnail((2000, 2000))
            im.convert('RGB').save(p, quality=88)
        d.update(src='assets/' + f, w=im.width, h=im.height)
        if f.startswith('photos/'):
            d['credit'] = 'Wikimedia Commons'
    out.append(d)
out.sort(key=lambda d: d['at'])
hdr = '// Gerado por data/build_fotos.py a partir de data/fotos.txt — não editar à mão.\n'
open(os.path.join(ROOT, 'assets', 'fotos.js'), 'w', encoding='utf-8').write(hdr + 'window.FOTOS = ' + json.dumps(out, ensure_ascii=False, indent=1) + ';\n')
print(len(out), 'fotos;', sum(1 for d in out if 'src' in d), 'com arquivo')
