import sys
import random
import pygame

import matplotlib.pyplot as plt

from pygame.locals import *

from entities import *
from globals import *
from level import Level

MENU = 0
PLAYING = 1
WON = 2
DIED = 3

game_state = MENU

pygame.init()
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

menu = pygame.image.load("assets/menu.png")

def display_menu(screen, selected_option):
    screen.fill(BLACK)
    screen.blit(menu, (0,0))
    font = pygame.font.Font(None, 50)
    start_text = font.render("START", True, LIGHT_BROWN if selected_option == 0 else WHITE)
    quit_text = font.render("QUIT", True, LIGHT_BROWN if selected_option == 1 else WHITE)
    screen_width, screen_height = screen.get_size()
    start_x = (screen_width - start_text.get_width()) // 2
    start_y = (screen_height - start_text.get_height()) // 2 - 50
    quit_x = (screen_width - quit_text.get_width()) // 2
    quit_y = (screen_height - quit_text.get_height()) // 2 + 50
    screen.blit(start_text, (start_x, start_y))
    screen.blit(quit_text, (quit_x, quit_y))
    pygame.display.flip()

def handle_menu_input(selected_option):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                if selected_option == 1:
                    pygame.quit()
                    sys.exit()
                return selected_option, PLAYING
            elif event.key == K_UP:
                selected_option = max(0, selected_option - 1)
            elif event.key == K_DOWN:
                selected_option = min(1, selected_option + 1)

    return selected_option, MENU

def is_game_over():
    return level.poison_alpha >= 255

def reset_level():
    global current_level, current_level_data, level
    current_level_data = level_data[current_level]
    level = Level(current_level_data["qubits"],
                  current_level_data["gates"],
                  current_level_data["goal_state"])

def load_next_level():
    global current_level, current_level_data, level
    current_level += 1
    if current_level <= len(level_data):
        current_level_data = level_data[current_level]
        level = Level(current_level_data["qubits"],
                      current_level_data["gates"],
                      current_level_data["goal_state"])
    else:
        global game_state
        game_state = WON
        print("Congratulations! You've completed all levels.")


def main():
    global game_state, current_level
    delta_time = 0
    running = True
    selected_option = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        if game_state == MENU:
            display_menu(screen, selected_option)
            selected_option, game_state = handle_menu_input(selected_option)
        elif game_state == PLAYING:
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
                        level.add_item_to_inventory(item)
                        level.items.remove(item)
                        level.gates.remove(item)
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
            screen.blit(level.box, (BOX_X-184, BOX_Y-164))

            for qubit in level.qubits:
                qubit.update(delta_time, dx, dy)
                qubit.draw(screen)

            for gate in level.gates:
                screen.blit(gate.sprite, gate.rect.topleft)

            screen.blit(player.sprite, player.rect.topleft)

            if is_game_over():
                game_state = DIED

            level.draw_inventory(screen)
            level.draw_states(screen)

            if not is_game_over():
                level.update_poison_color()
                level.draw_poison_bar(screen)
                level.poison_overlay.fill((0,0,0,0))
                level.poison_overlay.blit(level.poison, (0, 0))
                screen.blit(level.poison_overlay, (0,0))

            pygame.display.flip()

            current_time = pygame.time.get_ticks()
            delta_time = (current_time - delta_time) / 1000.0
            delta_time = min(delta_time, 0.1)

            player.update(delta_time, dx, dy)

            if level.is_completed():
                print("Level completed!")
                pygame.time.delay(1000)
                load_next_level()

        elif game_state == WON:
            font = pygame.font.Font(None, 100)
            text = font.render("YOU WON", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            font = pygame.font.Font(None, 36)
            return_text = font.render("Press Enter to return to main menu", True, WHITE)
            return_text_rect = return_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(return_text, return_text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        current_level = 1
                        game_state = MENU
                        selected_option = 0
                        reset_level()

        elif game_state == DIED:
            font = pygame.font.Font(None, 100)
            text = font.render("YOU DIED", True, RED)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            font = pygame.font.Font(None, 36)
            return_text = font.render("Press Enter to restart", True, WHITE)
            return_text_rect = return_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(return_text, return_text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        game_state = PLAYING
                        reset_level()

    pygame.quit()

if __name__ == "__main__":
    main()
