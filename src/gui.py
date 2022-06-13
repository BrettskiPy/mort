from constants import *

import arcade


class HandCursor(arcade.Sprite):
    def __init__(self, filename, scale=CURSOR_SCALE):
        super().__init__(filename, scale)
        self.set_hit_box([[-14, 0], [-35, 40], [10, 10]])
        self.holding_icon = False
        self.icon_held = None

    def grab_icon(self):
        if self.holding_icon:
            arcade.draw_lrwh_rectangle_textured(
                self.center_x - self.icon_held.width / 2 - 5,
                self.center_y - self.icon_held.height / 2 + 10,
                self.icon_held.width,
                self.icon_held.height,
                self.icon_held.texture,
            )


class MenuButton(arcade.Sprite):
    def __init__(self, description, filename, scale):
        super().__init__(filename, scale)
        self.description = description
        self.state = False

    def display_clicked(self):
        if self.state:
            arcade.draw_rectangle_outline(
                self.center_x, self.center_y, 54, 54, arcade.color.GOLD, 3
            )


class Portrait(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.center_x = 115
        self.center_y = GAME_HEIGHT - 90


class PortraitFrame(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.center_x = 280
        self.center_y = GAME_HEIGHT - 89


class Vault(arcade.Sprite):
    def __init__(self, filename, scale=CURSOR_SCALE, open=False):
        super().__init__(filename, scale)
        self.open = open
        self.mapped_carry_positions = self.mapped_carry_positions()

    def display_positions(self):
        for v in self.mapped_carry_positions.values():
            arcade.draw_rectangle_outline(
                v["x"], v["y"], v["width"], v["height"], color=arcade.color.LAVA
            )

    def mapped_carry_positions(self):
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
    def __init__(self, filename, scale=CURSOR_SCALE, open=False):
        super().__init__(filename, scale)
        self.open = open
        self.mapped_carry_positions = self.mapped_carry_positions()
        self.mapped_slot_positions = self.mapped_slot_positions()

    def position_icons(self, icon_list):
        if icon_list:
            for icon in icon_list:
                icon.center_x = self.mapped_carry_positions[icon.inv_pos]["x"]
                icon.center_y = self.mapped_carry_positions[icon.inv_pos]["y"]

    def display_positions(self):
        for v in self.mapped_carry_positions.values():
            arcade.draw_rectangle_outline(
                v["x"], v["y"], v["width"], v["height"], color=arcade.color.GREEN
            )

        for v in self.mapped_slot_positions.values():
            arcade.draw_rectangle_outline(
                v["x"], v["y"], v["width"], v["height"], color=arcade.color.RUBY
            )

    def mapped_slot_positions(self):
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

    def mapped_carry_positions(self):
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
