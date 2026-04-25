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
        self.jump_was_pressed = False

    def update(self, joysticks=None):
        keys = pygame.key.get_pressed()
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]
        jump_pressed = keys[pygame.K_SPACE]

        # Merge controller input from all connected joysticks.
        if joysticks:
            for joystick in joysticks:
                dpad_x = 0
                if joystick.get_numhats() > ControllerSettings.DPAD_INDEX:
                    dpad_x = joystick.get_hat(ControllerSettings.DPAD_INDEX)[0]

                axis_x = (
                    joystick.get_axis(ControllerSettings.MOVE_AXIS_X)
                    if joystick.get_numaxes() > ControllerSettings.MOVE_AXIS_X
                    else 0
                )
                move_left = move_left or dpad_x < 0 or axis_x < -ControllerSettings.AXIS_DEADZONE
                move_right = move_right or dpad_x > 0 or axis_x > ControllerSettings.AXIS_DEADZONE

                if joystick.get_numbuttons() > ControllerSettings.A_BUTTON:
                    jump_pressed = jump_pressed or bool(joystick.get_button(ControllerSettings.A_BUTTON))

        jump_just_pressed = jump_pressed and not self.jump_was_pressed

        if move_left:
            self.rect.x -= PlayerSettings.LEFT_SPEED
        if move_right:
            self.rect.x += PlayerSettings.RIGHT_SPEED
        if jump_just_pressed and self.on_ground:
            self.velocity_y = PlayerSettings.JUMP_STRENGTH
            self.on_ground = False

        self.velocity_y += PlayerSettings.GRAVITY  # Gravity
        self.rect.y += int(self.velocity_y)

        # Floor collision
        if self.rect.bottom >= ScreenSettings.HEIGHT:
            self.rect.bottom = ScreenSettings.HEIGHT
            self.velocity_y = PlayerSettings.INITIAL_VELOCITY_Y
            self.on_ground = True

        self.jump_was_pressed = jump_pressed