import arcade


class Head(arcade.Sprite):
    def __init__(self, filename, scale, player):
        super().__init__(filename, scale)
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Body(arcade.Sprite):
    def __init__(self, filename, scale, player):
        super().__init__(filename, scale)
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Legs(arcade.Sprite):
    def __init__(self, filename, scale, player):
        super().__init__(filename, scale)
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Boot(arcade.Sprite):
    def __init__(self, filename, scale, player):
        super().__init__(filename, scale)
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Glove(arcade.Sprite):
    def __init__(self, filename, scale, player):
        super().__init__(filename, scale)
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Cloak(arcade.Sprite):
    def __init__(self, filename, scale, player):
        super().__init__(filename, scale)
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()
