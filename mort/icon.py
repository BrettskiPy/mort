import arcade
from mort.constants import ICON_SCALE


class InventoryIcon(arcade.Sprite):
    def __init__(
        self,
        filename,
        item_referenced,
        inventory_icon_list,
        scale=ICON_SCALE,
    ):
        super().__init__(filename, scale)
        self.filename = filename
        self.item_referenced = item_referenced
        self.pos = 0
        self.inventory_icon_list = inventory_icon_list
        self.set_inv_position()

    def set_inv_position(self):
        sorted_inv_list = [icon.pos for icon in self.inventory_icon_list]
        sorted_inv_list.sort()
        if len(sorted_inv_list) >= 1:
            if self.missing_elements(sorted_inv_list):
                self.pos = min(self.missing_elements(sorted_inv_list))
            else:
                self.pos = max(sorted_inv_list) + 1

    def missing_elements(self, sorted_inv_list):
        start, end = sorted_inv_list[0], sorted_inv_list[-1]
        return sorted(set(range(0, end + 1)).difference(sorted_inv_list))


class InventorySlotIcon(arcade.Sprite):
    def __init__(self, filename, scale, item_referenced, inv_window=None):
        super().__init__(filename, scale)
        self.filename = filename
        self.item_referenced = item_referenced
        self.inv_window = inv_window
        self.set_inv_position()

    def set_inv_position(self):
        if self.inv_window:
            item_type = self.item_referenced.__class__.__name__
            self.center_x = self.inv_window.mapped_slot_positions[item_type]["x"]
            self.center_y = self.inv_window.mapped_slot_positions[item_type]["y"]


class VaultIcon(arcade.Sprite):
    def __init__(
        self,
        filename,
        item_referenced,
        vault_icon_list,
        scale=ICON_SCALE,
    ):
        super().__init__(filename, scale)
        self.filename = filename
        self.item_referenced = item_referenced
        self.pos = 0
        self.vault_icon_list = vault_icon_list
        self.set_vault_position()

    def set_vault_position(self):
        sorted_vault_list = [icon.pos for icon in self.vault_icon_list]
        sorted_vault_list.sort()
        if len(sorted_vault_list) >= 1:
            if self.missing_elements(sorted_vault_list):
                self.pos = min(self.missing_elements(sorted_vault_list))
            else:
                self.pos = max(sorted_vault_list) + 1

    def missing_elements(self, sorted_inv_list):
        start, end = sorted_inv_list[0], sorted_inv_list[-1]
        return sorted(set(range(0, end + 1)).difference(sorted_inv_list))
