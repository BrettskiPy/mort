import arcade

class Icon(arcade.Sprite):
    def __init__(self, filename, scale, item_data):
        super().__init__(filename, scale)
        self.item_data = item_data
        self.inv_pos = None



