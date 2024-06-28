from tile import Rotation, Tile


class EmptyTile(Tile):

    def __init__(self):
        super().__init__(name="0")


class Wall(Tile):

    def __init__(self, 
                 width: int = 1, 
                 height: int = 1, 
                 connectable: list[Rotation] = ..., 
                 name: str = "No Tile"):
        super().__init__(width, height, connectable, name)


class LineTileNS(Tile):

    def __init__(self):
        super().__init__(connectable=[Rotation.NORTH, Rotation.SOUTH], name="L")
        self.allowed_tiles = {
            Rotation.NORTH: [LineTileNS, CrossTile],
            Rotation.EAST: [LineTileNS],
            Rotation.SOUTH: [LineTileNS, CrossTile],
            Rotation.WEST: [LineTileNS],
        }

class LineTileWE(Tile):

    def __init__(self):
        super().__init__(connectable=[Rotation.NORTH, Rotation.SOUTH], name="L")
        self.allowed_tiles = {
            Rotation.NORTH: [LineTileWE],
            Rotation.EAST: [LineTileWE, CrossTile],
            Rotation.SOUTH: [LineTileWE],
            Rotation.WEST: [LineTileWE, CrossTile],
        }

class CrossTile(Tile):

    def __init__(self):
        super().__init__(name="+")