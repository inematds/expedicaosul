"""Gera sprites dos carros (vista de cima + perfil) no flux2-klein local, fundo chroma."""
import json, base64, os, sys
from geo_util import get, HERE

ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'cars_raw')
os.makedirs(OUT, exist_ok=True)

BG = 'on a flat uniform solid magenta (#FF00FF) chroma key background, nothing else in frame'
JOBS = {
    'defender_top': ("Orthographic top-down aerial photograph looking straight down at a white Land Rover Defender 110 (new generation, 2023), "
                     "the car points up toward the top of the image, whole car visible and centered, black roof rails, roof and bonnet clearly visible, "
                     "photorealistic, sharp, studio lighting, " + BG, 640, 1024),
    'tucson_top': ("Orthographic top-down aerial photograph looking straight down at a silver-grey Hyundai Tucson SUV (2023), "
                   "the car points up toward the top of the image, whole car visible and centered, panoramic glass roof, roof rails, "
                   "photorealistic, sharp, studio lighting, " + BG, 640, 1024),
    'defender_side': ("Side profile photograph of a white Land Rover Defender 110 (new generation, 2023) facing right, full car visible, "
                      "roof rack, all-terrain tyres, photorealistic automotive photo, soft studio light, " + BG, 1280, 768),
    'tucson_side': ("Side profile photograph of a silver-grey Hyundai Tucson SUV (2023) facing right, full car visible, "
                    "photorealistic automotive photo, soft studio light, " + BG, 1280, 768),
}
seeds = [int(s) for s in sys.argv[1:]] or [11, 22, 33]
for name, (prompt, w, h) in JOBS.items():
    for seed in seeds:
        fn = os.path.join(OUT, f'{name}_{seed}.png')
        if os.path.exists(fn):
            continue
        body = json.dumps(dict(model='flux2-klein', prompt=prompt, steps=4, width=w, height=h, guidance_scale=1.0, seed=seed)).encode()
        d = json.loads(get('http://localhost:8000/generate', data=body, headers={'Content-Type': 'application/json'}, timeout=600))
        open(fn, 'wb').write(base64.b64decode(d['image']))
        print('ok', fn, flush=True)
