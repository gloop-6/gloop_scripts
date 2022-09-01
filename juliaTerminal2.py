import os,time
import math
w,h = 60,41
e = "["

s = ""
i=0
maxSteps = 100
x,y,x1,y1,x2,y2,c=0,0,0,0,0,0,0
scale = 0.6
offsetX,offsetY=0,0
def clamp(a,n,b):
    return min(b,max(a,(n)))
os.system("color")
print("\x1b[?25l")
cxList = []
cyList = []
for i in range(10000):
    t = i/50
    
    cxList.append(0.7885*math.cos((t)+(5.1*8)*math.pi/180))
    cyList.append(0.7887*math.sin((t)+(5.1)*math.pi/180))
os.system("mode con:cols="+str(w+1)+"lines="+str(h+5))
t=0
while True:
    t+=1
    s = ""
    i+=0.1

    r2 = (1+(1+4*(cxList[t%len(cxList)]**2+cyList[t%len(cyList)]**2)**0.5)**0.5)/2+0.001
    for y in range(h):
        if y != 0:
            s=f"{s}\n"
        for x in range(w):
            n = 0
            ax = 1.0*(x-w/2)/(0.5*scale*w) + offsetX
            ay = 1.0*(y-h/2)/(0.5*scale*h) + offsetY
            while (ax**2)+(ay**2) < r2**2 and n < maxSteps:
                g2 = (ax**2)-(ay**2)
                ax = 2*ax*ay + cyList[t%len(cyList)]
                ay = g2 + cxList[t%len(cxList)]
                n = n+1
            r = clamp(0,int(5*math.sin((i+(n/maxSteps)*13)-math.pi/4)),5)
            g = clamp(0,int(5*math.sin((i+(n/maxSteps)*13))),5)
            b = clamp(0,int(5*math.sin((i+(n/maxSteps)*13)+math.pi/4)),5)
            col = 16 + (36 * r) + (6 * g) + b
            s = s + f"\x1B[38;5;{col}m█{e}0m"
    print("\033[?25l")
    print("\033[2H")
    print(s)  

