"""Find long straight dark lines (walls/dotted boundaries) on plan 0205 via projection peaks."""
import numpy as np, sys
from PIL import Image
SRC='/workspace/crystal-palace/references/muse-drive/images/commons/Guide_to_the_Crystal_Palace_and_Park_1856_(147900384).jpg'
a=np.asarray(Image.open(SRC).convert('L'),dtype=float); d=(a<120).astype(float)
axis,c0,c1,s0,s1,thr=sys.argv[1:7]; c0,c1,s0,s1=map(int,(c0,c1,s0,s1)); thr=float(thr)
prof = d[s0:s1,c0:c1].sum(0) if axis=='v' else d[c0:c1,s0:s1].sum(1)
base = c0
pk=[(i+base,int(prof[i])) for i in range(1,len(prof)-1) if prof[i]>=thr and prof[i]>=prof[i-1] and prof[i]>=prof[i+1]]
print(pk)
