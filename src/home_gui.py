from constants import *

import arcade
from arcade import Sprite, color


class RightPanel(arcade.Sprite):
    def __init__(
        self,
        button_list,
        filename=":assets:gui/right_side_bar.png",
        scale=HOME_RIGHT_PANEL,
    ):
        super().__init__(filename, scale)
        self.center_x = GAME_WIDTH - 30
        self.center_y = GAME_HEIGHT / 2
        self.generate_buttons(button_list)

    @classmethod
    def generate_buttons(cls, button_list):
        """Generates the buttons and button panel on the right of the home screen"""
        buttons = ["inventory", "vault", "trade", "upgrade", "portals", "fight"]
        height = 136
        for button in range(len(buttons)):
            menu_button = MenuButton(
                buttons[button],
                f":assets:gui/button/{buttons[button]}.png",
            )
            menu_button.center_x = GAME_WIDTH - 29
            menu_button.center_y = GAME_HEIGHT / 2 + height
            button_list.append(menu_button)
            height -= 54


class HandCursor(arcade.Sprite):
    def __init__(self, filename=":assets:cursor/glove_point.png", scale=CURSOR_SCALE):
        super().__init__(filename, scale)
        self.set_hit_box([[-14, 0], [-35, 40], [10, 10]])
        self.holding_icon = False
        self.icon_held: Sprite = False  # type: ignore

    def grab_icon(self):
        if self.holding_icon:
            arcade.draw_lrwh_rectangle_textured(
                self.center_x - self.icon_held.width / 2 - 5,
                self.center_y - self.icon_held.height / 2 + 10,
                self.icon_held.width,
                self.icon_held.height,
                self.icon_held.texture,
            )

    def set_cursor_position(self, x, y):
        self.center_x = x
        self.center_y = y

    def attempt_icon_hold(self, window, *args):
        """Checks to see if the cursor is capable of holding onto an item's icon. If an item icon is capable of being
        held, it will transfer the item's data into the cursor_hand object"""
        if window.open:
            collision = arcade.check_for_collision_with_lists(
                self,
                args,
            )
            if collision:
                self.holding_icon = True
                for icon in collision:
                    self.icon_held = icon
            else:
                self.icon_held = None

    def point(self):
        self.texture = arcade.load_texture(":assets:cursor/glove_point.png")

    def grab(self):
        self.texture = arcade.load_texture(":assets:cursor/glove_grab.png")

    def reset(self):
        self.holding_icon = False
        self.icon_held = None
        self.point()


class MenuButton(arcade.Sprite):
    def __init__(self, description, filename, scale=RIGHT_BUTTON_SCALE):
        super().__init__(filename, scale)
        self.description = description
        self.state = False

    def display_clicked(self):
        if self.state:
            arcade.draw_rectangle_outline(
                self.center_x, self.center_y, 54, 54, color.GOLD, 3
            )

    @classmethod
    def deactivate_all_buttons(cls, button_list):
        """Deactivates all buttons"""
        for button in button_list:
            button.state = False


class ItemStatPopup(arcade.Sprite):
    def __init__(
        self, cursor, inv_icon_list, vault_icon_list, inv_slot_icon_list, showing=False
    ):
        super().__init__()
        self.showing = showing
        self.cursor = cursor
        self.inv_icon_list = inv_icon_list
        self.vault_icon_list = vault_icon_list
        self.inv_slot_icon_list = inv_slot_icon_list

    def show(self):
        self.showing = True

    def hide(self):
        self.showing = False

    def item_background_popup_display(self):
        """Upon pressing the required key and hovering over an item this popup will appear as a background for the item
        stats to be drawn on"""
        if self.showing:
            collision = arcade.check_for_collision_with_lists(
                self.cursor,
                (
                    self.inv_icon_list,
                    self.vault_icon_list,
                    self.inv_slot_icon_list,
                ),
            )
            for icon in collision:
                arcade.draw_texture_rectangle(
                    icon.center_x,
                    icon.center_y + 100,
                    200,
                    150,
                    arcade.load_texture(":assets:gui/item_popup_background.png"),
                )
                arcade.Text(
                    icon.item_referenced.name.title().replace("_", " "),
                    icon.center_x - 85,
                    icon.center_y + 145,
                    color.BLEU_DE_FRANCE,
                    14,
                    bold=True,
                    align="center",
                    width=170,
                ).draw()
                y_offset = 120
                for stat, value in icon.item_referenced.stats.items():
                    arcade.Text(
                        f"{stat}: {value}",
                        icon.center_x - 75,
                        icon.center_y + y_offset,
                        color.WHITE,
                        12,
                        align="center",
                        width=150,
                    ).draw()
                    y_offset -= 25


