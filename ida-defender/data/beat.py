"""Estimativa de BPM e fase por fluxo espectral + pente de autocorrelação."""
import numpy as np, subprocess, sys
f=sys.argv[1]; t0=float(sys.argv[2]) if len(sys.argv)>2 else 12; t1=float(sys.argv[3]) if len(sys.argv)>3 else 55
raw=subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar','22050','-f','s16le','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.int16).astype(np.float32)/32768; sr=22050; hop=256
fr=np.lib.stride_tricks.sliding_window_view(a,2048)[::hop]
S=np.abs(np.fft.rfft(fr*np.hanning(2048),axis=1))
fl=np.maximum(0,np.diff(np.log1p(S*10),axis=0)).sum(1); fps=sr/hop
t=np.arange(len(fl))/fps
m=(t>t0)&(t<t1); e=fl[m]-np.convolve(fl[m],np.ones(32)/32,'same')
best=[]
for bpm in np.arange(70,150,0.05):
    L=60/bpm*fps
    sc=sum(np.dot(e[:-int(round(k*L))],e[int(round(k*L)):]) for k in (1,2,4,8))
    best.append((sc,bpm))
best.sort(); top=best[-5:]
print('top', [(round(b,2)) for s,b in top])
bpm=top[-1][1]; B=60/bpm
ph=np.zeros(64); idx=((t[m]%B)/B*64).astype(int)%64; np.add.at(ph,idx,fl[m])
print('bpm',round(bpm,2),'beat',round(B,4),'beat phase',round(np.argmax(ph)/64*B,3))
# fase do compasso (4 batidas)
P=4*B; ph4=np.zeros(64); np.add.at(ph4,((t[m]%P)/P*64).astype(int)%64,fl[m]); print('bar',round(P,4),'bar phase',round(np.argmax(ph4)/64*P,3))
