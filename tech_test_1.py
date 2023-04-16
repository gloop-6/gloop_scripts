#by gloop#5445

#KEYBINDS:
#Q - change movement mode
#E - change shading mode
#R - change spawn/delete mode
#WASD - movement
#Enter - interact
import os,time,ctypes,math,random,colorsys,operator
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
class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def __contains__(self,val):
        return bool(self.x == val or self.y == val or self.z == val)
    def __bool__(self):
        return bool(self.x or self.y or self.z)
    def length(self):
        return math.hypot(self.x,self.y,self.y)
    def lerp(self,other,t):
        return vec3(
            (1-t)*self.x+t*other.x,
            (1-t)*self.y+t*other.y,
            (1-t)*self.z+t*other.z
            )
    def distance(self,other):
        return math.hypot(self.x-other.x,self.y-other.y,self.z-other.z)
    def sign(self):
        return vec3(
        1 if self.x>0 else -1 if self.x<0 else 0,
        1 if self.y>0 else -1 if self.y<0 else 0,
        1 if self.z>0 else -1 if self.y<0 else 0
        )
    def in_box(self,x_range,y_range,z_range):
        return x_range[0]<self.x<x_range[1] and y_range[0]<self.y<y_range[1] and z_range[0]<self.z<z_range[1]
    def clamp(self,minimum,maximum):
        return vec3(
        max(minimum.x, min(maximum.x, self.x)),
        max(minimum.y, min(maximum.y, self.y)),
        max(minimum.z, min(maximum.z, self.z))
        )
    def _equality_op(op):
        def _vec_op(a,b):
            if type(b) == vec3:
                return op(a.x,b.x) and op(a.y,b.y) and op(a.z,b.z)
            if type(b) in (list,tuple):
                return op(a.x,b[0]) and op(a.y,b[1]) and op(a.z,b[2])
            if type(b) in (int,float):
                return op(a.x,b) and op(a.y,b) and op(a.z,b)
        return _vec_op
    def _arithmetic_op(op):
        def _vec_op(a,b):
            if type(b) == vec3:
                return vec3(op(a.x,b.x), op(a.y,b.y), op(a.z,b.z))
            if type(b) in (list,tuple):
                return vec3(op(a.x,b[0]), op(a.y,b[1]), op(a.z,b[2]))
            if type(b) in (int,float):
                return vec3(op(a.x,b), op(a.y,b), op(a.z,b))
        return _vec_op
    def _generic_op(op):
        def _vec_op(a):
            return vec3(op(a.x), op(a.y), op(a.z))
        return _vec_op
    __eq__ = _equality_op(operator.eq)
    __lt__ = _equality_op(operator.lt)
    __le__ = _equality_op(operator.le)
    __gt__ = _equality_op(operator.gt)
    __ge__ = _equality_op(operator.ge)
    __ne__ = _equality_op(operator.ne)

    __rmul__ = _arithmetic_op(operator.mul)
    __radd__ = _arithmetic_op(operator.add)
    __rsub__ = _arithmetic_op(operator.sub)
    __rtruediv__ = _arithmetic_op(operator.truediv)
    __rfloordiv__ = _arithmetic_op(operator.floordiv)
    __rmod__ = _arithmetic_op(operator.neg)
    __rpow__ = _arithmetic_op(operator.pow)

    __mul__ = _arithmetic_op(operator.mul)
    __add__ = _arithmetic_op(operator.add)
    __sub__ = _arithmetic_op(operator.sub)
    __truediv__ = _arithmetic_op(operator.truediv)
    __floordiv__ = _arithmetic_op(operator.floordiv)
    __mod__ = _arithmetic_op(operator.neg)
    __pow__ = _arithmetic_op(operator.pow)
    __floor__ = _generic_op(math.floor) 
    __round__ = _generic_op(round)
    __ceil__ = _generic_op(math.ceil)
    __trunc__ = _generic_op(math.trunc)
    __abs__ = _generic_op(abs)

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}, {self.y})"
    def __hash__(self):
        return hash((self.x, self.y))
    def __contains__(self,val):
        return bool(self.x == val or self.y == val)
    def __bool__(self):
        return bool(self.x or self.y)
    def length(self):
        return math.hypot(self.x,self.y)
    def lerp(self,other,t):
        return vec2((1-t)*self.x+t*other.x,(1-t)*self.y+t*other.y)
    def distance(self,other):
        return math.hypot(self.x-other.x,self.y-other.y)
    def sign(self):
        return vec2(
        1 if self.x>0 else -1 if self.x<0 else 0,
        1 if self.y>0 else -1 if self.y<0 else 0
        )
    def in_box(self,x_range,y_range):
        return x_range[0]<self.x<x_range[1] and y_range[0]<self.y<y_range[1]
    def clamp(self,minimum,maximum):
        return vec2(
        max(minimum.x, min(maximum.x, self.x)),
        max(minimum.y, min(maximum.y, self.y))
        )
    def _equality_op(op):
        def _vec_op(a,b):
            if type(b) == vec2:
                return op(a.x,b.x) and op(a.y,b.y)
            if type(b) in (list,tuple):
                return op(a.x,b[0]) and op(a.y,b[1])
            if type(b) in (int,float):
                return op(a.x,b) and op(a.y,b)
        return _vec_op
    def _arithmetic_op(op):
        def _vec_op(a,b):
            if type(b) == vec2:
                return vec2(op(a.x,b.x), op(a.y,b.y))
            if type(b) in (list,tuple):
                return vec2(op(a.x,b[0]), op(a.y,b[1]))
            if type(b) in (int,float):
                return vec2(op(a.x,b), op(a.y,b))
        return _vec_op
    def _generic_op(op):
        def _vec_op(a):
            return vec2(op(a.x), op(a.y))
        return _vec_op
    __eq__ = _equality_op(operator.eq)
    __lt__ = _equality_op(operator.lt)
    __le__ = _equality_op(operator.le)
    __gt__ = _equality_op(operator.gt)
    __ge__ = _equality_op(operator.ge)
    __ne__ = _equality_op(operator.ne)

    __rmul__ = _arithmetic_op(operator.mul)
    __radd__ = _arithmetic_op(operator.add)
    __rsub__ = _arithmetic_op(operator.sub)
    __rtruediv__ = _arithmetic_op(operator.truediv)
    __rfloordiv__ = _arithmetic_op(operator.floordiv)
    __rmod__ = _arithmetic_op(operator.neg)
    __rpow__ = _arithmetic_op(operator.pow)

    __mul__ = _arithmetic_op(operator.mul)
    __add__ = _arithmetic_op(operator.add)
    __sub__ = _arithmetic_op(operator.sub)
    __truediv__ = _arithmetic_op(operator.truediv)
    __floordiv__ = _arithmetic_op(operator.floordiv)
    __mod__ = _arithmetic_op(operator.neg)
    __pow__ = _arithmetic_op(operator.pow)
    __floor__ = _generic_op(math.floor) 
    __round__ = _generic_op(round)
    __ceil__ = _generic_op(math.ceil)
    __trunc__ = _generic_op(math.trunc)
    __abs__ = _generic_op(abs)

