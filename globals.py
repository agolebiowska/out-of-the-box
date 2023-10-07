import pygame

WIDTH, HEIGHT = 1920, 1080

TOP_MARGIN, BOTTOM_MARGIN = 250, 200
BOX_WIDTH = 1430
BOX_HEIGHT = 544
BOX_X, BOX_Y = (WIDTH - BOX_WIDTH) // 2, TOP_MARGIN
font_file = "assets/joystix.otf"

WHITE = (255, 255, 235)
BLUE = (77, 166, 255)
MAGENTA = (255, 107, 151)
GREEN = (142, 222, 93)
RED = (176, 48, 93)
BLACK = (39, 39, 54)

level_data = {
    1: {
        "qubits": 1,
        "gates": ['x'],
        "goal_state": '1',
    },
    2: {
        "qubits": 2,
        "gates": ['x', 'h'],
        "goal_state": '0-',
    },
    3: {
        "qubits": 2,
        "gates": ['h', 'h'],
        "goal_state": '++'
    },
    4: {
        "qubits": 2,
        "gates": ['x', 'cx'],
        "goal_state": 'll'
    }
}

