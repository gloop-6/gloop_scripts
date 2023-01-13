import math, os, time,tkinter
os.system("title mandelbrot")
e = "["
fgEsc = f"{e}38;5;"
bgEsc = f"{e}38;5;"
reset = f"{e}0m"
colorMode = 0
def colTrig(h,offset=(math.pi/4)):
    n = h * math.pi
    r = int(5*abs(math.sin(n-offset)))
    g = int(5*abs(math.sin(n)))
    b = int(5*abs(math.sin(n+offset)))
    return 16 + (36 * r) + (6 * g) + b
def colRamp(h,offsets=[3,5,8]):
    o1,o2,o3 = offsets
    r = int(5*(h/o1))
    g = int(5*(h/o2))
    b = int(5*(h/o3))
    return 16 + (36 * r) + (6 * g) + b
w,h = 100,50
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

rStart,rEnd = -0.7,0.7
iStart,iEnd = 0,1
os.system(f"mode con: cols={w*2} lines={(h*3)+3}")
print(f"{e}?25l")

for y in range(-h,h):
    print()
    for x in range(-w,w):
        c = complex(rStart + (x / w) * (rEnd - rStart),iStart + (y / h) * (iEnd - iStart))
        m = (mandelbrot(c)/maxIter)*3
        color = 0
        match colorMode:
            case 0:
                color = colRamp(1-m,[1,6,2])
            case 1:
                color = colTrig(m,math.pi*(1+math.sin(t/10)))
        print(f"{fgEsc}{color}m█{reset}",end="")

os.system("pause >nul")