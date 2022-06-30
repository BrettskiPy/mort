import arcade
from mort.constants import *


class Head(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, name, scale=HELMET_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats
        self.name = name

    def update(self):
        self.center_x = self.player.center_x
        self.center_y = self.player.center_y


class Body(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, name, scale=BODY_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats
        self.name = name

    def update(self):
        self.center_x = self.player.center_x
        self.center_y = self.player.center_y


class Legs(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, name, scale=LEGS_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats
        self.name = name

    def update(self):
        self.center_x = self.player.center_x
        self.center_y = self.player.center_y


class Boots(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, name, scale=BOOTS_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats
        self.name = name

    def update(self):
        self.center_x = self.player.center_x
        self.center_y = self.player.center_y


class Gloves(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, name, scale=GLOVES_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats
        self.name = name

    def update(self):
        self.center_x = self.player.center_x
        self.center_y = self.player.center_y


class Cloak(arcade.Sprite):
    def __init__(self, filename, icon_image, player, stats, name, scale=CLOAK_SCALE):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player
        self.stats = stats
        self.name = name

    def update(self):
        self.center_x = self.player.center_x
        self.center_y = self.player.center_y
