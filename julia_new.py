from PIL import Image
import math
import functools
#by _gloop/gloop#5445
#=======
w,h = 500,500
zoom = (0.8,0.8)
offset = (0,0)

default_c_value = complex(0.5,0.3)
use_generated_c_value = True
c_value_offset = 0.31

hue_offset = 0.1
trig_offset = -math.pi/4
max_iterations = 50
#=======
def generate_c_value(t):
    return complex(
            0.7885*math.cos(t+(5.1*8)*math.pi/180),
            0.7887*math.sin(t+(5.1)*math.pi/180)
        )
if use_generated_c_value:
    c = generate_c_value(c_value_offset)
else:
    c = default_c_value
w,h = w//2,h//2
@functools.cache
def julia(z,c):
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
            amt_complete = (y/(h*2))+0.5
            print(f"{amt_complete*100:.0f}%",progress_bar(20,amt_complete),end="    \r")
        for x in range(-w,w):
            z = complex(
                offset[0] + (x / w)/ zoom[0],
                offset[1] + (y / h)/ zoom[1]
                )
            m = julia(z,c)
            if m==max_iterations:
                color = (0,0,0)
            else:
                color = color_from_trig((m/max_iterations)+hue_offset,offset=trig_offset)
            data.append(color)
    im.putdata(data)
    im.save('julia_set_render.png')    
if __name__ == "__main__":
    main()
