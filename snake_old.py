#sorry about the code, this is an old mess from when i started writing python

#CONFIG START
foodSpawnCount = 10
w,h=50,30
rainbowMode = False
loop = True
sColor = (1,0,0.4)
#CONFIG END

def main():
    t = 0
    def clamp(minimum,n,maximum):
        return max(minimum,min(maximum,n))
    try:
        gameSpeed = float(input("gamespeed: "))
    except ValueError:
        gameSpeed = 0.1
    gameSpeed = clamp(0,abs(gameSpeed),0.3)
    gameRunning = 1
    global foodSpawnCount
    foodChar,snakeChars,bgChar = "●","██"," "
    import os,msvcrt,time,random,colorsys
    global w 
    global h
    area = w * h
    global mDir
    
    mDir = [(0,-1),(0,1),(-1,0),(1,0)][random.randint(0,3)]
    hPos = (random.randint(1,w-1),random.randint(1,h-1))
    
    snake = [hPos]
    snake.append((hPos[0]+mDir[0],hPos[1]+mDir[1]))
    snake.append((hPos[0]+mDir[0]+mDir[0],hPos[1]+mDir[1]+mDir[1]))
    global score
    global foodCount
    foodCount = foodSpawnCount
    global rainbowMode
    rainbowColors = [31,91,33,93,32,92,36,96,34,94,35,95]
    score = 0
    board = {}
    os.system(f"mode con:cols={w+4} lines={h+5}")
    e = "["
    print("\x1b[?25l")
    os.system("title Snake")
    os.system("color ")
    for y in range(h):
        for x in range(w):
            board[(x,y)]=bgChar
    mvKeys = {"w":(0,-1),"s":(0,1),"a":(-1,0),"d":(1,0)}
    mvOpp = {"w":"s","s":"w","a":"d","d":"a"}
    menucolor = 90
    def colRGB(r,g,b):
        r = int(r*5)
        g = int(g*5)
        b = int(b*5)
        return 16 + (36 * r) + (6 * g) + b
    def colHSV(h,s,v):
        rgb = colorsys.hsv_to_rgb(h,s,v)
        r = int(rgb[0]*5)
        g = int(rgb[1]*5)
        b = int(rgb[2]*5)
        return 16 + (36 * r) + (6 * g) + b
    def snakeColor(rainbowMode,offset=0):
        if rainbowMode == True:
            return colHSV((t/100)+(offset/3),1,1)
        else:
            return colRGB(sColor[0],sColor[1],sColor[2])

    charColors = {foodChar:f"{e}31m"}


    scoreColor = [33,37]
    def addFood():
        while True:
            x,y=(random.randint(1,w-1),random.randint(1,h-1))
            if board[(x,y)] not in snakeChars:
                board[(x,y)]=foodChar
                break
    def updateSnake():
        global foodCount
        global score
        oX,oY = (snake[0][0]+mDir[0])%w,(snake[0][1]+mDir[1])%h
        dX,dY = (snake[0][0]+mDir[0]),(snake[0][1]+mDir[1])
        if loop == False and (dX>=w or dX<0 or dY>=h or dY<0):
            gameOver()
        if board[(oX,oY)] in snakeChars:
            gameOver()
        if board[(oX,oY)]==foodChar:
            score = score + 1
            snake.append(snake[0])
            for i in range(len(snake)-1,0,-1):
                snake[i]=snake[i-1]
            snake[0]=(oX,oY)
            if foodCount <= 0:
                for i in range(foodSpawnCount):
                    addFood()
                foodCount = foodSpawnCount  
            else:
                foodCount -= 1
        else:       
            for i in range(len(snake)-1,0,-1):
                snake[i]=snake[i-1]
            snake[0]=(oX,oY)
    def gameOver():
        global gameRunning
        gameRunning = 0
        os.system("cls")
        print(f"{e}31m    GAME OVER{e}0m")
        main()
    def updateBoard():
        updateSnake()
        for y in range(h):
            for x in range(w):
                if board[(x,y)] in snakeChars:
                    board[(x,y)]=bgChar
        for i in range(len(snake)):
            if i == 0:
                board[snake[i]]=snakeChars[0]
            else:
                board[snake[i]]=snakeChars[1]
        drawBoard()
    for i in range(foodSpawnCount):
        addFood()
    def drawBoard():
        s = ""
        for y in range(h):
            if y !=0:
                s = f"{s}\n"
            for x in range(w):
                char = board[(x,y)]
                if char in charColors:
                    s = f"{s}{charColors[char]}{char}{e}{menucolor}m"
                else:
                    s = f"{s}{char}"
        s = s.replace("\n","║\n ║")
        outText = f"\u001b[0;0H{e}{menucolor}m{chr(32)*6}{e}{scoreColor[0]}mSCORE: {e}{scoreColor[1]}m{score}{e}0m{e}{menucolor}m\n "
        outText = f"{outText}╔{chr(9552)*w}╗\n ║{s}║\n ╚{chr(9552)*w}╝"
        print(outText)
        print(foodCount)
        if gameSpeed != 0:
            time.sleep(gameSpeed)
    os.system("cls")
    drawBoard()
    while gameRunning == 1:     
        t += 1
        if rainbowMode == True:
            charColors = {snakeChars[0]:f"[38;5;{snakeColor(True)}m",snakeChars[1]:f"[38;5;{snakeColor(True,1)}m",foodChar:f"{e}31m"}
        else:
            charColors = {snakeChars[0]:f"[38;5;{snakeColor(False)}m",snakeChars[1]:f"[38;5;{snakeColor(False,1)}m",foodChar:f"{e}31m"}            
        updateBoard()
        if foodCount == 0:
            for i in range(foodSpawnCount):
                addFood()
            foodCount = foodSpawnCount
        if msvcrt.kbhit():
            ch = str(msvcrt.getch())[1::].replace("'","")
            if ch in mvKeys:
                if (mvKeys[ch][0]*-1,mvKeys[ch][1]*-1) != mDir:
                    mDir = mvKeys[ch]
                    s = ""
main()