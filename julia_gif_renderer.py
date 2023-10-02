from PIL import Image
import math
import functools
#by _gloop/gloop#5445
#=======
w,h = 200,200
offset = (0,0)
zoom = (0.8,0.8)
hue_offset = 0.1
frame_count = 50
max_iterations = 50
chunk_size = 6
speed = 3
trig_offset = -math.pi/4
#=======

c = complex(
    0.7885*math.cos((5.1*8)*math.pi/180),
    0.7887*math.sin((5.1)*math.pi/180)
)
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

@functools.cache
def generate_c_value(t):
    return complex(
            0.7885*math.cos(t+(5.1*8)*math.pi/180),
            0.7887*math.sin(t+(5.1)*math.pi/180)
        )

def main():
    frames = []
    for i in range(frame_count):
        t = i/frame_count
        c = generate_c_value(t*speed)
        im  = Image.new( mode = "RGB", size = (w*2, h*2))
        data = []
        for y in range(-h,h):
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
        frames.append(im)
        print(f"{t*100:.0f}% complete... {progress_bar(20,t)}",end="  \r")
    frames[0].save('julia_set_render.gif',
               save_all = True, append_images = frames[1:], 
               optimize = True, duration = 1, loop=0)
if __name__ == "__main__":
    main()
