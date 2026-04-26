import pygame
from settings import AssetPaths, TileSettings, ColorSettings
 
class RenderManager:
    def __init__(self, screen):
        self.screen = screen
        
        # The terrain sheet is 16x16 tiles — slice out the top-left stone tile
        # then scale it up to 32x32 to match our tile grid
        sheet = pygame.image.load(AssetPaths.TILE_WALL).convert()
        self.tile_wall = sheet.subsurface((288, 80, TileSettings.SIZE, TileSettings.SIZE))
 
    def draw_map(self, current_map):
        """Draw the tile map based on the current map layout."""
        for row_index, row in enumerate(current_map):
            for col_index, tile in enumerate(row):
                if tile == 'x':
                    x = col_index * TileSettings.SIZE
                    y = row_index * TileSettings.SIZE
                    self.screen.blit(self.tile_wall, (x, y))