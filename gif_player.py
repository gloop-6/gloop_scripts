#by gloop#5445
#=#
default_image_size = (50,50)
default_image_path = "test.gif"
default_frame_duration = 0.1
double_width = True
#=#
from PIL import Image
import os,time,argparse
os.system("")
parser = argparse.ArgumentParser()
parser.add_argument('--image_size',default=default_image_size)
parser.add_argument('--file_path',default=default_image_path)
parser.add_argument('--frame_duration',default=default_frame_duration,type=float)
parser.add_argument('--double_width',default=double_width,type=bool)
args = vars(parser.parse_args())
if args["image_size"]!=default_image_size:
    image_size = ''.join(c for c in args["image_size"] if c not in ' ()')
    image_size = [int(i) for i in image_size.split(",")]
else:
    image_size = default_image_size
file_path = args["file_path"]
frame_duration = args["frame_duration"]
double_width = args["double_width"]
print("\x9b2J\x9b0;0H\x9b?25l")

gif = Image.open(file_path)

def color_from_rgb(color):
    r,g,b = color
    return f"\x1b[48;2;{r};{g};{b}m"

def process_gif_frame(f):
    if double_width:
        char = "  "
    else:
        char = " "
    f = f.convert("RGB")
    if f.size[0]>image_size[0] and f.size[1]>image_size[1]:
        f=f.resize(image_size)
    px=f.load()
    w,h = f.size
    output = ""
    for y in range(0,h):
        output+="\n"
        for x in range(0,w):
            pixel_color = px[x,y][:3]
            output+=f"{color_from_rgb(pixel_color)}"+f"{char}\x1b[0m"
    return (output)

def generate_frames():
    frames = []
    for i in range(0,gif.n_frames):
            gif.seek(i)
            frames.append(process_gif_frame(gif))
    return frames

frames = generate_frames()
while True:
    for frame in frames:

        print(frame)
        print("\x9bH\x9b?25l")
        time.sleep(frame_duration)
