import pygame
from settings import AssetPaths, TileSettings, ColorSettings
 
class RenderManager:
    def __init__(self, screen):
        self.screen = screen
        self.tile_wall = pygame.image.load(AssetPaths.TILE_WALL).convert()
 
    def draw_map(self, current_map):
        """Draw the tile map based on the current map layout."""
        for row_index, row in enumerate(current_map):
            for col_index, tile in enumerate(row):
                if tile == 'x':
                    x = col_index * TileSettings.SIZE
                    y = row_index * TileSettings.SIZE
                    self.screen.blit(self.tile_wall, (x, y))