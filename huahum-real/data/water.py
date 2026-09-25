"""Baixa polígonos de água (OSM) e repinta os lagos das camadas de satélite + grade de cor.
Saída: assets/map/<layer>_g.jpg (graded)."""
import json, os, urllib.parse
import numpy as np, cv2
from PIL import Image
from geo_util import get, lonlat_to_px, HERE

ROOT = os.path.dirname(HERE)
MAP = os.path.join(ROOT, 'assets', 'map')
L = json.load(open(os.path.join(HERE, 'layers.json')))
WF = os.path.join(HERE, 'water_osm.json')

if not os.path.exists(WF):
    bb = (-41.25, -73.40, -38.95, -69.80)
    q = f"""[out:json][timeout:180];
(way["natural"="water"]({bb[0]},{bb[1]},{bb[2]},{bb[3]});
 relation["natural"="water"]({bb[0]},{bb[1]},{bb[2]},{bb[3]});
 way["waterway"="riverbank"]({bb[0]},{bb[1]},{bb[2]},{bb[3]}););
out geom;"""
    data = get('https://overpass-api.de/api/interpreter', data=urllib.parse.urlencode({'data': q}).encode(), timeout=300)
    open(WF, 'wb').write(data)
osm = json.load(open(WF))


def join_rings(ways):
    """ways: lista de listas de (lon,lat). Junta por extremidades em anéis fechados."""
    ways = [list(w) for w in ways if len(w) > 1]
    rings = []
    while ways:
        cur = ways.pop(0)
        changed = True
        while cur[0] != cur[-1] and changed:
            changed = False
            for i, w in enumerate(ways):
                if w[0] == cur[-1]:
                    cur += w[1:]
                elif w[-1] == cur[-1]:
                    cur += w[::-1][1:]
                elif w[-1] == cur[0]:
                    cur = w + cur[1:]
                elif w[0] == cur[0]:
                    cur = w[::-1] + cur[1:]
                else:
                    continue
                ways.pop(i)
                changed = True
                break
        rings.append(cur)
    return rings


polys = []  # (outer_rings, inner_rings)
for e in osm['elements']:
    if e['type'] == 'way' and 'geometry' in e:
        g = [(p['lon'], p['lat']) for p in e['geometry']]
        if g[0] == g[-1]:
            polys.append(([g], []))
    elif e['type'] == 'relation':
        outer = [[(p['lon'], p['lat']) for p in m['geometry']] for m in e['members'] if m.get('role') == 'outer' and 'geometry' in m]
        inner = [[(p['lon'], p['lat']) for p in m['geometry']] for m in e['members'] if m.get('role') == 'inner' and 'geometry' in m]
        polys.append((join_rings(outer), join_rings(inner)))
print('polígonos de água', len(polys))

WATER_DEEP = np.array([22, 52, 70], np.float32)   # BGR-agnóstico: usamos RGB abaixo
WATER_SHORE = np.array([38, 88, 104], np.float32)

for name, m in L.items():
    z = m['z']
    im = np.array(Image.open(os.path.join(MAP, f'{name}.jpg')).convert('RGB')).astype(np.float32)
    H, W = im.shape[:2]
    mask = np.zeros((H, W), np.uint8)
    for outer, inner in polys:
        for ring, val in [(r, 255) for r in outer] + [(r, 0) for r in inner]:
            if len(ring) < 4:
                continue
            pts = np.array([[lonlat_to_px(lo, la, z)[0] - m['ox'], lonlat_to_px(lo, la, z)[1] - m['oy']] for lo, la in ring], np.float32)
            if pts[:, 0].max() < 0 or pts[:, 1].max() < 0 or pts[:, 0].min() > W or pts[:, 1].min() > H:
                continue
            cv2.fillPoly(mask, [np.round(pts * 4).astype(np.int32)], val, lineType=cv2.LINE_AA, shift=2)
    # distância à margem → gradiente de profundidade
    dist = cv2.distanceTransform((mask > 127).astype(np.uint8), cv2.DIST_L2, 5)
    scale = {10: 5, 12: 10, 14: 26}[z]
    t = np.clip(dist / scale, 0, 1)[..., None]
    water = WATER_SHORE * (1 - t) + WATER_DEEP * t
    # textura sutil do satélite dentro d'água (luminância centrada, baixa amplitude)
    lum = im.mean(axis=2, keepdims=True)
    blur = cv2.GaussianBlur(lum, (0, 0), 6)[..., None] if lum.ndim == 2 else cv2.GaussianBlur(lum[..., 0], (0, 0), 6)[..., None]
    water = water + (lum - blur) * 0.10
    a = (cv2.GaussianBlur(mask, (0, 0), 0.8).astype(np.float32) / 255)[..., None]
    out = im * (1 - a) + water * a
    # grade de terra: leve dessaturação, contraste e tom quente nas altas
    g = out / 255
    lumg = g.mean(axis=2, keepdims=True)
    g = lumg + (g - lumg) * 0.82
    g = np.clip((g - 0.03) * 1.08, 0, 1)
    g = g ** 1.06
    g[..., 0] *= 1.03
    g[..., 2] *= 0.97
    out = np.clip(g * 255, 0, 255).astype(np.uint8)
    Image.fromarray(out).save(os.path.join(MAP, f'{name}_g.jpg'), quality=88, optimize=True)
    Image.fromarray(mask).save(os.path.join(HERE, 'qa', f'mask_{name}.png'))
    print(name, 'ok', W, H)
