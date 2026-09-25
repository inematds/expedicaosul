"""Lê só o cabeçalho de cada foto dentro do zip (EXIF: hora, GPS, miniatura) — evita baixar 1 GB pelo drive remoto."""
import zipfile, io, json, sys
from PIL import Image
ZIP = sys.argv[1]
z = zipfile.ZipFile(ZIP)
out = []
for zi in z.infolist():
    if not zi.filename.lower().endswith('.jpg'):
        continue
    with z.open(zi) as f:
        head = f.read(160 * 1024)
    rec = {'name': zi.filename.split('/')[-1], 'size': zi.file_size, 'method': zi.compress_type}
    try:
        im = Image.open(io.BytesIO(head))
        ex = im.getexif()
        rec['w'], rec['h'] = im.size
        rec['orient'] = ex.get(274)
        rec['dt'] = ex.get(306)
        gps = ex.get_ifd(0x8825)
        if gps and 2 in gps:
            f2 = lambda v: float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600
            lat = f2(gps[2]) * (-1 if gps.get(1) == 'S' else 1)
            lon = f2(gps[4]) * (-1 if gps.get(3) == 'W' else 1)
            rec['lat'], rec['lon'] = lat, lon
        th = ex.get_ifd(0x0001)  # IFD1 = miniatura
        off, ln = th.get(513), th.get(514)
        if off and ln:
            # offset relativo ao início do TIFF (APP1 + 'Exif\0\0')
            i = head.find(b'Exif\x00\x00') + 6
            open(f'fotos_raw/thumbs/{rec["name"]}', 'wb').write(head[i + off:i + off + ln])
            rec['thumb'] = True
    except Exception as e:
        rec['err'] = str(e)[:80]
    out.append(rec)
    print(rec['name'], rec.get('dt'), rec.get('lat'), rec.get('lon'), rec.get('thumb'), rec.get('err', ''), flush=True)
json.dump(out, open('fotos_raw/scan.json', 'w'), indent=1)
