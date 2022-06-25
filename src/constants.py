from pathlib import Path
from time import time

# Server
SERVER = "http://127.0.0.1:8000"

# Path
ASSETS_PATH = (Path(__file__).parent / "assets").resolve()

# Items
WEAPON_SCALE = 3
HELMET_SCALE = 3
BODY_SCALE = 3
LEGS_SCALE = 3
GLOVES_SCALE = 3
BOOTS_SCALE = 3
CLOAK_SCALE = 3
MAIN_HAND_SCALE = 3
OFF_HAND_SCALE = 3

# Game
CAMERA_SPEED = 0.1
PLAYER_SCALE = 3

# GUI
INVENTORY_SCALE = 1
VAULT_SCALE = 1
HOME_RIGHT_PANEL = 1.5
CURSOR_SCALE = 0.4
RIGHT_BUTTON_SCALE = 1.5
PORTRAIT_PANEL_SCALE = 2.5
PORTRAIT_SCALE = 0.23
ICON_SCALE = 1.5

# The constant projection size regardless of window size
GAME_WIDTH = 1280
GAME_HEIGHT = 720
GAME_ASPECT_RATIO = GAME_WIDTH / GAME_HEIGHT
WINDOW_TITLE = "Mort"

# Discord RPC
CLIENT_ID = "SOME ID U GET FROM https://discord.dev"
DISCORD_RPC_ASSETS = {
    "large_image": "some_name.png",
    "small_image": "some_name_2.png",  # We set the game name as the app name
    "state": "<state of the player>",
    "buttons": [
        {
            "label": "Checkout Mort on GitHub",
            "url": "https://github.com/BrettskiPy/mort",
        }
    ],
    "start": time(),
}
