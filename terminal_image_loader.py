#by gloop#5445
from PIL import Image
import os,sys,importlib,ctypes

pillow_installed =  importlib.util.find_spec("PIL")
class coord(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
class console_font(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", coord),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * 32)]
font = console_font()
font.cbSize = ctypes.sizeof(console_font)
font.nFont = 1
font.dwFontSize.X = 1
font.dwFontSize.Y = 1
font.FontFamily = 54
font.FaceName = "Cascadia Code"
handle = ctypes.windll.kernel32.GetStdHandle(-11)
ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))
os.system("title Terminal Image Loader")
input_file = sys.argv[1]
def color_from_rgb(col):
    r,g,b = col
    return f"\x1b[38;2;{r};{g};{b}m"
if pillow_installed != None:
    with Image.open(input_file) as im:
        w,h = im.size
        px=im.load()
    for y in range(0,h):
        print()
        for x in range(0,w):
            pixel_color = px[x,y][:3]
            print(f"{color_from_rgb(pixel_color)}██\x1b[0m",end="")
else:
    print(f"{color_from_rgb((255,0,0))}PIL is not installed")
    print(f"please run the following command in CMD: pip install pillow")
os.system("pause >nul")