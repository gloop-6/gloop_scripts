import math,time,os
w,h = 70,40
e = "["

i=0
maxIter = 100
x,y,x1,y1,x2,y2,c=0,0,0,0,0,0,0
zoom = 1
offsetX,offsetY=-0.2,-0.5

os.system("color")
def clamp(a,n,b):
    return min(b,max(a,(n)))
def main(t):
    s = ""
    for pixY in range(h):
        if pixY != 0:
            s = f"{s}\n"
        for pixX in range(w):
            x1 = offsetX+(2.47*(pixX/w)-1.53)/zoom
            y1 = offsetY+(2*(pixY/h)-0.5)/zoom
            i=0
            x,y=0,0
            while x*x + y*y <= 4 and i < maxIter:
                xtemp = x*x - y*y + x1
                y=(x+x)*y + y1
                x = xtemp
                i += 1

            r = clamp(0,int(5*math.sin((t+(i/maxIter)*11)-math.pi/4)),5)
            g = clamp(0,int(5*math.sin((t+(i/maxIter)*11))),5)
            b = clamp(0,int(5*math.sin((t+(i/maxIter)*11)+math.pi/4)),5)
            col = 16 + (36 * r) + (6 * g) + b
            s = s + f"\x1B[38;5;{col}m {e}0m"
    print("\033[2H")
    print(s)
t=0
while True:
    main(t)
    t+=0.1


os.system("pause")
