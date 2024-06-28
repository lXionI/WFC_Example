from enum import Enum
from abc import ABC

from pydantic import BaseModel

class Rotation(Enum):
    NORTH = 0       # 0°
    EAST = 1        # 90° 
    SOUTH = 2       # 180°
    WEST = 3        # 270°
    ALL = 4         # 360*


class AbstractTile(ABC):

    def __init__(self) -> None:
        super().__init__()


class Tile(BaseModel, AbstractTile):
    mesh: str
    sockets: list[int]
    """ Representation of one pattern as part of the wave.

    Connections - tile needs to know, which parts are connected
    """

    def __repr__(self) -> str:
        return self.mesh
    # def __init__(self,
    #              mesh: str,
    #              sockets: list[str]):
    #     self.mesh = mesh # i will use this as a placeholder for name/images
    #     self.sockets = sockets
    # def __init__(self, 
    #              width: int=1, 
    #              height: int=1, 
    #              connectable: list[Rotation] = [Rotation.ALL],
    #              name: str="No Tile"):
    #     self.width = width
    #     self.height = height
    #     self.connectable = connectable
    #     self.name = name
    #     self.allowed_tiles = {
    #         Rotation.NORTH: [],
    #         Rotation.EAST: [],
    #         Rotation.SOUTH: [],
    #         Rotation.WEST: [],
    #     }

class SuperpositionTile(AbstractTile):
    def __init__(self, possible_tiles: list[Tile]):
        self.possible_tiles = possible_tiles
        
    def __repr__(self) -> str:
        return str(len(self.possible_tiles))