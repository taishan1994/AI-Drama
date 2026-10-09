#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FONT=ROOT/'fonts/MaShanZheng-Regular.ttf'
CREAM=(239,229,207,255)
RED=(170,36,34,220)
DARK=(0,0,0,220)

def glow_text(im, xy, text, size, *, fill=CREAM, anchor=None, stroke=1):
    font=ImageFont.truetype(str(FONT),size)
    # A soft black shadow, then a restrained vermilion offset gives the brush
    # title depth while preserving its hand-painted edges.
    shadow=Image.new('RGBA',im.size,(0,0,0,0)); sd=ImageDraw.Draw(shadow)
    sd.text((xy[0]+9,xy[1]+15),text,font=font,fill=DARK,anchor=anchor,stroke_width=stroke+2,stroke_fill=DARK)
    shadow=shadow.filter(ImageFilter.GaussianBlur(5))
    im.alpha_composite(shadow)
    d=ImageDraw.Draw(im)
    d.text((xy[0]+5,xy[1]+7),text,font=font,fill=RED,anchor=anchor,stroke_width=stroke+1,stroke_fill=(99,19,23,230))
    d.text(xy,text,font=font,fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=(25,23,20,240))

def brush_stroke(im, points, width=16):
    layer=Image.new('RGBA',im.size,(0,0,0,0))
    d=ImageDraw.Draw(layer)
    d.line(points,fill=(164,31,29,190),width=width,joint='curve')
    # tapered, irregular ends make the underline feel painted, not geometric.
    x0,y0=points[0]; x1,y1=points[-1]
    d.polygon([(x0-10,y0-2),(x0+15,y0-10),(x0+25,y0+7),(x0-4,y0+6)],fill=(164,31,29,185))
    d.polygon([(x1-20,y1-4),(x1+11,y1-7),(x1+2,y1+4),(x1-28,y1+8)],fill=(164,31,29,165))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.7)))

# Landscape: layered brush lettering over the shadowed left third.
im=Image.open(ROOT/'source/横屏_无字背景.png').convert('RGB').resize((2560,1440),Image.Resampling.LANCZOS).convert('RGBA')
w,h=im.size
grad=Image.new('RGBA',(w,h),(0,0,0,0)); px=grad.load()
for x in range(w):
    a=int(125*max(0,1-x/(w*.55))**1.7)
    for y in range(h): px[x,y]=(3,6,9,a)
im.alpha_composite(grad)
brush_stroke(im,[(105,822),(198,808),(290,818),(394,801)],14)
glow_text(im,(100,840),'行尸危机：',128)
glow_text(im,(85,1000),'黑石镇',236,stroke=2)
im.convert('RGB').save(ROOT/'行尸危机_黑石镇_横屏封面_2560x1440.png',optimize=True)

# Portrait: compact, right-aligned calligraphy in the dark sky.
im=Image.open(ROOT/'source/竖屏_无字背景.png').convert('RGB').resize((1440,2160),Image.Resampling.LANCZOS).convert('RGBA')
w,h=im.size
grad=Image.new('RGBA',(w,h),(0,0,0,0)); px=grad.load()
for y in range(500):
    a=int(100*max(0,1-y/500)**.8)
    for x in range(w): px[x,y]=(2,4,8,a)
im.alpha_composite(grad)
brush_stroke(im,[(950,362),(1065,350),(1190,357),(1342,340)],12)
glow_text(im,(1345,64),'行尸危机：',78,anchor='ra')
glow_text(im,(1345,158),'黑石镇',142,anchor='ra',stroke=2)
im.convert('RGB').save(ROOT/'行尸危机_黑石镇_竖屏封面_1440x2160.png',optimize=True)
print('Updated calligraphic title typography.')
