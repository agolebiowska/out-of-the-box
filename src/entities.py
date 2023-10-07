import pygame
import random

from globals import *

class Player:
    def __init__(self, x, y, level_box):
        self.animations = ["down", "left", "right", "up", "idle"]
        self.frames = {animation: [] for animation in self.animations}
        self.load_frames(pygame.image.load('assets/player.png'))
        self.move_speed = 7
        self.animation = "idle"
        self.frame_index = 0
        self.sprite = self.frames[self.animation][self.frame_index]
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (x, y)
        self.animation_speed = 0.5
        self.animation_timer = 0
        self.level_box = level_box

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
            self.sprite = self.frames[self.animation][self.frame_index]

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

        if not self.level_box.contains(self.rect):
            self.rect.clamp_ip(self.level_box)

    def is_colliding(self, items):
        return any(self.rect.colliderect(item.rect) for item in items)

class Qubit():
    def __init__(self, id, level_box):
        self.animations = ["down", "left", "right", "up"]
        self.frames = {animation: [] for animation in self.animations}
        self.load_frames(pygame.image.load('assets/qubit.png'))
        self.move_speed = 8

        self.animation = random.choice(self.animations)
        self.frame_index = 0
        self.sprite = self.frames[self.animation][self.frame_index]
        self.rect = self.sprite.get_rect()
        self.rect.topleft = self.random_position()
        self.animation_speed = 0.4
        self.animation_timer = 0
        self.level_box = level_box
        self.id = id

        self.font = pygame.font.Font(font_file, 20)
        self.id_text = self.font.render(f"Q{self.id}", True, (255, 255, 255))
        self.id_text_rect = self.id_text.get_rect()
        self.id_text_rect.midtop = (self.rect.centerx, self.rect.top - 10)

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
        if self.level_box.contains(new_rect):
            self.rect = new_rect

    def update(self, delta_time, dx, dy):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.animation])
            self.sprite = self.frames[self.animation][self.frame_index]

        if self.direction == "up":
            self.move(0, -self.move_speed)
        elif self.direction == "down":
            self.move(0, self.move_speed)
        elif self.direction == "left":
            self.move(-self.move_speed, 0)
        elif self.direction == "right":
            self.move(self.move_speed, 0)

        if random.random() < 0.01:
            self.direction = random.choice(self.animations)

        if not self.level_box.contains(self.rect):
            self.rect.clamp_ip(self.level_box)

        self.id_text_rect.midtop = (self.rect.centerx, self.rect.top - 10)

    def draw(self, screen):
        screen.blit(self.sprite, self.rect.topleft)
        screen.blit(self.id_text, self.id_text_rect)

    def random_position(self):
        return (random.randint(BOX_X, BOX_X + BOX_WIDTH - 16), 
                random.randint(BOX_Y, BOX_Y + BOX_HEIGHT - 16))


class Gate():
    def __init__(self, id, level_box):
        self.id = id
        self.animations = ["idle"]
        self.frames = {animation: [] for animation in self.animations}
        self.load_frames(pygame.image.load(f'assets/{id}.png'))
        self.animation = "idle"
        self.frame_index = 0
        self.sprite = self.frames[self.animation][self.frame_index]
        self.rect = self.random_position()

    def load_frames(self, sprite_sheet):
        num_rows = 1
        num_cols = 1
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

    def random_position(self):
        x = random.randint(BOX_X, BOX_X + BOX_WIDTH - 16)
        y = random.randint(BOX_Y, BOX_Y + BOX_HEIGHT - 16)
        return pygame.Rect(x, y, 32, 32)
