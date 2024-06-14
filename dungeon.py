import curses
import numpy as np
from subprocess import run
from static import dungeonObjects

class Dungeon:
    def __init__(self):
        self.SIZE_X = 67
        self.SIZE_Y = 13
        self.__tilemap = np.empty([self.SIZE_X, self.SIZE_Y], int)

        # copy in
        file = open("d1.txt", "r")
        lines = file.readlines()
        y = 0
        for line in lines:
            x = 0
            for char in line:
                #print(f"self.__tilemap[{x}][{y}] = {ord(char)}")
                self.__tilemap[x][y] = ord(char)
                x += 1
            y += 1

    def draw(self, stdscr):
        for y in range(0, self.SIZE_Y):
            for x in range(0, self.SIZE_X):
                stdscr.addch(y,x,chr(self.__tilemap[x][y]))
        
        for obj in dungeonObjects:
            icon, x, y, _ = obj
            stdscr.addch(y,x,icon)

    def get_tile(self, x:int, y:int) -> str:
        return chr(self.__tilemap[x][y])
            
    def set_tile(self, x:int, y:int, ch:str) -> None:
        self.__tilemap[x][y] = ord(ch)
    
def main(stdscr):
    curses.curs_set(0)
    dungeon = Dungeon()
    
    player_icon = "@"
    pos_y = 5
    pos_x = 2
    
    def dialogueBox(text:str):
        stdscr.clear()
        lines = text.splitlines()
        
        width = len(min(lines))
        height = len(lines)

        win = curses.newwin(height+2,width+2,0,0)
        win.addstr(1,1,text)
        win.box()
        win.refresh()
        win.getch()
        return


    def move(x,y):
        nonlocal pos_x
        nonlocal pos_y
        new_x = pos_x + x
        new_y = pos_y + y

        for obj in dungeonObjects:
            _, x, y, message = obj
            if new_x == x and new_y == y:
                dialogueBox(message)
        if dungeon.get_tile(new_x, new_y) not in ["-", "+", "|"]:
            pos_y = new_y
            pos_x = new_x
            
    while(True):
        stdscr.clear()
        dungeon.draw(stdscr)
        stdscr.addch(pos_y, pos_x, player_icon)
        stdscr.addstr(14, 0, str(pos_x)+ ' ' +str(pos_y))

        key = stdscr.getkey()
        match key:
            case "KEY_UP":
                move(0, -1)
            case "KEY_DOWN":
                move(0, +1)
            case "KEY_LEFT":
                move(-1, 0)
            case "KEY_RIGHT":
                move(+1, 0)

        if (pos_x, pos_y) == (1, 5):
            stdscr.clear()
            return   


    

if __name__ == "__main__":
    curses.wrapper(main)