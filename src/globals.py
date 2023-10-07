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
    # 1. Apply X to Q0.
    1: {
        "qubits": 1,
        "gates": ['x'],
        "goal_state": [ 0+0j, 1+0j ],
    },
    # 1. Apply H gate to Q0. 2. Apply Z gate to Q0.
    2: {
        "qubits": 1,
        "gates": ['h', 'z'],
        "goal_state": [ 0.707+0j, -0.707+0j ],
    },
    # 1. Apply H gates to both qubits.
    3: {
        "qubits": 2,
        "gates": ['h', 'h'],
        "goal_state": [ 0.5+0j, 0.5+0j, 0.5+0j, 0.5+0j ]
    },
    # 1. Apply NOT gate to Q0. 2. Apply CNOT gate to Q0.
    4: {
        "qubits": 2,
        "gates": ['x', 'cx'],
        "goal_state": [ 0+0j, 0+0j, 0+0j, 1+0j ]
    },
    # 1. Apply H gate to Q0. 2. Apply CNOT gate to Q0.
    5: {
        "qubits": 2,
        "gates": ['cx', 'h'],
        "goal_state": [ 0.707+0j, 0+0j, 0+0j, 0.707+0j ],
    },
    # 1. Apply RY gate to Q0. 2. Apply CNOT gate to Q0. 3. Apply NOT gate to Q1.
    6: {
        "qubits": 2,
        "gates": ['ry', 'cx', 'x'],
        "goal_state": [ 0+0j, 0.707+0j, 0.707+0j, 0+0j ],
    },
    # 1. Apply X gate to Q0. 2. Apply X gate to Q1. 3. Apply T gate to Q0.
    7: {
        "qubits": 3,
        "gates": ['x', 'x', 'ccx'],
        "goal_state": [ 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 1+0j ],
    },
    # 1. Apply H gate to Q0. 2. Apply H gate to Q2. 3. Apply CNOT gate to Q1. 4. Apply CNOT gate to Q0.
    8: {
        "qubits": 3,
        "gates": ['h', 'h', 'cx', 'cx'],
        "goal_state": [ 0.5+0j, 0+0j, 0+0j, 0.5+0j, 0.5+0j, 0+0j, 0+0j, 0.5+0j ],
    },
    # 1. Apply X gate to Q0. 2. Apply X to Q1. 3. Apply X to Q2. 4. Apply H to Q1. 5. Apply CCX to Q1.
    9: {
        "qubits": 4,
        "gates": ['x', 'x', 'x', 'h', 'ccx'],
        "goal_state": [ 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0.707+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, -0.707+0j ],
    },
    # 1. Apply RY gate to Q0. 2. Apply X to Q1. 3. Apply H to Q2. 4. Apply H to Q3. 5. Apply CX to Q0.
    10: {
        "qubits": 4,
        "gates": ['ry', 'h', 'h', 'x', 'cx'],
        "goal_state": [ 0+0j, 0.354+0j, 0.354+0j, 0+0j, 0+0j, 0.354+0j, 0.354+0j, 0+0j, 0+0j, 0.354+0j, 0.354+0j, 0+0j, 0+0j, 0.354+0j, 0.354+0j, 0+0j ],
    }
}

