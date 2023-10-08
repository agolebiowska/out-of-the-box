import sys
import random
import pygame

import matplotlib.pyplot as plt

from pygame.locals import *

from entities import *
from globals import *
from level import Level

# todo:
# 1. Huge list of possible levels with difficulty and randomly choosing them
# 2. Increase qubits speed with levels
# 3. Add items for player to take, like temporary speed, ctrl+z etc.
# 4. Adjust poison speed per level.
# 5. Make kitty in the top corner say mean things - maybe wrong tips?
# 6. Make difficulty levels to choose (poison speed)

MENU = 0
PLAYING = 1
WON = 2
DIED = 3

game_state = MENU

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF)
pygame.display.set_caption("Out of the box")
clock = pygame.time.Clock()

pygame.mixer.music.load('assets/music_3.mp3')
pygame.mixer.music.play(-1)

plt.style.use('bloch.mplstyle')

current_level = 1
current_level_data = level_data[current_level]
level = Level(qubits_num=current_level_data["qubits"],
              gates=current_level_data["gates"],
              goal_state=current_level_data["goal_state"])

player = Player(100, 100, level.box_rect)

menu = pygame.image.load("assets/menu.png")
menu = pygame.transform.scale(menu, (1920,1080))

kitty_corner = pygame.image.load("assets/kitty_corner.png")
tail_corner = pygame.image.load("assets/tail_corner.png")

def display_menu(screen, selected_option):
    screen.fill(BLACK)
    screen.blit(menu, (0,0))
    font = pygame.font.Font(font_file, 50)
    title_font = pygame.font.Font(font_file, 100)
    start_text = font.render("START", True, PURPLE if selected_option == 0 else WHITE)
    quit_text = font.render("QUIT", True,  PURPLE if selected_option == 1 else WHITE)
    title = title_font.render("Out of the Box", True, WHITE)
    screen_width, screen_height = screen.get_size()
    start_x = (screen_width - start_text.get_width()) // 2
    start_y = (screen_height - start_text.get_height()) // 2 - 50
    quit_x = (screen_width - quit_text.get_width()) // 2
    quit_y = (screen_height - quit_text.get_height()) // 2 + 50
    title_x = (screen_width - title.get_width()) // 2
    title_y = (screen_height - title.get_height()) // 2 - 300
    screen.blit(title, (title_x, title_y))
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
    return (level.poison_alpha >= 255 or
            (len(level.gates) <= 0 and all(v is None for v in level.inventory)) and
            not level.is_completed(screen))

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
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_state = MENU
                    reset_level()

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
                        elif keys[pygame.K_4]:
                            level.use_gate_on_qubit(3, item)
                        elif keys[pygame.K_5]:
                            level.use_gate_on_qubit(4, item)

            clock.tick(60)

            screen.fill(BLACK)

            level.draw_inventory(screen)
            level.draw_states(screen)
            screen.blit(level.box, (BOX_X-184, BOX_Y-164))

            for gate in level.gates:
                screen.blit(gate.sprite, gate.rect.topleft)

            for qubit in level.qubits:
                qubit.update(delta_time, dx, dy)
                qubit.draw(screen)

            screen.blit(player.sprite, player.rect.topleft)
            screen.blit(kitty_corner, (0, 0))
            screen.blit(tail_corner, (WIDTH - tail_corner.get_width(), HEIGHT - tail_corner.get_height()))

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

            if level.is_completed(screen):
                print("Level completed!")
                pygame.time.delay(1000)
                load_next_level()

            if is_game_over():
                game_state = DIED

        elif game_state == WON:
            font = pygame.font.Font(font_file, 100)
            text = font.render("YOU WON", True, BLUE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            font = pygame.font.Font(font_file, 36)
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
            font = pygame.font.Font(font_file, 100)
            text = font.render("YOU DIED", True, RED)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            font = pygame.font.Font(font_file, 36)
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
