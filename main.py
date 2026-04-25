from __future__ import annotations

import pygame
import sys

from settings import ControllerSettings, ScreenSettings, PlayerSettings
from sprites import Player
from render import RenderManager
from tile_maps import MAP_01

class GameManager:
    def __init__(self):
        pygame.init()
        self.setup_controllers()
        self.screen = pygame.display.set_mode((ScreenSettings.RESOLUTION), pygame.SCALED)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Platformer")

        self.render_manager = RenderManager(self.screen)
        self.player = Player(*PlayerSettings.INITIAL_POSITION)

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

            self.screen.fill((0, 0, 0))

            # Update and draw player
            self.player.update(self.joysticks)
            self.screen.blit(self.player.image, self.player.rect)

            # Draw the map
            self.render_manager.draw_map(MAP_01)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()