import curses
from curses import wrapper
from static import *
import world
import dungeon
import world_setup
import datetime as dt
from util import PlayerCommittedSuicide

def init_colors():
    curses.init_pair(1, curses.COLOR_RED, 0)
    curses.init_pair(2, curses.COLOR_YELLOW, 0)
    curses.init_pair(3, curses.COLOR_GREEN, 0)
    curses.init_pair(4, curses.COLOR_BLUE, 0)
    curses.init_pair(5, curses.COLOR_MAGENTA, 0)
    curses.init_pair(6, curses.COLOR_CYAN, 0)


def main(stdscr):
    curses.curs_set(0)
    init_colors()

    # state variables
    warpCoreEjected = False
    currentStar: StarName = "HAN FEI"
    currentPlanet: str | None = None
    fuelUnits = 256
    maxFuelUnits = 25565
    collectedResources = world.CollectedResources()

    date = dt.date.today()
    date = date.replace(year=2721)
    
    x = 2
    y = 2
    nx = 0
    ny = 0
    currentDeck = deck1

    def swap_deck1_maps():
        if not warpCoreEjected:
            temp = deck1["map"]
            deck1["map"] = deck1["map_alt"]
            deck1["map_alt"] = temp

    def terminalWindow():
        curses.curs_set(1)
        stdscr.clear()
        stdscr.box()
        win = curses.newwin(10, 50, 0, 0)
        
        def addstr_byline(window, cursory:int, cursorx:int, string:str):
            # Splits multiline string into individual lines, and adds them one by one
            # This has the effect of keeping the x-coordinate of the added string constant,
            # instead of it returning to the left side of the screen
            y = cursory
            for line in string.splitlines():
                window.addstr(y, cursorx, line)

                # reset line position for overflow. wait for user to confirm
                if y >= curses.LINES - 4:
                    window.addstr(y+2, cursorx, "[press any key to continue...]")
                    window.getkey()
                    window.clear()
                    window.box()
                    y = 1

                y += 1

        while(True):
            stdscr.clear()
            stdscr.box()
            y = 1
            stdscr.move(y, 1)
            datestring = date.strftime(f"%A, %B %d %Y")
            stdscr.addstr(y, 1, f"Today is {datestring}")
            y = 2
            stdscr.addstr(y, 1, "Please enter search term")

            y = 3
            stdscr.addch(y, 1, ">")
            stdscr.refresh()
            
            curses.echo()
            queryString = stdscr.getstr().decode("utf-8")

            y = 4

            write_lore = lambda text: addstr_byline(stdscr, y, 1, text) 

            querySuccess = False
            for key in lore.keys():
                if key in queryString:
                    write_lore(lore[key])
                    querySuccess = True
                    break
            if not querySuccess:
                stdscr.addstr(y, 1, "?")

            stdscr.refresh()
            c = stdscr.getkey()
            if(c != "\n"):
                break

        stdscr.clear()
        curses.echo()
        curses.curs_set(0)
        return
    
    def dialogueBox(text:str):
        stdscr.clear()
        win = curses.newwin(20,60,0,0)
        win.addstr(1,1,text)
        win.box()
        win.refresh()
        win.getch()
        return

    def menuDialogue(prompt:str, *args: tuple[str, str]):
        stdscr.clear()
        win = curses.newwin(20,60,0,0)
        win.addstr(1,0,prompt)
        win.box()
        y = 2
        for opt in args:
            win.addstr(y,1,f"{opt[0]}: {opt[1]}")
            y += 1
        win.refresh()
        ch = win.getkey()

        return ch

    def displayStarMap():
        stdscr.clear()
        stdscr.addstr(1,1,f"CURRENT LOCATION: {currentStar}")
        stdscr.addstr(2,1,starmap)
        stdscr.box()
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        return

    def displayPlanets():
        stdscr.clear()
        win = curses.newwin(20, 60, 0, 0)
        win.addstr(1,1, "SELECT DESTINATON")
        planets = starSystemPlanets[currentStar]

        y = 2
        index = 1
        for planet in planets:
            win.addstr(y, 1, f"{index}: {planet}")
            y += 1
            index += 1
        win.box()
        win.refresh()
        selected = win.getkey()

        try:
            return planets[int(selected) - 1]
        except:
            return False

    def displayAdjacentSystems():
        stdscr.clear()
        win = curses.newwin(20, 60, 0, 0)
        win.addstr(1,1, "SELECT TARGET SYSTEM " + f"/ {fuelUnits}u/{maxFuelUnits}u OF FUEL REMAINING.")
        adjacentSystems = starmapAdjacencyList[currentStar]
        y = 2
        index = 1
        for star in adjacentSystems:
            win.addstr(y, 1, f"{index}: {star[0]}: {star[1]}u AWAY")
            y += 1
            index += 1
        win.box()
        win.refresh()
        selected = win.getkey()

        try:
            return adjacentSystems[int(selected) - 1]
        except:
            return (False, False)


    while(True):
        stdscr.addstr(0,0,currentDeck["map"])
    
        for obj in currentDeck["objects"]:
            stdscr.addch(obj[1] + currentDeck["offsets"][0], obj[2], obj[0])

        stdscr.addch(y + currentDeck["offsets"][0], x, '@', curses.color_pair(3))
        c = stdscr.getkey()

        if(c == "KEY_UP"):
            ny = -1
        elif(c == "KEY_DOWN"):
            ny = 1
        elif(c == "KEY_LEFT"):
            nx = -1
        elif(c == "KEY_RIGHT"):
            nx = 1
        
        nextPos = (y + ny, x + nx)
        for obj in currentDeck["objects"]:
            if( nextPos == (obj[1], obj[2])):
                nx = 0
                ny = 0
                if(obj[0] == "0"):
                    if(currentDeck == deck1):
                        stdscr.clear()
                        currentDeck = deck0
                        y, x = deck0["objects"][0][1:3] # slice of (icon, y, x) -> (y, x)
                        y += 1
                    elif(currentDeck == deck0):
                        stdscr.clear()
                        currentDeck = deck1
                        y, x = deck1["objects"][0][1:3]
                        y += 1
                elif(obj[0] == "#"): # computer terminal
                    terminalWindow()
                elif(obj[0] == "Ø"): # airlock controls

                    airlock = menuDialogue(" open airlock?", ("1", "yes"), ("2", "no"))
                    if(airlock == "1"):
                        if(currentPlanet == None):
                            dialogueBox("You enter the airlock,\n and it depressurizes with you inside it.\n\n You are dead.")
                            raise(PlayerCommittedSuicide("Ejected Into Space"))
                        elif(currentPlanet == "WEISS ASTEROID MINING"):
                            # begin dungeon.py
                            # ----------------
                            dungeon.main(stdscr)
                            # ----------------
                        else:
                            # begin world.py
                            # -------------- 

                            #test_world = world.World(' ', 100, 100, 854827, [(",", 0.1), ('%', 0.01), ("C", 0.01)], [('H', 2, 5, 8)])
                            current_world = world_setup.world_objects[currentPlanet]
                            new_resources: world.CollectedResources = world.main(stdscr, (15, 30), current_world, (50, 50))
                            collectedResources += new_resources
                            # --------------
                elif(obj[0] == "&"): # refinery
                    sel = menuDialogue(" select refinery command:",\
                        ("1", "refine resources"),\
                        ("2", "view current resources"),)

                    if(sel == "1"):
                        sel1 = menuDialogue(f" refine all resources?", ("1", "yes"), ("2", "no"))
                        if(sel1 == "1"):
                            newFuel = collectedResources.convert()
                            if fuelUnits+newFuel <= maxFuelUnits:
                                fuelUnits += newFuel
                                collectedResources.zero()
                                dialogueBox(f"{newFuel}u added.\
                                    \n {fuelUnits}u/{maxFuelUnits}u")
                            else:
                                dialogueBox("tank capacity will be exceeded. halting refinement.")
                        else:
                            pass

                    elif(sel == "2"):
                        dialogueBox(f"""water: {collectedResources.water} -> {collectedResources.convert("water")}
hydrocarbons: {collectedResources.hydrocarbons} -> {collectedResources.convert("hydrocarbons")}
oxides: {collectedResources.oxides} -> {collectedResources.convert("oxides")}
total fuel to be ref:: Star ined: {collectedResources.convert()}u""")

                elif(obj[0] == "»"): # flight computer
                    sel = menuDialogue(" select autopilot command:",\
                        ("1","eject warp core"),\
                        ("2", "view nearby systems"),\
                        ("3", "view current system"),\
                        ("4", "set new course"),\
                        ("5", ("land" if currentPlanet==None else "take off") ))
                    if(sel == "1"):
                        # eject warp core
                        dialogueBox("warp core ejected. maximum velocity: 0.5c")
                        swap_deck1_maps()
                        warpCoreEjected = True
                        stdscr.clear()
                    elif(sel ==  "2"):
                        # view nearby systems
                        displayStarMap()
                    elif(sel == "3"):
                        # view current system
                        dialogueBox(f"{currentStar}\n{starSystemMapLegend}\n{starSystemMaps[currentStar]}")
                    elif(sel == "4"):
                        # set new course
                        if(warpCoreEjected):
                            dialogueBox("no warp capability")
                        elif(currentPlanet != None):
                            dialogueBox("cannot activate warp drive in gravity well")
                        else:
                            nextSystem, fuelCost = displayAdjacentSystems()
                            if(nextSystem):
                                if(fuelCost <= fuelUnits):
                                    sel = menuDialogue(f" commit to route? this will consume {fuelCost}u of fuel.", ("1", "yes"), ("2", "no"))
                                    if(sel == "1"):
                                        fuelUnits -= fuelCost
                                        currentStar = nextSystem
                                        dialogueBox(f"traveling to {nextSystem}. remaining fuel: {fuelUnits}u")
                                    else:
                                        dialogueBox("aborting route.")
                                else:
                                    dialogueBox("insufficient fuel.")
                    elif(sel == "5"):
                        # land / take off
                        if(currentPlanet == None):
                            nextPlanet = displayPlanets()
                            if(nextPlanet):
                                dialogueBox(f"landing on {nextPlanet}...")
                                swap_deck1_maps()
                                currentPlanet = nextPlanet
                            else:
                                dialogueBox('landing aborted')
                        else:
                            dialogueBox("returning to orbit.")
                            swap_deck1_maps()
                            currentPlanet = None


                elif(len(obj) > 3):
                    dialogueBox(obj[3])
                

        # this sucks
        if(nextPos[1] <= currentDeck["borders"][0] or\
           nextPos[1] >= currentDeck["borders"][1] or\
           nextPos[0] <= currentDeck["borders"][2] or\
           nextPos[0] >= currentDeck["borders"][3]):

           nx = 0
           ny = 0

        x += nx
        y += ny
        nx = 0
        ny = 0
        
        stdscr.refresh()
    
    return    

if __name__ == "__main__":
    wrapper(main)
