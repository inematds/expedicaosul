import numpy as np, cv2, glob, os
from PIL import Image
from scipy import ndimage
os.makedirs('/home/nmaldaner/projetos/expedicaosul/volta-defender/data/ferry_cut',exist_ok=True)
for f in sorted(glob.glob('/home/nmaldaner/projetos/expedicaosul/volta-defender/data/ferry_raw/*.png')):
    im=np.array(Image.open(f).convert('RGB')).astype(np.float32); r,g,b=im[...,0],im[...,1],im[...,2]
    m=np.clip(((np.minimum(r,b)-g)-60)/80,0,1); alpha=cv2.GaussianBlur(1-m,(0,0),0.7)
    s=np.clip(np.minimum(r,b)-g,0,None); im[...,0]-=s; im[...,2]-=s
    rgba=np.dstack([np.clip(im,0,255),alpha*255]).astype(np.uint8)
    ys,xs=np.where(alpha>0.1); rgba=rgba[ys.min():ys.max()+1, xs.min():xs.max()+1]
    Image.fromarray(rgba).save(f.replace('ferry_raw','ferry_cut')); print(os.path.basename(f), rgba.shape)
