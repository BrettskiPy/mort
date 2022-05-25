import arcade
from constants import SCREEN_WIDTH


class Player(arcade.Sprite):
    def __init__(self, filename, scale, alive=True):
        super().__init__(filename, scale)
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = self.height / 2
        self.alive = alive

    def update(self):
        """Move the player"""
