import pygame
import sys
import random
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
from pygame.locals import *
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector

WIDTH, HEIGHT = 1920, 1080
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF)
pygame.display.set_caption("Out of the box")
clock = pygame.time.Clock()

TOP_MARGIN, BOTTOM_MARGIN = 100, 200
BOX_WIDTH, BOX_HEIGHT = WIDTH - 100, HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
BOX_X, BOX_Y = (WIDTH - BOX_WIDTH) // 2, TOP_MARGIN
SLOT_WIDTH, SLOT_HEIGHT = 40, 40
FONT = pygame.font.Font(None, 36)
PLAYER_SPEED = 5

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

poison_timer = 300
poison_color = (0, 255, 0)
poison_alpha = 0
poison_overlay = pygame.Surface((BOX_WIDTH, BOX_HEIGHT), pygame.SRCALPHA)

plt.style.use('dark_background')
inventory = [None, None, None]
player_rect = pygame.Rect(100, 100, 40, 40)
level_box_rect = pygame.Rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT)
state_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
state_needs_update = True
goal_state_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
goal_state_show = True

class Item:
    def __init__(self, id, rect, color, item_type, state=[]):
        self.rect = rect
        self.color = color
        self.id = id
        self.item_type = item_type
        self.state = state

class Player:
    def __init__(self, x, y, sprite_sheet, game_box):
        self.animations = ["down", "left", "right", "up", "idle"]
        self.frames = {animation: [] for animation in self.animations}
        self.load_frames(sprite_sheet)

        self.animation = "idle"
        self.frame_index = 0
        self.image = self.frames[self.animation][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_speed = 0.5
        self.animation_timer = 0
        self.game_box = game_box

    def load_frames(self, sprite_sheet):
        num_rows = 5
        num_cols = 6
        scale_factor = 4
        frame_width = sprite_sheet.get_width() // num_cols
        frame_height = sprite_sheet.get_height() // num_rows

        for row, animation in enumerate(self.animations):
            for col in range(num_cols):
                x = col * frame_width
                y = row * frame_height
                subsurface_width = min(frame_width, sprite_sheet.get_width() - x)
                subsurface_height = min(frame_height, sprite_sheet.get_height() - y)
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, subsurface_width, subsurface_height))
                frame = pygame.transform.scale(frame, (subsurface_width * scale_factor, subsurface_height * scale_factor))
                self.frames[animation].append(frame)

    def update(self, delta_time, dx, dy):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.animation])
            self.image = self.frames[self.animation][self.frame_index]

    def move(self, dx, dy):
        if dx > 0:
            self.animation = "right"
        elif dx < 0:
            self.animation = "left"
        elif dy > 0:
            self.animation = "down"
        elif dy < 0:
            self.animation = "up"
        else:
            self.animation = "idle"

        self.rect.move_ip(dx, dy)

        if not self.game_box.contains(self.rect):
            self.rect.clamp_ip(self.game_box)

    def is_colliding(self, items):
        return any(self.rect.colliderect(item.rect) for item in items)

class Qubit(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, game_box, id):
        super().__init__()
        self.animations = ["down", "left", "right", "up"]
        self.frames = {animation: [] for animation in self.animations}
        self.load_frames(sprite_sheet)

        self.animation = random.choice(self.animations)
        self.frame_index = 0
        self.image = self.frames[self.animation][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.random_position()
        self.animation_speed = 0.6
        self.animation_timer = 0
        self.game_box = game_box
        self.id = id

        self.direction = random.choice(self.animations)

    def load_frames(self, sprite_sheet):
        num_rows = 4
        num_cols = 3
        scale_factor = 4
        frame_width = sprite_sheet.get_width() // num_cols
        frame_height = sprite_sheet.get_height() // num_rows

        for row, animation in enumerate(self.animations):
            for col in range(num_cols):
                x = col * frame_width
                y = row * frame_height
                subsurface_width = min(frame_width, sprite_sheet.get_width() - x)
                subsurface_height = min(frame_height, sprite_sheet.get_height() - y)
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, subsurface_width, subsurface_height))
                frame = pygame.transform.scale(frame, (subsurface_width * scale_factor, subsurface_height * scale_factor))
                self.frames[animation].append(frame)

    def move(self, dx, dy):
        if dx > 0:
            new_direction = "right"
        elif dx < 0:
            new_direction = "left"
        elif dy > 0:
            new_direction = "down"
        elif dy < 0:
            new_direction = "up"

        self.direction = new_direction
        self.animation = new_direction

        new_rect = self.rect.move(dx, dy)
        if self.game_box.contains(new_rect):
            self.rect = new_rect

    def update(self, delta_time, dx, dy):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.animation])
            self.image = self.frames[self.animation][self.frame_index]

        if self.direction == "up":
            self.move(0, -1)
        elif self.direction == "down":
            self.move(0, 1)
        elif self.direction == "left":
            self.move(-1, 0)
        elif self.direction == "right":
            self.move(1, 0)

        if random.random() < 0.01:
            self.direction = random.choice(self.animations)

        if not self.game_box.contains(self.rect):
            self.rect.clamp_ip(self.game_box)

    def random_position(self):
        return (random.randint(BOX_X, BOX_X + BOX_WIDTH - 10), 
                random.randint(BOX_Y, BOX_Y + BOX_HEIGHT - 10))

