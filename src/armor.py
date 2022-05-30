import arcade


class Head(arcade.Sprite):
    def __init__(self, filename, scale, icon_image, player):
        super().__init__(filename, scale)
        self.filename = filename
        self.icon_image = icon_image
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Body(arcade.Sprite):
    def __init__(self, filename, scale, equip_image, player):
        super().__init__(filename, scale)
        self.equip_image = equip_image
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Legs(arcade.Sprite):
    def __init__(self, filename, scale, equip_image, player):
        super().__init__(filename, scale)
        self.equip_image = equip_image
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Boots(arcade.Sprite):
    def __init__(self, filename, scale, equip_image, player):
        super().__init__(filename, scale)
        self.equip_image = equip_image
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Gloves(arcade.Sprite):
    def __init__(self, filename, scale, equip_image, player):
        super().__init__(filename, scale)
        self.equip_image = equip_image
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()


class Cloak(arcade.Sprite):
    def __init__(self, filename, scale, equip_image, player):
        super().__init__(filename, scale)
        self.equip_image = equip_image
        self.player = player

    def update(self):
        if self.player.alive:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
        else:
            self.kill()
