import arcade
from constants import *


class Head(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, scale=HELMET_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Body(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, scale=BODY_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Legs(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, scale=LEGS_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Boots(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, scale=BOOTS_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Gloves(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, scale=GLOVES_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Cloak(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, scale=CLOAK_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()
