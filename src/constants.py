from pathlib import Path

# Server
SERVER = "http://127.0.0.1:8000"

# Menu

ASSETS_PATH = (Path(__file__).parent / "assets").resolve()

# Player
WEAPON_SCALE = 3
HELMET_SCALE = 3
BODY_SCALE = 3
LEGS_SCALE = 3
GLOVES_SCALE = 3
BOOTS_SCALE = 3
MAIN_HAND_SCALE = 3
OFF_HAND_SCALE = 3

# Game
CAMERA_SPEED = 0.1
PLAYER_SCALE = 3
CURSOR_SCALE = 0.4
RIGHT_BUTTON_SCALE = 1.5
PORTRAIT_PANEL_SCALE = 2.5
PORTRAIT_SCALE = 0.23
ICON_SCALE = 1.5
INGAME_WINDOW_SCALE = 1

DAYLIGHT_SPEED = 0.1

# The constant projection size regardless of window size
GAME_WIDTH = 1280
GAME_HEIGHT = 720
GAME_ASPECT_RATIO = GAME_WIDTH / GAME_HEIGHT

WINDOW_TITLE = "Mort"
