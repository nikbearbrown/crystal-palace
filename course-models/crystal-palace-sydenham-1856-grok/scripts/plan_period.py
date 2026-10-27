"""Estimate column-grid period (px) on plan 0205 by autocorrelation of dark-pixel profiles along strips."""
import numpy as np, sys
from PIL import Image
SRC='/workspace/crystal-palace/references/muse-drive/images/commons/Guide_to_the_Crystal_Palace_and_Park_1856_(147900384).jpg'
a=np.asarray(Image.open(SRC).convert('L'),dtype=float)
def period(prof,lo=40,hi=110):
    p=prof-prof.mean(); ac=np.correlate(p,p,'full')[len(p)-1:]; ac/=ac[0]
    k=lo+np.argmax(ac[lo:hi]); return k,ac[k]
for spec in sys.argv[1:]:
    axis,c0,c1,s0,s1=spec.split(':'); c0,c1,s0,s1=map(int,(c0,c1,s0,s1))
    if axis=='h': prof=(255-a[s0:s1,c0:c1]).sum(0)
    else: prof=(255-a[c0:c1,s0:s1]).sum(1)
    k,v=period(prof); print(spec,'period_px',k,'corr',round(v,3))
