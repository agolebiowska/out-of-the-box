import sys
import random
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np

import pygame
from pygame.locals import *

from entities import *
from globals import *
from level import Level

pygame.init()
FONT = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF)
pygame.display.set_caption("Out of the box")
clock = pygame.time.Clock()

plt.style.use('dark_background')

current_level = 1
current_level_data = level_data[current_level]
level = Level(qubits_num=current_level_data["qubits"],
              gates=current_level_data["gates"],
              goal_state=current_level_data["goal_state"])

player = Player(100, 100, level.box_rect)

def check_level_completion():
    return False

def is_game_over():
    return level.poison_alpha >= 255

def reset_level():
    level = Level(current_level_data["qubits"],
                  current_level_data["gates"],
                  current_level_data["goal_state"])

def load_next_level():
    global current_level, current_level_data
    current_level += 1
    if current_level <= len(level_data):
        current_level_data = level_data[current_level]
        level = Level(current_level_data["qubits"],
                      current_level_data["gates"],
                      current_level_data["goal_state"])
    else:
        print("Congratulations! You've completed all levels.")
        pygame.quit()
        sys.exit()


def main():
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
            dy = -player.move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = player.move_speed 
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -player.move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = player.move_speed

        player.move(dx, dy)

        for item in level.items:
            if player.is_colliding([item]):
                if isinstance(item, Gate):
                    add_item_to_inventory(item)
                    level.items.remove(item)
                elif isinstance(item, Qubit):
                    if keys[pygame.K_1]:
                        level.use_gate_on_qubit(0, item)
                    elif keys[pygame.K_2]:
                        level.use_gate_on_qubit(1, item)
                    elif keys[pygame.K_3]:
                        level.use_gate_on_qubit(2, item)

        clock.tick(60)

        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, level.box_rect)

        for qubit in level.qubits:
            qubit.update(delta_time, dx, dy)
            screen.blit(qubit.image, qubit.rect.topleft)

        for gate in level.gates:
            screen.blit(gate.sprite, gate.rect.topleft)

        screen.blit(player.image, player.rect.topleft)

        if not is_game_over():
            level.update_poison_color()
            pygame.draw.rect(level.poison_overlay, level.poison_color, (0, 0, WIDTH, HEIGHT))
            screen.blit(level.poison_overlay, (BOX_X, BOX_Y))

        level.draw_inventory(screen)
        level.draw_states(screen)
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
