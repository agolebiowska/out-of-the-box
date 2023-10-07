import pygame

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.backends.backend_agg as agg
import numpy as np

from globals import *
from entities import Qubit, Gate

class Level:
    def __init__(self, qubits_num, gates, goal_state):
        self.box = pygame.image.load("assets/box.png")
        self.box = pygame.transform.scale(self.box, (1820, 780))
        self.box_rect = pygame.Rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT)
        self.goal_state = Statevector.from_label(goal_state)
        self.qubits = self.load_qubits(qubits_num)
        self.gates = self.load_gates(gates)
        self.current_state = Statevector.from_label("0" * qubits_num)
        self.quantum_circuit = self.create_quantum_circuit(qubits_num)
        self.items = self.qubits + self.gates
        self.inventory = [None, None, None, None, None]
        self.state_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.state_needs_update = True
        self.goal_state_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.goal_state_show = True
        self.poison_timer = 300
        self.poison_alpha = 0
        self.poison = pygame.image.load("assets/poison.png").convert_alpha()
        self.poison = pygame.transform.scale(self.poison, (WIDTH, HEIGHT))
        self.poison_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.font = pygame.font.Font(font_file, 36)
        self.slot_image = pygame.image.load("assets/slot.png")

    def load_qubits(self, qubits_num):
        qubits = []
        for id in range(qubits_num):
            qubit = Qubit(id, self.box_rect)
            qubits.append(qubit)
        return qubits

    def load_gates(self, gate_ids):
        gates = []
        for id in gate_ids:
            gate = Gate(id, self.box_rect)
            gates.append(gate)
        return gates

    def create_quantum_circuit(self, qubits_num):
        q = QuantumRegister(qubits_num)
        c = ClassicalRegister(qubits_num)
        qc = QuantumCircuit(q, c)
        return qc

    def use_gate_on_qubit(self, gate_index, qubit):
        if self.inventory[gate_index] is not None:
            selected_gate = self.inventory[gate_index]

            if selected_gate.id == "x":
                self.quantum_circuit.x(qubit.id)
            elif selected_gate.id == "h":
                self.quantum_circuit.h(qubit.id)

            backend = Aer.get_backend("statevector_simulator")
            result = backend.run(self.quantum_circuit).result()
            psi = result.get_statevector(self.quantum_circuit)
            self.current_state = psi
            self.state_needs_update = True
            self.inventory[gate_index] = None

    def draw_inventory(self, screen):
        SLOT_WIDTH, SLOT_HEIGHT = 64, 64
        inventory_width = len(self.inventory) * SLOT_WIDTH
        start_x = (WIDTH - inventory_width) // 2
        for i, item in enumerate(self.inventory):
            slot_x = start_x + i * SLOT_WIDTH
            slot_y = HEIGHT - 150
            screen.blit(self.slot_image, (slot_x, slot_y))
            if item is not None and isinstance(item, Gate):
                sprite_x = slot_x + (SLOT_WIDTH - item.sprite.get_width()) // 2
                sprite_y = slot_y + (SLOT_HEIGHT - item.sprite.get_height()) // 2
                screen.blit(item.sprite, (sprite_x, sprite_y))

    def add_item_to_inventory(self, item):
        for i, slot in enumerate(self.inventory):
            if slot is None:
                self.inventory[i] = item
                return

    def plot_bloch_sphere(self, state, label):
        fig = plot_bloch_multivector(state, figsize=(2,2))
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        wh = canvas.get_width_height()
        return pygame.image.fromstring(raw_data, wh, "RGB")

    def draw_states(self, screen):
        if self.goal_state_show:
            self.goal_state_surface = self.plot_bloch_sphere(self.goal_state, "goal")
        if self.state_needs_update:
            self.state_surface = self.plot_bloch_sphere(self.current_state, "current")
        goal_state_x = (WIDTH + len(self.inventory) * 64) // 2
        current_state_x = (WIDTH - len(self.inventory) * 64) // 2 - self.state_surface.get_width()
        y_position = HEIGHT - BOTTOM_MARGIN

        screen.blit(self.goal_state_surface, (goal_state_x, y_position))
        screen.blit(self.state_surface, (current_state_x, y_position))
        self.goal_state_show = False
        self.state_needs_update = False

    def draw_poison_bar(self, screen):
        progress_bar_width = 255
        progress_bar_height = 20
        progress_bar_x = (WIDTH - progress_bar_width) // 2
        progress_bar_y = 30
        pygame.draw.rect(screen, WHITE, (progress_bar_x - 2, progress_bar_y - 2, progress_bar_width + 4, progress_bar_height + 4))
        pygame.draw.rect(screen, GREEN, (progress_bar_x, progress_bar_y, self.poison_alpha, progress_bar_height))

    def update_poison_color(self):
        self.poison_alpha += 0.2
        self.poison.set_alpha(self.poison_alpha)

    def is_completed(self):
        return self.current_state.equiv(self.goal_state)

