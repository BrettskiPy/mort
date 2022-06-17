import arcade

class UpgradeAnimation(arcade.Sprite):
    """The animation for upgrade success or failure"""

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list
        self.center_x = 370
        self.center_y = 300

    def update(self):

        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()