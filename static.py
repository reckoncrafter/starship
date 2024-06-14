from typing import Literal

def getfilestr(filename: str):
    with open(filename, "r") as file:
        return file.read()

deck1 = {
    "map": getfilestr("assets/asciiart/deck1map.txt"),
    "map_alt": getfilestr("assets/asciiart/deck1mapalt.txt"),

    "objects":[
    # hatch
    ("0", 1, 11),

    ("B", 1, 1, "bro is *not* sleepy"),
    ("#", 1, 3),
    ("»", 2, 35),
    ("Ø", 0, 15),

    # walls lmao
    ("|", 1, 10),
    ("|", 3, 10),
    ("|", 1, 29),
    ("|", 3, 29),
],
    "borders":(0, 35, 0, 4),
    "offsets":(4, 0)
}

deck0 = {
    "map": getfilestr("assets/asciiart/deck0map.txt"),

    "objects":[
    ("0", 1, 1),

    # boxes
    ("▄", 1, 10, "this one is fucking weird."),
    ("▄", 2, 5, "a crate of emergency food rations"),
    ("▄", 2, 6, "a crate of tools and medical supplies"),
    ("&", 1, 13),

    ("?", 2, 20, "You don't remember bringing this aboard. It's a note stuck to the wall. It reads: \"STILLHERE\"")
],
    "borders": (0, 21, 0, 4),
    "offsets": (0, 0)
}

starmap = getfilestr("assets/asciiart/starmap.txt")

type Star = Literal["ALETHIA", "AMPHITRYON", "LIANSHAN", "OB", "CADMUS", "TOKUGAWA", "APOLLONIA", "HAN_FEI"]

starmapAdjacencyList = {
    "ALETHIA": [("AMPHITRYON", 256), ("LIANSHAN", 128)],
    "AMPHITRYON": [("ALETHIA", 256), ("CADMUS", 128)],
    "LIANSHAN": [("ALETHIA", 128), ("OB", 128), ("HAN FEI", 1024)],
    "OB": [("LIANSHAN", 128), ("CADMUS", 128)],
    "CADMUS": [("OB", 128),("AMPHITRYON", 128),("TOKUGAWA", 512), ("APOLLONIA", 32)],
    "TOKUGAWA": [("CADMUS", 512)],
    "APOLLONIA": [("CADMUS", 32)],
    "HAN FEI": [("LIANSHAN", 1024)]
}

starSystemMapLegend = getfilestr("assets/text/starSystemMapLegend.txt")

# lore = {
#     "mission": getfilestr("assets/text/mission.lore.txt"),
#     "fairhaven": getfilestr("assets/text/fairhaven.lore.txt"),
#     "weiss": getfilestr("assets/text/weiss.lore.txt"),
#     "cadmus": getfilestr("assets/text/cadmus.lore.txt"),
#     "ship": getfilestr("assets/text/ship.lore.txt")
# }

# The Lore object behaves identically to the dict above,
# but generates its list automatically from the contents of
# the assets/text directory.from os import listdir

from os import listdir
class Lore:
    def __init__(self):
        self.directory = "assets/text/"
        self.files = filter(lambda x: (".lore.txt" in x), listdir("assets/text"))
        self.kwords = [x.split('.')[0] for x in self.files]

    def __getitem__(self, key) -> str:
        if key in self.kwords:
            return getfilestr(f"{self.directory}{key}.lore.txt")
        else:
            raise KeyError
        
    def keys(self) -> list[str]:
        return self.kwords

    def values(self) -> list[str]:
        return [getfilestr(f"{self.directory}{x}") for x in self.files]

lore = Lore()

starSystemPlanets = {
    "ALETHIA": ["AL-1", "AL-2", "AL-3"],
    "AMPHITRYON": ["AM-1"],
    "LIANSHAN": ["L-1"],
    "OB": ["O-1", "O-1a", "O-1b", "O-1c", "O-2"],
    "CADMUS": ["WEISS ASTEROID MINING"],
    "TOKUGAWA": ["T-1"],
    "APOLLONIA": ["AP-1", "AP-2", "AP-2a"],
    "HAN FEI": ["H-1"]
}

starSystemMaps = {
    "ALETHIA": """
    *  -  -  - AL-1 - AL-2 -  -  - | -  -  -  - AL-3
    """,
    "AMPHITRYON":"""
    * - AM-1 -  -  -  -  - | -  -  -  -  - |
    """,
    "LIANSHAN":"""
    * -  -  |  -  -  -  -  - L-1 -  -
    """,
    "OB":"""
    % -  -  -  - O-1 | -  -  -  - O-2 -
          [O-1a, 0-1b, 0-1c]
    """,
    "CADMUS":"""
    * -  -  |
          [WEISS ASTEROID MINING]
    """,
    "TOKUGAWA":"""
    * -  -  -  - | T-1
    """,
    "APOLLONIA": """
    * -  -  AP-1 -  - | - AP-2
                         [AP-2a]
    """,
    "HAN FEI": """
    * -  -  -  -  -  -  -  -  -  -  -  - H-1 |
    """
}

dungeonObjects = [
    # small rooms
    ('!', 4, 3, "John Aieslaby"),
    ('!', 8, 3, "Sadie Humbolt"),
    ('!', 12, 3,"Jason Funderburger"),
    ('!', 16, 3,"Salem Forester"),
    ('!', 20, 3,"Dawn Finn"),
    ('!', 24, 3,"Victor Stoker"),
    ('!', 28, 3,"Leon Kennedy"),
    ('!', 32, 3,"Harry"),
    ('!', 36, 3,"Sael Libodottan"),
    ('!', 40, 3,"Carson Barr"),

    # large rooms
    ('!', 5, 7, "Isa Stoltenberg"),

    # utility rooms
    ('!', 53, 3, "Exercise Room"),
    ('!', 61, 3, "Laundry Room"),
    ('!', 43, 7, "Mess Hall"),
    ('!', 63, 7, "Utility Closet"),
    ('!', 29, 7, "Science Lab")
]