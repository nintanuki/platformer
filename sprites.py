import pygame
from settings import (
    AssetPaths,
    ControllerSettings,
    PlayerSettings,
    ScreenSettings,
    EnemySettings
)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.image = pygame.image.load(AssetPaths.PLAYER).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity_y = PlayerSettings.INITIAL_VELOCITY_Y
        self.on_ground = False

        self.game = game

    def get_input(self, joysticks):
        keys = pygame.key.get_pressed()
 
        # --- Collect controller state in a single pass ---
        joystick_x = 0.0 # Default to no horizontal input
        jump_held = False # Track if any joystick has the jump button held
        dpad_x = 0
        dpad_y = 0
 
        for joy in joysticks:
            x = joy.get_axis(ControllerSettings.MOVE_AXIS_X)
            # Ignore stick drift when the player isn't touching the controller
            if abs(x) > ControllerSettings.AXIS_DEADZONE:
                joystick_x = x
            jump_held |= joy.get_button(ControllerSettings.A_BUTTON)
            dpad_x, dpad_y = joy.get_hat(0)

        # --- Horizontal movement ---
        # Gather all horizontal input into one variable
        moving_left = (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
            or joystick_x < -0.5          # analog stick (with deadzone)
            or dpad_x < 0                  # d-pad
        )
        moving_right = (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
            or joystick_x > 0.5            # analog stick (with deadzone)
            or dpad_x > 0                  # d-pad
        )

        if moving_left:
            self.rect.x -= PlayerSettings.LEFT_SPEED
        if moving_right:
            self.rect.x += PlayerSettings.RIGHT_SPEED
 
        # --- Jump ---
        # Check if jump is pressed and player is on the ground
        # This is to prevent double jumps (maybe a powerup can disable this later)
        if (keys[pygame.K_SPACE] or jump_held) and self.on_ground:
            self.velocity_y = PlayerSettings.JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self):
        """Apply gravity to the player's vertical velocity and update position."""
        # --- Gravity and vertical position ---
        self.velocity_y += PlayerSettings.GRAVITY
        self.rect.y += self.velocity_y

    def handle_horizontal_collision(self):
        """Check for horizontal collisions and adjust position accordingly."""
        self.on_ground = False # Reset on_ground before checking collisions
        self.game.collision.resolve_horizontal(self.rect)

    def handle_vertical_collision(self):
        """Check for vertical collisions and adjust position and velocity accordingly."""
        for solid_rect in self.game.collision.check_collision(self.rect):
            if self.velocity_y > 0 and self.rect.bottom > solid_rect.top:
                self.rect.bottom = solid_rect.top
                self.velocity_y = 0
                self.on_ground = True
            elif self.velocity_y < 0 and self.rect.top < solid_rect.bottom:
                self.rect.top = solid_rect.bottom
                self.velocity_y = 0

    def handle_stomp(self):
        for enemy in self.game.enemies:
            if self.velocity_y > 0 and self.rect.colliderect(enemy.rect):
                if self.rect.bottom <= enemy.rect.centery:
                    enemy.kill()
                    self.velocity_y = PlayerSettings.STOMP_BOUNCE

    def update(self, joysticks):
        """
        Update the player's position based on input and handle collisions.
        
        Args:
            joysticks (list of pygame.joystick.Joystick): List of initialized joysticks to check for input.
        """
        self.get_input(joysticks)
        self.apply_gravity()
        self.handle_horizontal_collision()
        self.handle_vertical_collision()
        self.handle_stomp()

class Enemy(pygame.sprite.Sprite):
    """An enemy that moves back and forth, reversing direction when hitting a wall."""

    def __init__(self, x, y, game):
        super().__init__()
        self.image = pygame.image.load(AssetPaths.ENEMY).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.game = game
        self.direction = EnemySettings.INITIAL_DIRECTION

    def move(self):
        self.rect.x += EnemySettings.SPEED * self.direction

    def handle_horizontal_collision(self):
        hit = self.game.collision.resolve_horizontal(self.rect)
        if hit != 0:
            self.direction *= -1

    def update(self):
        self.move()
        self.handle_horizontal_collision()