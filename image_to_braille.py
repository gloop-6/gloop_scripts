
from PIL import Image
import copy
import os,sys
os.system("title ImgToBraille")
inputFile = sys.argv[1]
pixRes = [2,4]
pixArea= pixRes[0]*pixRes[1]
d = dict(zip(range(0,8),[7,8,3,6,2,5,1,4]))
d2 = dict(zip(range(8),[1,0,3,2,5,4,7,6]))
dotsMap = dict(zip(range(8),[64,128,4,32,2,16,1,8]))
indexMap = dict(zip(range(8),[6,7,4,5,2,3,0,1]))
def brailleFromBits(bits):
    if len(bits)<8:
        bits = [0]*(8-len(bits)) + bits
    ch = 0x2800
    bitsCopy = [bits[indexMap[idx]] for idx,_ in enumerate(bits)] 
    ch += sum([bit*dotsMap[idx] for idx,bit in enumerate(bitsCopy)])
    return chr(ch)

def clamp(minimum,n,maximum):
    return max(minimum,min(maximum,n))
with Image.open(inputFile) as im:
    w,h = im.size
    px=im.load()
s = ""
exposure =1
nW = 8
imgData = {}
for y in range(h):
    for x in range(w):
        imgData[(x,y)]=sum(px[x,y][:3])/255
        
imgDataCopy = copy.deepcopy(imgData)
for y in range(h):
    for x in range(w):
        error=imgDataCopy[(x,y)]-int(imgDataCopy[(x,y)])*2
        if x < w-1:
            imgDataCopy[(x+1,y)]+= error * (7/16)
        if y < h-1:
            if x>0:
                imgDataCopy[(x-1,y+1)]+= error * (3/16)
            imgDataCopy[(x,y+1)]+= error * (5/16)
            if x<w-1:
                imgDataCopy[(x+1,y+1)]+=error/16
        imgData[(x,y)] = imgDataCopy[(x,y)]
            
for y in range(0,h,pixRes[1]):
    s+="\n"
    for x in range(0,w,pixRes[0]):
        curCh = []
        for y2 in range(0,pixRes[1]):
            yOff = y+y2
            for x2 in range(pixRes[0]-1,-1,-1):
                xOff = x-x2
                if clamp(0,xOff,w-1)==xOff and clamp(0,yOff,h-1)==yOff:
                    curCh+=[clamp(0,int(imgData[(xOff,yOff)]),1)]
        s+=brailleFromBits(curCh)
print(s)
os.system("pause >nul")