movement_directions = vec2(0, -1), vec2(-1, 0), vec2(0, 1), vec2(1, 0)
movement_directions += vec2(0, -1.5), vec2(-1.5, 0), vec2(0, 1.5), vec2(1.5, 0)
movement_keys = ["w", "a", "s", "d","W","A","S","D"]

keys_1="`1234567890-=[]\\;\'"
keys_2 ="~!@#$%^&*()_+{}|:\""
uppercase_table =str.maketrans(keys_1,keys_2)
lowercase_table =str.maketrans(keys_2,keys_1)
def get_keys():
    keys = set()
    if os_type=="nt":
        for i in range(0x00,0xff):
            key = ctypes.windll.user32.GetKeyState(i)
            if key in [0xff80,0xff81] and key != 0:
                n = ctypes.windll.user32.MapVirtualKeyA(ctypes.c_short(i),2)
                n = chr(n).lower().translate(lowercase_table)
                if ctypes.windll.user32.GetKeyState(0x10) in [0xff80,0xff81]:
                    n = n.upper().translate(uppercase_table)
                if n != "\x00":
                    keys.add(n)
        if msvcrt.kbhit():
            msvcrt.getch() #this is just to get rid of stray keypresses
    elif os_type=="posix":
        for i in range(0x00,0xff):
            try:
                if i == 0x10:
                    print( keyboard.is_pressed(chr(i)))
                n = chr(i).lower().translate(lowercase_table)
                key = keyboard.is_pressed(n)
                if keyboard.is_pressed("shift"):
                    n = n.upper().translate(uppercase_table)
                if key:
                    keys.add(n)
            except ValueError:
                pass
    return list(keys)

def handle_keys():
    k = get_keys()
    global circle_mode,action_mode,prev_keypresses,movement_mode
    dir = vec2(0,0)
    movement_keys_pressed = [i for i in k if i in movement_keys]

    if "\r" in k:
        player_action(action_mode)
    if "q" in k and "q" not in prev_keypresses:
        movement_mode+=1
        movement_mode%=2
    if "Q" in k and "Q" not in prev_keypresses:
        movement_mode-=1
        movement_mode%=2
    if "e" in k and "e" not in prev_keypresses:
        circle_mode+=1
        circle_mode%=3
    if "E" in k and "E" not in prev_keypresses:
        circle_mode-=1
        circle_mode%=3
    if "r" in k and "r" not in prev_keypresses:
        action_mode+=1
        action_mode%=4
    if "R" in k and "R" not in prev_keypresses:
        action_mode-=1
        action_mode%=4
    
    if movement_keys_pressed:
        first_key = movement_keys_pressed[-1]
        dir = movement_directions[movement_keys.index(first_key)]
        if len(movement_keys_pressed) > 1:
            
            second_key = movement_keys_pressed[-2]
            dir+=movement_directions[movement_keys.index(second_key)]
            if movement_mode == 1:
                dir/=2
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

