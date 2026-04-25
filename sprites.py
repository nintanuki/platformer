import pygame
from settings import ScreenSettings, PlayerSettings, ControllerSettings

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.image = pygame.Surface((PlayerSettings.WIDTH, PlayerSettings.HEIGHT))
        self.image.fill((PlayerSettings.COLOR))
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

        for solid_rect in self.game.collision.check_collision(self.rect):
            # Only resolve horizontally if the tile is actually to the side of the player.
            # Without this check, floor tiles would also trigger horizontal resolution.
            if self.rect.centery > solid_rect.top and self.rect.centery < solid_rect.bottom:
                if self.rect.right > solid_rect.left and self.rect.left < solid_rect.left:
                    self.rect.right = solid_rect.left
                if self.rect.left < solid_rect.right and self.rect.right > solid_rect.right:
                    self.rect.left = solid_rect.right

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
        print(self.rect.x)