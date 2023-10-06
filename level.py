import pygame

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np

from globals import *
from entities import Qubit, Gate

class Level:
    def __init__(self, qubits_num, gates, goal_state):
        self.box_rect = pygame.Rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT)
        self.goal_state = Statevector.from_label(goal_state)
        self.qubits = self.load_qubits(qubits_num)
        self.gates = self.load_gates(gates)
        self.current_state = Statevector.from_label("0" * qubits_num)
        self.quantum_circuit = self.create_quantum_circuit(qubits_num)
        self.items = self.qubits + self.gates
        self.inventory = [None, None, None]
        self.state_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.state_needs_update = True
        self.goal_state_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.goal_state_show = True
        self.poison_timer = 300
        self.poison_color = (0, 255, 0)
        self.poison_alpha = 0
        self.poison_overlay = pygame.Surface((BOX_WIDTH, BOX_HEIGHT), pygame.SRCALPHA)

    def load_qubits(self, qubits_num):
        qubits = []
        for id in range(qubits_num):
            qubit = Qubit(id, self.box_rect)
            qubits.append(qubit)
        return qubits

    def load_gates(self, gates):
        gates = []
        for id in gates:
            gate = Gate(id, self.box_rect)
            gates.append(gate)
        return gates

    def create_quantum_circuit(self, qubits_num):
        q = QuantumRegister(qubits_num)
        c = ClassicalRegister(qubits_num)
        qc = QuantumCircuit(q, c)
        return qc

    def use_gate_on_qubit(gate_index, qubit, inventory):
        if inventory[gate_index] is not None:
            selected_gate = inventory[gate_index]
            qc = self.quantum_circuit

            if selected_gate == "X":
                qc.x(qubit.id)
            elif selected_gate == "H":
                qc.h(qubit.id)

        backend = Aer.get_backend("statevector_simulator")
        result = backend.run(qc).result()
        psi = result.get_statevector(qc)
        self.current_state = psi
        self.state_needs_update = True
        inventory[selected_gate_index] = None

    def draw_inventory(self, screen):
        for i, item in enumerate(self.inventory):
            pygame.draw.rect(
                screen, WHITE, (i * SLOT_WIDTH, 0, SLOT_WIDTH, SLOT_HEIGHT), 2
            )
            if item is not None:
                text = FONT.render(item, True, WHITE)
                screen.blit(text, (i * SLOT_WIDTH + 10, 10))

    def add_item_to_inventory(self, item):
        for i, slot in enumerate(self.inventory):
            if slot is None:
                self.inventory[i] = item.id
                return

    def plot_bloch_sphere(self, state, label):
        fig = plot_bloch_multivector(state, figsize=(1.6, 1.6))
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        wh = canvas.get_width_height()
        return pygame.image.fromstring(raw_data, wh, "RGB")

    def draw_states(self, screen):
        if self.goal_state_show:
            self.goal_state_surface = self.plot_bloch_sphere(self.goal_state, "test")
        if self.state_needs_update:
            self.state_surface = self.plot_bloch_sphere(self.current_state, "test")
        screen.blit(self.goal_state_surface, (WIDTH - 400, HEIGHT - BOTTOM_MARGIN))
        screen.blit(self.state_surface, (100, HEIGHT - BOTTOM_MARGIN))
        self.goal_state_show = False
        self.state_needs_update = False

    def update_poison_color(self):
        self.poison_alpha += 0.1
        self.poison_color = (0, 255, 0, self.poison_alpha)
