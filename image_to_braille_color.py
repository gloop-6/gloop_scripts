from PIL import Image
import copy
import os,sys
os.system("title ImgToBraille")
input_file = sys.argv[1]
pix_res = [2,4]
pix_area= pix_res[0]*pix_res[1]
ansi_escape = "\x1b["
reset_escape = f"{ansi_escape}0m"
fg_escape = f"{ansi_escape}38;5;"
d = dict(zip(range(0,8),[7,8,3,6,2,5,1,4]))
d2 = dict(zip(range(8),[1,0,3,2,5,4,7,6]))
dots_map = dict(zip(range(8),[64,128,4,32,2,16,1,8]))
index_map = dict(zip(range(8),[6,7,4,5,2,3,0,1]))
def col_from_rgb(c):
    r,g,b = c
    r = int(5*(r/255))
    g = int(5*(g/255))
    b = int(5*(b/255))
    return f"{fg_escape}{16 + (36 * r) + (6 * g) + b}m"
def braille_from_bits(bits):
    if len(bits)<8:
        bits = [0]*(8-len(bits)) + bits
    ch = 0x2800
    bits_copy = [bits[index_map[idx]] for idx,_ in enumerate(bits)] 
    ch += sum([bit*dots_map[idx] for idx,bit in enumerate(bits_copy)])
    return chr(ch)

def clamp(minimum,n,maximum):
    return max(minimum,min(maximum,n))
with Image.open(input_file) as im:
    w,h = im.size
    px=im.load()
s = ""
exposure = 1
nW = 8
img_data = {}
for y in range(h):
    for x in range(w):
        img_data[(x,y)]=sum(px[x,y][:3])/255

img_data_copy = copy.deepcopy(img_data)
for y in range(h):
    for x in range(w):
        error=img_data_copy[(x,y)]-int(img_data_copy[(x,y)])*2
        if x < w-1:
            img_data_copy[(x+1,y)]+= error * (7/16)
        if y < h-1:
            if x>0:
                img_data_copy[(x-1,y+1)]+= error * (3/16)
            img_data_copy[(x,y+1)]+= error * (5/16)
            if x<w-1:
                img_data_copy[(x+1,y+1)]+=error/16
        img_data[(x,y)] = img_data_copy[(x,y)]

img_color = {}      
for y in range(0,h,pix_res[1]):
    print(s)
    s=""
    for x in range(0,w,pix_res[0]):
        curCh = []
        for y2 in range(0,pix_res[1]):
            yOff = y+y2
            for x2 in range(pix_res[0]-1,-1,-1):
                
                xOff = x-x2
                
                if clamp(0,xOff,w-1)==xOff and clamp(0,yOff,h-1)==yOff:
                    curCh+=[clamp(0,int(img_data[(xOff,yOff)]),1)]
        s+=f"{col_from_rgb(px[x,y][:3])}{braille_from_bits(curCh)}{reset_escape}"
os.system("pause >nul")