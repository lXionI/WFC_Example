from level import Level
from tile import Tile
from renderer import Renderer
import matplotlib.pyplot as plt

import json


def load_debug_tiles(path_to_json: str="./src/tiles/debug_tiles.json") -> list[Tile]:
    debug_tiles = []
    with open(path_to_json) as f:
        json_tile = json.loads(f.read())
    for tile in json_tile["Tiles"]:
        loaded_tile = Tile.model_validate(tile)
        debug_tiles.append(loaded_tile)
    return debug_tiles


if __name__ == "__main__":
    n_tiles = 10
    list_tiles = load_debug_tiles("./src/tiles/debug_tiles.json")
    list_tiles.remove(list_tiles[0])
    level = Level(n_tiles, n_tiles, list_tiles, render_progress=True)
    level.collapse()
    print(level)
    Renderer(level).plot()
    plt.show()