class Portrait(arcade.Sprite):
    def __init__(self, filename=":assets:gui/portraits/23.png", scale=PORTRAIT_SCALE):
        super().__init__(filename, scale)
        self.center_x = 115
        self.center_y = GAME_HEIGHT - 90


class PortraitFrame(arcade.Sprite):
    def __init__(
        self,
        filename=":assets:gui/portrait_frame/portrait_frame.png",
        scale=PORTRAIT_PANEL_SCALE,
    ):
        super().__init__(filename, scale)
        self.center_x = 280
        self.center_y = GAME_HEIGHT - 89


class Vault(arcade.Sprite):
    def __init__(self, filename=":assets:gui/vault.png", scale=VAULT_SCALE, open=False):
        super().__init__(filename, scale)
        self.open = open
        self.mapped_carry_positions: dict = self.map_carry_positions()

    def position_icons(self, icon_list):
        if icon_list:
            for icon in icon_list:
                icon.center_x = self.mapped_carry_positions[icon.pos]["x"]
                icon.center_y = self.mapped_carry_positions[icon.pos]["y"]

    def display_positions(self):
        for v in self.mapped_carry_positions.values():
            arcade.draw_rectangle_outline(
                v["x"], v["y"], v["width"], v["height"], color=color.LAVA
            )

    def display(self):
        """Displays and positions the vault window"""
        self.open = True
        self.position_vault_window()

    def position_vault_window(self):
        """Positions the vault window"""
        self.center_x = GAME_WIDTH - self.width / 2 - 65
        self.center_y = GAME_HEIGHT / 2

    def deactivate(self):
        """Deactivates the vault window display"""
        self.open = False

    def refresh(self, vault_icon_list):
        """Refreshes and repositions the current location of the icons within the inventory window"""
        self.position_icons(vault_icon_list)

    def map_carry_positions(self):
        # FIXME This function is trash but works.....
        center_x = 713
        center_y = 594
        width_step = 63
        width = 60
        height = 60
        map_data = dict()
        for count in range(63):
            if count >= 0 and count <= 6:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }

            if count == 7:
                center_x = 713
                center_y = 530

            if count >= 7 and count <= 13:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }

            if count == 14:
                center_x = 713
                center_y = 467

            if count >= 14 and count <= 20:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }

            if count == 21:
                center_x = 713
                center_y = 404

            if count >= 21 and count <= 27:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }

            if count == 28:
                center_x = 713
                center_y = 341

            if count >= 28 and count <= 34:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }

            if count == 35:
                center_x = 713
                center_y = 278

            if count >= 35 and count <= 41:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }

            if count == 42:
                center_x = 713
                center_y = 215

            if count >= 42 and count <= 48:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }

            if count == 49:
                center_x = 713
                center_y = 152

            if count >= 49 and count <= 55:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }

            if count == 56:
                center_x = 713
                center_y = 89

            if count >= 56 and count <= 62:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }
        return map_data


