import random
from dataclasses import dataclass

from player import Player
from gui import *
from icon import *
from item_local_map import item_map

import arcade
from arcade import key


@dataclass
class Item:
    name: str
    stats: dict


class HomeView(arcade.View):
    def __init__(self):
        super().__init__()
        # Background image will be stored in this variable
        self.background = None
        self.time_of_day = 255
        self.daylight = True

        # View variables
        self.current_cursor_posx = 0
        self.current_cursor_posy = 0

        # Sprite lists
        self.player_list = None
        self.static_gui_list = None
        self.right_side_button_list = None
        self.inventory_list = None
        self.vault_list = None

        # Equipped lists
        self.equipped_list = None

        # Icons lists
        self.inventory_icon_list = None
        self.inventory_icon_slot_list = None

        # Sprite variables
        self.player = None
        self.cursor_hand = None
        self.inventory_window = None
        self.vault_window = None
        self.portrait_frame = None
        self.portrait = None
        self.total_item_stats = None

    def setup(self):

        # Sprite lists
        self.inventory_list = arcade.SpriteList()
        self.inventory_slot_list = arcade.SpriteList()
        self.vault_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.static_gui_list = arcade.SpriteList()
        self.right_side_button_list = arcade.SpriteList()

        self.equipped_list = arcade.SpriteList()

        self.inventory_icon_list = arcade.SpriteList()
        self.inventory_icon_slot_list = arcade.SpriteList()

        # Create sprites
        self.cursor_hand = HandCursor(":assets:cursor/glove_point.png", CURSOR_SCALE)
        self.player = Player(":assets:base/demigod_male.png", PLAYER_SCALE)
        self.player_list.append(self.player)

        self.generate_test_items()  # item test creation

        # Generate GUI
        self.portrait_frame = PortraitFrame(
            ":assets:gui/portrait_frame/portrait_frame.png", PORTRAIT_PANEL_SCALE
        )
        self.portrait = Portrait(":assets:gui/portraits/23.png", PORTRAIT_SCALE)
        self.background = arcade.load_texture(":assets:background/4.png")
        self.generate_home_right_panel()

    def on_draw(self):
        self.window.apply_gui_camera()
        self.clear()
        self.window.apply_game_camera()

        self.timed_lighting_with_background()
        self.portrait.draw(pixelated=True)
        self.portrait_frame.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        self.static_gui_list.draw(pixelated=True)
        self.right_side_button_list.draw(pixelated=True)

        self.equipped_list.draw(pixelated=True)

        if self.inventory_window:
            self.inventory_window.draw(pixelated=True)
            # self.inventory_window.display_positions()  # debugging visual
            self.inventory_icon_list.draw(pixelated=True)
            self.inventory_icon_slot_list.draw(pixelated=True)
            self.display_total_item_stats()

        if self.vault_window:
            self.vault_window.draw(pixelated=True)
            # self.vault_window.display_positions()  # debugging visual

        for button in self.right_side_button_list:
            if button.state:
                button.display_clicked()

        if self.cursor_hand.holding_icon:
            self.cursor_hand.grab_icon()

        self.vault_list.draw(pixelated=True)

        self.cursor_hand.draw()

        # self.cursor_hand.draw_hit_box(color=arcade.color.RED, line_thickness=1)  # debug visual

    def on_update(self, delta_time):
        # List updates
        self.vault_list.update()
        self.player_list.update()
        self.static_gui_list.update()
        self.right_side_button_list.update()

        self.equipped_list.update()

        self.inventory_icon_list.update()
        self.inventory_icon_slot_list.update()

        # Individual sprite updates
        self.cursor_hand.on_update()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.set_cursor_position(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.cursor_hand = HandCursor(":assets:cursor/glove_grab.png", CURSOR_SCALE)
            self.set_cursor_position(x, y)
            self.right_panel_onclick_actions()
            self.cursor_holding_icon_check()

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.inv_icon_to_equip_check(x, y)
            self.slot_icon_to_inv_check()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.cursor_hand.icon_held:
                self.icon_drop_swap(x, y)
            self.cursor_hand = HandCursor(
                ":assets:cursor/glove_point.png", CURSOR_SCALE
            )
            self.set_cursor_position(x, y)

        if button == arcade.MOUSE_BUTTON_RIGHT:
            pass

    def set_cursor_position(self, x, y):
        self.cursor_hand.center_x = x
        self.cursor_hand.center_y = y

    def on_key_press(self, key, modifiers):
        self.window_key_router(key)

        # FIXME key x is test
        if key == arcade.key.X:
            self.generate_test_server_items()
            if self.inventory_window:
                self.inventory_window.position_icons(self.inventory_icon_list)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        pass

    def display_total_item_stats(self):
        self.total_item_stats = dict()
        for item in self.equipped_list:
            for stat, value in item.stats.items():
                if self.total_item_stats.get(stat):
                    self.total_item_stats[stat] += value
                else:
                    self.total_item_stats[stat] = value

        if self.total_item_stats:
            x = GAME_WIDTH - self.inventory_window.width
            y = GAME_HEIGHT - 100
            for stat, value in self.total_item_stats.items():
                arcade.Text(f'{stat}: {value}', x, y, arcade.color.WHITE, 15, 5).draw()
                y -= 35

    def cursor_holding_icon_check(self):
        collision = arcade.check_for_collision_with_list(
            self.cursor_hand, self.inventory_icon_list
        )
        if collision:
            self.cursor_hand.holding_icon = True
            for icon in collision:
                self.cursor_hand.icon_held = icon

    def slot_icon_to_inv_check(self):
        collision_slot_icon = arcade.check_for_collision_with_list(
            self.cursor_hand, self.inventory_icon_slot_list
        )
        if collision_slot_icon:
            for icon in collision_slot_icon:
                new_inv_icon = InventoryIcon(
                    icon.filename, icon.item_referenced, self.inventory_icon_list
                )
                self.inventory_icon_list.append(new_inv_icon)
                icon.item_referenced.kill()
                icon.kill()
                self.refresh_all_windows()

    def inv_icon_to_equip_check(self, x, y):
        collision_icon = arcade.check_for_collision_with_list(
            self.cursor_hand, self.inventory_icon_list
        )
        if collision_icon:
            for icon in collision_icon:
                self.equip_item_to_player(icon)
                self.cursor_hand = HandCursor(
                    ":assets:cursor/glove_point.png", CURSOR_SCALE
                )
                self.set_cursor_position(x, y)

    def timed_lighting_with_background(self):
        if self.daylight:
            self.time_of_day -= DAYLIGHT_SPEED
            if self.time_of_day < 1:
                self.daylight = False
        else:
            self.time_of_day += DAYLIGHT_SPEED
            if self.time_of_day == 255:
                self.daylight = True
        arcade.draw_lrwh_rectangle_textured(
            0,
            0,
            GAME_WIDTH,
            GAME_HEIGHT,
            self.background,
            alpha=round(self.time_of_day),
        )

    def generate_home_right_panel(self):
        self.right_side_bar = arcade.Sprite(":assets:gui/right_side_bar.png", 1.5)
        self.position_home_right_panel()
        self.static_gui_list.append(self.right_side_bar)

        buttons = ["inventory", "vault", "trade", "blacksmith", "portals", "fight"]
        height = 136
        for button in range(len(buttons)):
            self.button = MenuButton(
                buttons[button],
                f":assets:gui/button/{buttons[button]}.png",
                RIGHT_BUTTON_SCALE,
            )
            self.button.center_x = GAME_WIDTH - 29
            self.button.center_y = GAME_HEIGHT / 2 + height
            self.right_side_button_list.append(self.button)
            height -= 54

    def right_panel_onclick_actions(self):
        for button in arcade.check_for_collision_with_list(
            self.cursor_hand, self.right_side_button_list
        ):
            if button.state:
                self.deactivate_all_buttons_windows()
            else:
                self.deactivate_all_buttons_windows()
                button.state = True
                if button.description == "inventory":
                    self.inventory_display()
                    self.inventory_window.position_icons(self.inventory_icon_list)
                elif button.description == "vault":
                    self.vault_window_display()
                elif button.description == "trade":
                    print("Trading")
                elif button.description == "blacksmith":
                    print("blacksmithing")
                elif button.description == "portals":
                    print("portaling")
                elif button.description == "fight":
                    print("fighting")

    def position_home_right_panel(self):
        self.right_side_bar.center_x = GAME_WIDTH - 30
        self.right_side_bar.center_y = GAME_HEIGHT / 2

    def inventory_display(self):
        self.inventory_window = Inventory(
            ":assets:gui/inventory.png", INGAME_WINDOW_SCALE
        )
        self.position_inventory()
        self.right_side_button_list[0].state = True

    def refresh_inventory_window(self):
        if self.inventory_window:
            self.inventory_window.position_icons(self.inventory_icon_list)

    def inventory_deactivate(self):
        self.inventory_window = None

    def position_inventory(self):
        self.inventory_window.center_x = (
            GAME_WIDTH - self.inventory_window.width / 2 - 65
        )
        self.inventory_window.center_y = GAME_HEIGHT / 2

    def vault_window_display(self):
        self.vault_window = Vault(":assets:gui/vault.png", INGAME_WINDOW_SCALE)
        self.position_vault_window()
        self.right_side_button_list[1].state = True

    def position_vault_window(self):
        self.vault_window.center_x = GAME_WIDTH - self.vault_window.width / 2 - 65
        self.vault_window.center_y = GAME_HEIGHT / 2

    def vault_window_deactivate(self):
        self.vault_window = None

    def deactivate_all_windows(self):
        self.inventory_deactivate()
        self.vault_window_deactivate()

    def deactivate_all_buttons(self):
        for other_buttons in self.right_side_button_list:
            other_buttons.state = False

    def deactivate_all_buttons_windows(self):
        self.deactivate_all_windows()
        self.deactivate_all_buttons()

    def refresh_all_windows(self):
        if self.inventory_window:
            self.refresh_inventory_window()

    def window_key_router(self, key):
        # TODO refactor this into a clean function
        if key == arcade.key.I:
            if self.inventory_window:
                self.deactivate_all_buttons_windows()
            elif [button.state for button in self.right_side_button_list]:
                self.deactivate_all_buttons_windows()
                self.inventory_display()
                self.inventory_window.position_icons(self.inventory_icon_list)

        if key == arcade.key.V:
            if self.vault_window:
                self.deactivate_all_buttons_windows()
            elif [button.state for button in self.right_side_button_list]:
                self.deactivate_all_buttons_windows()
                self.vault_window_display()

        if key == arcade.key.T:
            print("trade")

        if key == arcade.key.B:
            print("blacksmith")

        if key == arcade.key.P:
            print("portals")

        if key == arcade.key.F:
            print("fight")

    def icon_drop_swap(self, cursor_x, cursor_y):
        collision = arcade.check_for_collision_with_list(
            self.cursor_hand, self.inventory_icon_list
        )
        if collision:
            for icon in collision:
                self.cursor_hand.icon_held.center_x, icon.center_x = (
                    icon.center_x,
                    self.cursor_hand.icon_held.center_x,
                )
                self.cursor_hand.icon_held.center_y, icon.center_y = (
                    icon.center_y,
                    self.cursor_hand.icon_held.center_y,
                )
                self.cursor_hand.icon_held.inv_pos, icon.inv_pos = (
                    icon.inv_pos,
                    self.cursor_hand.icon_held.inv_pos,
                )
                index1 = self.inventory_icon_list.index(self.cursor_hand.icon_held)
                index2 = self.inventory_icon_list.index(icon)
                self.inventory_icon_list[index1], self.inventory_icon_list[index2] = (
                    self.inventory_icon_list[index1],
                    self.inventory_icon_list[index2],
                )
        else:
            for (
                inv_number,
                icon_mapped_data,
            ) in self.inventory_window.mapped_carry_positions.items():
                if (
                    cursor_x >= icon_mapped_data["x"]
                    and cursor_x <= icon_mapped_data["x"] + icon_mapped_data["width"]
                    and cursor_y <= icon_mapped_data["y"]
                    and cursor_y >= icon_mapped_data["y"] - icon_mapped_data["height"]
                    and inv_number
                    not in [icon.inv_pos for icon in self.inventory_icon_list]
                ):
                    self.cursor_hand.icon_held.inv_pos = inv_number

        self.refresh_all_windows()
        self.cursor_hand = HandCursor(":assets:cursor/glove_point.png", CURSOR_SCALE)
        self.set_cursor_position(cursor_x, cursor_y)

    def equip_item_to_player(self, icon):
        item_type = type(icon.item_referenced)
        if isinstance(icon.item_referenced, item_type):
            if any(isinstance(equipped, item_type) for equipped in self.equipped_list):
                self.equip_swap(icon, item_type)
            else:
                self.equip_empty_slot(icon)

        self.refresh_all_windows()
        icon.kill()

    def equip_empty_slot(self, icon):
        self.equipped_list.append(icon.item_referenced)
        slot_icon = InventorySlotIcon(
            icon.item_referenced.icon_image,
            ICON_SCALE,
            icon.item_referenced,
            inv_window=self.inventory_window,
        )
        self.inventory_icon_slot_list.append(slot_icon)

    def equip_swap(self, icon, item_type):
        """If the player equips a new item with the same type, it will kill the icon in that slot and
        create the a new item icon in its place. It will also kill the equipment on the player and
        create an equipment icon in the inventory in its place."""

        # FIXME simplify this complex function
        # gets the old equipped item
        for item in self.equipped_list:
            if isinstance(item, item_type):
                old_equipped_item = item
                break

        new_equipped_item = icon.item_referenced
        self.equipped_list.append(new_equipped_item)

        new_slot_icon = InventorySlotIcon(
            icon.item_referenced.icon_image,
            ICON_SCALE,
            icon.item_referenced,
            inv_window=self.inventory_window,
        )

        for old_slot_icon in self.inventory_icon_slot_list:
            if isinstance(old_slot_icon.item_referenced, item_type):
                old_slot_icon.kill()

        self.inventory_icon_slot_list.append(new_slot_icon)

        old_icon = InventoryIcon(
            filename=old_equipped_item.icon_image,
            scale=ICON_SCALE,
            item_referenced=old_equipped_item,
            inventory_icon_list=self.inventory_icon_list,
        )
        old_icon.inv_pos = icon.inv_pos
        self.inventory_icon_list.append(old_icon)
        old_equipped_item.kill()

    def create_item_and_icon(self, test_item_data):
        name = test_item_data.name
        image = item_map[name]["image"]
        icon = item_map[name]["icon"]
        item_type = item_map[name]["type"]
        stats = test_item_data.stats

        item = item_type(
            image,
            icon,
            self.player,
            stats,
        )
        icon = InventoryIcon(
            item.icon_image,
            item,
            self.inventory_icon_list,
        )
        self.inventory_icon_list.append(icon)

    # --------------------------------- Item generation functions used for testing -------------------
    def generate_test_server_items(self):
        test_server_items = [
            Item(
                name="black_horn",
                stats={
                    "Health": random.randint(1, 10),
                    "Armor": random.randint(1, 10),
                },
            ),
            Item(
                name="coat_red",
                stats={
                    "Health": random.randint(1, 10),
                    "Armor": random.randint(1, 10),
                },
            ),
            Item(
                name="red_legs",
                stats={
                    "Health": random.randint(1, 10),
                    "Armor":  random.randint(1, 10),
                },
            ),
            Item(
                name="robe_blue",
                stats={
                    "Health": random.randint(1, 10),
                    "Armor": random.randint(1, 10),
                },
            ),
            Item(
                name="axe_executioner",
                stats={
                    "Base damage": random.randint(1, 10),
                    "Fire damage": random.randint(1, 10),
                },
            ),
        ]
        for item in test_server_items:
            self.create_item_and_icon(item)

    def generate_test_items(self):
        pass


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(GAME_WIDTH, GAME_HEIGHT, WINDOW_TITLE, resizable=True)
        self.views = {}
        self.set_min_size(GAME_WIDTH, GAME_HEIGHT)
        self._fullscreen = False

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == key.F11:
            if self.fullscreen:
                # Will revert back to window mode using the window's
                # original size (before fullscreen)
                self.set_fullscreen(False)
            else:
                # By default this enters fullscreen with the primary
                # monitor's native screen size
                self.set_fullscreen(True)

    def apply_game_camera(self):
        """
        Apply a camera for the game contents.
        This is temporary until we have a proper camera.
        """
        # Set the viewport taking aspect ratio into account.
        # We add black borders horizontally and vertically if needed
        expected_width = int(self.height * GAME_ASPECT_RATIO)
        expected_height = int(expected_width / GAME_ASPECT_RATIO)

        if expected_width > self.width:
            expected_width = self.width
            expected_height = int(expected_width / GAME_ASPECT_RATIO)

        blank_space_x = self.width - expected_width
        blank_space_y = self.height - expected_height

        self.ctx.viewport = (
            blank_space_x // 2,
            blank_space_y // 2,
            expected_width,
            expected_height,
        )

        # The projection is constant regardless if window size.
        # We're simply projecting the same geometry into a larger screen area.
        self.ctx.projection_2d = 0, GAME_WIDTH, 0, GAME_HEIGHT

    def apply_gui_camera(self):
        """
        Apply a camera covering the entire screen regardless
        of game size. This was mainly intended for the mouse cursor
        and possibly drawing some nice border graphics when needed.
        """
        self.ctx.viewport = 0, 0, self.width, self.height
        self.ctx.projection_2d = 0, self.width, 0, self.height


def main():
    arcade.resources.add_resource_handle("assets", ASSETS_PATH)
    window = GameWindow()
    window.center_window()
    home_view = HomeView()
    home_view.setup()
    window.set_mouse_visible(False)
    window.show_view(home_view)
    window.set_location(500, 100)
    arcade.run()


if __name__ == "__main__":
    main()
