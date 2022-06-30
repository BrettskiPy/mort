# TODO Implement background FX

# def timed_lighting_with_background(self):
#     """Draws a background that slowly changes from light/dark"""
#     if self.daylight:
#         self.time_of_day -= DAYLIGHT_SPEED
#         if self.time_of_day < 1:
#             self.daylight = False
#     else:
#         self.time_of_day += DAYLIGHT_SPEED
#         if self.time_of_day == 255:
#             self.daylight = True
#     arcade.draw_lrwh_rectangle_textured(
#         0,
#         0,
#         GAME_WIDTH,
#         GAME_HEIGHT,
#         self.background,
#         alpha=round(self.time_of_day),
#     )
