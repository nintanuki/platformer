import pygame
from settings import ScreenSettings, PlayerSettings, ControllerSettings

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PlayerSettings.WIDTH, PlayerSettings.HEIGHT))
        self.image.fill((PlayerSettings.COLOR))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity_y = PlayerSettings.INITIAL_VELOCITY_Y
        self.on_ground = False

    def get_input(self, joysticks):
        keys = pygame.key.get_pressed()
 
        # --- Collect controller state in a single pass ---
        joystick_x = 0.0 # Default to no horizontal input
        jump_held = False # Track if any joystick has the jump button held
 
        for joy in joysticks:
            x = joy.get_axis(ControllerSettings.MOVE_AXIS_X)
            # Ignore stick drift when the player isn't touching the controller
            if abs(x) > ControllerSettings.AXIS_DEADZONE:
                joystick_x = x
            jump_held |= joy.get_button(ControllerSettings.A_BUTTON)
 
        # --- Horizontal movement ---
        if keys[pygame.K_LEFT] or joystick_x < 0:
            self.rect.x -= PlayerSettings.LEFT_SPEED
        if keys[pygame.K_RIGHT] or joystick_x > 0:
            self.rect.x += PlayerSettings.RIGHT_SPEED
 
        # --- Jump ---
        # Check if jump is pressed and player is on the ground
        # This is to prevent double jumps (maybe a powerup can disable this later)
        if (keys[pygame.K_SPACE] or jump_held) and self.on_ground:
            self.velocity_y = PlayerSettings.JUMP_STRENGTH
            self.on_ground = False
 
        # --- Gravity and vertical position ---
        self.velocity_y += PlayerSettings.GRAVITY
        self.rect.y += self.velocity_y
 
        # Floor collision
        if self.rect.bottom >= ScreenSettings.HEIGHT:
            self.rect.bottom = ScreenSettings.HEIGHT
            self.velocity_y = PlayerSettings.INITIAL_VELOCITY_Y
            self.on_ground = True

    def update(self, joysticks):
        self.get_input(joysticks)