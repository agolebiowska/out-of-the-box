import pygame

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere
import matplotlib.backends.backend_agg as agg
import numpy as np
import matplotlib.pyplot as plt

from globals import *
from entities import Qubit, Gate

class Level:
    def __init__(self, qubits_num, gates, goal_state):
        self.box = pygame.image.load("assets/box.png")
        self.box = pygame.transform.scale(self.box, (1820, 780))
        self.box_rect = pygame.Rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT)
        self.goal_state = Statevector(np.array(goal_state))
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
        self.pacz = pygame.image.load("assets/pacz.png")

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
            elif selected_gate.id == "cx":
                if len(self.qubits) == 2: # todo: fix?
                    self.quantum_circuit.cx(0, 1)
                elif len(self.qubits) > qubit.id+1:
                   self.quantum_circuit.cx(qubit.id, qubit.id+1) 
            elif selected_gate.id == "t":
                self.quantum_circuit.t(qubit.id)
            elif selected_gate.id == "z":
                self.quantum_circuit.z(qubit.id)
            elif selected_gate.id == "ry":
                self.quantum_circuit.ry(np.pi/2, qubit.id)
            elif selected_gate.id == "ccx":
                if len(self.qubits) > qubit.id+2:
                    self.quantum_circuit.ccx(qubit.id, qubit.id+1, qubit.id+2)

            simulator = Aer.get_backend('statevector_simulator')
            job = execute(self.quantum_circuit, simulator)
            result = job.result()
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

    def plot_sphere(self, state):
        fig = plot_state_qsphere(state, show_state_phases=False, figsize=(3,3))
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        wh = canvas.get_width_height()
        return pygame.image.fromstring(raw_data, wh, "RGB")

    def draw_states(self, screen):
        if self.goal_state_show:
            self.goal_state_surface = self.plot_sphere(self.goal_state)
        if self.state_needs_update:
            self.state_surface = self.plot_sphere(self.current_state)
        goal_state_x = (WIDTH + len(self.inventory) * 64) // 2
        current_state_x = (WIDTH - len(self.inventory) * 64) // 2 - self.state_surface.get_width()
        y_position = HEIGHT - 264
        screen.blit(self.goal_state_surface, (goal_state_x, y_position))
        screen.blit(self.state_surface, (current_state_x, y_position))
        self.goal_state_show = False
        self.state_needs_update = False
        screen.blit(self.pacz, (689, 1006))
        screen.blit(self.pacz, (1308, 1001))
        font = pygame.font.Font(font_file, 24)
        state_text = font.render("Current state >", True, MAGENTA)
        goal_text = font.render("< Goal state", True, GREEN)
        state_text_x = current_state_x - self.state_surface.get_width()
        goal_text_x = goal_state_x + self.goal_state_surface.get_width()
        screen.blit(state_text, (state_text_x, HEIGHT - 160))
        screen.blit(goal_text, (goal_text_x, HEIGHT - 160))
        plt.close()

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

    def is_completed(self, screen):
        decimal_places = 3
        current_state_rounded = np.round(self.current_state, decimals=decimal_places)
        goal_state_rounded = np.round(self.goal_state, decimals=decimal_places)

        is_completed = (len(self.gates) <= 0 and
                all(v is None for v in self.inventory) and
                np.all(current_state_rounded == goal_state_rounded))

        if is_completed:
            font = pygame.font.Font(font_file, 24)
            current_state_x = (WIDTH - len(self.inventory) * 64) // 2 - self.state_surface.get_width()
            state_text = font.render("Current state >", True, GREEN)
            state_text_x = current_state_x - self.state_surface.get_width()
            screen.blit(state_text, (state_text_x, HEIGHT - 160))

        return is_completed

