import random
from dataclasses import dataclass
from typing import Dict

from src.armor import *
from src.home_gui import *
from src.player import Player
from src.icon import *
from src.item_local_map import item_map

import arcade
from arcade import key


# TODO remove this when server is done
@dataclass
class Item:
    name: str
    stats: dict


class HomeView(arcade.View):
    """The home view is the default view. This contains a panel on the right side of
    the screen with links to various other views. Note: All panel options will transfer the home view to a new view
    except for the inventory and vault options."""

    def __init__(self):
        super().__init__()

        # Background image will be stored in this variable
        # Local game states
        self.item_to_vault_enabled = False

        # Sprite lists
        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.inventory_slot_list: arcade.SpriteList = arcade.SpriteList()
        self.static_gui_list: arcade.SpriteList = arcade.SpriteList()
        self.right_panel_button_list: arcade.SpriteList = arcade.SpriteList()
        self.inventory_list: arcade.SpriteList = arcade.SpriteList()

        # Equipped lists
        self.equipped_list: arcade.SpriteList = arcade.SpriteList()

        # Icons lists
        self.inventory_icon_list: arcade.SpriteList = arcade.SpriteList()
        self.inventory_icon_slot_list: arcade.SpriteList = arcade.SpriteList()
        self.vault_icon_list: arcade.SpriteList = arcade.SpriteList()

        # Sprite variables
        self.player: Player = Player()
        self.cursor_hand: HandCursor = HandCursor()
        self.inventory_window: Inventory = Inventory()
        self.vault_window: Vault = Vault()

        self.portrait_frame: PortraitFrame = PortraitFrame()
        self.portrait: Portrait = Portrait()
        self.total_item_stats: dict = {}
        self.item_popup = ItemStatPopup(
            self.cursor_hand,
            self.inventory_icon_list,
            self.vault_icon_list,
            self.inventory_icon_slot_list,
        )

        # Music
        self.songs: Dict[str : arcade.Sound] = {
            "dreams": arcade.Sound(
                file_name=":assets:music/the_field_of_dreams.mp3",
                streaming=True,
            )
        }
        self.music_volume = 1

        # Sound
        self.sounds: Dict[str : arcade.Sound] = {
            "equip": arcade.Sound(":assets:sounds/inventory/equip.mp3"),
            "swap": arcade.Sound(":assets:sounds/inventory/item_swap.mp3"),
        }
        self.sound_volume = 0.5

    def setup(self):
        self.player_list.append(self.player)
        self.static_gui_list.append(
            RightPanel(
                self.right_panel_button_list,
            )
        )
        self.generate_test_server_items()
        self.songs["dreams"].play(
            loop=True,
            speed=0.6,
        )

    def on_draw(self):
        # window
        self.window.apply_gui_camera()
        self.clear()
        self.window.apply_game_camera()

        # GUI
        self.portrait.draw(pixelated=True)
        self.portrait_frame.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        self.static_gui_list.draw(pixelated=True)
        self.right_panel_button_list.draw(pixelated=True)
        MenuButton.display_clicked(self.right_panel_button_list)
        if self.inventory_window.open:
            self.inventory_window.draw(pixelated=True)
            # self.inventory_window.display_positions()  # debugging visual
            self.inventory_icon_list.draw(pixelated=True)
            self.inventory_icon_slot_list.draw(pixelated=True)
            self.inventory_window.display_total_item_stats()
        if self.vault_window.open:
            self.vault_window.draw(pixelated=True)
            # self.vault_window.display_positions()  # debugging visual
            self.vault_icon_list.draw(pixelated=True)

        # Sprite Lists
        self.equipped_list.draw(pixelated=True)

        # Misc (drawn last)
        self.cursor_hand.grab_icon()
        self.item_popup.item_background_popup_display()
        self.cursor_hand.draw()

        # self.cursor_hand.draw_hit_box(color=arcade_color.RED, line_thickness=1)  # debug visual

    def on_update(self, delta_time):
        # List updates
        self.equipped_list.update()

        # Individual sprite updates
        self.cursor_hand.on_update()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.cursor_hand.set_cursor_position(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.right_panel_click_actions()
            self.holdable_icon_in_window_check()
            self.cursor_hand.grab()

        if button == arcade.MOUSE_BUTTON_RIGHT:
            if self.item_to_vault_enabled and self.inventory_window.open:
                self.inv_to_vault_check()

            if self.inventory_window.open:
                self.inv_icon_to_equip_check()
                self.slot_icon_to_inv_check()
                self.inventory_window.calculate_total_item_stats(self.equipped_list)
                self.inventory_window.display_total_item_stats()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.cursor_hand.icon_held:
                if self.inventory_window.open:
                    self.icon_drop_swap(
                        x, y, self.inventory_window, self.inventory_icon_list
                    )
                elif self.vault_window.open:
                    self.icon_drop_swap(x, y, self.vault_window, self.vault_icon_list)

        self.cursor_hand.reset()

        if button == arcade.MOUSE_BUTTON_RIGHT:
            pass

    def on_key_press(self, key_pressed, modifiers):
        self.inv_or_vault_key_router(key_pressed)
        self.views_key_router(key_pressed)

        if key_pressed == key.LCTRL or modifiers == key.MOD_CTRL:
            self.item_popup.show()

        if key_pressed == key.LALT or modifiers == key.MOD_ALT:
            self.item_to_vault_enabled = True

        # FIXME key x is a test to populate additional inventory items
        if key_pressed == key.X:
            self.generate_test_server_items()
            if self.inventory_window.open:
                self.inventory_window.position_icons(self.inventory_icon_list)

    def on_key_release(self, key_pressed, modifiers):
        if key_pressed == key.LCTRL:
            self.item_popup.hide()

        if key_pressed == key.LALT:
            self.item_to_vault_enabled = False

    def holdable_icon_in_window_check(self):
        for window in (self.inventory_window, self.vault_window):
            self.cursor_hand.attempt_icon_hold(
                window, self.inventory_icon_list, self.vault_icon_list
            )

    def slot_icon_to_inv_check(self):
        """Checks for a cursor collision with an equipped slot icon. It will then create a new icon in the inventory with
        the respective item data"""
        collision_slot_icon = arcade.check_for_collision_with_list(
            self.cursor_hand,
            self.inventory_icon_slot_list,
        )
        if collision_slot_icon:
            for icon in collision_slot_icon:  # type: ignore
                print(icon)
                icon: InventorySlotIcon
                new_inv_icon = InventoryIcon(
                    icon.filename, icon.item_referenced, self.inventory_icon_list
                )
                self.inventory_icon_list.append(new_inv_icon)
                icon.item_referenced.kill()
                icon.kill()
                self.refresh_all_windows()

    def inv_icon_to_equip_check(self):
        """Checks for a cursor collision with an inventory item. It will then create a new icon in the correct item type
        equipped slot. This new icon will also contain the item's data"""
        collision_icon = arcade.check_for_collision_with_list(
            self.cursor_hand,
            self.inventory_icon_list,
        )
        if collision_icon:
            for icon in collision_icon:
                self.equip_item_to_player(icon)
                self.cursor_hand.point()

    def inv_to_vault_check(self):
        collision_icon = arcade.check_for_collision_with_list(
            self.cursor_hand,
            self.inventory_icon_list,
        )
        if collision_icon:
            for icon in collision_icon:
                icon: InventoryIcon
                new_inv_icon = VaultIcon(
                    icon.filename, icon.item_referenced, self.vault_icon_list
                )
                self.vault_icon_list.append(new_inv_icon)
                icon.item_referenced.kill()
                icon.kill()
                self.refresh_all_windows()

    def right_panel_click_actions(self):
        """Activates actions based on a user clicking the respective button"""
        for button in arcade.check_for_collision_with_list(
            self.cursor_hand, self.right_panel_button_list
        ):
            button: MenuButton
            if button.state:
                self.deactivate_all_buttons_windows()
            else:
                self.deactivate_all_buttons_windows()
                button.state = True
                if button.description == "inventory":
                    self.inventory_window.display()
                    self.inventory_window.position_icons(self.inventory_icon_list)
                elif button.description == "vault":
                    self.vault_window.display()
                elif button.description == "trade":
                    print("Trading")
                elif button.description == "upgrade":
                    print("upgrading")
                elif button.description == "portals":
                    print("portaling")
                elif button.description == "fight":
                    print("fighting")

    def deactivate_all_windows(self):
        """Deactivates all window displays"""
        self.inventory_window.deactivate()
        self.vault_window.deactivate()

    def deactivate_all_buttons_windows(self):
        """Deactivates all buttons and all windows"""
        self.deactivate_all_windows()
        MenuButton.deactivate_all_buttons(self.right_panel_button_list)

    def refresh_all_windows(self):
        """Refreshes all active windows with their respective icon positions"""
        self.inventory_window.refresh(self.inventory_icon_list)
        self.vault_window.refresh(self.vault_icon_list)

    def inv_or_vault_key_router(self, key_pressed):
        """A key router for inventory or vault"""
        # TODO refactor this into a clean function
        if key_pressed == key.I:
            if self.inventory_window.open:
                self.deactivate_all_buttons_windows()
            elif [button.state for button in self.right_panel_button_list]:  # type: ignore
                self.deactivate_all_buttons_windows()
                self.inventory_window.display()
                self.inventory_window.position_icons(self.inventory_icon_list)
                self.right_panel_button_list[0].state = True

        if key_pressed == key.V:
            if [button.state for button in self.right_panel_button_list]:  # type: ignore
                self.deactivate_all_buttons_windows()
                self.vault_window.display()
                self.right_panel_button_list[1].state = True  # type: ignore

    def views_key_router(self, key_pressed):
        """A key router for views accessible from the home view"""
        if key_pressed == key.T:
            print("trade")

        if key_pressed == key.U:
            print("upgrading")

        if key_pressed == key.P:
            print("portals")

        if key_pressed == key.F:
            print("fight")

    def icon_drop_swap(self, cursor_x, cursor_y, window, icon_list):
        """Drops an icon at the current released position (in inventory or vault). If an item exists in
        the dropped position it will swap positions with the icon it is dropped upon"""
        # FIXME simplify this complex function
        collision = arcade.check_for_collision_with_list(self.cursor_hand, icon_list)
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
                self.cursor_hand.icon_held.pos, icon.pos = (
                    icon.pos,
                    self.cursor_hand.icon_held.pos,
                )
                index1 = icon_list.index(self.cursor_hand.icon_held)
                index2 = icon_list.index(icon)
                (icon_list[index1], icon_list[index2],) = (
                    icon_list[index1],
                    icon_list[index2],
                )
        else:
            for (
                inv_number,
                icon_mapped_data,
            ) in window.mapped_carry_positions.items():
                if (
                    icon_mapped_data["x"]
                    <= cursor_x
                    <= icon_mapped_data["x"] + icon_mapped_data["width"]
                    and icon_mapped_data["y"]
                    >= cursor_y
                    >= icon_mapped_data["y"] - icon_mapped_data["height"]
                    and inv_number not in [icon.pos for icon in icon_list]
                ):
                    self.cursor_hand.icon_held.pos = inv_number

        self.sounds["swap"].play(volume=self.sound_volume)
        self.refresh_all_windows()
        self.cursor_hand.point()

    def equip_item_to_player(self, icon):
        """Checks the type of item about to be equipped and places the new icon in the correct inventory slot position
        and places the actual item on the player. If the item type is already equipped it will swap.
        """
        item_type = type(icon.item_referenced)
        if isinstance(icon.item_referenced, item_type):
            if any(isinstance(equipped, item_type) for equipped in self.equipped_list):
                self.equip_swap(icon, item_type)
            else:
                self.equip_empty_slot(icon)

        self.sounds["equip"].play(volume=self.sound_volume)
        self.refresh_all_windows()
        icon.kill()

    def equip_correct_order(self, item_equipped):
        """Ensures specific draw order. EX: The legs need to be drawn before the body to appear correct"""
        if isinstance(item_equipped, Legs):
            self.equipped_list.insert(0, item_equipped)
        else:
            self.equipped_list.append(item_equipped)

    def equip_empty_slot(self, icon):
        """If the item equip inventory slot is empty, the new icon will appear in the correct slot location and a new visual
        item will appear on the player."""

        # To properly display the legs they need to be in front of the body armor in the list order
        self.equip_correct_order(icon.item_referenced)

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
        old_equipped_item: Item = None  # type: ignore
        for item in self.equipped_list:
            if isinstance(item, item_type):
                old_equipped_item = item  # type: ignore
                break

        self.equip_correct_order(icon.item_referenced)

        new_slot_icon = InventorySlotIcon(
            icon.item_referenced.icon_image,
            ICON_SCALE,
            icon.item_referenced,
            inv_window=self.inventory_window,
        )

        for old_slot_icon in self.inventory_icon_slot_list:  # type: ignore
            old_slot_icon: InventorySlotIcon
            if isinstance(old_slot_icon.item_referenced, item_type):
                old_slot_icon.kill()

        self.inventory_icon_slot_list.append(new_slot_icon)

        old_icon = InventoryIcon(
            filename=old_equipped_item.icon_image,
            scale=ICON_SCALE,
            item_referenced=old_equipped_item,
            inventory_icon_list=self.inventory_icon_list,
        )
        old_icon.pos = icon.pos
        self.inventory_icon_list.append(old_icon)
        old_equipped_item.kill()

    def create_item_and_icon(self, test_item_data):
        """Creates a new item and icon from incoming item data"""
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
