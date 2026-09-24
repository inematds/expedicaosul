import json, base64, os, urllib.request
OUT='/home/nmaldaner/projetos/expedicaosul/volta-defender/data/ferry_raw'; os.makedirs(OUT,exist_ok=True)
prompt=("Orthographic top-down aerial photograph looking straight down at a modern white high-speed passenger catamaran ferry, "
        "the bow points up toward the top of the image, whole vessel visible and centered, dark blue windows, orange and white livery accents, "
        "empty open car deck at the stern, photorealistic, sharp, on a flat uniform solid magenta (#FF00FF) chroma key background, no water, nothing else in frame")
for seed in (7,17,27):
    body=json.dumps(dict(model='flux2-klein',prompt=prompt,steps=4,width=512,height=1024,guidance_scale=1.0,seed=seed)).encode()
    req=urllib.request.Request('http://localhost:8000/generate',data=body,headers={'Content-Type':'application/json'})
    d=json.loads(urllib.request.urlopen(req,timeout=600).read())
    open(f'{OUT}/ferry_{seed}.png','wb').write(base64.b64decode(d['image'])); print('ok',seed)
