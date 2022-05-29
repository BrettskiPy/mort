import arcade


class MainHand(arcade.Sprite):
    def __init__(self, filename, scale, player):
        super().__init__(filename, scale)
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class OffHand(arcade.Sprite):
    def __init__(self, filename, scale, player):
        super().__init__(filename, scale)
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()