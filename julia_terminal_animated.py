#by gloop#5445
#=== Config ==#
w,h = 32,32
max_iterations = 80
r_start,r_end = 0,2
i_start,i_end = 0,2
chars = ".,*3456789abcde."
#=============#
import math, os, time
os.system("")
print("\x1b[2J\x1b[0;0H\x1b[?25l\x1b];Julia Set\a")

def color_from_trig(h,offset=(math.pi/4)):
    n = h * math.pi
    r = int(255*abs(math.sin(n-offset)))
    g = int(255*abs(math.sin(n)))
    b = int(255*abs(math.sin(n+offset)))
    return f"\x1b[38;2;{r};{g};{b}m"

def clamp(minimum,n,maximum):
    return max(minimum,min(maximum,n))

def julia(z,c):
    n = 0
    while abs(z) <= 2 and n < max_iterations:
        z = z*z + c
        n += 1
    return n

def render(t):
    print("\x1b[0;0H\x1b[?25l")
    c = complex(
    0.7885*math.cos(t+(5.1*8)*math.pi/180),
    0.7887*math.sin(t+(5.1)*math.pi/180)
    )
    for y in range(-h,h):
        print()
        for x in range(-w,w):
            z = complex(
                r_start + (x / w) * (r_end - r_start),
                i_start + (y / h) * (i_end - i_start)
                )
            j = julia(z,c)/max_iterations
            character = chars[int(clamp(0,j*len(chars),len(chars)-1))]*2
            color = color_from_trig(j-0.9,math.pi/4)
            print(f"{color}{character}\x1b[0m",end="")
    print(f"\nC: ({c.real:.2f},{c.imag:.2f})")
t = 0
while True:
    t += 0.02
    render(t)
    time.sleep(0.02)