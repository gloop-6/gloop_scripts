#by gloop#5445

#KEYBINDS:
#Q - change movement mode
#E - change shading mode
#R - change spawn/delete mode
#WASD - movement
#Enter - interact
from vector_class import vec2,vec3
import os,time,ctypes,math,random,colorsys
os_type = os.name
if os_type=="nt":
    import msvcrt
    from ctypes import wintypes
elif os_type=="posix":
    import keyboard #pip install keyboard
w,h = 80,40
os.system("")
print(f"\x1b[8;{h+7};{(w*2)+8}t")
print("\x1b[2J\x1b[0;0H\x1b[?25l")

max_circle_count = 50
circle_mode = 0
action_mode = 1
spawn_cooldown = 0
movement_mode = 0
modes = ["None","Particles","Circles","Delete"]
circle_render_modes = ["Shaded","Flat","Hollow"]
movement_modes = ["Direct","Smooth"]
prev_keypresses = []

movement_directions = vec2(0, -1), vec2(-1, 0), vec2(0, 1), vec2(1, 0)
movement_keys = ["w", "a", "s", "d"]

keys_1="`1234567890-=[]\\;\'"
keys_2 ="~!@#$%^&*()_+{}|:\""
uppercase_table =str.maketrans(keys_1,keys_2)
lowercase_table =str.maketrans(keys_2,keys_1)

os_name = os.name
#os_name = "posix"
if os_name == "nt":
    import msvcrt
elif os_name == "posix":
    import keyboard

def get_keys():
    keys_to_remove = "~!@#$%^&*()_+{}?<>|:\"\x00\n"
    keys_to_replace = {
        "\x1b":"Escape",
        "\r":"Enter",
        "\x08":"Backspace",
        "\t":"Tab",
        " ":"Space"
    }
    keys = set()
    keys_hex = set()
    if os_name=="nt":
        function_keys = {i:f"F{idx+1}"for idx,i in enumerate(range(0x70,0x85))}
        modifiers = {0x10:"Shift",0x11:"Control",0x12:"Alt"}
        for mod in modifiers:
            key = ctypes.windll.user32.GetKeyState(mod)
            if key in [0xff80,0xff81]:
                keys.add(modifiers[mod])
        for i in range(0x08,0xff):
            key = ctypes.windll.user32.GetKeyState(i)
            if key in [0xff80,0xff81]:
                k = ctypes.windll.user32.MapVirtualKeyA(ctypes.c_short(i),2)
                k = chr(k).lower()
                if k in keys_to_replace:
                    k = keys_to_replace[k]
                if i in function_keys:
                    keys.add(function_keys[i])
                keys.add(k)
                keys_hex.add(hex(i))
        if msvcrt.kbhit():
            msvcrt.getch()
    elif os_name=="posix":
        modifiers = ["shift","control","alt"]
        function_keys = [f"f{i}"for i in range(1,25)]
        for key in function_keys:
            if keyboard.is_pressed(key):
                keys.add(key.capitalize())
        for mod in modifiers:
            if keyboard.is_pressed(mod):
                keys.add(mod.capitalize())
        for i in range(0x08,0xff):
            k = chr(i).lower()
            try:
                key = keyboard.is_pressed(k)
                if key:
                    if k in keys_to_replace:
                        k = keys_to_replace[k]
                    if i in function_keys:
                        keys.add(function_keys[i])
                    keys.add(k)
            except ValueError:
                pass
    return [i for i in keys if i not in keys_to_remove]

def handle_keys():
    k = get_keys()
    global circle_mode,action_mode,prev_keypresses,movement_mode
    dir = vec2(0,0)
    movement_keys_pressed = [i for i in k if i in movement_keys]

    if "Enter" in k:
        player_action(action_mode)
    n = 1
    movement_speed_multiplier = 1
    if "Shift" in k:
        n*=-1
        movement_speed_multiplier = 1.5
    if "q" in k and "q" not in prev_keypresses:
        
        movement_mode+=n
        movement_mode%=2
    if "e" in k and "e" not in prev_keypresses:
        circle_mode+=n
        circle_mode%=3

    if "r" in k and "r" not in prev_keypresses:
        action_mode+=n
        action_mode%=4

    
    if movement_keys_pressed:
        first_key = movement_keys_pressed[-1]
        dir = movement_directions[movement_keys.index(first_key)]
        if len(movement_keys_pressed) > 1:
            
            second_key = movement_keys_pressed[-2]
            dir+=movement_directions[movement_keys.index(second_key)]

            if movement_mode == 1:
                dir/=2
        dir *= movement_speed_multiplier
    prev_keypresses = k
    return dir

