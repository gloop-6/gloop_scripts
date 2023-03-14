# by gloop#5445
import os, time, colorsys, msvcrt, random
from collections import deque

os.system("title Snake 2.1")
w, h = 60, 30
food_spawn_count = 20
snake_initial_pos = (w // 2, h // 2)
ansi_escape = "\x1b["
reset = f"{ansi_escape}0m"
fg_escape = f"{ansi_escape}38;2;"
bg_escape = f"{ansi_escape}48;2;"
food_shine_chance = 0.01
snake_colors = ["336633", "669966"]
food_colors = ["993333", "cc3333", "ff6666", "ff9933", "ff6666", "cc3333", "993333"]
death_anim_colors = ["cc3333", "993333", "663333", "333333", "000000"]
level_colors = [
    [102, 102, 102],
    [153, 150, 102],
    [102, 99, 51],
    [102, 105, 153],
    [51, 54, 102],
    [102, 102, 102],
]
menu_colors = ["987533", "ffe68c"]
snake_color_list = [
    ["336633", "669966"],
    ["789a25", "9ec246"],
    ["9a8e25", "c2c046"],
    ["996e29", "d1913c"],
    ["994e29", "cb623c"],
    ["992929", "cb3c3c"],
    ["992976", "d1428e"],
    ["792999", "bc3ccb"],
]
snake_color_list += [
    ["5e2999", "6f3ccb"],
    ["3c3aa9", "505bdc"],
    ["3a64a9", "5098dc"],
    ["3a96a9", "50d3dc"],
    ["47b4a1", "6af3c0"],
    ["bebebe", "e3e3e3"],
    ["979797", "bebebe"],
    ["5e5e5e", "979797"],
]
snake_color_list += [
    ["464646", "5e5e5e"],
    ["68593d", "8c7750"],
    ["d670b3", "ffa9e4"],
    ["d06c69", "ffa2b2"],
    ["dca964", "ffc89a"],
    ["cebe73", "fff8a8"],
    ["bace73", "ecffa8"],
    ["8de2ca", "b6ffeb"],
]
snake_color_list += [
    ["8dd6e2", "b6f6ff"],
    ["8db8e2", "b6dfff"],
    ["8d97e2", "b6c0ff"],
    ["be8de2", "d8b6ff"],
    ["99836f", "c5ad98"],
    ["108a89", "3da7a5"],
    ["495a67", "687f90"],
    ["5b6a33", "899653"],
]
snake_color_list = deque(snake_color_list)
difficulty_colors = ["336633", "789a25", "9a8e25", "996e29", "992929"]
for i in range(1, 100):
    level_colors.append(
        [random.randint(10, 255), random.randint(10, 255), random.randint(10, 255)]
    )
snake_death_chars = "█▓▒░. "
food_death_chars = "●*•.  "
movement_keys = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
food_char = "●"
snake_char = "█"
death_text_pos = (w // 2, h // 2)
level = 0
food = {}
snake_parts = [snake_initial_pos]
difficulty_options = [0.12, 0.08, 0.06, 0.04, 0.02]
difficulty_text_options = ["Super Easy", "Easy", "Medium", "Hard", "Impossible"]
difficulty = 1


def spawn_food():
    i = 0
    t = 0
    while i < food_spawn_count:
        if t >= 1000:
            break
        r = random_pos((0, w), (0, h - 1))
        if r not in food and r not in snake_parts:
            food[r] = 0
            i += 1
        t += 1


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
    snake_dir = (0, 0)
    step = 0
    snake_parts = [snake_initial_pos]
    for i in range(3):
        snake_parts.append((snake_parts[0][0], snake_parts[0][1] + i))
    spawn_food()
    os.system(f"mode con: cols={w+2} lines={h+6}")


def clamp(minimum, n, maximum):
    return max(minimum, min(maximum, n))


def random_pos(x_range, y_range):
    min_x, max_x = x_range
    min_y, max_y = y_range
    return (random.randint(min_x, max_x), random.randint(min_y, max_y))


def color_from_rgb(r=0, g=0, b=0, mode="fg", color_array=None):
    if color_array is not None:
        r, g, b = color_array
    if mode == "fg":
        mode = 38
    if mode == "bg":
        mode = 48
    return f"\x1b[{mode};2;{r};{g};{b}m"


def color_from_hsv(h=0, s=0, v=0, mode="fg", color_array=None):
    if color_array is not None:
        h, s, v = color_array
    r, g, b = [int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v)]
    return color_from_rgb(r, g, b, mode)


def hex_to_rgb(h):
    return [int(h[i : i + 2], 16) for i in range(0, 6, 2)]


def color_from_hexcode(h):
    return color_from_rgb(color_array=hex_to_rgb(h))


def adjust_color_brightness(color, level):
    return [clamp(0, int(i) + int(level), 255) for i in color]


def col_from_hsv(c):
    h, s, v = c
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r = int(5 * r)
    g = int(5 * g)
    b = int(5 * b)
    return f"{fg_escape}{16 + (36 * r) + (6 * g) + b}m"


def update_snake(snake, move_dir):
    global food_eaten

    mX, mY = move_dir
    head = (snake[0][0] + mX, snake[0][1] + mY)

    if head in food:
        del food[head]
        food_eaten += 1
        snake.append(snake[-1])

    if snake_dir != (0, 0):
        if head in snake[1:]:
            return False
        for i in range(len(snake_parts) - 1, 0, -1):
            snake[i] = snake[i - 1]
        snake[0] = head
    if clamp(0, head[0], w - 1) != head[0] or clamp(0, head[1], h - 1) != head[1]:
        return False
    return True


def draw_box(s, w, color):
    bar = f"{color_from_rgb(color_array=color)}║{reset}"
    lines = s.split("\n")
    output = []

    for i in lines:
        output += [bar + i + bar]

    output = "\n".join(output)
    output = f"{color_from_rgb(color_array=color)}╔" + "═" * w + f"╗\n{reset}" + output
    output += f"\n{color_from_rgb(color_array=color)}╚" + "═" * w + f"╝\n{reset}"
    return output


def render():
    s = ""
    for y in range(h):
        if y != 0:
            s += "\n"
        for x in range(w):
            ch = " "
            if (x, y) in food:
                col = food_colors[food[(x, y)]]
                ch = f"{color_from_hexcode(col)}{food_char}{ansi_escape}0m"

            if (x, y) in snake_parts:
                if (x, y) == snake_parts[0]:

                    ch = f"{color_from_hexcode(snake_colors[1])}{snake_char}{reset}"
                else:
                    ch = f"{color_from_hexcode(snake_colors[0])}{snake_char}{reset}"
            s += ch
    print(f"{ansi_escape}0;0H")
    print(
        ((w // 2) - 10) * " " + f"Level: {level}" + (" " * 5) + f"Score: {food_eaten}"
    )
    print(draw_box(s, w, level_colors[level]))
    # print(s)


def get_key():
    if msvcrt.kbhit():
        return str(msvcrt.getch())[2:-1]


def rainbow_text(string, t):
    return "".join(
        [
            color_from_hsv(idx / len(string) + t, 0.6, 1) + i
            for idx, i in enumerate(string)
        ]
    )


def death_anim(alt_death=False):
    os.system("cls")
    for idx, i in enumerate(death_anim_colors):
        s = f"{ansi_escape}0;0H"
        for y in range(h):
            s += "\n"
            for x in range(w):
                ch = " "
                if (x, y) in food:
                    ch = f"{fg_escape}{color_from_hexcode(i)}{food_death_chars[idx]}{reset}"
                if (x, y) in snake_parts:
                    ch = f"{fg_escape}{color_from_hexcode(i)}{snake_death_chars[idx]}{reset}"
                s += ch
        print(s)
        time.sleep(0.1)
    os.system("cls")
    if alt_death == True:
        print(
            "\n" * (h // 2) + " " * ((w // 2) - 10),
            color_from_hexcode("ff1100") + "lol",
        )
        print(" " * ((w // 2) - 10) + f" Skill: issue")
    else:
        print(
            "\n" * (h // 2) + " " * ((w // 2) - 10),
            color_from_hexcode("ff1100") + "GAME OVER",
        )
        print(" " * ((w // 2) - 10) + f" Score: {food_eaten} Level: {level}")


def flash_text(string, t, base_color, flash_colors):
    string = (len(flash_colors) * "¶") + string + (len(flash_colors) * "¶")
    s = ""
    for idx, i in enumerate(string):
        front = t % len(string * 3)
        back = t % len(string * 3) + len(flash_colors) - 1
        if i != "¶":
            if front <= idx <= back:
                s += color_from_hexcode(
                    flash_colors[(idx - front + 2) % len(flash_colors) - 1]
                )
            else:
                s += color_from_hexcode(base_color)
            s += i
    return s


def menu(mode):
    print(f"{ansi_escape}0;0H")
    os.system("cls")
    os.system(f"mode con: cols={w+2} lines={h+6}")
    print(f"{ansi_escape}?25l")
    if mode == "main_menu":
        flash = 0
        selected_option = 0
        options = ["Start Game", "Options", "Quit"]
        render_menu(selected_option, options, mode)
        while True:
            if random.randint(1, 40) == 1 and flash == 0:
                flash = 15
            key = get_key()
            if key == "w":
                selected_option -= 1
            if key == "s":
                selected_option += 1
            selected_option %= 3
            if key == "\\r":
                if selected_option == 0:
                    return
                elif selected_option == 1:
                    menu("options_menu")

                elif selected_option == 2:
                    exit()
            if flash > 0:
                flash -= 1
            render_menu(selected_option, options, mode, args=[flash])
            time.sleep(0.1)

    if mode == "pause_menu":
        selected_option = 0
        options = ["Exit Menu", "Options", "Quit"]
        render_menu(selected_option, options, mode)
        while True:
            key = get_key()
            if key == "w":
                selected_option -= 1
            if key == "s":
                selected_option += 1
            selected_option %= 3
            if key == "\\r":
                if selected_option == 0:
                    os.system("cls")
                    return
                elif selected_option == 1:
                    menu("options_menu")

                elif selected_option == 2:
                    exit()
                return
            if key == "\\x1b":
                os.system("cls")
                return
            render_menu(selected_option, options, mode)

    elif mode == "options_menu":
        selected_option = 0

        options = ["Pause Menu", "Color", "Difficulty"]
        render_menu(selected_option, options, mode)
        while True:
            key = get_key()
            if key == "w":
                selected_option -= 1
            if key == "s":
                selected_option += 1
            selected_option %= 3
            if key == "\\r":
                if selected_option == 0:
                    menu("pause_menu")
                    return
                elif selected_option == 1:
                    menu("color_palette")
                elif selected_option == 2:
                    menu("difficulty_selector")
            if key == "\\x1b":
                os.system("cls")
                return
            render_menu(selected_option, options, mode)

    elif mode == "color_palette":
        selected_color = 0
        global snake_colors
        render_menu(selected_color, list(snake_color_list)[1:25], mode)
        while True:
            key = get_key()
            if key is not None:
                if key == "a":
                    snake_color_list.rotate(-1)
                if key == "d":
                    snake_color_list.rotate(1)
                selected_color %= len(snake_color_list)
                if key == "\\r":
                    snake_colors = snake_color_list[13]
                if key == "\\x1b":
                    os.system("cls")
                    return
                render_menu(selected_color, list(snake_color_list)[1:25], mode)

    elif mode == "difficulty_selector":
        global difficulty
        selected_difficulty = 1
        render_menu(selected_difficulty, difficulty_colors, mode)
        while True:
            key = get_key()
            if key is not None:
                if key == "a":
                    selected_difficulty -= 1
                    os.system("cls")
                if key == "d":
                    selected_difficulty += 1
                    os.system("cls")
                selected_difficulty = clamp(0, selected_difficulty, 4)
                if key == "\\r":
                    difficulty = selected_difficulty
                    difficulty_index = selected_difficulty
                    os.system("cls")
                if key == "\\x1b":
                    os.system("cls")
                    return
                render_menu(selected_difficulty, difficulty_colors, mode)


def render_menu(n, values, mode, args=[]):
    s = ""
    if mode == "main_menu":
        options = values
        print(f"{ansi_escape}0;0H")
        if args:
            text = flash_text(
                "Snake",
                args[0] - 1,
                "65bd00",
                ["92eb00", "affa2d", "d7ffa2", "ffffff", "d7ffa2", "affa2d", "92eb00"],
            )
        else:
            text = color_from_rgb(color_array=[101, 189, 0]) + "Snake"
        text = "\x1b[2m" + text
        print("\n" * (h // 2) + " " * ((w // 2) - 4) + text + "\n")

        for idx, i in enumerate(options):
            if idx == n:
                arrow = "\x1b[0m► "
            else:
                arrow = "  "
            print(
                (w // 2 - 8) * " "
                + arrow
                + f"{color_from_hexcode(menu_colors[idx==n])}{i}"
            )

        print(
            "\n" * (10)
            + " " * ((w // 2) - 8)
            + color_from_hexcode("d41360")
            + f"by gloop#5445{reset}\n"
        )

    elif mode == "color_palette":
        colors = values
        global snake_colors
        print(f"{ansi_escape}0;0H")
        print(
            "\n" * (h // 2)
            + " " * ((w // 2) - 5)
            + color_from_hexcode("d41360")
            + f"Color Selector{reset}\n"
        )
        print(((w // 2) + 2) * " ", end="")
        print(
            color_from_hexcode(snake_colors[0])
            + "▼\x1b[0m"
            + "\n"
            + " " * ((w // 2) - 10),
            end="",
        )
        s += (
            "".join(color_from_hexcode(i[1]) + "█" for i in colors)
            + "\n"
            + " " * ((w // 2) - 10)
        )
        s += "".join(color_from_hexcode(i[0]) + "█" for i in colors)
        print(s)
    elif mode == "pause_menu":
        options = values

        print(f"{ansi_escape}0;0H")
        print(
            "\n" * (h // 2)
            + " " * ((w // 2) - 4)
            + color_from_hexcode("0088ff")
            + f"Paused{reset}\n"
        )
        for idx, i in enumerate(options):
            if idx == n:
                arrow = "\x1b[0m► "
            else:
                arrow = "  "
            print(
                (w // 2 - 8) * " "
                + arrow
                + f"{color_from_hexcode(menu_colors[idx==n])}{i}"
            )

    elif mode == "options_menu":
        options = values
        print(f"{ansi_escape}0;0H")
        print(
            "\n" * (h // 2)
            + " " * ((w // 2) - 4)
            + color_from_hexcode("0088ff")
            + f"Options{reset}\n"
        )
        for idx, i in enumerate(options):
            if idx == n:
                arrow = "\x1b[0m► "
            else:
                arrow = "  "
            print(
                (w // 2 - 8) * " "
                + arrow
                + f"{color_from_hexcode(menu_colors[idx==n])}{i}"
            )

    elif mode == "difficulty_selector":
        global difficulty_index
        s = ""
        options = values
        print(f"{ansi_escape}0;0H")
        print(
            "\n" * (h // 2)
            + " " * ((w // 2) - 10)
            + color_from_hexcode("0088ff")
            + f"Difficulty Selection{reset}\n"
        )
        difficulty_text = difficulty_text_options[difficulty]
        print(
            (" " * ((w // 2) - len(difficulty_text) // 2))
            + color_from_hexcode(difficulty_colors[difficulty])
            + difficulty_text,
            "\n",
        )
        print(
            (" " * (-7 + (w // 2) + n * 3))
            + color_from_hexcode(difficulty_colors[difficulty])
            + f"▼{reset}"
        )
        print((" " * ((w // 2) - 8)), end="")
        for idx, i in enumerate(options):
            color = hex_to_rgb(difficulty_colors[idx])
            selected = idx == n
            color = adjust_color_brightness(color, selected * 30)
            color = color_from_rgb(color_array=color)
            s += f"{color}███"
        print(s)


spawn_food()
print(f"{ansi_escape}?25l")
init()
menu("main_menu")


def main():
    global level
    global snake_dir
    global snake_parts
    global step
    alt_death = False
    init()
    while True:
        key = get_key()
        if key is not None:
            if key in movement_keys:
                dir = movement_keys[key]
                if snake_dir == (0, 0) and key == "s":
                    alt_death = True
                if (dir[0] * -1, dir[1] * -1) != snake_dir:
                    snake_dir = dir
            if key == "r":
                os.system(f"mode con: cols={w+2} lines={h+6}")
                break
            if key == "\\x1b":
                menu("pause_menu")
        a = update_snake(snake_parts, snake_dir)
        if a == False:
            death_anim(alt_death)
            os.system("pause >nul")
            break
        if len(food) == 0:
            spawn_food()
            level += 1
        for i in food:
            if random.uniform(0, 1) < food_shine_chance:
                food[i] = len(food_colors) - 1
            if food[i] != 0 and step % 2 == 0:
                food[i] -= 1
        render()
        step += 1
        time.sleep(difficulty_options[difficulty])
    main()


main()
