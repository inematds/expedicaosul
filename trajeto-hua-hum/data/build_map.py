"""Baixa tiles de satélite (Esri World Imagery) e monta 3 camadas no mesmo sistema Web Mercator.
Grava assets/map/<layer>.jpg + data/layers.json (origem em pixels globais de cada zoom)."""
import json, math, os, io, time, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from geo_util import get, lonlat_to_px, HERE

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'assets', 'map')
CACHE = os.path.join(HERE, 'tiles')
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)
URL = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'

LAYERS = {
    # nome: (zoom, lon_min, lat_min, lon_max, lat_max)
    'wide': (10, -73.40, -41.25, -69.80, -38.95),
    'mid': (12, -71.98, -40.36, -71.08, -39.84),
    'det': (14, -71.775, -40.205, -71.295, -39.985),
}


def tile(z, x, y):
    fn = os.path.join(CACHE, f'{z}_{x}_{y}.jpg')
    if not os.path.exists(fn):
        for a in range(5):
            try:
                data = get(URL.format(z=z, x=x, y=y), timeout=30)
                open(fn, 'wb').write(data)
                break
            except Exception as e:
                time.sleep(2 + a * 2)
        else:
            raise RuntimeError(f'tile falhou {z}/{x}/{y}')
    return fn


meta = {}
for name, (z, lo0, la0, lo1, la1) in LAYERS.items():
    x0, y0 = lonlat_to_px(lo0, la1, z)  # topo-esquerda
    x1, y1 = lonlat_to_px(lo1, la0, z)
    tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int(x1 // 256), int(y1 // 256)
    jobs = [(z, tx, ty) for ty in range(ty0, ty1 + 1) for tx in range(tx0, tx1 + 1)]
    print(name, 'tiles', len(jobs), flush=True)
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda j: tile(*j), jobs))
    W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    im = Image.new('RGB', (W, H))
    for (zz, tx, ty) in jobs:
        im.paste(Image.open(os.path.join(CACHE, f'{zz}_{tx}_{ty}.jpg')).convert('RGB'), ((tx - tx0) * 256, (ty - ty0) * 256))
    # recorta exatamente no bbox pedido
    cx0, cy0 = int(x0 - tx0 * 256), int(y0 - ty0 * 256)
    cx1, cy1 = int(x1 - tx0 * 256), int(y1 - ty0 * 256)
    im = im.crop((cx0, cy0, cx1, cy1))
    im.save(os.path.join(OUT, f'{name}.jpg'), quality=90)
    meta[name] = dict(z=z, ox=tx0 * 256 + cx0, oy=ty0 * 256 + cy0, w=im.width, h=im.height)
    print(name, meta[name], flush=True)

json.dump(meta, open(os.path.join(HERE, 'layers.json'), 'w'), indent=1)
