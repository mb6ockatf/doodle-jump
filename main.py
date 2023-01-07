#!/usr/bin/env python3
import sys
import os
from random import randint
import pygame

pygame.init()
FPS = 70
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
pygame.display.set_caption("DOODLE JUMP")
black = pygame.Color("black")
white = pygame.Color("white")
difficulty = 6
running = True


def load_image(name: str) -> pygame.Surface:
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"file '{fullname}' not found")
        pygame.quit()
    image = pygame.image.load(fullname)
    image.set_colorkey(black)
    image.convert_alpha()
    return image


class Tile(pygame.sprite.Group):
    def __init__(self,
                 is_broken: bool,
                 group: pygame.sprite.Group,
                 player_jump: int,
                 player_x: int):
        super().__init__(group)
        self.is_broken = is_broken
        self.is_falling = False
        if self.is_broken:
            image_name = "broken_tile.png"
        else:
            image_name = "tile.png"
        image = load_image(image_name)
        self.image = pygame.transform.scale(image, (155, 35))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = (self.width, self.height)
        self.rect = self.image.get_rect()
        center_height = self.generate_height()
        center_width = self.generate_width(player_jump, player_x)
        self.rect.center = (center_width, center_height)
        self._edges = None
        self.rect.y = center_height

    def generate_width(self, correction_radius: int, correction_x: int) -> int:
        minimal = correction_x - correction_radius
        minimal = round(minimal)
        if minimal < 0:
            minimal = 0
        maximal = correction_x + correction_radius
        maximal = round(maximal)
        if maximal > screen_width:
            maximal = screen_width
        return randint(minimal, maximal)

    def generate_height(self) -> int:
        value = randint(screen_height // 4, screen_height // 3 * 2)
        value = int(round(value, -1))
        return value

    @property
    def edges(self) -> tuple:
        if not self._edges:
            left_edge = self.rect.x - self.width // 2
            right_edge = self.rect.x + self.width // 2
            self._edges = (left_edge, right_edge)
        return self._edges

"""
    def update(self):
        if self.is_broken and self.is_falling:
            self.fall()

    def fall(self):
        self.rect.y += 50
        if self.rect.y > screen_height:
            self.kill()
"""


class Hopalong(pygame.sprite.Sprite):
    def __init__(self, name: str, group: pygame.sprite.Group):
        super().__init__(group)
        self.jump_height = int(round(screen_height // 3 * 2, -1))
        self.move_length = screen_width // 2
        self.is_moving_up = None
        self.left_to_move_up = self.jump_height
        self.is_moving_right = None
        self.is_facing_right = False
        self.on_tile_edges = None
        self.name = name
        self.image_storage = {}
        self.image = None
        if self.name in ("sprout", "bird"):
            size = (100, 100)
            sprite_left = load_image(self.name + "_left.png")
            sprite_left = pygame.transform.scale(sprite_left, size)
            sprite_right = load_image(self.name + "_right.png")
            sprite_right = pygame.transform.scale(sprite_right, size)
            self.image_storage[self.name + "_left"] = sprite_left
            self.image_storage[self.name + "_right"] = sprite_right
            if self.image is None:
                self.image = self.image_storage[self.name + "_left"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = (self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.center = screen_height, screen_width // 2

    def update(self, group: pygame.sprite.Group, shift: int):
        if self.is_facing_right is True:
            self.image = self.image_storage[self.name + "_right"]
        else:
            self.image = self.image_storage[self.name + "_left"]
        shift = self.move(group, shift)
        return shift

    def move(self, group: pygame.sprite.Group, shift: int):
        is_still = not self.is_moving_up
        is_colliding = self.is_having_collision(group)
        if is_still and is_colliding:
            self.left_to_move_up = self.jump_height
            self.is_moving_up = True
            self.on_tile_edges = is_colliding.edges
            if shift == 0:
                shifting_height = self.count_shift(is_colliding)
                if shifting_height > 0:
                    shift = shifting_height
        if self.is_moving_right is True:
            self.rect.x += 18
            self.is_facing_right = True
            if self.rect.x > screen_width:
                self.rect.x = 0
        elif self.is_moving_right is False:
            self.rect.x -= 18
            self.is_facing_right = False
            if self.rect.x < 0:
                self.rect.x = screen_width
        if self.is_moving_right is not None:
            self.is_moving_right = None
        if self.on_tile_edges:
            edges = self.on_tile_edges
            if edges[0] > self.rect.x or edges[1] < self.rect.x:
                self.on_tile_edges = None
                self.is_moving_up = False
        if self.is_moving_up is True:
            if self.rect.y > 0:
                self.rect.y -= 10
            self.left_to_move_up -= 10
        elif self.is_moving_up is False:
            self.rect.y += 10
        if not self.left_to_move_up:
            if self.is_moving_up:
                self.is_moving_up = False
            else:
                self.is_moving_up = True
            self.left_to_move_up = self.jump_height
        return shift

    def is_alive(self):
        if self.rect.y > screen_height:
            return False
        return True

    def is_having_collision(self, group: pygame.sprite.Group) -> pygame.sprite.Sprite:
        for sprite in group:
            if not (sprite.edges[0] < self.rect.x < sprite.edges[1]):
                continue
            if sprite.rect.y - self.rect.y != 80:
                continue
            return sprite

    def count_shift(self, platform: pygame.sprite.Sprite):
        measurer = platform.rect.y
        value = round(screen_height - 200 - measurer, -1)
        value = int(value)
        return value


sprites = ["bird", "sprout"]
player_group = pygame.sprite.Group()
sprite_name = sprites[randint(0, 1)]
hopalong = Hopalong(sprite_name, player_group)
tiles_group = pygame.sprite.Group()
tile = Tile(False, tiles_group, hopalong.move_length, hopalong.rect.x)
print(screen_width, screen_height)
print(tile.rect.x, tile.rect.y)
SHIFT = 0
STEP =  0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_UP:
                if hopalong.is_moving_up is None:
                    hopalong.is_moving_up = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        hopalong.is_moving_right = True
    elif keys[pygame.K_LEFT]:
        hopalong.is_moving_right = False
    if hopalong.is_alive() is False:
        running = False
    is_shifting = player_group.update(tiles_group, SHIFT)
    if is_shifting:
        SHIFT = is_shifting
        STEP = SHIFT // 10
        newcomers = randint(1, 3)
        for _ in range(newcomers):
            correction_data = (hopalong_move_length, hopalong.rect.x)
            tile = Tile(False, tiles_group, *correction_data)
        broken_newcomers = randint(1, 2)
        for _ in range(broken_newcomers):
            correction_data = (hopalong_move_length, hopalong.rect.x)
            tile = Tile(True, tiles_group, *correction_data)
    if SHIFT <= 0:
        shift = 0
    else:
        for entity in tiles_group:
            entity.rect.y += STEP
        SHIFT -= STEP
    tiles_group.update()
#    screen.fill(black)
    player_group.draw(screen)
    tiles_group.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()

