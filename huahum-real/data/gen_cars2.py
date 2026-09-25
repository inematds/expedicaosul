"""Sprites: VW Taos prata + Land Rover Defender 110 clássica (~2000, Td5 branca). flux2-klein local, fundo chroma."""
import json, base64, os, sys
from geo_util import get, HERE
OUT = os.path.join(HERE, 'cars_raw2'); os.makedirs(OUT, exist_ok=True)
BG = 'on a flat uniform solid magenta (#FF00FF) chroma key background, nothing else in frame'
TAOS = 'a silver Volkswagen Taos compact SUV (2023)'
DEF = 'a white classic Land Rover Defender 110 station wagon from around year 2000 (Td5, boxy flat body panels, flat bonnet, black steel wheels, safari roof rack, spare wheel on the rear door)'
JOBS = {
  'taos_top': (f"Orthographic top-down aerial photograph looking straight down at {TAOS}, the car points up toward the top of the image, whole car visible and centered, dark roof, roof rails, photorealistic, sharp, studio lighting, " + BG, 640, 1024),
  'defender_top': (f"Orthographic top-down aerial photograph looking straight down at {DEF}, the car points up toward the top of the image, whole car visible and centered, roof rack clearly visible, photorealistic, sharp, studio lighting, " + BG, 640, 1024),
  'taos_side': (f"Side profile photograph of {TAOS} facing right, full car visible, photorealistic automotive photo, soft studio light, " + BG, 1280, 768),
  'defender_side': (f"Side profile photograph of {DEF} facing right, full car visible, photorealistic automotive photo, soft studio light, " + BG, 1280, 768),
}
seeds = [int(s) for s in sys.argv[1:]] or [11, 22, 33]
for name, (prompt, w, h) in JOBS.items():
    for seed in seeds:
        fn = os.path.join(OUT, f'{name}_{seed}.png')
        if os.path.exists(fn): continue
        body = json.dumps(dict(model='flux2-klein', prompt=prompt, steps=4, width=w, height=h, guidance_scale=1.0, seed=seed)).encode()
        d = json.loads(get('http://localhost:8000/generate', data=body, headers={'Content-Type': 'application/json'}, timeout=600))
        open(fn, 'wb').write(base64.b64decode(d['image'])); print('ok', fn, flush=True)
