#firesim, by gloop#5445
max_particles = 1600
energy_loss_rate = 0.2

r = 1
w,h = 60,30
import os,random,colorsys,time,math
os.system("")
from vector_class import vec2, vec3
force_vec = vec2(0,-0.002)
print("\x1b[2J\x1b[0;0H\x1b[?25l")
print(f"\x1b[8;{h+3};{w+3}t")
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
def random_vec2(x_range,y_range):
    x_min,x_max = x_range
    y_min,y_max = y_range
    return vec2(random.uniform(x_min,x_max),random.uniform(y_min,y_max))
fire_chars = " .▪*●■▓█"
def fire_color(energy):
    multiplier = 0.5
    r = int(min(1,energy/(2*multiplier))*255)
    g = int(min(1,energy/(6*multiplier))*255)
    b = int(min(1,energy/(8*multiplier))*255)
    char = fire_chars[min(len(fire_chars)-1,int(energy/multiplier))]
    return color_from_rgb(r,g,b),char
class part:
    def __init__(self,pos,vel,energy,flagged_for_removal):
        self.pos = pos
        self.vel = vel
        self.energy = energy
        self.flagged_for_removal = flagged_for_removal
    def update(self):
        self.energy-=energy_loss_rate
        if self.energy<=0 or not self.pos.in_box((0,0),(w,h)):
            i.flagged_for_removal = True
        self.vel = self.vel + force_vec
        self.vel = self.vel.clamp(vec2(-0.3,-0.3),vec2(1,1))
        self.pos = math.floor(self.pos+self.vel)
particles = set()
def spawn_particle():
    if len(particles)<max_particles:
        pos = vec2(random.randint(0,w),h)
        vel = random_vec2((0,0),(-0.01,0.01))
        life = random.uniform(1,5)
        particles.add(part(pos,vel,life,False))
def get_particle_positions():
    return {i.pos:i for i in particles}
def render():
    particle_positions = get_particle_positions()
    s = ""
    for y in range(h):
        print(s)
        s=""
        for x in range(w):
            ch = " "
            if (x,y) in particle_positions:
                particle_instance = particle_positions[(x,y)]
                color,char = fire_color(particle_instance.energy)
                ch = color+char+"\x1b[0m"
            s+=ch
    print(f"Particle Count: {len(particles)}")
    print("\x1b[0;0H")
for i in range(max_particles):
    spawn_particle()
while True:
    for i in particles:
        i.update()
    render()
    particles = set([i for i in particles if not i.flagged_for_removal])
    t = 0
    while len(particles)<max_particles and t<1000:
        t+=1
        spawn_particle()
    time.sleep(0.02)