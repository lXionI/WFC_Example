# from level import Level
from tile import Tile, SuperpositionTile
import matplotlib.pyplot as plt

class Renderer:

    def __init__(self, level) -> None:
        self.level = level
        self.__setup__()
        # plt.ion()

    def __setup__(self):
        self.fig, self.ax = plt.subplots(ncols=self.level.width, nrows=self.level.height)
        for i, row in enumerate(self.level._level):
            for col in range(len(row)):
                tile = row[col]
                if type(tile) != Tile:
                    continue
                image = plt.imread("./images/" + tile.mesh + ".png")
                self.ax.ravel()[i * len(row) + col].imshow(image, cmap="gray")
                self.ax.ravel()[i * len(row) + col].set_axis_off()
        for row in self.ax:
            for a in row:
                a.set_xticklabels([])
                a.set_yticklabels([])
                # a.set_aspect('equal')
        # plt.tight_layout()
        self.fig.set_figwidth(self.level.width)
        self.fig.set_figheight(self.level.height)

    def update_tile(self, idw, idh, new_tile):
        if type(new_tile) != Tile:
            return
        image = plt.imread("./images/" + new_tile.mesh + ".png")
        self.ax.ravel()[idw * self.level.height + idh].imshow(image, cmap="gray")

    def plot(self):
        plt.subplots_adjust(wspace=0, hspace=0)
        # self.fig.canvas.draw()
        plt.draw()
        plt.pause(0.1)
        # plt.plot()