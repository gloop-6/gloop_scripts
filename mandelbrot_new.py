from PIL import Image
import math
import functools
import multiprocessing
#by _gloop/gloop#5445
#=======
w,h = 1000,1000
chunk_size = 30
hue_offset = 0.1
r_start,r_end = -0.7,0.7
i_start,i_end = 0,1
max_iterations = 50
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
offset = -math.pi/4
def process_line(y):
    line = []
    for x in range(-w,w):
        c = complex(
            r_start + (x / w) * (r_end - r_start),
            i_start + (y / h) * (i_end - i_start)
            )
        m = mandelbrot(c)
        if m==max_iterations:
            color = (0,0,0)
        else:
            color = color_from_trig((m/max_iterations)+hue_offset,offset=offset)
        line+=[color]
    return line
def main():
    im  = Image.new( mode = "RGB", size = (w*2, h*2))
    lines = []
    with multiprocessing.Pool() as p:
        for y,result in enumerate(p.imap(process_line, range(-h,h),chunk_size)):
            lines += result
            amount_complete = (y)/(h*2)
            print(f"{amount_complete*100:.0f}% complete... {progress_bar(20,amount_complete)}",end="\r")
    im.putdata(lines)
    im.save('mandelbrot_set_render.png')    
if __name__ == "__main__":
    main()
    




