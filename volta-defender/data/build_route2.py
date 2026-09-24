"""Rota longa genérica por config: pernas OSRM + ferry (OSM), km cumulativo único.
Uso: python3 build_route2.py trip.json   (roda dentro da pasta data da viagem)
trip.json: {"legs": ["osrm_A.json", "FERRY", "osrm_B.json"], "ferry_reverse": false,
            "border": {"bbox": [s,w,n,e], "km": [k0,k1], "from": "UY", "to": "BR"},
            "countries": [["AR",0], ...] (preenchido depois com km reais),
            "stops": [[id, nome, tipo, km_override|null], ...], "passages": [[id, nome, lon, lat], ...]}"""
import json, os, sys, bisect, time, urllib.parse
from geo_util import get, haversine, lonlat_to_px, HERE

T = json.load(open(sys.argv[1]))
Z = 14
STOPS = json.load(open('stops.json'))
coords, cum, marks, hours = [], [], {}, 0.0


def add(seq):
    for p in seq:
        p = tuple(p)
        if coords:
            d = haversine(coords[-1], p)
            if d < 1e-6:
                continue
            cum.append(cum[-1] + d)
        else:
            cum.append(0.0)
        coords.append(p)


steps_src = []
for leg in T['legs']:
    if leg == 'FERRY':
        F = json.load(open('ferry.json'))
        g = F['coords'][::-1] if T.get('ferry_reverse') else F['coords']
        marks['ferry0'] = cum[-1] / 1000
        add(g)
        marks['ferry1'] = cum[-1] / 1000
        steps_src.append(('FERRY', marks['ferry0']))
    else:
        r = json.load(open(leg))['routes'][0]
        k0 = cum[-1] / 1000 if cum else 0.0
        add(r['geometry']['coordinates'])
        hours += r['duration'] / 3600
        steps_src.append((r, k0))
TOTAL = cum[-1] / 1000
print('total', round(TOTAL, 1), 'ferry', round(marks['ferry0'], 1), '->', round(marks['ferry1'], 1))


def at_km(km):
    m = km * 1000
    i = max(1, min(len(cum) - 1, bisect.bisect_left(cum, m)))
    a, b = coords[i - 1], coords[i]
    t = (m - cum[i - 1]) / max(1e-9, cum[i] - cum[i - 1])
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def km_of(pt):
    best = (1e18, 0)
    for i in range(len(coords)):
        d = haversine(pt, coords[i])
        if d < best[0]:
            best = (d, cum[i] / 1000)
    return best[1], best[0]


STEP = 0.15
pts = []
for k in range(int(TOTAL / STEP) + 2):
    x, y = lonlat_to_px(*at_km(min(TOTAL, k * STEP)), Z)
    pts.append([round(x, 1), round(y, 1)])

roads = []
for src, k in steps_src:
    if src == 'FERRY':
        roads.append([round(k, 2), 'FERRY · COLONIA EXPRESS'])
        continue
    for leg in src['legs']:
        for s in leg['steps']:
            ref = (s.get('ref') or '').split(';')[0].strip()
            name = ref or s.get('name') or ''
            if s['distance'] > 3000 and name:
                roads.append([round(k, 2), name])
            k += s['distance'] / 1000
comp = []
for k, n in roads:
    if not comp or comp[-1][1] != n:
        comp.append([k, n])

EF = 'elev.json'
if not os.path.exists(EF):
    samples = [min(TOTAL, i * 5.0) for i in range(int(TOTAL / 5) + 2)]
    ll = [at_km(k) for k in samples]
    ele = []
    for i in range(0, len(ll), 100):
        chunk = '|'.join(f'{la:.5f},{lo:.5f}' for lo, la in ll[i:i + 100])
        for a in range(5):
            try:
                d = json.loads(get('https://api.opentopodata.org/v1/srtm30m?locations=' + chunk, timeout=60)); break
            except Exception:
                time.sleep(4)
        ele += [r['elevation'] for r in d['results']]
        time.sleep(1.3)
    json.dump({'km': samples, 'ele': ele}, open(EF, 'w'))
E = json.load(open(EF))
ele = [(e if e is not None else 0) for e in E['ele']]
for i, k in enumerate(E['km']):
    if marks['ferry0'] <= k <= marks['ferry1']:
        ele[i] = 0

border, km_border = [], None
if T.get('border'):
    b = T['border']
    BF = 'border_osm.json'
    if not os.path.exists(BF):
        q = f'[out:json][timeout:60];way["boundary"="administrative"]["admin_level"="2"]({b["bbox"][0]},{b["bbox"][1]},{b["bbox"][2]},{b["bbox"][3]});out geom;'
        open(BF, 'wb').write(get('https://overpass-api.de/api/interpreter', data=urllib.parse.urlencode({'data': q}).encode(), timeout=120))
    BB = json.load(open(BF))
    border = [[[round(v, 1) for v in lonlat_to_px(p['lon'], p['lat'], Z)] for p in e['geometry']] for e in BB['elements'] if 'geometry' in e]
    bpts = [p for w in border for p in w]
    best = (1e18, 0)
    for k in range(int(b['km'][0] / STEP), min(int(b['km'][1] / STEP), len(pts))):
        x, y = pts[k]
        d = min((x - bx) ** 2 + (y - by) ** 2 for bx, by in bpts)
        if d < best[0]:
            best = (d, k * STEP)
    km_border = round(best[1], 1)
    print('fronteira km', km_border, 'dist px', round(best[0] ** .5, 1))

stops = []
for sid, name, kind, override in T['stops']:
    if override == 'ferry0': km, dist = marks['ferry0'], 0
    elif override == 'ferry1': km, dist = marks['ferry1'], 0
    elif override == 'start': km, dist = 0.0, 0
    elif override == 'end': km, dist = TOTAL, 0
    else: km, dist = km_of(tuple(STOPS[sid]))
    lo, la = at_km(km); x, y = lonlat_to_px(lo, la, Z)
    stops.append(dict(id=sid, name=name, kind=kind, km=round(km, 1), x=round(x, 1), y=round(y, 1), lon=round(lo, 4), lat=round(la, 4), snap_m=round(dist)))
    print(f'{sid:12s} {km:8.1f} snap {round(dist)} m')
for pid, name, lon, lat in T.get('passages', []):
    km, dist = km_of((lon, lat))
    lo, la = at_km(km); x, y = lonlat_to_px(lo, la, Z)
    stops.append(dict(id=pid, name=name, kind='pass', km=round(km, 1), x=round(x, 1), y=round(y, 1), lon=round(lo, 4), lat=round(la, 4), snap_m=round(dist)))
    print(f'{pid:12s} {km:8.1f} (passagem) afast {round(dist/1000,1)} km')
stops.sort(key=lambda s: s['km'])

out = dict(total_km=round(TOTAL, 1), step_km=STEP, z=Z, pts=pts, km_ferry=[round(marks['ferry0'], 2), round(marks['ferry1'], 2)],
           km_border=km_border, border=border, roads=comp, elev=dict(km=E['km'], ele=[round(v) for v in ele]), stops=stops,
           ferry=json.load(open('ferry.json'))['duration_tag'], osrm_hours=round(hours, 1),
           road_km=round(TOTAL - (marks['ferry1'] - marks['ferry0']), 1), countries=T.get('countries'))
json.dump(out, open('route_full.json', 'w'))
print('ok', len(pts), 'pts', 'elev', min(ele), max(ele), 'horas OSRM', round(hours, 1))
