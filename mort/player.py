import arcade
from mort.constants import GAME_WIDTH, PLAYER_SCALE


class Player(arcade.Sprite):
    def __init__(
        self, filename=":assets:base/demigod_male.png", scale=PLAYER_SCALE, alive=True
    ):
        super().__init__(filename, scale)
        self.center_x = GAME_WIDTH / 2
        self.center_y = self.height / 2

    def update(self):
        """Move the player"""
        pass
