import arcade


class Icon(arcade.Sprite):
    def __init__(self, filename, scale, item_data, icon_list):
        super().__init__(filename, scale)
        self.item_data = item_data
        self.inv_pos = 0
        self.icon_list = icon_list
        self.set_inv_position()

    def set_inv_position(self):
        sorted_inv_list = [icon.inv_pos for icon in self.icon_list]
        sorted_inv_list.sort()
        if len(sorted_inv_list) == 1:
            self.inv_pos = 1
        elif len(sorted_inv_list) > 1:
            if self.missing_elements(sorted_inv_list):
                self.inv_pos = min(self.missing_elements(sorted_inv_list))
            else:
                self.inv_pos = max(sorted_inv_list) + 1
        else:
            self.inv_pos = 0

    def missing_elements(self, sorted_inv_list):
        start, end = sorted_inv_list[0], sorted_inv_list[-1]
        return sorted(set(range(start, end + 1)).difference(sorted_inv_list))
