"""Gera assets/route.js: rota reamostrada por km (em px globais z14), altimetria SRTM, fronteira, waypoints.
Tudo que aparece na tela sai daqui (fonte: OSRM/OSM, OpenTopoData SRTM30m, OSM admin_level=2)."""
import json, os, bisect, time, urllib.parse
from geo_util import get, load_route, lonlat_to_px, nearest_on_route, HERE

ROOT = os.path.dirname(HERE)
coords, cum, osrm = load_route()
TOTAL = cum[-1] / 1000
Z = 14


def at_km(km):
    m = km * 1000
    i = max(1, min(len(cum) - 1, bisect.bisect_left(cum, m)))
    a, b = coords[i - 1], coords[i]
    t = (m - cum[i - 1]) / max(1e-9, cum[i] - cum[i - 1])
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# rota reamostrada a cada 25 m
STEP = 0.025
N = int(TOTAL / STEP) + 1
pts = []
for k in range(N + 1):
    km = min(TOTAL, k * STEP)
    lo, la = at_km(km)
    x, y = lonlat_to_px(lo, la, Z)
    pts.append([round(x, 2), round(y, 2)])

# altimetria SRTM30m a cada 250 m
EF = os.path.join(HERE, 'elev.json')
if not os.path.exists(EF):
    samples = [min(TOTAL, i * 0.25) for i in range(int(TOTAL / 0.25) + 2)]
    ll = [at_km(k) for k in samples]
    elev = []
    for i in range(0, len(ll), 100):
        chunk = '|'.join(f'{la:.6f},{lo:.6f}' for lo, la in ll[i:i + 100])
        d = json.loads(get('https://api.opentopodata.org/v1/srtm30m?locations=' + chunk, timeout=60))
        elev += [r['elevation'] for r in d['results']]
        time.sleep(1.2)
    json.dump({'km': samples, 'ele': elev}, open(EF, 'w'))
E = json.load(open(EF))
print('elev min/max', min(E['ele']), max(E['ele']))

# fronteira AR/CL (OSM admin_level=2) na janela do mapa
BF = os.path.join(HERE, 'border_osm.json')
if not os.path.exists(BF):
    q = """[out:json][timeout:120];
way["boundary"="administrative"]["admin_level"="2"](-40.40,-72.05,-39.80,-71.05);
out geom;"""
    open(BF, 'wb').write(get('https://overpass-api.de/api/interpreter', data=urllib.parse.urlencode({'data': q}).encode(), timeout=180))
B = json.load(open(BF))
border = []
for e in B['elements']:
    g = [lonlat_to_px(p['lon'], p['lat'], Z) for p in e.get('geometry', [])]
    border.append([[round(x, 1), round(y, 1)] for x, y in g])
print('border ways', len(border))

# km da troca de país = onde a rota cruza a fronteira (mudança RP48 -> CH 203 confirma)
steps = osrm['routes'][0]['legs'][0]['steps']
ch203 = next(s for s in steps if '203' in (s.get('ref') or '') + (s.get('name') or ''))
km_ch203, _ = nearest_on_route(tuple(ch203['maneuver']['location']), coords, cum)
# cruzamento geométrico: ponto da rota mais próximo da linha de fronteira
best = (1e18, 0)
bpts = [p for w in border for p in w]
for k in range(int(38 / STEP), int(48 / STEP)):
    x, y = pts[k]
    d = min((x - bx) ** 2 + (y - by) ** 2 for bx, by in bpts)
    if d < best[0]:
        best = (d, k * STEP)
km_border = round(best[1], 2)
print('km troca RP48->CH203', round(km_ch203, 2), '| km cruzamento fronteira', km_border, 'dist px', best[0] ** .5)

WAYPOINTS = [
    # id, nome, km (snap do OSM), lon/lat do OSM
    ('sma', 'San Martín de los Andes', 0.0),
    ('lacar', 'Lago Lácar', 3.57),          # Mirador "El Balcón" (OSM node 2946552909, 18 m da rota)
    ('ripio', 'Alto da RP48', 16.5),       # ponto mais alto do trajeto (SRTM30m, elev.json)
    ('yuco', 'Playa de Yuco', 27.11),       # OSM node 8395568189
    ('nonthue', 'Lago Nonthué', 38.32),     # OSM relation 6430979
    ('huahum', 'Puerto Hua Hum', 41.25),    # OSM node 198413718
    ('border', 'Paso Hua Hum', km_border),  # cruzamento geométrico da linha de fronteira
    ('pirehueico', 'Puerto Pirehueico', round(TOTAL, 2)),
]
wps = []
for wid, name, km in WAYPOINTS:
    lo, la = at_km(km)
    x, y = lonlat_to_px(lo, la, Z)
    ei = min(range(len(E['km'])), key=lambda i: abs(E['km'][i] - km))
    wps.append(dict(id=wid, name=name, km=round(km, 2), x=round(x, 1), y=round(y, 1), ele=round(E['ele'][ei]), lon=round(lo, 5), lat=round(la, 5)))
    print(wid, km, 'ele', round(E['ele'][ei]))

L = json.load(open(os.path.join(HERE, 'layers.json')))
# rótulos: centroides dos polígonos OSM (water_osm.json); países de cada lado da linha OSM admin_level=2
LABELS = [('Lago Lácar', -71.50, -40.167, 'lake'), ('Lago Nonthué', -71.642, -40.137, 'lake'),
          ('Lago Lolog', -71.45, -40.045, 'lake'), ('Lago Queñi', -71.712, -40.160, 'lake'),
          ('Lago Pirihueico', -71.775, -39.975, 'lake'),
          ('ARGENTINA', -71.60, -40.085, 'country'), ('CHILE', -71.80, -40.090, 'country')]
out = dict(total_km=round(TOTAL, 2), step_km=STEP, z=Z, pts=pts, elev=dict(km=E['km'], ele=[round(v) for v in E['ele']]),
           border=border, km_border=km_border, waypoints=wps, layers=L,
           osrm_duration_min=round(osrm['routes'][0]['duration'] / 60),
           labels=[dict(t=t, x=round(lonlat_to_px(lo, la, Z)[0], 1), y=round(lonlat_to_px(lo, la, Z)[1], 1), k=k) for t, lo, la, k in LABELS])
open(os.path.join(ROOT, 'assets', 'route.js'), 'w').write('window.ROUTE = ' + json.dumps(out, separators=(',', ':')) + ';\n')
print('route.js ok, pts', len(pts))