class Gate(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, game_box, id):
        super().__init__()
        self.id = id
        self.sprite = sprite_sheet
        self.rect = self.random_position()

    def random_position(self):
        x = random.randint(BOX_X, BOX_X + BOX_WIDTH - 10)
        y = random.randint(BOX_Y, BOX_Y + BOX_HEIGHT - 10)
        return pygame.Rect(x, y, 20, 20)

def random_position(existing_items):
    return pygame.Rect(random.randint(BOX_X, BOX_X + BOX_WIDTH - 10), 
                       random.randint(BOX_Y, BOX_Y + BOX_HEIGHT - 10), 
                       20, 20)

def is_position_valid(rect, existing_items):
    return level_box_rect.contains(rect) and not any(rect.colliderect(item.rect) for item in existing_items)

def create_item(id, existing_items, rect_size, color, item_type):
    while True:
        rect = random_position(existing_items)
        if is_position_valid(rect, existing_items):
            return Item(rect=rect, color=color, id=id, item_type=item_type)

def create_quantum_circuit(qbits):
    q = QuantumRegister(qbits)
    c = ClassicalRegister(qbits)
    qc = QuantumCircuit(q, c)
    return qc

qubits = []
gates = []

qubit_sprite_sheet = pygame.image.load('assets/qubit.png')
gate_sprite_sheet = pygame.image.load('assets/qubit.png')

def load_qubits(sprite_sheet, num_qubits):
    qubits = []
    for i in range(num_qubits):
        qubit = Qubit(sprite_sheet, level_box_rect, i)
        qubits.append(qubit)
    return qubits

level_data = {
    1: {
        "qubits": load_qubits(qubit_sprite_sheet, 1),
        "gates": [Gate(gate_sprite_sheet, level_box_rect, "X")],
        "goal_state": Statevector.from_label('1'),
        "current_state": Statevector.from_label('0' * 1),
        "quantum_circuit": create_quantum_circuit(1)
    },
    2: {
        "qubits": load_qubits(qubit_sprite_sheet, 2),
        "gates": [Gate(gate_sprite_sheet, level_box_rect, "X"), Gate(gate_sprite_sheet, level_box_rect, "H")],
        "goal_state": Statevector.from_label('01'),
        "current_state": Statevector.from_label('0' * 2),
        "quantum_circuit": create_quantum_circuit(2)
    }
}

current_level = 2
current_data = level_data[current_level]
level_items = current_data["gates"] + current_data["qubits"]

def update_quantum_state():
    global state_needs_update
    state_needs_update = True

def draw_inventory():
    for i, item in enumerate(inventory):
        pygame.draw.rect(screen, WHITE, (i * SLOT_WIDTH, 0, SLOT_WIDTH, SLOT_HEIGHT), 2)
        if item is not None:
            text = FONT.render(item, True, WHITE)
            screen.blit(text, (i * SLOT_WIDTH + 10, 10))

def add_item_to_inventory(item):
    for i, slot in enumerate(inventory):
        if slot is None:
            inventory[i] = item.id
            return

