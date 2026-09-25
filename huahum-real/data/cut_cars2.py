"""Recorta o fundo magenta dos sprites escolhidos -> assets/cars/*.png (RGBA, crop no bbox)."""
import numpy as np, os
from PIL import Image
PICK = {'taos_top': 'taos_top_22', 'defender_top': 'defender_top_22', 'taos_side': 'taos_side_33', 'defender_side': 'defender_side_11'}
for out, src in PICK.items():
    a = np.asarray(Image.open(f'cars_raw2/{src}.png').convert('RGB')).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # "magentice": R e B altos acima de G
    m = np.minimum(r, b) - g
    alpha = 1 - np.clip((m - 40) / 60, 0, 1)
    # despill: limita R e B ao máximo de G + margem nos pixels de borda
    spill = np.clip((np.minimum(r, b) - g) / 255, 0, 1)[..., None]
    cap = np.maximum(g, (r + b) / 2 * 0)[..., None]
    rgb = a.copy()
    lim = g[..., None] + 18
    rgb[..., [0, 2]] = np.where(alpha[..., None] < 1, np.minimum(rgb[..., [0, 2]], lim), rgb[..., [0, 2]])
    im = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), 'RGBA')
    im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
    im.save(f'../assets/cars/{out}.png'); print(out, im.size)
