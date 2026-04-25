class ScreenSettings:
        WIDTH = 600
        HEIGHT = 800
        RESOLUTION = (WIDTH, HEIGHT)
        FPS = 60

class ColorSettings:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

class PlayerSettings:
    WIDTH = 32
    HEIGHT = 32
    COLOR = ColorSettings.RED
    GRAVITY = 0.5
    JUMP_STRENGTH = -10
    INITIAL_VELOCITY_Y = 0
    LEFT_SPEED = 5
    RIGHT_SPEED = 5

class ControllerSettings:
    DPAD_INDEX = 0
    MOVE_AXIS_X = 0
    AXIS_DEADZONE = 0.25

    A_BUTTON = 0
    B_BUTTON = 1
    X_BUTTON = 2
    Y_BUTTON = 3
    L1_BUTTON = 4
    R1_BUTTON = 5
    START_BUTTON = 7
    SELECT_BUTTON = 6
