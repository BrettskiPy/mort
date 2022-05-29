from armor import *
from player import Player
from gui import *
from icon import *
from weapon import *
import constants

import arcade


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
        self.inventory_slot_list = None
        self.vault_list = None
        # Equipped lists
        self.equipped_helmet_list = None
        self.equipped_body_list = None
        self.equipped_legs_list = None
        self.equipped_boots_list = None
        self.equipped_gloves_list = None
        self.equipped_main_hand_list = None
        self.equipped_off_hand_list = None
        # Icons lists
        self.icon_list = None

        # Sprite variables
        self.player = None
        self.cursor_hand = None
        self.inventory_window = None
        self.vault_window = None
        self.vault_inventory_window = None
        self.portrait_frame = None
        self.portrait = None

    def setup(self):

        # Sprite lists
        self.inventory_list = arcade.SpriteList()
        self.inventory_slot_list = arcade.SpriteList()
        self.vault_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.static_gui_list = arcade.SpriteList()
        self.right_side_button_list = arcade.SpriteList()

        self.equipped_helmet_list = arcade.SpriteList()
        self.equipped_body_list = arcade.SpriteList()
        self.equipped_legs_list = arcade.SpriteList()
        self.equipped_boots_list = arcade.SpriteList()
        self.equipped_gloves_list = arcade.SpriteList()
        self.equipped_main_hand_list = arcade.SpriteList()
        self.equipped_off_hand_list = arcade.SpriteList()

        self.icon_list = arcade.SpriteList()

        # Create sprites
        self.cursor_hand = HandCursor(":assets:cursor/glove_point.png", CURSOR_SCALE)
        self.player = Player(":assets:player.png", PLAYER_SCALE)
        self.player_list.append(self.player)

        self.generate_test_items() # item test creation

        # Generate GUI
        self.portrait_frame = PortraitFrame(
            ":assets:gui/portrait_frame/portrait_frame.png", PORTRAIT_PANEL_SCALE
        )
        self.portrait = Portrait(":assets:gui/portraits/6.png", PORTRAIT_SCALE)
        self.background = arcade.load_texture(":assets:background/4.png")
        self.generate_home_right_panel()

    def on_draw(self):
        self.clear()
        self.timed_lighting_with_background()
        self.portrait.draw(pixelated=True)
        self.portrait_frame.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        self.static_gui_list.draw(pixelated=True)
        self.right_side_button_list.draw(pixelated=True)

        self.equipped_body_list.draw(pixelated=True)
        self.equipped_helmet_list.draw(pixelated=True)
        self.equipped_legs_list.draw(pixelated=True)
        self.equipped_boots_list.draw(pixelated=True)
        self.equipped_gloves_list.draw(pixelated=True)
        self.equipped_main_hand_list.draw(pixelated=True)
        self.equipped_off_hand_list.draw(pixelated=True)

        if self.inventory_window:
            self.inventory_window.draw(pixelated=True)
            # self.inventory_window.display_positions()  # debugging visual
            self.icon_list.draw(pixelated=True)

        if self.vault_window:
            self.vault_window.draw(pixelated=True)
            # self.vault_window.display_positions()  # debugging visual
            self.vault_inventory_window.draw(pixelated=True)
            # self.vault_inventory_window.display_positions()  # debugging visual
            self.icon_list.draw(pixelated=True)

        for button in self.right_side_button_list:
            if button.state:
                button.display_clicked()

        if self.cursor_hand.holding_icon:
            self.cursor_hand.grab_icon()

        self.inventory_slot_list.draw(pixelated=True)
        self.vault_list.draw(pixelated=True)
        self.cursor_hand.draw()

        # self.cursor_hand.draw_hit_box(color=arcade.color.RED, line_thickness=1)

    def on_update(self, delta_time):
        # List updates
        self.inventory_list.update()
        self.inventory_slot_list.update()
        self.vault_list.update()
        self.player_list.update()
        self.static_gui_list.update()
        self.right_side_button_list.update()

        self.equipped_helmet_list.update()
        self.equipped_body_list.update()
        self.equipped_legs_list.update()
        self.equipped_boots_list.update()
        self.equipped_gloves_list.update()
        self.equipped_main_hand_list.update()
        self.equipped_off_hand_list.update()
        self.icon_list.update()

        # Individual sprite updates
        self.cursor_hand.on_update()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.set_cursor_position(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.cursor_hand = HandCursor(":assets:cursor/glove_grab.png", CURSOR_SCALE)
        self.set_cursor_position(x, y)
        self.right_panel_onclick_actions()

        collision = arcade.check_for_collision_with_list(
            self.cursor_hand, self.icon_list
        )
        if collision:
            self.cursor_hand.holding_icon = True
            for icon in collision:
                self.cursor_hand.icon_held = icon

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.cursor_hand.icon_held:
            collision = arcade.check_for_collision_with_list(
                self.cursor_hand, self.icon_list
            )
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
                index1 = self.icon_list.index(self.cursor_hand.icon_held)
                index2 = self.icon_list.index(icon)
                self.icon_list[index1], self.icon_list[index2] = (
                    self.icon_list[index1],
                    self.icon_list[index2],
                )

        self.cursor_hand = HandCursor(":assets:cursor/glove_point.png", CURSOR_SCALE)
        self.set_cursor_position(x, y)

    def set_cursor_position(self, x, y):
        self.cursor_hand.center_x = x
        self.cursor_hand.center_y = y

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        self.window_key_router(key)

        # FIXME key x is test
        if key == arcade.key.X:
            self.icon_2 = Icon(":assets:icons/test_hat.png", ICON_SCALE, "some cool hat")
            self.icon_2.set_inv_position(self.icon_list)
            self.icon_list.append(self.icon_2)
            if self.inventory_window:
                self.inventory_window.position_icons(self.icon_list)
            if self.vault_inventory_window:
                self.vault_inventory_window.position_icons(self.icon_list)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        pass

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
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
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
            self.button.center_x = SCREEN_WIDTH - 29
            self.button.center_y = SCREEN_HEIGHT / 2 + height
            self.right_side_button_list.append(self.button)
            height -= 54

    def right_panel_onclick_actions(self):
        for button in arcade.check_for_collision_with_list(
            self.cursor_hand, self.right_side_button_list
        ):
            if button.state:
                self.deactivate_all_windows()
                self.deactivate_all_buttons()
            else:
                self.deactivate_all_windows()
                self.deactivate_all_buttons()
                button.state = True
                if button.description == "inventory":
                    self.inventory_display()
                    self.inventory_window.position_icons(self.icon_list)
                elif button.description == "vault":
                    self.vault_window_display()
                    self.vault_inventory_window.position_icons(self.icon_list)
                elif button.description == "trade":
                    print("Trading")
                elif button.description == "blacksmith":
                    print("blacksmithing")
                elif button.description == "portals":
                    print("portaling")
                elif button.description == "fight":
                    print("fighting")

    def position_home_right_panel(self):
        self.right_side_bar.center_x = SCREEN_WIDTH - 30
        self.right_side_bar.center_y = SCREEN_HEIGHT / 2

    def inventory_display(self):
        self.inventory_window = Inventory(
            ":assets:gui/inventory.png", INGAME_WINDOW_SCALE
        )
        self.position_inventory()
        self.right_side_button_list[0].state = True

    def inventory_deactivate(self):
        self.inventory_window = None

    def position_inventory(self):
        self.inventory_window.center_x = (
            SCREEN_WIDTH - self.inventory_window.width / 2 - 65
        )
        self.inventory_window.center_y = SCREEN_HEIGHT / 2

    def vault_window_display(self):
        self.vault_window = Vault(":assets:gui/vault.png", INGAME_WINDOW_SCALE)
        self.position_vault_window()
        self.right_side_button_list[1].state = True
        self.vault_inventory_window_display()
        self.position_vault_inventory_window()

    def position_vault_window(self):
        self.vault_window.center_x = SCREEN_WIDTH - self.vault_window.width / 2 - 65
        self.vault_window.center_y = SCREEN_HEIGHT / 2

    def vault_window_deactivate(self):
        self.vault_window = None

    def vault_inventory_window_display(self):
        self.vault_inventory_window = Inventory(
            ":assets:gui/inventory.png", INGAME_WINDOW_SCALE, vault_inventory=True
        )
        self.position_vault_inventory_window()

    def position_vault_inventory_window(self):
        self.vault_inventory_window.center_x = (
            self.vault_inventory_window.width / 2 + 40
        )
        self.vault_inventory_window.center_y = SCREEN_HEIGHT / 2

    def vault_inventory_window_deactivate(self):
        self.vault_inventory_window = None

    def deactivate_all_windows(self):
        self.inventory_deactivate()
        self.vault_window_deactivate()
        self.vault_inventory_window_deactivate()

    def deactivate_all_buttons(self):
        for other_buttons in self.right_side_button_list:
            other_buttons.state = False

    def window_key_router(self, key):
        # TODO refactor this into a clean function
        if key == arcade.key.I:
            if self.inventory_window:
                self.deactivate_all_windows()
                self.deactivate_all_buttons()
            elif [button.state for button in self.right_side_button_list]:
                self.deactivate_all_windows()
                self.deactivate_all_buttons()
                self.inventory_display()
                self.inventory_window.position_icons(self.icon_list)

        if key == arcade.key.V:
            if self.vault_window:
                self.deactivate_all_windows()
                self.deactivate_all_buttons()
            elif [button.state for button in self.right_side_button_list]:
                self.deactivate_all_windows()
                self.deactivate_all_buttons()
                self.vault_window_display()
                self.vault_inventory_window.position_icons(self.icon_list)

        if key == arcade.key.T:
            print("trade")

        if key == arcade.key.B:
            print("blacksmith")

        if key == arcade.key.P:
            print("portals")

        if key == arcade.key.F:
            print("fight")

    def generate_test_items(self):
        for _ in range(5):
            self.icon_1 = Icon(
                ":assets:icons/test_helm.png", ICON_SCALE, "some cool hat"
            )
            self.icon_1.set_inv_position(self.icon_list)
            self.icon_list.append(self.icon_1)
            self.icon_2 = Icon(":assets:icons/test_hat.png", ICON_SCALE, "some cool hat")
            self.icon_2.set_inv_position(self.icon_list)
            self.icon_list.append(self.icon_2)

        self.item_1 = Head(
            ":assets:armor/head/wizard_red.png", HELMET_SCALE, self.player
        )
        self.equipped_helmet_list.append(self.item_1)

        self.item_2 = Body(
            ":assets:armor/body/coat_red.png", BODY_SCALE, self.player
        )
        self.equipped_body_list.append(self.item_2)

        self.item_3 = Legs(":assets:armor/legs/leg_armor_0.png", LEGS_SCALE, self.player)
        self.equipped_legs_list.append(self.item_3)

        self.item_4 = Gloves(":assets:armor/gloves/glove_gray.png", GLOVES_SCALE, self.player)
        self.equipped_gloves_list.append(self.item_4)

        self.item_5 = Boots(":assets:armor/boots/blue_gold.png", BOOTS_SCALE, self.player)
        self.equipped_boots_list.append(self.item_5)

        self.item_6 = MainHand(":assets:weapons/main_hand/scythe_new.png", MAIN_HAND_SCALE, self.player)
        self.equipped_main_hand_list.append(self.item_6)

        self.item_7 = OffHand(":assets:weapons/off_hand/shield_large_dd_dk.png", OFF_HAND_SCALE, self.player)
        self.equipped_off_hand_list.append(self.item_7)

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
        self.views = {}


def main():
    arcade.resources.add_resource_handle("assets", constants.ASSETS_PATH)

    window = MyWindow()
    window.center_window()
    home_view = HomeView()
    home_view.setup()
    window.set_mouse_visible(False)
    window.show_view(home_view)
    window.set_location(500, 100)
    arcade.run()


if __name__ == "__main__":
    main()
