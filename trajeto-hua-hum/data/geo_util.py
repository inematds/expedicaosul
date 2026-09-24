"""Utilidades geográficas compartilhadas: rota OSRM parametrizada por km e projeção Web Mercator."""
import json, math, os, urllib.request, urllib.parse, time

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'expedicaosul-trajeto/1.0 (pesquisa/educacao; nei.maldaner)'}


def get(url, timeout=60, data=None, headers=None):
    h = dict(UA)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    return urllib.request.urlopen(req, timeout=timeout).read()


def haversine(a, b):
    """a, b = (lon, lat) -> metros"""
    R = 6371008.8
    lo1, la1, lo2, la2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    d = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(d))


def load_route():
    d = json.load(open(os.path.join(HERE, 'osrm.json')))
    coords = d['routes'][0]['geometry']['coordinates']
    cum = [0.0]
    for i in range(1, len(coords)):
        cum.append(cum[-1] + haversine(coords[i - 1], coords[i]))
    return coords, cum, d


def nearest_on_route(pt, coords, cum):
    """retorna (km ao longo da rota, distância perpendicular aproximada em m)"""
    best = (1e18, 0)
    for i in range(len(coords) - 1):
        a, b = coords[i], coords[i + 1]
        # projeção local equiretangular
        kx = math.cos(math.radians(pt[1])) * 111320
        ky = 110540
        ax, ay = (a[0] - pt[0]) * kx, (a[1] - pt[1]) * ky
        bx, by = (b[0] - pt[0]) * kx, (b[1] - pt[1]) * ky
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy or 1e-9
        t = max(0, min(1, -(ax * dx + ay * dy) / L2))
        px, py = ax + t * dx, ay + t * dy
        dist = math.hypot(px, py)
        if dist < best[0]:
            best = (dist, (cum[i] + t * (cum[i + 1] - cum[i])) / 1000)
    return best[1], best[0]


# Web Mercator: pixel global no zoom z (tile 256)
def lonlat_to_px(lon, lat, z):
    n = 256 * 2 ** z
    x = (lon + 180) / 360 * n
    s = math.sin(math.radians(lat))
    y = (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n
    return x, y
