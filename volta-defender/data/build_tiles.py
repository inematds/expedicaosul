"""Mosaicos Esri World Imagery para uma viagem longa.
Uso: python3 build_tiles.py <route_full.json> <assets_dir>
Camadas: 'ov' z7 (visão geral), 'cor' z8 (corredor), e por parada: 'p10_<id>' z10 (±1.2°) e 'p12_<id>' z12 (±0.3° lon, ±0.25° lat).
Grava <assets_dir>/map/<nome>.jpg (graduado) e <assets_dir>/layers.js (window.LAYERS)."""
import json, os, sys, time, math
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import numpy as np
from geo_util import get, lonlat_to_px, HERE

R = json.load(open(sys.argv[1]))
ASSETS = sys.argv[2]
OUT = os.path.join(ASSETS, 'map'); os.makedirs(OUT, exist_ok=True)
CACHE = os.path.join(HERE, 'tiles'); os.makedirs(CACHE, exist_ok=True)
URL = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'

lons = [s['lon'] for s in R['stops']]; lats = [s['lat'] for s in R['stops']]
# bbox da rota a partir dos pontos (px z14 -> lon/lat)
def unpx(x, y, z=14):
    n = 256 * 2 ** z
    return x / n * 360 - 180, math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
ll = [unpx(*p) for p in R['pts'][::20]]
lo0, lo1 = min(p[0] for p in ll), max(p[0] for p in ll)
la0, la1 = min(p[1] for p in ll), max(p[1] for p in ll)
cx, cy = (lo0 + lo1) / 2, (la0 + la1) / 2
LAYERS = [
    ('ov', 7, cx - 17, cy - 9.5, cx + 17, cy + 9.5),
    ('cor', 8, lo0 - 2.2, la0 - 1.8, lo1 + 2.2, la1 + 1.8),
]
for s in R['stops']:
    LAYERS.append((f"p10_{s['id']}", 10, s['lon'] - 1.2, s['lat'] - 1.0, s['lon'] + 1.2, s['lat'] + 1.0))
    LAYERS.append((f"p12_{s['id']}", 12, s['lon'] - 0.3, s['lat'] - 0.25, s['lon'] + 0.3, s['lat'] + 0.25))
for extra in R.get('extra_patches', []):
    LAYERS.append(tuple(extra))


def tile(z, x, y):
    fn = os.path.join(CACHE, f'{z}_{x}_{y}.jpg')
    if not os.path.exists(fn):
        for a in range(6):
            try:
                open(fn, 'wb').write(get(URL.format(z=z, x=x, y=y), timeout=30)); break
            except Exception:
                time.sleep(2 + a * 2)
        else:
            raise RuntimeError(f'tile {z}/{x}/{y}')
    return fn


def grade(im):
    g = np.asarray(im).astype(np.float32) / 255
    l = g.mean(axis=2, keepdims=True)
    g = l + (g - l) * 0.85
    g = np.clip((g - 0.03) * 1.08, 0, 1) ** 1.06
    g[..., 0] *= 1.03; g[..., 2] *= 0.97
    return Image.fromarray(np.clip(g * 255, 0, 255).astype(np.uint8))


meta = {}
for name, z, a0, b0, a1, b1 in LAYERS:
    x0, y0 = lonlat_to_px(a0, b1, z); x1, y1 = lonlat_to_px(a1, b0, z)
    tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int(x1 // 256), int(y1 // 256)
    jobs = [(z, tx, ty) for ty in range(ty0, ty1 + 1) for tx in range(tx0, tx1 + 1)]
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda j: tile(*j), jobs))
    W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    im = Image.new('RGB', (W, H))
    for (zz, tx, ty) in jobs:
        im.paste(Image.open(os.path.join(CACHE, f'{zz}_{tx}_{ty}.jpg')).convert('RGB'), ((tx - tx0) * 256, (ty - ty0) * 256))
    cx0, cy0, cx1, cy1 = int(x0 - tx0 * 256), int(y0 - ty0 * 256), int(x1 - tx0 * 256), int(y1 - ty0 * 256)
    im = grade(im.crop((cx0, cy0, cx1, cy1)))
    im.save(os.path.join(OUT, f'{name}.jpg'), quality=86, optimize=True)
    meta[name] = dict(z=z, ox=tx0 * 256 + cx0, oy=ty0 * 256 + cy0, w=im.width, h=im.height, kind=name.split('_')[0])
    print(name, z, len(jobs), 'tiles', im.size, flush=True)
open(os.path.join(ASSETS, 'layers.js'), 'w').write('window.LAYERS = ' + json.dumps(meta) + ';\n')
print('ok', len(meta), 'camadas')
