import random
from dataclasses import dataclass

from player import Player
from gui import *
from icon import *
from item_local_map import item_map
from game_window import GameWindow
from animation import Fire

import arcade

# TODO remove this when server is done
@dataclass
class Item:
    name: str
    stats: dict


class HomeView(arcade.View):
    def __init__(self):
        super().__init__()

        # Background image will be stored in this variable
        self.background = None

        # Local game states
        self.time_of_day = 255
        self.daylight = True
        self.upgrading = False
        self.upgrade_pentagram = None

        # Sprite lists
        self.player_list = None
        self.static_gui_list = None
        self.right_side_button_list = None
        self.inventory_list = None

        # fire animation preloading
        self.fire = False
        self.fire_list = None
        self.fire_texture_list = []
        file_name = ":assets:/animations/particlefx_14.png"
        self.fire_texture_list = arcade.load_spritesheet(file_name, 128, 128, 8, 64)

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
        self.item_popup_background = None

        # Sound and music
        self.music_player = None
        self.music_volume = 1
        self.sound = None
        self.sound_volume = 0.5

    def setup(self):

        # Sprite lists
        self.inventory_list = arcade.SpriteList()
        self.inventory_slot_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.static_gui_list = arcade.SpriteList()
        self.right_side_button_list = arcade.SpriteList()
        self.equipped_list = arcade.SpriteList()
        self.inventory_icon_list = arcade.SpriteList()
        self.inventory_icon_slot_list = arcade.SpriteList()
        # Sprite animation lists
        self.fire_list = arcade.SpriteList()

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
        self.upgrade_pentagram = arcade.Sprite(
            ":assets:gui/upgrade_area/pentagram.png",
            0.9,
            center_x=375,
            center_y=GAME_HEIGHT / 2 - 75,
        )

        # Sound and Music
        self.music_player = arcade.Sound(
            file_name=":assets:music/the_field_of_dreams.mp3", streaming=True
        ).play(loop=True, speed=0.6)

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
        # FIXME have this sort by the proper draw order when equipment gets added to the list
        self.equipped_list.draw(pixelated=True)

        if self.upgrading:
            self.upgrade_pentagram.draw(pixelated=True)

        if self.inventory_window:
            self.inventory_window.draw(pixelated=True)
            # self.inventory_window.display_positions()  # debugging visual
            self.inventory_icon_list.draw(pixelated=True)
            self.inventory_icon_slot_list.draw(pixelated=True)
            self.display_total_item_stats()
            if self.item_popup_background:
                self.item_background_popup_show()

        if self.vault_window:
            self.vault_window.draw(pixelated=True)
            # self.vault_window.display_positions()  # debugging visual

        for button in self.right_side_button_list:
            if button.state:
                button.display_clicked()

        if self.cursor_hand.holding_icon:
            self.cursor_hand.grab_icon()

        self.cursor_hand.draw()

        # draw animations

        self.fire_list.draw()

        # self.cursor_hand.draw_hit_box(color=arcade.color.RED, line_thickness=1)  # debug visual

    def on_update(self, delta_time):
        # List updates
        self.equipped_list.update()

        # Individual sprite updates
        self.cursor_hand.on_update()

        self.fire_list.update()
        if self.fire:
            # Make an explosion
            explosion = Fire(self.fire_texture_list)

            # Move it to the location of the coin
            explosion.center_x = 370
            explosion.center_y = 300

            # Call update() because it sets which image we start on
            explosion.update()

            # Add to a list of sprites that are explosions
            self.fire_list.append(explosion)

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
            self.calculate_total_item_stats()

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

    def on_key_press(self, key, modifiers):
        self.window_key_router(key)

        # FIXME key x is test
        if key == arcade.key.X:
            self.generate_test_server_items()
            if self.inventory_window:
                self.inventory_window.position_icons(self.inventory_icon_list)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LCTRL:
            self.item_popup_background = False

        if key == arcade.key.T:
            self.fire = False

    def set_cursor_position(self, x, y):
        self.cursor_hand.center_x = x
        self.cursor_hand.center_y = y

    def item_background_popup_show(self):
        if self.item_popup_background:
            collision = arcade.check_for_collision_with_list(
                self.cursor_hand, self.inventory_icon_list
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
                    arcade.color.BLEU_DE_FRANCE,
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
                        arcade.color.WHITE,
                        12,
                        align="center",
                        width=150,
                    ).draw()
                    y_offset -= 25

    def calculate_total_item_stats(self):
        self.total_item_stats = dict()
        for item in self.equipped_list:
            for stat, value in item.stats.items():
                if self.total_item_stats.get(stat):
                    self.total_item_stats[stat] += value
                else:
                    self.total_item_stats[stat] = value

    def display_total_item_stats(self):
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
                            arcade.color.RED_PURPLE,
                            12,
                            align="left",
                        ).draw()
                    elif stat_name == "armor":
                        arcade.Text(
                            f"{stat}: {value}",
                            stat_x_pos,
                            armor_text_y,
                            arcade.color.ASH_GREY,
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
                            arcade.color.ASH_GREY,
                            12,
                            align="left",
                        ).draw()
                    elif stat_name == "fire damage":
                        arcade.Text(
                            f"{stat}: {value}",
                            stat_x_pos,
                            weapon_text_y,
                            arcade.color.RED,
                            12,
                            align="left",
                        ).draw()
                    elif stat_name == "ice damage":
                        arcade.Text(
                            f"{stat}: {value}",
                            stat_x_pos,
                            weapon_text_y,
                            arcade.color.CYAN,
                            12,
                            align="left",
                        ).draw()
                    weapon_text_y -= 35

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
                self.sound = arcade.Sound(":assets:sounds/inventory/equip.mp3").play(
                    volume=self.sound_volume
                )

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

        buttons = ["inventory", "vault", "trade", "upgrade", "portals", "fight"]
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
                    self.vault_display()
                elif button.description == "trade":
                    print("Trading")
                elif button.description == "upgrade":
                    print("upgrading")
                    self.background = arcade.load_texture(
                        ":assets:background/plain_black.png"
                    )
                    self.inventory_display_from_upgrade()
                    self.inventory_window.position_icons(self.inventory_icon_list)
                    self.upgrading = True
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
        self.background = arcade.load_texture(":assets:background/4.png")

    def inventory_display_from_upgrade(self):
        self.inventory_window = Inventory(
            ":assets:gui/inventory.png", INGAME_WINDOW_SCALE
        )
        self.position_inventory()
        self.right_side_button_list[3].state = True

    def refresh_inventory_window(self):
        self.inventory_window.position_icons(self.inventory_icon_list)

    def inventory_deactivate(self):
        self.inventory_window = None

    def position_inventory(self):
        self.inventory_window.center_x = (
            GAME_WIDTH - self.inventory_window.width / 2 - 65
        )
        self.inventory_window.center_y = GAME_HEIGHT / 2

    def vault_display(self):
        self.vault_window = Vault(":assets:gui/vault.png", INGAME_WINDOW_SCALE)
        self.position_vault_window()
        self.right_side_button_list[1].state = True
        self.background = arcade.load_texture(":assets:background/4.png")

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
        self.upgrading = False

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
                self.vault_display()

        if key == arcade.key.T:
            print("trade")
            self.fire = True

        if key == arcade.key.U:
            if self.upgrading:
                self.deactivate_all_buttons_windows()
            else:
                self.background = arcade.load_texture(
                    ":assets:background/plain_black.png"
                )
                self.inventory_display_from_upgrade()
                self.inventory_window.position_icons(self.inventory_icon_list)
                self.upgrading = True

        if key == arcade.key.P:
            print("portals")

        if key == arcade.key.F:
            print("fight")

        if key == arcade.key.LCTRL:
            self.item_popup_background = True

    def icon_drop_swap(self, cursor_x, cursor_y):
        if self.inventory_window:
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
                    (
                        self.inventory_icon_list[index1],
                        self.inventory_icon_list[index2],
                    ) = (
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
                        and cursor_x
                        <= icon_mapped_data["x"] + icon_mapped_data["width"]
                        and cursor_y <= icon_mapped_data["y"]
                        and cursor_y
                        >= icon_mapped_data["y"] - icon_mapped_data["height"]
                        and inv_number
                        not in [icon.inv_pos for icon in self.inventory_icon_list]
                    ):
                        self.cursor_hand.icon_held.inv_pos = inv_number

        self.sound = arcade.Sound(":assets:sounds/inventory/item_swap.mp3").play(
            volume=self.sound_volume
        )
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
        self.sound = arcade.Sound(":assets:sounds/inventory/equip.mp3").play(
            volume=self.sound_volume
        )
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

        item = item_type(image, icon, self.player, stats, name)
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
                    "Armor": random.randint(1, 10),
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
                    "Ice damage": random.randint(1, 30),
                },
            ),
            Item(
                name="gauntlet_blue",
                stats={
                    "Health": random.randint(1, 10),
                    "Armor": random.randint(1, 10),
                },
            ),
        ]
        for item in test_server_items:
            self.create_item_and_icon(item)

    def generate_test_items(self):
        pass


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