class Inventory(arcade.Sprite):
    def __init__(
        self, filename=":assets:gui/inventory.png", scale=INVENTORY_SCALE, open=False
    ):
        super().__init__(filename, scale)
        self.open = open
        self.mapped_carry_positions: dict = self.map_carry_positions()
        self.mapped_slot_positions: dict = self.map_slot_positions()
        self.total_item_stats = {}

    def position_icons(self, icon_list):
        if icon_list:
            for icon in icon_list:
                icon.center_x = self.mapped_carry_positions[icon.pos]["x"]
                icon.center_y = self.mapped_carry_positions[icon.pos]["y"]

    def display_positions(self):
        for v in self.mapped_carry_positions.values():
            arcade.draw_rectangle_outline(
                v["x"], v["y"], v["width"], v["height"], color=color.GREEN
            )

        for v in self.mapped_slot_positions.values():
            arcade.draw_rectangle_outline(
                v["x"], v["y"], v["width"], v["height"], color=color.RUBY
            )

    def display(self):
        """Displays and positions the inventory window"""
        self.open = True
        self.position_inventory_window()

    def position_inventory_window(self):
        """Positions the inventory window"""
        self.center_x = GAME_WIDTH - self.width / 2 - 65
        self.center_y = GAME_HEIGHT / 2

    def deactivate(self):
        """Deactivates the inventory window display"""
        self.open = False

    def refresh(self, inventory_icon_list):
        """Refreshes and repositions the current location of the icons within the inventory window"""
        if self.open:
            self.position_icons(inventory_icon_list)

    def map_slot_positions(self):
        width = 62
        height = 62
        map_data = dict()
        map_data["Head"] = {"x": 1058, "y": 610, "width": width, "height": height}
        map_data["Cloak"] = {"x": 1133, "y": 610, "width": width, "height": height}
        map_data["Shoulder"] = {
            "x": 982,
            "y": 540,
            "width": width,
            "height": height,
        }
        map_data["Body"] = {"x": 1058, "y": 540, "width": width, "height": height}
        map_data["Necklace"] = {
            "x": 1133,
            "y": 540,
            "width": width,
            "height": height,
        }
        map_data["Gloves"] = {"x": 982, "y": 470, "width": width, "height": height}
        map_data["Belt"] = {"x": 1058, "y": 470, "width": width, "height": height}
        map_data["MainHand"] = {"x": 982, "y": 400, "width": width, "height": height}
        map_data["Legs"] = {"x": 1058, "y": 402, "width": width, "height": height}
        map_data["Offhand"] = {"x": 1133, "y": 400, "width": width, "height": height}
        map_data["Ring1"] = {"x": 982, "y": 330, "width": width, "height": height}
        map_data["Boots"] = {"x": 1058, "y": 331, "width": width, "height": height}
        map_data["Ring2"] = {"x": 1133, "y": 331, "width": width, "height": height}

        return map_data

    def map_carry_positions(self):
        # FIXME clean this function up
        center_y = 235
        width_step = 63
        width = 60
        height = 60
        map_data = dict()
        center_x = 712
        for count in range(21):
            if count >= 0 and count <= 6:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }
            if count == 7:
                center_x = 712
                center_y = 170
            if count >= 7 and count <= 13:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }
            if count == 14:
                center_x = 712
                center_y = 105
            if count >= 14 and count <= 21:
                center_x += width_step
                map_data[count] = {
                    "x": center_x,
                    "y": center_y,
                    "width": width,
                    "height": height,
                }

        return map_data

    def calculate_total_item_stats(self, equipped_list):
        """Calculates the current item stats for both weapons and armor to be used for display in the inventory"""
        self.total_item_stats = {}
        for item in equipped_list:
            for stat, value in item.stats.items():
                if self.total_item_stats.get(stat):
                    self.total_item_stats[stat] += value
                else:
                    self.total_item_stats[stat] = value

    def display_total_item_stats(self):
        """Displays the total item stats. This will differentiate between weapons and armor. Also it will display
        the various stats with their respective colors."""
        armor_starting_height = GAME_HEIGHT - 130
        weapon_starting_height = GAME_HEIGHT - 320

        armor_text_y = armor_starting_height
        weapon_text_y = weapon_starting_height
        stat_x_pos = 770

        if self.total_item_stats:
            for stat, value in self.total_item_stats.items():
                stat_name = stat.lower()
                if stat_name in ["health", "armor"]:
                    if stat_name == "health":
                        arcade.Text(
                            f"{stat}: {value}",
                            stat_x_pos,
                            armor_text_y,
                            color.RED_PURPLE,
                            12,
                            align="left",
                        ).draw()
                    elif stat_name == "armor":
                        arcade.Text(
                            f"{stat}: {value}",
                            stat_x_pos,
                            armor_text_y,
                            color.ASH_GREY,
                            12,
                            align="left",
                        ).draw()
                    armor_text_y -= 35
                else:
                    if stat_name == "base damage":
                        arcade.Text(
                            f"{stat}: {value}",
                            stat_x_pos,
                            weapon_text_y,
                            color.ASH_GREY,
                            12,
                            align="left",
                        ).draw()
                    elif stat_name == "fire damage":
                        arcade.Text(
                            f"{stat}: {value}",
                            stat_x_pos,
                            weapon_text_y,
                            color.RED,
                            12,
                            align="left",
                        ).draw()
                    elif stat_name == "ice damage":
                        arcade.Text(
                            f"{stat}: {value}",
                            stat_x_pos,
                            weapon_text_y,
                            color.CYAN,
                            12,
                            align="left",
                        ).draw()
                    weapon_text_y -= 35
