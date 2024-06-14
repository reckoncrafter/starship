# World() default paramaters for in-game planets
# World:
#    base_tile: str,
#    size_x: int,
#    size_y: int,
#    randon_seed: int,
#    random_tiles: list[tuple[str, int]],
#    cluster_tiles: ClusterDefinition
#
# ClusterDefinition = tuple[str,int,int,int]
#   tile: str,
#   min_size: int,
#   max_size: int,
#   num_clusters: int,

from world import World
# World(' ', 100, 100, 854827, [(",", 0.1), ('%', 0.01), ("C", 0.01)], [('H', 2, 5, 8)])


randomtile_set_default = [(',', 0.1), ('%', 0.01), ("C", 0.01)]
randomtile_set_1 = [('.', 0.08), ("X", 0.08)]
randomtile_set_2 = [('\"', 0.3), ("C", 0.02), ("X", 0.005)]

clustertile_set_1 = [('H', 2, 5, 8)]

def world_base(random_seed, base_tile=' ', random_tiles=randomtile_set_default, cluster_tiles=[]):
    return World(base_tile, 100, 100, random_seed, random_tiles, cluster_tiles)


# building these objects takes a few seconds on startup
# consider refactoring this into an object that builds the World() objects on demand.
world_objects = {
    "AL-1": world_base(474321, random_tiles=[('\"', 0.3), ('%', 0.01), ("C", 0.008)], cluster_tiles=clustertile_set_1),
    "AL-2": world_base(412452, random_tiles=randomtile_set_1),
    "AL-3": world_base(657567, base_tile='+', random_tiles=[('X', 0.02)]),

    "AM-1": world_base(668431),
    
    "L-1":  world_base(471734, cluster_tiles=[('H', 2, 10, 16)]),

    "O-1":  world_base(698123),
    "O-1a": world_base(396088),
    "O-1b": world_base(378548),
    "O-1c": world_base(395565),
    "O-2":  world_base(119441),

    "T-1":  world_base(123476),

    "AP-1": world_base(996642),
    "AP-2": world_base(556546),
    "AP-2a":world_base(222222),

    "H-1":  world_base(599296)
}


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