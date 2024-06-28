from typing import Any
from random import randint
from tile import SuperpositionTile, AbstractTile, Tile
from renderer import Renderer
from time import sleep


class Matrix:

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

        self._matrix = []
        self.__setup__()

    def __setup__(self):
        matrix = []
        for i in range(self.width):
            row = []
            for j in range(self.height): 
                row.append(None)
            matrix.append(row)
        self._matrix = matrix

    def __getitem__(self, idx):
        return self._matrix[idx]

class Level:

    def __init__(self, 
                 width: int, 
                 height: int, 
                 waves: list,
                 render_progress: bool=True) -> None:
        self.width = width
        self.height = height
        self.waves = waves
        self.render_progress = render_progress

        # self._level = [[SuperpositionTile(waves)] * width] * height
        self._level = Matrix(width, height)
        self.__setup__(waves)

        self.renderer = Renderer(self)

    def restrict_rule_edges(self, waves, socket) -> list:
        allowed_tiles = []
        for tile in waves:
            if tile.sockets[socket] == 0:
                allowed_tiles.append(tile)
        return allowed_tiles

    def __setup__(self, waves):
        # Restrictions for First row
        first_row_tiles = self.restrict_rule_edges(waves, 0)
        # Restrictions for Last row
        last_row_tiles = self.restrict_rule_edges(waves, 2)
        # Restrictions for First col
        left_col_tiles = self.restrict_rule_edges(waves, 1)
        # Restrictions for Last col
        right_col_tiles = self.restrict_rule_edges(waves, 3)
        for i in range(self.width):
            for j in range(self.height):
                self._level[i][j] = SuperpositionTile(waves)
                if i == 0:
                    self._level[i][j] = SuperpositionTile(first_row_tiles)
                if j == 0:
                    self._level[i][j] = SuperpositionTile(right_col_tiles)
                if j == self.width - 1:
                    self._level[i][j] = SuperpositionTile(left_col_tiles)
                if i == self.height - 1:
                    self._level[i][j] = SuperpositionTile(last_row_tiles)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self._level = self.collapse()
        return self
    
    def __repr__(self):
        level_repr = ""
        for row in self._level:
            level_repr += str(row) + "\n"
        return level_repr

    def find_lowest_entropy(self) -> tuple[int, int]:
        lowest_value = 1_000
        lowest_w_idx, lowest_h_idx = -1, -1
        lowest_entropy_dict = dict([])
        # it->1 / -it->99 [] 
        for i in range(self.width):
            for j in range(self.height):
                current_tile = self._level[i][j]
                if type(current_tile) == SuperpositionTile:
                    if len(current_tile.possible_tiles) < lowest_value:
                        lowest_value = len(current_tile.possible_tiles)
                        lowest_entropy_dict[lowest_value] = [(i, j)]
                    elif len(current_tile.possible_tiles) == lowest_value:
                        lowest_entropy_dict[lowest_value].append((i, j))
        try:
            lowest_key = min(lowest_entropy_dict.keys())
        except ValueError:
            return -1, -1
        if len(lowest_entropy_dict[lowest_key]) > 0:
            # print(f"Possible Options: {len(lowest_entropy_dict[lowest_key])}")
            random_tile_idx = randint(0, len(lowest_entropy_dict[lowest_key])-1)
            lowest_w_idx, lowest_h_idx = lowest_entropy_dict[lowest_key][random_tile_idx]
        return lowest_w_idx, lowest_h_idx

    def update_superposition(self, socket_idx, current_socket, super_tile):
        if type(super_tile) != SuperpositionTile:
            return
        new_possibilities = []
        for tile in super_tile.possible_tiles:
            if tile.sockets[socket_idx] == current_socket:
                new_possibilities.append(tile)
        if len(new_possibilities) == 0:
           new_possibilities.append(Tile(mesh="wall", sockets=[0, 0, 0, 0]))
        super_tile.possible_tiles = new_possibilities

    def set_new_tile(self, idw, idh, new_tile: AbstractTile) -> None:
        self._level[idw][idh] = new_tile
        # update neighbours - reduce possibilites of superpositions
        # Remember: sockets List[N, E, S, W]
        # print(new_tile.sockets)
        # Neighours: 
        # Order: N E S W

        # Update North tile
        if idw - 1 != -1:
            self.update_superposition(2, new_tile.sockets[0], self._level[idw-1][idh])
        if idh + 1 < self.height:
            self.update_superposition(3, new_tile.sockets[1], self._level[idw][idh+1])
        if idw + 1 < self.width:
            self.update_superposition(0, new_tile.sockets[2], self._level[idw+1][idh])
        if idh - 1 != -1:
           self.update_superposition(1, new_tile.sockets[3], self._level[idw][idh-1])

    def collapse(self) -> None:
        # find lowest entropy - if all same - select random
        # update cell from superposition to definite
        # update neighbours
        # repeat 1 until no more cells are in superposition

        # Case 1 - what if not all cells can be become definite?
        #          Collision in "solving" -> have any tile to close
        # Case 2 - takes too long -> optimize with bit shifting and
        #          and better searching algorithms (currently O(n^2))
        self.renderer.fig.show()
        while True:
            lowest_w_idx, lowest_h_idx = self.find_lowest_entropy()
            if lowest_w_idx == -1 and lowest_h_idx == -1:
                # No Superposition left
                return
            super_tile = self._level[lowest_w_idx][lowest_h_idx]
            if type(super_tile) != SuperpositionTile:
                return
            current_possibilites = len(super_tile.possible_tiles)
            # take one possible tile - otherwise use wall
            # TODO: introduce "dead ends" instead of straight "wall"
            print(super_tile.possible_tiles)
            tile_index = randint(0, max(1, current_possibilites-1)) 
            # self._level[lowest_w_idx][lowest_h_idx] = super_tile.possible_tiles[tile_index]
            try:
                self.set_new_tile(lowest_w_idx, lowest_h_idx, super_tile.possible_tiles[tile_index])
            except IndexError:
                print(super_tile.possible_tiles)
            if self.render_progress:
                self.renderer.update_tile(lowest_w_idx, lowest_h_idx, self._level[lowest_w_idx][lowest_h_idx])
                self.renderer.plot()
                sleep(.01)