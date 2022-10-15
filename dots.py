import math,random,time,os
w,h = 30,30
dotsMax = 50
velRange = 0.01
forceDistanceRepel = 4
forceDistanceAttract = 10
forceAmtRepel = -0.012
forceAmtAttract = 0.004
os.system("title dots")
os.system("color ")
os.system(f"mode con:cols={w+1} lines={h+1}")
print('\033[?25l', end="")
def clamp(a,n,b):
    return min(b,max(a,(n)))
class dot:
    def __init__(dot,pos,vel):
        dot.pos = pos
        dot.vel = vel
e = "["
dotsList = []
for i in range(dotsMax):
    dotsList.append(dot([0,0],[0,0]))
    dotsList[i].pos = [random.randint(1,w-1),random.randint(1,h-1)]
    dotsList[i].vel = [random.uniform(-velRange,velRange),random.uniform(-velRange,velRange)]
def colTrig(h,offset=(math.pi/4)):
    n = h * math.pi
    r = int(5*abs(math.sin(n-offset)))
    g = int(5*abs(math.sin(n)))
    b = int(5*abs(math.sin(n+offset)))
    return 16 + (36 * r) + (6 * g) + b
def getDotDist(dot1,dot2):
    p1,p2 = dot1.pos,dot2.pos
    d = ((p2[0]-p1[0])**2)+((p2[1]-p1[1])**2)
    if d==0: return 0
    else: return d**0.5
def getDotAngle(dot1,dot2):
    p1,p2 = dot1.pos,dot2.pos 
    ang = [p2[0]-p1[0],p2[1]-p1[1]]
    return math.atan2(ang[1],ang[0])
def getForce(dot1,dot2,amt):
    
    theta = getDotAngle(dot1,dot2)
    ForceX = math.cos(theta)*amt
    ForceY = math.sin(theta)*amt
    return ForceX,ForceY
def updateDot(dot):
    p,v = dot.pos,dot.vel
    p = [clamp(0,p[0],w),clamp(0,p[1],h)]
    for i in dotsList:
        if i!=dot and getDotDist(dot,i) < forceDistanceAttract:
            f = getForce(dot,i,forceAmtAttract)
            v = [v[0]+f[0],v[1]+f[1]]
        p = [clamp(1,p[0]+v[0],w-1),clamp(1,p[1]+v[1],h-1)]
        if i!=dot and getDotDist(dot,i) < forceDistanceRepel:
            f = getForce(dot,i,forceAmtRepel)
            v = [v[0]+f[0],v[1]+f[1]]
        p = [clamp(1,p[0]+v[0],w-1),clamp(1,p[1]+v[1],h-1)]
    dot.vel = [clamp(-2,v[0]*0.8,2),clamp(-2,v[1]*0.8,2)]
    dot.pos = p
def render(t):
    s = ""
    for y in range(h):
        if y!=0:
            s = f"{s}\n"
        for x in range(w):
            ch = " "
            for i in dotsList:
                if [x,y] == [int(i.pos[0]),int(i.pos[1])]:
                    color = colTrig(t+(i.vel[0]+i.vel[1])*2)
                    ch = f"[38;5;{color}m•{e}0m"

            s = f"{s}{ch}"
    print(f"\u001b[0;0H{s}")
t=0
while True:
    t += 0.01
    for i in dotsList:
        updateDot(i)
    render(t)