def use_gate_on_qubit(selected_gate_index, qubit):
    if inventory[selected_gate_index] is not None:
        selected_gate = inventory[selected_gate_index]
        qc = current_data["quantum_circuit"]
        qubit_index = current_data["qubits"].index(qubit)

        if selected_gate == "X":
            qc.x(qubit_index)
        elif selected_gate == "H":
            qc.h(qubit_index)
        elif selected_gate == "CX":
            pass

        backend = Aer.get_backend('statevector_simulator')
        result = backend.run(qc).result()
        psi = result.get_statevector(qc)
        current_data["current_state"] = psi
        update_quantum_state()
        inventory[selected_gate_index] = None

def plot_bloch_sphere(state, label):
    fig = plot_bloch_multivector(state, figsize=(1.6, 1.6))
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    wh = canvas.get_width_height()
    return pygame.image.fromstring(raw_data, wh, "RGB") 

def draw_states():
    global state_surface, state_needs_update
    global goal_state_show, goal_state_surface
    if goal_state_show:
        goal_state = current_data.get("goal_state")
        goal_state_surface = plot_bloch_sphere(goal_state, "test") 
    if state_needs_update:
        current_state = current_data.get("current_state")
        state_surface = plot_bloch_sphere(current_state, "test") 
    screen.blit(goal_state_surface, (WIDTH - 400, HEIGHT - BOTTOM_MARGIN))
    screen.blit(state_surface, (100, HEIGHT - BOTTOM_MARGIN))
    goal_state_show = False
    state_needs_update = False

def check_level_completion():
    return False

def update_poison_color():
    global poison_alpha, poison_color
    poison_alpha += .1
    poison_color = (0, 255, 0, poison_alpha)

def is_game_over():
    return poison_alpha >= 255

def reset_level():
    global poison_alpha, current_level, current_data, level_items, player_rect, inventory
    current_data = level_data[current_level]
    level_items = current_data["gates"] + current_data["qubits"]
    player_rect.topleft = (BOX_X + BOX_WIDTH // 2, BOX_Y + BOX_HEIGHT // 2)
    poison_alpha = 0
    inventory = [None, None, None]

def load_next_level():
    global poison_alpha, current_level, current_data, level_items, player_rect, inventory
    current_level += 1
    if current_level <= len(level_data):
        current_data = level_data[current_level]
        level_items = current_data["gates"] + current_data["qubits"]
        player_rect.topleft = (BOX_X + BOX_WIDTH // 2, BOX_Y + BOX_HEIGHT // 2)
        poison_alpha = 0
        inventory = [None, None, None]
    else:
        print("Congratulations! You've completed all levels.")
        pygame.quit()
        sys.exit()


def main():
    player = Player(100,
                    100,
                    pygame.image.load('assets/player.png'),
                    level_box_rect)

    delta_time = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = PLAYER_SPEED
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED

        player.move(dx, dy)

        for item in level_items:
            if player.is_colliding([item]):
                if isinstance(item, Gate):
                    add_item_to_inventory(item)
                    level_items.remove(item)
                elif isinstance(item, Qubit):
                    if keys[pygame.K_1]:
                        use_gate_on_qubit(0, item)
                    elif keys[pygame.K_2]:
                        use_gate_on_qubit(1, item)
                    elif keys[pygame.K_3]:
                        use_gate_on_qubit(2, item)

        clock.tick(60)

        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, level_box_rect)

        for qubit in current_data["qubits"]:
            qubit.update(delta_time, dx, dy)
            screen.blit(qubit.image, qubit.rect.topleft)

        for gate in current_data["gates"]:
            screen.blit(gate.sprite, gate.rect.topleft)

        screen.blit(player.image, player.rect.topleft)

        if not is_game_over():
            update_poison_color()
            pygame.draw.rect(poison_overlay, poison_color, (0, 0, WIDTH, HEIGHT))
            screen.blit(poison_overlay, (BOX_X, BOX_Y))

        draw_inventory()
        draw_states()
        pygame.display.flip()

        if is_game_over():
            reset_level()

        if check_level_completion():
            print("Level completed!")
            pygame.time.delay(3000)
            load_next_level()

        current_time = pygame.time.get_ticks()
        delta_time = (current_time - delta_time) / 1000.0
        delta_time = min(delta_time, 0.1)

        player.update(delta_time, dx, dy)

    pygame.quit()

if __name__ == "__main__":
    main()
