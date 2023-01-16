#by gloop#5445
ansi_escape = "\x1b["
bg_escape = f"{ansi_escape}48;5;"
fg_escape = f"{ansi_escape}38;5;"
reset_escape = f"{ansi_escape}0m"
bounce_dampen = 0.75
def col_from_rgb(c):
    r,g,b = c
    r = int(5*r)
    g = int(5*g)
    b = int(5*b)
    return f"{fg_escape}{16 + (36 * r) + (6 * g) + b}m"

import math,random,os,time
os.system("title particle_sim_test")
w,h = 60,40
trail_max_length = 2
ground_height = 30
class part:
    def __init__(self,pos,vel,color,trail,life):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.trail = trail
        self.life = life
particles = []

def get_distance(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    d = abs(complex(x2-x1,y2-y1))
    return max(0.003,d)

def clamp(minimum,n,maximum):
    return max(minimum,min(maximum,n))

def random_pos(x_range,y_range):
    min_x,max_x = x_range
    min_y,max_y = y_range
    return (random.randint(min_x,max_x),random.randint(min_y,max_y))

def random_vel(x_range,y_range):
    min_x,max_x = x_range
    min_y,max_y = y_range
    return (random.uniform(min_x,max_x),random.uniform(min_y,max_y))

def random_color(ranges):
    return tuple([random.uniform(r[0],r[1]) for r in ranges])

def spawn_particles(count):
    for _ in range(count):
        particle_pos = random_pos((0,w),(0,ground_height))
        particle_vel = random_vel((-1,1),(-1,1))
        particle_color = random_color(((0,1),(0,1),(0,1)))
        particle_trail = []
        particle_life = 90
        particles.append(part(particle_pos,particle_vel,particle_color,particle_trail,particle_life))
    
def reset_particle(particle):
    spawn_particles(1)
    if particle in particles:
        particles.pop(particles.index(particle))

def update_trail(particle):
    trail = particle.trail
    pos = particle.pos
    pos = [int(pos[0]),int(pos[1])]
    trail.append(pos)
    if len(trail)>trail_max_length:
        trail.pop(0)
    particle.trail = trail

def get_force(body1,body2):
    x1,y1 = body1.pos
    x2,y2 = body2.pos
    d = get_distance(body1.pos,body2.pos)
    force_strength = 0.4
    return [((x2-x1)/d)*force_strength,((y2-y1)/d)*force_strength]

def update_particle(particle):
    particle.life -=1
    if particle.life <= 0:
        reset_particle(particle)
    pos = particle.pos
    update_trail(particle)
    vel = particle.vel
    vel = [vel[0],vel[1]+0.1]
    if pos[1]>ground_height-1:
        vel = [vel[0],vel[1]*-bounce_dampen]
    for i in particles:
        if i!=particle:
            if get_distance(i.pos,particle.pos)<2:
                force = get_force(i,particle)
                vel = [vel[0]+force[0],vel[1]+force[1]]
    vel = [clamp(-2,vel[0],2)*0.99,clamp(-2,vel[1],2)*0.99]

    pos = [pos[0]+vel[0],pos[1]+vel[1]]
    if clamp(0,pos[0],w)!=pos[0] or clamp(0,pos[1],h)!=pos[1]:
        reset_particle(particle)
    particle.pos = pos
    particle.vel = vel

def render():
    s = f"{ansi_escape}0;0H"
    for y in range(h):
        if y!=0:
            s+="\n"
        for x in range(w):
            ch = " "
            for i in particles:
                if [x,y] in i.trail:
                    trail_color = [clamp(0,i-0.1,1) for i in i.color]
                    ch = f"{col_from_rgb(trail_color)}.{reset_escape}"
                if [x,y]==[int(i.pos[0]),int(i.pos[1])]:
                    ch = f"{col_from_rgb(i.color)}●{reset_escape}"
            if y>=ground_height:
                ch = "█"
            s+=ch
    print(s)
spawn_particles(10)
while True:

    for i in particles:
        update_particle(i)
    render()
    time.sleep(0.03)
