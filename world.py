import curses
from curses import wrapper
import numpy as np
from random import choices, choice, seed, randint
from dataclasses import dataclass
from typing import Self
from util import PlayerDied

#tiles = range(ord('\u2591'), ord('\u2593'))
tiles = ['\u2591', '\u2592', '\u2593']
fueltiles = {"H": 4, "X": 1, "C": 2}

class InputError(Exception):
    def __init__(self, errorValue):
        self.errorValue = errorValue
    def __str__(self):
        return f"{self.errorValue} is not a valid input."

@dataclass
class CollectedResources:
    hydrocarbons: int = 0
    oxides: int = 0
    water: int = 0

    CONV_WATER: int = 5
    CONV_OXIDES: int = 10
    CONV_HC: int = 50
    def sum(self) -> int:
        return self.hydrocarbons + self.oxides + self.water
    
    def __add__(self, operand: Self) -> Self:
        return CollectedResources(self.hydrocarbons + operand.hydrocarbons, self.oxides + operand.oxides, self.water + operand.water)

    def zero(self):
        self.hydrocarbons = 0
        self.oxides = 0
        self.water = 0
    def convert(self, resource=None) -> int:
        if not resource:
            return (self.water * self.CONV_WATER) + (self.oxides * self.CONV_OXIDES) + (self.hydrocarbons * self.CONV_HC)
        else:
            match resource:
                case "water":
                    return self.water * self.CONV_WATER
                case "oxides":
                    return self.oxides * self.CONV_OXIDES
                case "hydrocarbons":
                    return self.hydrocarbons * self.CONV_HC

class World:
    #                              TILE, MIN_SIZE, MAX_SIZE, NUM_CLUSTERS
    type ClusterDefinition = tuple[str,  int,      int,      int]
    def __init__(self, base_tile: str, size_x: int, size_y: int, random_seed: int, random_tiles: list[tuple[str, int]], cluster_tiles: ClusterDefinition):
        self.base_tile = base_tile
        self.size_x = size_x
        self.size_y = size_y
        self.random_tiles = random_tiles
        self.cluster_tiles = cluster_tiles
        self.__tilemap  = np.empty([self.size_x, self.size_y], dtype=int)
        self.__colormap = np.empty([self.size_x, self.size_y], dtype=int)
        seed(random_seed)
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                self.__tilemap[x][y] = ord(self.base_tile)
                for rtile in random_tiles:
                    prob = rtile[1]
                    tile = rtile[0]
                    if choices(population=[True, False], weights=[prob, 1 - prob], k=1)[0]:
                        self.__tilemap[x][y] = ord(tile)
                        if tile in fueltiles.keys():
                            self.__colormap[x][y] = fueltiles[tile]
                        
        for ctile in cluster_tiles:
            self.random_clusters(ctile[1], ctile[2], ctile[3], ctile[0])
    

    def get_tile(self, y, x) -> int:
        return self.__tilemap[y][x]

    def set_tile(self, y, x, tile) -> None:
        self.__tilemap[y][x] = ord(tile)

    def get_tile_color(self, y, x) -> int:
        return self.__colormap[y][x]
    
    def set_tile_color(self, y, x, color_pair) -> None:
        self.__colormap[y][x] = color_pair

    def make_cluster(self, y: int, x: int, tile: str, cluster_size: int) -> None:
        for dy in range(-cluster_size, cluster_size+1):
            for dx in range(-cluster_size, cluster_size+1):
                if (abs(dx) + abs(dy)) <= cluster_size:
                    try:
                        self.set_tile(y+dy, x+dx, tile)
                        if tile in fueltiles.keys():
                            self.set_tile_color(y+dy, x+dx, fueltiles[tile])
                    except(IndexError):
                        pass

    def random_clusters(self, min_size: int, max_size: int, num_clusters: int, tile: str) -> None:
        for _ in range(num_clusters):
            size = randint(min_size, max_size)
            y = randint(0, self.size_y-1)
            x = randint(0, self.size_x-1)
            self.make_cluster(y, x, tile, size)