def clamp(minimum,n,maximum):
    return max(minimum,min(maximum,n))

def color_from_rgb(r=0, g=0, b=0, mode="fg", color_array=None):
    if color_array is not None:
        if type(color_array)==vec3:
            r=color_array.x
            g=color_array.y
            b=color_array.z
        else:
            r, g, b = color_array
    if mode == "fg":
        mode = 38
    if mode == "bg":
        mode = 48
    return f"\x1b[{mode};2;{r};{g};{b}m"

def color_from_hsv(h=0, s=0, v=0, mode="fg", color_array=None):
    if color_array is not None:
        if type(color_array)==vec3:
            h=color_array.x
            s=color_array.y
            v=color_array.z
        else:
            h, s, v = color_array
    r, g, b = [int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v)]
    return color_from_rgb(r, g, b, mode)

def hex_to_rgb(h):
    return [int(h[i : i + 2], 16) for i in range(0, 6, 2)]

def color_from_hexcode(h, mode="fg"):
    return color_from_rgb(color_array=hex_to_rgb(h), mode=mode)

def color_ramp(color1,color2,fac):
    return color_from_rgb(color_array=color1.lerp(color2,fac))

def random_vec3(minimum,maximum):
    if type(minimum)==vec3:
        min_x,min_y,min_z = minimum.x,minimum.y,minimum.z
    else:
        min_x,min_y,min_z = minimum
    if type(maximum)==vec3:
        max_x,max_y,max_z = maximum.x,maximum.y,maximum.z
    else:
        max_x,max_y,max_z = maximum

    return vec3(
        random.uniform(min_x,max_x),
        random.uniform(min_y,max_y),
        random.uniform(min_z,max_z)
    )
def player_action(mode):
    if mode == 1:
        spawn_particle(p.pos,p.vel,random.randint(3,5))
    if mode == 2:
        global spawn_cooldown
        c_color = random_vec3(vec3(10,10,10),vec3(255,255,255))
        if spawn_cooldown == 0:
            spawn_circle(p.pos,p.vel,random.uniform(1.5,7.4),c_color)
            spawn_cooldown = 5
    if mode == 3:
        circle_positions = get_circle_positions()
        particle_positions = get_particle_positions()
        if p.pos.floor() in circle_positions:
            circ = circle_positions[p.pos.floor()]
            c_instance = circles[circles.index(circ)]
            c_instance.remove()
        if p.pos.floor() in particle_positions:
            part = particle_positions[p.pos.floor()]
            p_instance = particles[particles.index(part)]
            p_instance.remove()

