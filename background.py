import pygame
from constants import * # import all constants from constants.py
# Optimized background handling
class ScaledBackground:

    # initialize the background
    def __init__(self, img, max_zoom_level):
        self.img = img # the image
        self.max_zoom_level = max_zoom_level # zoom
        self.scaled_images = {}

    
    
    def get_scaled_image(self, zoom_level):
        if zoom_level not in self.scaled_images:
            # Scale the image only if it's not already cached
            bg_width = max(SCREEN_WIDTH, WIDTH * (zoom_level / 10))
            bg_height = max(SCREEN_HEIGHT, HEIGHT * (zoom_level / 10))

            scaled_bg = pygame.transform.scale(self.img, (int(bg_width), int(bg_height))) # the background scaled
            self.scaled_images[zoom_level] = scaled_bg # add the scaled image zoom_level to the array
        return self.scaled_images[zoom_level]
