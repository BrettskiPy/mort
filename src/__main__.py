from views.home import *
from game_window import GameWindow

import arcade
from arcade import resources


def main():
    resources.add_resource_handle("assets", ASSETS_PATH)
    window = GameWindow()
    window.center_window()
    window.setup_discord_rpc()
    home_view = HomeView()
    home_view.setup()
    window.set_mouse_visible(False)
    window.show_view(home_view)
    window.set_location(500, 100)
    arcade.run()


if __name__ == "__main__":
    main()
