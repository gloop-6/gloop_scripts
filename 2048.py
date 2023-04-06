# by gloop#5445
import os, time, msvcrt, random, colorsys

os.system("")
print("\x1b[?25l\x1b[0;0H")
tile_size = 5
tile_width = 11
w, h = 54, 28
os.system(f"cls&title 2048-Python&mode con: cols={w} lines={h}")
movement_directions = (0, -1), (-1, 0), (0, 1), (1, 0)
movement_keys = ["w", "a", "s", "d"]
background_color = "bbada2"
empty_tile_color = "cdc1b4"
tile_colors = [
    "eee4da",
    "ede0c0",
    "f2b179",
    "f59563",
    "f67c60",
    "f65e3b",
    "edcf73",
    "edcc62",
    "edc850",
    "edc53f",
    "edc22d",
]
text_colors = ["776e65", "776e65", "f9f6f2"]


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


def color_from_hexcode(h, mode="fg"):
    return color_from_rgb(color_array=hex_to_rgb(h), mode=mode)


board_size = range(0, 4)


def clamp(minimum, n, maximum):
    return max(minimum, min(maximum, n))


def add_pos(a, b):
    return (a[0] + b[0], a[1] + b[1])


def get_key():
    if msvcrt.kbhit():
        return str(msvcrt.getch())[2:-1]


def random_pos(x_range, y_range):
    min_x, max_x = x_range
    min_y, max_y = y_range
    return (random.randint(min_x, max_x), random.randint(min_y, max_y))


class tile:
    def __init__(self, pos, value, moving=False, update_delay=0):
        self.pos = pos
        self.value = value
        self.update_delay = update_delay

    def compress(self, dir):
        tile_positions = get_tile_positions()
        if self.update_delay == 0:
            new_pos = add_pos(self.pos, movement_directions[dir])
            if new_pos not in tile_positions:
                if 0 <= new_pos[0] < 4 and 0 <= new_pos[1] < 4:
                    self.pos = new_pos

    def merge(self, dir):
        global game_running
        tile_positions = get_tile_positions()
        if self.update_delay == 0:
            new_pos = add_pos(self.pos, movement_directions[dir])
            if new_pos in tile_positions:
                other = tile_positions[new_pos]
                if other.value == self.value:
                    tiles.pop(tiles.index(other))
                    self.value += 1

        if self.value == 11:
            win_screen()
            game_running = False
            return


def get_empty_tiles():
    global game_running, grace_moves
    tile_positions = get_tile_positions()
    empty_tiles = []
    for y in range(4):
        for x in range(4):
            if (x, y) not in tile_positions:
                empty_tiles.append((x, y))
    if empty_tiles:
        grace_moves = 3
        return empty_tiles
    else:
        grace_moves -= 1
    if grace_moves == 0:
        game_over_screen()
        game_running = False
        return


def get_tile_attrib(attrib):
    return {getattr(i, attrib): i for i in tiles}


def get_tile_attrib_reversed(attrib):
    return {i: getattr(i, attrib) for i in tiles}


def get_tile_positions():
    return get_tile_attrib("pos")


def spawn_tile(update_delay=1):
    possible_spawn_locations = get_empty_tiles()
    if possible_spawn_locations:
        spawn_location = random.choice(possible_spawn_locations)
        tile_type = [1, 2][random.randint(1, 10) == 10]
        tiles.append(tile(spawn_location, tile_type, update_delay))


def compress_tiles(dir):
    tile_positions = get_tile_positions()
    y_range = range(4)
    x_range = range(4)
    if dir == 2:
        y_range = range(3, -1, -1)
    if dir == 3:
        x_range = range(3, -1, -1)
    for _ in range(3):
        for y in y_range:
            for x in x_range:
                if (x, y) in tile_positions:
                    tile = tile_positions[(x, y)]
                    tile.compress(dir)
        render()
        time.sleep(0.02)


def merge_tiles(dir):
    tile_positions = get_tile_positions()
    y_range = range(4)
    x_range = range(4)
    if dir == 2:
        y_range = range(3, -1, -1)
    if dir == 3:
        x_range = range(3, -1, -1)

    for y in y_range:
        for x in x_range:
            if (x, y) in tile_positions:
                tile = tile_positions[(x, y)]
                tile.merge(dir)


tiles = []
bg_color = color_from_hexcode(background_color, mode="bg")
empty_tile_color = color_from_hexcode(empty_tile_color, mode="bg")


def render():
    s = ""
    grid_bar = bg_color + " " * (10 + (tile_width * 4)) + "\n"
    for y in range((4 * tile_size)):
        if y != 0:
            s += "\x1b[0m" + bg_color + "  \n"
        if (y % tile_size) == 0:
            s += grid_bar
        for x in range(4):
            ch = (
                "\x1b[0m"
                + bg_color
                + "  "
                + empty_tile_color
                + (" " * tile_width)
                + bg_color
            )
            for i in tiles:
                tile_value = str(2**i.value).center(tile_width, " ")
                tile_color = color_from_hexcode(tile_colors[i.value - 1], mode="bg")
                tile_bar = "  " + tile_color + (" " * tile_width) + bg_color
                if i.pos == (x, y // tile_size):
                    ch = tile_bar
                    if y % tile_size == 2:
                        text_color = color_from_hexcode(
                            text_colors[min(i.value, 3) - 1], mode="fg"
                        )
                        ch = f"  {tile_color}{text_color}{tile_value}{bg_color}"
            s += ch
    s += bg_color + "  \n" + " " * (10 + (tile_width * 4))
    print(f"\x1b[0;0H\n{s}\x1b[0m\x1b[?25l")


def game_over_screen():
    os.system("cls")
    print(
        (("\n") * (h // 2))
        + (" " * (w // 2 - 5))
        + color_from_hexcode("ff3333")
        + "Game Over"
    )
    os.system("pause >nul")


def win_screen():
    os.system("cls")
    print(
        (("\n") * (h // 2))
        + (" " * (w // 2 - 5))
        + color_from_hexcode("3355ff")
        + "You Win!"
    )
    os.system("pause >nul")


render()
get_empty_tiles()
grace_moves = 3
game_running = True


def main():
    global game_running, tiles, grace_moves
    game_running = True
    last_direction_moved = None
    tiles = []
    for _ in range(2):
        spawn_tile()
    os.system("cls")
    render()
    while True:
        if not game_running:
            return
        k = get_key()
        if k in movement_keys:
            if k != last_direction_moved:
                spawn_tile(4)
                last_direction_moved = k
            mov_dir = movement_keys.index(k)
            compress_tiles(mov_dir)
            merge_tiles(mov_dir)
            compress_tiles(mov_dir)
            render()


while True:
    main()
