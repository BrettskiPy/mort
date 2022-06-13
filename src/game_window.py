from constants import *

from arcade import key
import arcade


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(GAME_WIDTH, GAME_HEIGHT, WINDOW_TITLE, resizable=True)  # type: ignore
        self.views = {}
        self.set_min_size(GAME_WIDTH, GAME_HEIGHT)
        self._fullscreen = False

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == key.F11:
            if self.fullscreen:
                # Will revert back to window mode using the window's
                # original size (before fullscreen)
                self.set_fullscreen(False)  # type: ignore
            else:
                # By default this enters fullscreen with the primary
                # monitor's native screen size
                self.set_fullscreen(True)  # type: ignore

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
