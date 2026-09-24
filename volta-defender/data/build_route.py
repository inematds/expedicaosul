"""Rota da volta: OSRM (A) + ferry Colonia Express (OSM) + OSRM (B), km cumulativo único.
Saídas: data/route_full.json (para os outros scripts) e assets/route.js (para a composição)."""
import json, os, bisect, time, urllib.parse, math
from geo_util import get, haversine, lonlat_to_px, HERE

ROOT = os.path.dirname(HERE)
Z = 14
A = json.load(open(os.path.join(HERE, 'osrm_A.json')))['routes'][0]
B = json.load(open(os.path.join(HERE, 'osrm_B.json')))['routes'][0]
F = json.load(open(os.path.join(HERE, 'ferry.json')))
STOPS = json.load(open(os.path.join(HERE, 'stops.json')))

# --- concatena geometria com km cumulativo e marca trechos
coords, cum = [], []
def add(seq):
    for p in seq:
        if coords:
            d = haversine(coords[-1], p)
            if d < 1e-6:
                continue
            cum.append(cum[-1] + d)
        else:
            cum.append(0.0)
        coords.append(tuple(p))

add(A['geometry']['coordinates'])
km_ferry0 = cum[-1] / 1000
add(F['coords'])
km_ferry1 = cum[-1] / 1000
add(B['geometry']['coordinates'])
TOTAL = cum[-1] / 1000
print('total', round(TOTAL, 1), 'ferry', round(km_ferry0, 1), '->', round(km_ferry1, 1))


def at_km(km):
    m = km * 1000
    i = max(1, min(len(cum) - 1, bisect.bisect_left(cum, m)))
    a, b = coords[i - 1], coords[i]
    t = (m - cum[i - 1]) / max(1e-9, cum[i] - cum[i - 1])
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def km_of(pt):
    best = (1e18, 0)
    for i in range(0, len(coords) - 1):
        d = haversine(pt, coords[i])
        if d < best[0]:
            best = (d, cum[i] / 1000)
    return best[1], best[0]


STEP = 0.15
N = int(TOTAL / STEP) + 1
pts = []
for k in range(N + 1):
    x, y = lonlat_to_px(*at_km(min(TOTAL, k * STEP)), Z)
    pts.append([round(x, 1), round(y, 1)])

# --- nomes de estrada por km (steps do OSRM), trechos curtos (<3 km) herdam o anterior
roads = []
def steps_roads(route, km0):
    k = km0
    for leg in route['legs']:
        for s in leg['steps']:
            ref = (s.get('ref') or '').split(';')[0].strip()
            name = ref or s.get('name') or ''
            if s['distance'] > 3000 and name:
                roads.append([round(k, 2), name])
            k += s['distance'] / 1000
steps_roads(A, 0)
roads.append([round(km_ferry0, 2), 'FERRY · COLONIA EXPRESS'])
steps_roads(B, km_ferry1)
# compacta consecutivos iguais
comp = []
for k, n in roads:
    if not comp or comp[-1][1] != n:
        comp.append([k, n])
print('trechos de estrada', len(comp))

# --- altimetria SRTM30m a cada 5 km (água = null -> tratado como nível do rio)
EF = os.path.join(HERE, 'elev.json')
if not os.path.exists(EF):
    samples = [min(TOTAL, i * 5.0) for i in range(int(TOTAL / 5) + 2)]
    ll = [at_km(k) for k in samples]
    ele = []
    for i in range(0, len(ll), 100):
        chunk = '|'.join(f'{la:.5f},{lo:.5f}' for lo, la in ll[i:i + 100])
        for a in range(4):
            try:
                d = json.loads(get('https://api.opentopodata.org/v1/srtm30m?locations=' + chunk, timeout=60)); break
            except Exception as e:
                time.sleep(3)
        ele += [r['elevation'] for r in d['results']]
        time.sleep(1.3)
    json.dump({'km': samples, 'ele': ele}, open(EF, 'w'))
E = json.load(open(EF))
ele = [(e if e is not None else 0) for e in E['ele']]
for i, k in enumerate(E['km']):
    if km_ferry0 <= k <= km_ferry1:
        ele[i] = 0
print('elev min/max', min(ele), max(ele))

# --- fronteira UY/BR em Rivera/Livramento (OSM admin_level=2, bbox pequeno)
BF = os.path.join(HERE, 'border_uybr.json')
if not os.path.exists(BF):
    q = '[out:json][timeout:60];way["boundary"="administrative"]["admin_level"="2"](-31.05,-55.75,-30.75,-55.35);out geom;'
    open(BF, 'wb').write(get('https://overpass-api.de/api/interpreter', data=urllib.parse.urlencode({'data': q}).encode(), timeout=120))
BB = json.load(open(BF))
border = [[[round(v, 1) for v in lonlat_to_px(p['lon'], p['lat'], Z)] for p in e['geometry']] for e in BB['elements'] if 'geometry' in e]
bpts = [p for w in border for p in w]
k0 = int(1900 / STEP); k1 = int(2330 / STEP)
best = (1e18, 0)
for k in range(k0, min(k1, len(pts))):
    x, y = pts[k]
    d = min((x - bx) ** 2 + (y - by) ** 2 for bx, by in bpts)
    if d < best[0]:
        best = (d, k * STEP)
km_uybr = round(best[1], 1)
print('fronteira UY/BR km', km_uybr, 'dist px', round(best[0] ** .5, 1))

# --- paradas (do link) e passagens
stops = []
for sid, name, kind in [('sma', 'San Martín de los Andes', 'stop'), ('bb', 'Bahía Blanca', 'stop'), ('moreno', 'Moreno', 'stop'),
                        ('ferry_ba', 'Colonia Express · Buenos Aires', 'stop'), ('ferry_col', 'Colonia del Sacramento', 'stop'),
                        ('livramento', "Sant'Ana do Livramento", 'stop'), ('poa', 'Porto Alegre', 'stop'), ('canela', 'Canela', 'stop')]:
    km, dist = km_of(tuple(STOPS[sid]))
    if sid == 'ferry_ba': km = km_ferry0
    if sid == 'ferry_col': km = km_ferry1
    if sid == 'sma': km = 0.0
    if sid == 'canela': km = TOTAL
    lo, la = at_km(km); x, y = lonlat_to_px(lo, la, Z)
    stops.append(dict(id=sid, name=name, kind=kind, km=round(km, 1), x=round(x, 1), y=round(y, 1), lon=round(lo, 4), lat=round(la, 4), snap_m=round(dist)))
    print(sid, round(km, 1), 'snap', round(dist), 'm')

out = dict(total_km=round(TOTAL, 1), step_km=STEP, z=Z, pts=pts, km_ferry=[round(km_ferry0, 2), round(km_ferry1, 2)], km_uybr=km_uybr,
           roads=comp, elev=dict(km=E['km'], ele=[round(v) for v in ele]), border_uybr=border, stops=stops,
           ferry=dict(name=F['name'], duration=F['duration_tag'], osm_way=F['id']),
           osrm_hours=round((A['duration'] + B['duration']) / 3600, 1), road_km=round(TOTAL - (km_ferry1 - km_ferry0), 1))
json.dump(out, open(os.path.join(HERE, 'route_full.json'), 'w'))
print('route_full ok', len(pts), 'pts')
