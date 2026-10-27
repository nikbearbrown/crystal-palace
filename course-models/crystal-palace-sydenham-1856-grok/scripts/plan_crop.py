"""Crop a region of the 1856 ground plan (Muse 0205) with full-res pixel ticks, for registration."""
import sys
from PIL import Image, ImageDraw
SRC='/workspace/crystal-palace/references/muse-drive/images/commons/Guide_to_the_Crystal_Palace_and_Park_1856_(147900384).jpg'
x0,y0,x1,y1=map(int,sys.argv[1:5]); out=sys.argv[5]; step=int(sys.argv[6]) if len(sys.argv)>6 else 50
im=Image.open(SRC).convert('RGB').crop((x0,y0,x1,y1))
s=min(1400/(x1-x0),1400/(y1-y0)); im=im.resize((int((x1-x0)*s),int((y1-y0)*s)))
d=ImageDraw.Draw(im)
for x in range((x0//step+1)*step,x1,step):
    X=(x-x0)*s; d.line([(X,0),(X,8)],fill=(255,0,0)); d.text((X+1,8),str(x),fill=(255,0,0))
for y in range((y0//step+1)*step,y1,step):
    Y=(y-y0)*s; d.line([(0,Y),(8,Y)],fill=(0,0,255)); d.text((10,Y-5),str(y),fill=(0,0,255))
im.save(out)
