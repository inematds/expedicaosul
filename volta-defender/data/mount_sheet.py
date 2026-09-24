import os, glob
from PIL import Image
import numpy as np

# Dimensões das 3 imagens recortadas
cuts = sorted(glob.glob('/home/nmaldaner/projetos/expedicaosul/volta-defender/data/ferry_cut/*.png'))
images = [Image.open(f).convert('RGBA') for f in cuts]

# Redimensionar cada uma para altura 400, manter proporcao
target_h = 400
resized = []
widths = []
for img in images:
    w, h = img.size
    new_w = int(w * target_h / h)
    resized.append(img.resize((new_w, target_h), Image.LANCZOS))
    widths.append(new_w)

# Layout: lado a lado, 20px de margem entre
margin = 20
total_w = sum(widths) + (len(resized) - 1) * margin
total_h = target_h
bg_color = (30, 60, 90, 255)

# Criar canvas RGB do tamanho total
sheet = Image.new('RGB', (total_w, total_h), (30, 60, 90))

# Colar cada imagem redimensionada no canvas
x_pos = 0
for i, img in enumerate(resized):
    # Converter RGBA para RGB com fundo
    rgb_img = Image.new('RGB', img.size, (30, 60, 90))
    rgb_img.paste(img, (0, 0), img)
    sheet.paste(rgb_img, (x_pos, 0))
    x_pos += widths[i] + margin

# Criar pasta qa se não existir
qa_dir = '/home/nmaldaner/projetos/expedicaosul/volta-defender/data/qa'
os.makedirs(qa_dir, exist_ok=True)

# Salvar
out_path = os.path.join(qa_dir, 'ferry_sheet.jpg')
sheet.save(out_path, 'JPEG', quality=95)
print(f'Sheet saved: {out_path}')
print(f'Sheet dimensions: {sheet.size}')
for i, f in enumerate(cuts):
    print(f'{os.path.basename(f)}: {resized[i].size}')
