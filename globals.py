import pygame

WIDTH, HEIGHT = 1920, 1080

TOP_MARGIN, BOTTOM_MARGIN = 250, 200
# BOX_WIDTH, BOX_HEIGHT = WIDTH - 100, HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
BOX_WIDTH = 1430
BOX_HEIGHT = 544
BOX_X, BOX_Y = (WIDTH - BOX_WIDTH) // 2, TOP_MARGIN

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

level_data = {
    1: {
        "qubits": 1,
        "gates": ['x'],
        "goal_state": '1',
    },
    2: {
        "qubits": 2,
        "gates": ['x', 'h'],
        "goal_state": '01',
    }
}

