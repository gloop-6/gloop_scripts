#=by gloop#5445
#=#
flag_width,flag_height = 50,30
flag_type = "pride"
flag_offset = 20
flag_amplitude = 20
flag_scale = 15
flag_wave_speed = 0.1
flag_frequency = 1/6
flag_x_range = (1,-3)
frame_sleep_time = 0.02
#=#
flag_colors = {
    "pride":("ef4252","f7a531","ffd900", "52ad31", "00adde","844294"),
    "nonbinary":("fff731","ffffff","9c5ad6","292929"),
    "trans":("5bcffa","f5abb9","ffffff","f5abb9","5bcffa"),
    "bisexual":("d60270","9b4f96","0038a8",),
    "pansexual":("ff1b8d","ffd900","1bb3ff"),
    "lesbian":("d62900","ff9b55","ffffff","d462a5","a50062"),
    "gay":("068d6f","97e7c0","ffffff","7aace1","3c1977")
}

import os,math,time,sys
if len(sys.argv)>1:
    if sys.argv[1] in flag_colors:
        flag_type = sys.argv[1]
os.system("")
print("\x1b[0;0H\x1b[2J\x1b[?25l")

def color_from_hexcode(h, mode="fg"):
    modes = {"fg":38,"bg":48}
    r,g,b = [int(h[i : i + 2], 16) for i in range(0, 6, 2)]
    return f"\x1b[{modes[mode]};2;{r};{g};{b}m"
 

def clamp(minimum,n,maximum):
    return max(minimum,min(maximum,n))
def draw_flag(t,colors):
    print("\x1b[0;0H")
    s = ""
    w,h = flag_width,flag_height
    for y in range(h):
        s +="\n"
        for x in range(w):
            ch = " "
            if flag_x_range[0]<x<w-flag_x_range[1]:
                stripe_size = 1231
                amp = flag_amplitude/stripe_size
                n = ((int((math.sin(t+x*flag_frequency)*flag_amplitude)+y*len(colors)))-flag_offset)
                n/=flag_scale
                if 0<=n<(len(colors)):
                    ch=color_from_hexcode(colors[int(n)],mode="bg")+" \x1b[0m"
            s+=ch
    print(s)
t = 0
while True:
    draw_flag(t,flag_colors[flag_type])
    t+=flag_wave_speed
    time.sleep(frame_sleep_time)
