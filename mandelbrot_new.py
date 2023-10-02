from PIL import Image
import math
import functools
#by _gloop/gloop#5445
#=======
w,h = 1024,1024
offset = -0.4,0
zoom = 0.8,0.8
max_iterations = 50

hue_offset = 0.1
trig_offset = -math.pi/4
infill_color = (0,0,0)
#=======
w,h = w//2,h//2

@functools.cache
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iterations:
        z = z*z + c
        n += 1
    return n

@functools.cache
def color_from_trig(h,offset=(math.pi*(2/3))):
    n = h * math.pi
    r = int(255*abs(math.sin(n-offset)))
    g = int(255*abs(math.sin(n)))
    b = int(255*abs(math.sin(n+offset)))
    return r,g,b

def progress_bar(length,n):
    amount_complete = int(n*length)
    bar = "#"*amount_complete+("."*(length-(amount_complete)))
    return bar + " "*length

def main():
    im  = Image.new( mode = "RGB", size = (w*2, h*2))
    data = []
    for y in range(-h,h):
        if y%10==0:
            t = (y/(h*2))+0.5
            print(f"{t*100:.0f}%",progress_bar(20,t),end="    \r")
        for x in range(-w,w):
            z = complex(
                offset[0] + (x / w)/ zoom[0],
                offset[1] + (y / h)/ zoom[1]
                )
            m = mandelbrot(z)
            if m==max_iterations:
                color = infill_color
            else:
                color = color_from_trig((m/max_iterations)+hue_offset,offset=trig_offset)
            data.append(color)
    im.putdata(data)
    im.save('mandelbrot_set_render.png')    

if __name__ == "__main__":
    main()
