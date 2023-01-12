import math, os, time
os.system("title mandelbrot spin")

e = "["
fgEsc = f"{e}38;5;"
bgEsc = f"{e}38;5;"
reset = f"{e}0m"
def colTrig(h,offset=(math.pi/4)):
    n = h * math.pi
    r = int(5*abs(math.sin(n-offset)))
    g = int(5*abs(math.sin(n)))
    b = int(5*abs(math.sin(n+offset)))
    return 16 + (36 * r) + (6 * g) + b
w,h = 20,20
t=0
maxIter = 80
rotationSpeed = 0.1
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < maxIter:
        z = z*z + c
        n += 1
    return n
s = ""

def rotateCoords(pos,origin,t):
    oX,oY = origin
    x,y = pos
    c,s = math.cos(t),math.sin(t)
    x+=oX
    y+=oY
    x2 = (x*c) - (y * s)
    y2 = (x*s) + (y * c)
    return x2,y2

rStart,rEnd = -0.7,0.7
iStart,iEnd = 0,1
os.system(f"mode con: cols={w*2} lines={(h*2)+3}")
print(f"{e}?25l")

while True:
    print(f"{e}2H")
    for y in range(-h,h):
        s=""
        for x in range(-w,w):
            x2,y2 = rotateCoords((x,y),(0,0),t*rotationSpeed)
            c = complex(rStart + (x2 / w) * (rEnd - rStart),iStart + (y2 / h) * (iEnd - iStart))
            m = (mandelbrot(c)/maxIter)
            s+=f"{fgEsc}{colTrig(m,math.pi*(1+math.sin(t/10)))}m█{reset}"
        print(s)
    print(f"{e}2H")
    t+=0.1