def random_vec3(x_range,y_range,z_range):
    return vec3(
        random.uniform(x_range[0],x_range[1]),
        random.uniform(y_range[0],y_range[1]),
        random.uniform(z_range[0],z_range[1])
    )
def player_action(mode):
    if mode == 1:
        spawn_particle(p.pos,p.vel,random.randint(3,5))
    if mode == 2:
        global spawn_cooldown
        c_color = random_vec3((10,255),(10,255),(10,255))
        if spawn_cooldown == 0:
            spawn_circle(p.pos,p.vel,random.uniform(1.5,7.4),c_color)
            spawn_cooldown = 5
    if mode == 3:
        circle_positions = get_circle_positions()
        particle_positions = get_particle_positions()
        if math.floor(p.pos) in circle_positions:
            circ = circle_positions[math.floor(p.pos)]
            c_instance = circles[circles.index(circ)]
            c_instance.remove()
        if math.floor(p.pos) in particle_positions:
            part = particle_positions[math.floor(p.pos)]
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
        if new_pos.in_box((self.radius,w-self.radius),(self.radius,h-self.radius)):
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
        if new_pos.in_box((0,w),(0,h)):
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
            self.trail.insert(0,math.floor(self.pos))
        if abs(self.vel ) < vec2(0.04,0.04):
            self.vel  = vec2(0,0)
        if movement_mode == 1:
            new_pos = self.vel  + self.pos
        self.vel =self.vel.clamp(vec2(-1.4,-1.4),vec2(1.4,1.4))

        if new_pos.in_box((-1,w),(-1,h)):
            self.trail.insert(0,math.floor((self.pos+new_pos)/2))
            self.pos = new_pos
        else:
            if self.vel.length()>0.7:
                if not 0<=new_pos.x<w:
                    self.vel.x *=-0.8
                if not 0<=new_pos.y<h:
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
    return {math.floor(i.pos):i for i in particles}

def bresenham_circle(pos,radius):
    switch = 3 - (2 * radius)
    points = set()
    x = 0
    y = int(radius)
    x2,y2 = int(pos.x),int(pos.y)
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
                points.add(math.floor(vec2(x,y)+pos))
    return points
def radius_circle(pos,radius):
    points = set() 
    for y in range(-int(radius),int(radius)):
        for x in range(-int(radius),int(radius)):
            pos2 = vec2(0.5,0.5)
            if (vec2(x,y)+pos2).length()<radius:
                points.add((math.floor(vec2(x,y)+pos),(vec2(x,y)+pos2).length()))
    return points
def get_circle_render_positions():
    points = {}
    distances = {}
    if circle_mode==0:
        for i in circles:
            circ = radius_circle(math.floor(i.pos),i.radius)
            for k in circ:
                points[k[0]]=(i)
                distances[k[0]]=(i,k[1])
        return points,distances
    if circle_mode==1:
        for i in circles:
            circ = implicit_circle(math.floor(i.pos),i.radius)
            for k in circ:
                points[k]=(i)
                distances[k]=(i,0)
        return points,0
    if circle_mode==2:
        for i in circles:
            circ = bresenham_circle(math.floor(i.pos),i.radius)
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

def render(t):
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
    
            if vec2(x,y)==math.floor(p.pos):
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
                    circle_color = math.floor(c_instance.color - (shade/c_instance.radius)*150).clamp(vec3(0,0,0),vec3(255,255,255))
                else:
                    circle_color = math.floor(c_instance.color).clamp(vec3(0,0,0),vec3(255,255,255))
                circle_color = color_from_rgb(color_array=circle_color)
                ch = circle_color+"██\x1b[0m"
            if vec2(x,y)==math.floor(p.pos):
                hue = p.vel.length()/15
                sat = 0
                player_color = color_from_hsv(hue,sat,1)
                ch = player_color+"()\x1b[0m"
            line+=ch
        line="║"+line+"║"
    print(box_bottom)
    print(f" Player Speed: {p.vel.length():1f}, Shading: {circle_render_modes[circle_mode]}, Spawn mode: {modes[action_mode]}             ")
    print(f" Movement mode: {movement_modes[movement_mode]}          ")

    print(reset_screen)
    
render(0)
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
    render(t)

    time.sleep(0.02)