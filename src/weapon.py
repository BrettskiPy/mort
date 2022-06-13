import arcade
from constants import *


class MainHand(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, name, scale=HELMET_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats
        self.name = name

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class OffHand(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, name, scale=HELMET_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats
        self.name = name

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()
