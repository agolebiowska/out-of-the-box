import pygame

WIDTH, HEIGHT = 1920, 1080

TOP_MARGIN, BOTTOM_MARGIN = 250, 200
BOX_WIDTH = 1430
BOX_HEIGHT = 544
BOX_X, BOX_Y = (WIDTH - BOX_WIDTH) // 2, TOP_MARGIN
font_file = "assets/joystix.otf"

WHITE = (255, 255, 234)
BLUE = (77, 166, 255)
MAGENTA = (255, 107, 151)
GREEN = (142, 222, 93)
RED = (176, 48, 93)
BLACK = (39, 39, 54)
PURPLE = (128, 54, 106)

level_data = {
    1: {
        "qubits": 1,
        "gates": ['x'],
        "goal_state": [ 0+0j, 1+0j ],
    },
    2: {
        "qubits": 1,
        "gates": ['z'],
        "goal_state": [ 1+0j, 0+0j ],
    },
    3: {
        "qubits": 2,
        "gates": ['h', 'h'],
        "goal_state": [ 0.5+0j, 0.5+0j, 0.5+0j, 0.5+0j ]
    },
    4: {
        "qubits": 2,
        "gates": ['x', 'cx'],
        "goal_state": [ 0+0j, 0+0j, 0+0j, 1+0j ]
    },
    5: {
        "qubits": 2,
        "gates": ['cx', 'h'],
        "goal_state": [ 0.707+0j, 0+0j, 0+0j, 0.707+0j ],
    },
    6: {
        "qubits": 2,
        "gates": ['ry', 'cx', 'x'],
        "goal_state": [ 0+0j, 0.707+0j, 0.707+0j, 0+0j ],
    },
    7: {
        "qubits": 3,
        "gates": ['x', 'x', 't'],
        "goal_state": [ 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 1+0j ],
    },
    8: {
        "qubits": 3,
        "gates": ['h', 'h', 'cx', 'cx'],
        "goal_state": [ 0.5+0j, 0+0j, 0+0j, 0.5+0j, 0.5+0j, 0+0j, 0+0j, 0.5+0j ],
    },
    #9: {
    #    "qubits": 4,
    #    "gates": ['cz', 'ccx', 'h'],
    #    "goal_state": '0000',
    #},
    #10: {
    #    "qubits": 4,
    #    "gates": ['cy', 'x', 't'],
    #    "goal_state": '1100',
    #}
}

