from __future__ import annotations

import pygame
import sys

from sprites import Enemy, Player
from render import RenderManager
from settings import(
    AssetPaths,
    ControllerSettings,
    EnemySettings,
    ScreenSettings,
    PlayerSettings,
    TileSettings
)

# A level manager will be added later to handle multiple levels
# For now we will import this here and let game manager handle it directly
from tile_maps import MAP_01

class CollisionManager:
    """Manages collision detection between the player and the tile map."""
    def __init__(self, current_map):
        """
        Initialize the collision manager by converting the tile map into solid rects.
        Args:
            current_map (list of list of str): The tile map to be used for collision detection.
        """
        self.solid_rects = self.load_solid_rects(current_map) # Convert tile map to rects for collision detection

    def load_solid_rects(self, current_map):
        """
        Convert the tile map into a list of rects for collision detection.
        Args:
            current_map (list of list of str): The tile map to be converted.
        Returns:
            list of pygame.Rect: A list of rects representing solid tiles.
        """
        rects = [] # Create an empty list to hold the rects for solid tiles
        # Loop through the tile map and create rects for solid tiles
        for row_index, row in enumerate(current_map):
            for col_index, tile in enumerate(row):
                if tile == 'x':
                    x = col_index * TileSettings.SIZE
                    y = row_index * TileSettings.SIZE
                    rects.append(pygame.Rect(x, y, TileSettings.SIZE, TileSettings.SIZE))
        return rects

    def resolve_horizontal(self, rect):
        """
        Check for horizontal collisions and adjust the rect's position accordingly.
        Args:
            rect (pygame.Rect): The rect to check for collisions and adjust.
        Returns:
            int: -1 if collided with a left wall, 1 if collided with a right wall, 0 if no collision.
        """
        for solid_rect in self.check_collision(rect):
            # Only resolve horizontally if the tile is actually to the side of the player.
            # Without this check, floor tiles would also trigger horizontal resolution.
            if rect.centery > solid_rect.top and rect.centery < solid_rect.bottom:
                if rect.right > solid_rect.left and rect.left < solid_rect.left:
                    rect.right = solid_rect.left
                    return 1  # hit a right wall
                if rect.left < solid_rect.right and rect.right > solid_rect.right:
                    rect.left = solid_rect.right
                    return -1  # hit a left wall
        return 0  # no collision

    def check_collision(self, rect):
        """
        Check if the given rect collides with any solid tile rects.

        Args:
            rect (pygame.Rect): The rect to check for collisions.

        Returns:
            list of pygame.Rect: A list of rects that the given rect collides with.
        """

        # Return a list of all solid rects that collide with the given rect
        return [solid_rect for solid_rect in self.solid_rects if rect.colliderect(solid_rect)]

class GameManager:
    def __init__(self):
        pygame.init()
        self.setup_controllers()
        self.screen = pygame.display.set_mode((ScreenSettings.RESOLUTION), pygame.SCALED)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Platformer")

        self.render_manager = RenderManager(self.screen)
        self.current_map = MAP_01
        self.collision = CollisionManager(self.current_map)
        self.player = Player(*PlayerSettings.INITIAL_POSITION, self)
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy(*EnemySettings.INITIAL_POSITION, self))

    def setup_controllers(self):
        """Initialize joysticks and store them in a list for later use."""
        pygame.joystick.init()
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle fullscreen toggle
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == ControllerSettings.SELECT_BUTTON:
                        pygame.display.toggle_fullscreen()

            self.screen.fill(ScreenSettings.BACKGROUND_COLOR)

            # Draw the map
            self.render_manager.draw_map(MAP_01)

            # Update and draw player
            self.player.update(self.joysticks)
            self.screen.blit(self.player.image, self.player.rect)

            # Update and draw enemy
            self.enemies.update()
            self.enemies.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()