class circle:
    def __init__(self,pos,vel,radius,color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.color = color
    def update(self):
        new_pos = self.pos + self.vel
        for i in circles:
            if i!=self and math.floor(new_pos.distance(i.pos))<(self.radius + i.radius):
                self.vel += (new_pos - i.pos)/((self.radius + i.radius)*2)
                self.vel *= 0.8
                i.vel += (i.pos-new_pos)/((self.radius + i.radius)*2)
                i.vel = i.vel.clamp(vec2(-1,-1),vec2(1,1))
                i.vel *= 0.8

        if new_pos.distance(p.pos)<self.radius and action_mode!=3:
            self.vel += (new_pos - p.pos)/2

        self.vel *= 0.98
        self.vel=self.vel.clamp(vec2(-1,-1),vec2(1,1))
        if new_pos.in_box((self.radius,self.radius),(w-self.radius,h-self.radius)):
            self.pos = new_pos

        else:
            if not self.radius<=new_pos.x<(w-self.radius):
                self.vel.x *=-0.8
            if not self.radius<=new_pos.y<(h-self.radius):
                self.vel.y *=-0.8
            new_pos= self.pos.lerp(vec2(w//2,h//2),0.05)
            self.pos = new_pos
    def remove(self):
        if self in circles:
            circles.remove(self)
class particle:
    def __init__(self,pos,vel,life):
        self.pos = pos
        self.vel = vel
        self.life = life
    def update(self):
        new_pos = self.pos + self.vel
        self.vel *= 0.99
        self.life -= 1
        if self.life < 1:
            self.remove()
        for i in circles:
            if i!=self and math.floor(new_pos.distance(i.pos))<i.radius:
                self.vel += (new_pos - i.pos)/(i.radius)
                self.vel *= 0.8
                i.vel += (i.pos-new_pos)/((i.radius)*2)
                i.vel = i.vel.clamp(vec2(-1,-1),vec2(1,1))
                i.vel *= 0.8
        if abs(self.vel) < vec2(0.04,0.04):
            self.vel = vec2(0,0)
        self.vel=self.vel.clamp(vec2(-2,-2),vec2(2,2))
        if new_pos.in_box((0,0),(w,h)):
            self.pos = new_pos
        else:
            if not 0<=new_pos.x<w:
                self.vel.x *=-0.8
            if not 0<=new_pos.y<h:
                self.vel.y *=-0.8
    def remove(self):
        if self in particles:
            particles.remove(self)

class ply:
    def __init__(self,pos,vel,trail,trail_length):
        self.pos = pos
        self.vel = vel
        self.trail = trail
        self.trail_length = trail_length
    def update(self,dir):
        if movement_mode == 0:
            new_pos = self.pos + (dir)
            self.vel = vec2(0,0)
        elif movement_mode == 1:
            new_pos = self.pos + self.vel
        self.vel  = self.vel+dir/5
        self.vel  *= 0.9
        if len(self.trail)>self.trail_length:
            self.trail.pop(-1)
        else:
            self.trail.insert(0,self.pos.floor())
        if abs(self.vel ) < vec2(0.04,0.04):
            self.vel  = vec2(0,0)
        if movement_mode == 1:
            new_pos = self.vel  + self.pos
        self.vel = self.vel.clamp(vec2(-1.4,-1.4),vec2(1.4,1.4))

        if new_pos.in_box((0,0),(w-1,h-1)):
            self.trail.insert(0,((self.pos+new_pos)/2).floor())
            self.pos = new_pos
        else:
            if self.vel.length()>0.7:
                if not 0<=new_pos.x<=w:
                    self.vel.x *=-0.8
                if not 0<=new_pos.y<=h:
                    self.vel.y *=-0.8
                spawn_particle(self.pos,self.vel,random.randint(7,12))


def spawn_particle(pos,vel,count):
    for _ in range(count):
        particle_pos = pos
        particle_vel = vel+vec2(random.uniform(-1,1),random.uniform(-1,1))
        particle_life = random.randint(10,20)
        particles.append(particle(particle_pos,particle_vel,particle_life))
def draw_line(pos_1,pos_2):
    i=0
    x1,y1 = pos_1
    x2,y2 = pos_2
    dx = abs(x2 - x1)
    sx = 1 if x1 < x2 else -1
    dy = -abs(y2 - y1)
    sy = 1 if y1 < y2 else -1
    error = dx + dy
    points = set()
    while True:
        i+=1
        if i>1000:
            break
        points.add((x1,y1))
        if x1 == x2 and y1 == y2: break
        e2 = 2 * error
        if e2 >= dy:
            if x1 == x2: break
            error = error + dy
            x1 = x1 + sx
        if e2 <= dx:
            if y1 == y2: break
            error = error + dx
            y1 = y1 + sy
    return points

def spawn_circle(pos,vel,radius,color=vec3(0,0,0)):
    if len(circles)+1 < max_circle_count:
        circle_radius = radius
        circle_pos = pos
        circle_vel = vel + vec2(random.uniform(-1,1),random.uniform(-1,1))
        circle_color = color
        circles.append(circle(circle_pos,circle_vel,circle_radius,circle_color))

particles = []
p = ply(vec2(w//2,h//2),vec2(0,0),[],20)

trail_chars = "⬤⬣●◾•⬝     "
particle_chars = "⬝•◾x"
def get_particle_positions():
    return {i.pos.floor():i for i in particles}

def bresenham_circle(pos,radius):
    switch = 3 - (2 * radius)
    points = set()
    x = 0
    y = int(radius)
    x2,y2 = pos
    x2,y2 = int(x2),int(y2)
    while x <= y:
        points.add((x+x2,-y+y2))
        points.add((y+x2,-x+y2))
        points.add((y+x2,x+y2))
        points.add((x+x2,y+y2))
        points.add((-x+x2,y+y2))        
        points.add((-y+x2,x+y2))
        points.add((-y+x2,-x+y2))
        points.add((-x+x2,-y+y2))
        if switch < 0:
            switch = switch + (4 * x) + 6
        else:
            switch = switch + (4 * (x - y)) + 10
            y = y - 1
        x = x + 1
    return points
def implicit_circle(pos,radius):
    points = set()
    for y in range(-int(radius),int(radius)):
        for x in range(-int(radius),int(radius)):
            if (x+0.5)**2 + (y+0.5)**2 < (int(radius)**2):
                points.add((vec2(x,y)+pos).floor())
    return points
def radius_circle(pos,radius):
    points = set() 
    for y in range(-int(radius),int(radius)):
        for x in range(-int(radius),int(radius)):
            pos2 = vec2(0.5,0.5)
            if (vec2(x,y)+pos2).length()<radius:
                points.add(((vec2(x,y)+pos).floor(),(vec2(x,y)+pos2).length()))
    return points
def get_circle_render_positions():
    points = {}
    distances = {}
    if circle_mode==0:
        for i in circles:
            circ = radius_circle(i.pos.floor(),i.radius)
            for k in circ:
                points[k[0]]=(i)
                distances[k[0]]=(i,k[1])
        return points,distances
    if circle_mode==1:
        for i in circles:
            circ = implicit_circle(i.pos.floor(),i.radius)
            for k in circ:
                points[k]=(i)
                distances[k]=(i,0)
        return points,0
    if circle_mode==2:
        for i in circles:
            circ = bresenham_circle(i.pos.floor(),i.radius)
            for k in circ:
                points[k]=i
        return points,0
def get_circle_positions():
    points = {}
    for i in circles:
        circ = radius_circle(i.pos,i.radius)
        for k in circ:
            points[k[0]]=(i)
    return points
circles = []

def render():
    line = ""
    particle_positions = get_particle_positions()
    circle_positions,circle_distances = get_circle_render_positions()
    reset_screen = "\x1b[0;0H\x1b[?25l"
    box_top = "╔"+("═"*w*2)+"╗"
    box_bottom = "╚"+("═"*w*2)+"╝"
    print(box_top)
    for y in range(h+1):
        if y!=0:
            print(line)
            line = ""
        for x in range(w):
            ch = "  "
            if vec2(x,y) in particle_positions.keys():
                part = particle_positions[vec2(x,y)]
                particle_char = particle_chars[clamp(0,part.life//3,len(particle_chars)-1)]
                hue = part.vel.length()/15
                sat = 1-part.vel.length()/3
                val = part.life/10
                particle_color = color_from_hsv(hue,sat,val)
                ch = particle_color+particle_char+" \x1b[0m"

            if vec2(x,y) in p.trail:
                hue = 0.2-(p.trail.index(vec2(x,y))/100)
                sat = (p.trail.index(vec2(x,y))/26)+0.3
                particle_color = color_from_hsv(hue,sat,1)
                ch = particle_color+trail_chars[p.trail.index(vec2(x,y))//3]+" \x1b[0m"

            if vec2(x,y)==p.pos.floor():
                hue = p.vel.length()/15
                sat = 0
                player_color = color_from_hsv(hue,sat,1)
                ch = player_color+"()\x1b[0m"

            if vec2(x,y) in circle_positions:
                c = circle_positions[(x,y)]
                c_instance = circles[circles.index(c)]
                if circle_mode==0:
                    shade = circle_distances[(x,y)][1]
                    shade = vec3(shade,shade,shade)
                    circle_color = (c_instance.color - (shade/c_instance.radius)*150).floor().clamp(vec3(0,0,0),vec3(255,255,255))
                else:
                    circle_color = c_instance.color.floor().clamp(vec3(0,0,0),vec3(255,255,255))
                circle_color = color_from_rgb(color_array=circle_color)
                ch = circle_color+"██\x1b[0m"
            if vec2(x,y)==p.pos.floor():
                hue = p.vel.length()/15
                sat = 0
                player_color = color_from_hsv(hue,sat,1)
                ch = player_color+"()\x1b[0m"
            line+=ch
        line="║"+line+"║"
    print(box_bottom)
    print(f" Player Speed: {p.vel.length():1f}, Shading: {circle_render_modes[circle_mode]}, Spawn mode: {modes[action_mode]}             ")
    print(f" Movement mode: {movement_modes[movement_mode]}          ")
    print(p.pos.in_box((-1,-1),(w,h)))
    print(reset_screen)
    
render()
t=0
while True:
    if spawn_cooldown != 0:
        spawn_cooldown -= 1
    t+=0.05
    t%=2**16
    dir = handle_keys()
    #c.update()
    for i in particles:
        i.update()
    for i in circles:
        i.update()
    if dir:
        p.update(dir)
    else:
        p.update(vec2(0,0))
    render()
    time.sleep(0.02)
