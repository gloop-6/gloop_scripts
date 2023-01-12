#by gloop#5445
import os,time,colorsys,msvcrt,random
os.system("title Snake - Rewritten")
w,h = 60,30
food_spawn_count = 20
snake_initial_pos = (w//2,h//2)
ansi_escape = "\x1b["
reset = f"{ansi_escape}0m"
fg_escape = f"{ansi_escape}38;5;"
food_shine_chance = 0.01
snake_colors = ((0.2,0.4,0.2),(0.4,0.6,0.4))
food_colors = ((0.6,0.2,0.2),(0.8,0.2,0.2),(1,0.4,0.4),(1,0.6,0.2),(1,0.4,0.4),(0.8,0.2,0.2),(0.6,0.2,0.2))
death_anim_colors = ((0.8,0.2,0.2),(0.6,0.2,0.2),(0.4,0.2,0.2),(0.2,0.2,0.2),(0,0,0))
level_colors = [(0.4,0.4,0.2),(0.6,0.4,0.2),(0.4,0.2,0.2),(0.4,0.6,0.2),(0.2,0.4,0.6),(0.4,0.4,0.2)]
for i in range(1,100,3):

    level_colors.append([random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)])
snake_death_chars = "█▓▒░. "
food_death_chars = "●*•.  "
movement_keys = {"w":(0,-1),"s":(0,1),"a":(-1,0),"d":(1,0)}
food_char = "●"
snake_char = "█"
death_text_pos = (w//2,h//2)
level = 0
food = {}
snake_parts = [snake_initial_pos]
def spawn_food():
    i=0
    t=0
    while i<food_spawn_count: 
        if t>=1000:
            break
        r = random_pos((0,w),(0,h-1))
        if r not in food and r not in snake_parts:
            food[r]=0
            i+=1
        t+=1
def init():
    global food
    global snake_dir
    global step
    global snake_parts
    global food_eaten
    global level
    level = 0
    food = {}
    food_eaten = 0
    snake_dir = (0,0)
    step = 0
    snake_parts = [snake_initial_pos]
    for i in range(3):
        snake_parts.append((snake_parts[0][0],snake_parts[0][1]+i))
    spawn_food()
    os.system(f"mode con: cols={w+2} lines={h+6}")
def clamp(minimum,n,maximum):
    return max(minimum,min(maximum,n))

def random_pos(x_range,y_range):
    min_x,max_x = x_range
    min_y,max_y = y_range
    return (random.randint(min_x,max_x),random.randint(min_y,max_y))

def col_from_rgb(c):
    r,g,b = c
    r = int(5*r)
    g = int(5*g)
    b = int(5*b)
    return f"{fg_escape}{16 + (36 * r) + (6 * g) + b}m"

def col_from_hsv(c):
    h,s,v = c
    r,g,b = colorsys.hsv_to_rgb(h,s,v)
    r = int(5*r)
    g = int(5*g)
    b = int(5*b)
    return f"{fg_escape}{16 + (36 * r) + (6 * g) + b}m"

def update_snake(snake,move_dir):
    global food_eaten

    mX,mY = move_dir
    head = (snake[0][0]+mX,snake[0][1]+mY)
    
    if head in food:
        del food[head]
        food_eaten+=1
        snake.append(snake[-1])

    if snake_dir != (0,0):
        if head in snake[1:]:
            return False
        for i in range(len(snake_parts)-1,0,-1):
            snake[i]=snake[i-1]
        snake[0]=head
    if clamp(0,head[0],w)!=head[0] or clamp(0,head[1],h-1)!=head[1]:
        return False
    return True

spawn_food()

print(f"{ansi_escape}?25l")

def draw_box(s,w,color):
    bar = f"{col_from_rgb(color)}║{reset}"
    lines = s.split("\n")
    output = []

    for i in lines:
        output+=[bar+i+bar]

    output = "\n".join(output)
    output = f"{col_from_rgb(color)}╔" + "═"*w + f"╗\n{reset}" + output 
    output += f"\n{col_from_rgb(color)}╚" + "═"*w + f"╝\n{reset}"
    return output

def render():
    s = ""
    for y in range(h):
        if y!=0:
            s+="\n"
        for x in range(w):
            ch = " "
            if (x,y) in food:
                col = food_colors[food[(x,y)]]
                ch = f"{col_from_rgb(col)}{food_char}{ansi_escape}0m"

            if (x,y) in snake_parts:
                if (x,y)==snake_parts[0]:
                    ch = f"{col_from_rgb(snake_colors[1])}{snake_char}{reset}"
                else:
                    ch = f"{col_from_rgb(snake_colors[0])}{snake_char}{reset}"
            s+=ch
    print(f"{ansi_escape}0;0H")
    print(((w//2)-10)*" "+f"Level: {level}"+(" "*5)+f"Score: {food_eaten}")
    print(draw_box(s,w,level_colors[level]))
    #print(s)

init()

def death_anim(alt_death = False):
    os.system("cls")
    for idx,i in enumerate(death_anim_colors):
        s=f"{ansi_escape}0;0H"
        for y in range(h):
            s+="\n"
            for x in range(w):
                ch = " "
                if (x,y) in food:
                    ch = f"{fg_escape}{col_from_rgb(i)}{food_death_chars[idx]}{reset}"
                if (x,y) in snake_parts:
                    ch = f"{fg_escape}{col_from_rgb(i)}{snake_death_chars[idx]}{reset}"


                s+=ch

        print(s)
        time.sleep(0.1)
    os.system("cls")
    if alt_death == True:
        print("\n"*(h//2)+" "*((w//2)-10),f"{col_from_rgb((1,0,0))}lol")
        print(" "*((w//2)-10)+f" Skill: issue")

    else:
        print("\n"*(h//2)+" "*((w//2)-10),f"{col_from_rgb((1,0,0))}GAME OVER")
        print(" "*((w//2)-10)+f" Score: {food_eaten} Level: {level}")

def main():
    global level
    global snake_dir
    global snake_parts
    global step
    alt_death = False
    init()
    while True:
        if msvcrt.kbhit():
            key = str(msvcrt.getch())[2:-1]
            if key in movement_keys:

                dir = movement_keys[key]
                if snake_dir == (0,0) and key == "s":
                    alt_death = True
                if (dir[0]*-1,dir[1]*-1) != snake_dir:
                    snake_dir = dir
            if key=="r":
                os.system(f"mode con: cols={w+2} lines={h+6}")
                break
                
            if key=="\\x1b":
                os.system("cls")
                print("\n"*(h//2)+" "*((w//2)-1)+f"{col_from_rgb((0,0.5,1))}Paused{reset}")
                os.system("pause >nul & cls")
                os.system(f"mode con: cols={w+2} lines={h+6}")
                print(f"{ansi_escape}?25l")

        a=update_snake(snake_parts,snake_dir)
        if a == False:
            death_anim(alt_death)
            os.system("pause >nul")
            break

        if len(food)==0:
            spawn_food()
            level+=1

        for i in food:
            if random.uniform(0,1)<food_shine_chance:
                food[i]=len(food_colors)-1
            if food[i]!=0 and step%2==0:
                food[i]-=1

        render()
        step+=1
        time.sleep(0.1)
    main()
main()