def main(stdscr, VIEWPORT: tuple[int, int], world: World, initial_position = (50, 50)) -> CollectedResources:
    VIEWPORT_Y = VIEWPORT[0]
    VIEWPORT_X = VIEWPORT[1]
    WORLDSIZE_Y = world.size_y
    WORLDSIZE_X = world.size_x

    player = '@'
    loc_x = initial_position[0]
    loc_y = initial_position[1]

    playerResources = CollectedResources()
    playerCarryingCapacity = 150
    playerMaxLifeSupport = 500
    playerLifeSupport = 500

    curses.curs_set(0)

    ship_position = (loc_x+1, loc_y+1)

    def draw_life_support_meter():
        x = VIEWPORT_X + 1
        ch = "▄"
        height = VIEWPORT_Y
        div3 = height // 3

        stop = int( (playerLifeSupport / playerMaxLifeSupport) * height)
        def color(y):
            if y <= div3:
                return curses.color_pair(3) # green
            elif y <= div3 * 2:
                return curses.color_pair(2) # yellow
            else:
                return curses.color_pair(1) # red
        for y in range(height, height - stop, -1):
            stdscr.addch(y, x, ch, color(y))

    def draw_arrows_to_ship():
        y_dif = (loc_y - ship_position[1]) * 2
        x_dif = loc_x - ship_position[0] 
        ang = x_dif - y_dif
        
        def arrow(side):
            draw_arrow = lambda dy, dx, arr: stdscr.addch(VIEWPORT_Y//2 + dy, VIEWPORT_X//2 + dx, arr, curses.color_pair(1))
            match side:
                case 'up':
                    draw_arrow(-1, 0, '↑')
                case 'down':
                    draw_arrow(+1, 0, '↓')
                case 'left':
                    draw_arrow(0, -1, '←')
                case 'right':
                    draw_arrow(0, +1, '→')
        if abs(y_dif) > abs(x_dif): # north-south
            if(y_dif > 0):
                arrow("up")
            else:
                arrow("down")

        if abs(x_dif) > abs(y_dif): # east-west
            if(x_dif > 0):
                arrow("left")
            else:
                arrow("right")

    world.set_tile(loc_x+1, loc_y+0, "<")
    world.set_tile(loc_x+1, loc_y+1, "=")
    world.set_tile(loc_x+1, loc_y+2, ">")

    for i in range(0, 3):
        world.set_tile_color(loc_x+1, loc_y+i, 1)

    # drawing
    while(True):
        stdscr.clear()
        for x in range(0, VIEWPORT_X):
            world_x = loc_x + (x - VIEWPORT_X//2)
            for y in range(0, VIEWPORT_Y):
                world_y = loc_y + (y - VIEWPORT_Y//2)

                #stdscr.addch(y, x, gettile(loc_y + (y - VIEWPORT_Y//2), loc_x + (x - VIEWPORT_X//2)))
                if(not (world_x >= WORLDSIZE_X or world_y >= WORLDSIZE_Y or world_x <= 0 or world_y <= 0) ): # if tile is not out of bounds
                    #stdscr.addch(y, x, chr(world[ world_y ][ world_x ]))
                    color = world.get_tile_color(world_y, world_x)
                    if color:
                        stdscr.addch(y, x, chr(world.get_tile(world_y, world_x)), curses.color_pair(color))
                    else:
                        stdscr.addch(y, x, chr(world.get_tile(world_y, world_x)))
                else:
                    stdscr.addch(y, x, ' ')
        
        stdscr.addch(VIEWPORT_Y//2, VIEWPORT_X//2, player, curses.color_pair(3))

        stdscr.addstr(VIEWPORT_Y + 1, 0, f"{playerResources.water} H20")
        stdscr.addstr(VIEWPORT_Y + 2, 0, f"{playerResources.oxides} Oxides")
        stdscr.addstr(VIEWPORT_Y + 3, 0, f"{playerResources.hydrocarbons} Hydrocarbons")
        stdscr.addstr(VIEWPORT_Y + 4, 0, f"{playerResources.sum()} / {playerCarryingCapacity}")
        #stdscr.addstr(VIEWPORT_Y + 5, 0, f"Life Support: {playerLifeSupport}/{playerMaxLifeSupport}   ", curses.color_pair(6))

        draw_arrows_to_ship()
        draw_life_support_meter()

        stdscr.refresh()
        move = stdscr.getkey()

        match move:
            case "KEY_UP":
                if not loc_y-1 <= 0:
                    loc_y -= 1
            case "KEY_DOWN":
                if not loc_y+1 >= WORLDSIZE_Y:
                    loc_y += 1
            case "KEY_LEFT":
                if not loc_x-1 <= 0:
                    loc_x -= 1
            case "KEY_RIGHT":
                if not loc_x+1 >= WORLDSIZE_X:
                    loc_x += 1
            case _:
                raise(InputError(move))
                break
        playerLifeSupport -= 1
        if playerLifeSupport <= 0:
            raise PlayerDied("empty life support module.")
        
        if (loc_x, loc_y) == ship_position:
            break
        
        tileUnderFoot = chr(world.get_tile(loc_y, loc_x))
        if tileUnderFoot in fueltiles and playerResources.sum() < playerCarryingCapacity:
            world.set_tile(loc_y, loc_x, world.base_tile)
            world.set_tile_color(loc_y, loc_x, 0)
            match tileUnderFoot:
                case "H":
                    playerResources.water += 1
                case "X":
                    playerResources.oxides += 1
                case "C":
                    playerResources.hydrocarbons += 1
                case _:
                    pass
            

    stdscr.clear()
    return playerResources

if __name__ == "__main__":
    w: World = World(' ', 125, 125, 6823785, [(',', 0.1), ('X', 0.01), ('C', 0.01)], [('H', 2, 5, 8)])
    wrapper(main, (15, 30), w)
