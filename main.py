#!/usr/bin/env python3
import sys
import os
from random import randint
import pygame as pg

pg.init()
FPS = 70
sprite = "sprout.png"
clock = pg.time.Clock()
pg.mouse.set_visible(False)
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
info = pg.display.Info()
screen_width = info.current_w
screen_height = info.current_h
pg.display.set_caption("DOODLE JUMP")
black = pg.Color("black")
white = pg.Color("white")
difficulty = 6
shift = 0
step = 0
running = True

def load_image(name: str) -> pg.Surface:
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"file '{fullname}' not found")
        pg.quit()
    image = pg.image.load(fullname)
    image.set_colorkey(black)
    image.convert_alpha()
    return image


class Tile(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, hero: pg.sprite.Sprite):
        super().__init__(group)
        image = load_image("tile.png")
        self.image = pg.transform.scale(image, (155, 35))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = (self.width, self.height)
        self.rect = self.image.get_rect()
        center_height = self.generate_height()
        center_width = self.generate_width(hero)
        ### TRIANGLE
        self.rect.center = self.generate_width(hero), self.generate_height()
        self._edges = None
        self.is_in_progress = False
        self.progress_distance = None

    def generate_width(self, correction_by: pg.sprite.Sprite) -> int:
        radius = correction_by.move_length
        minimal = correction_by.rect.x - radius
        minimal = round(minimal)
        if minimal < 0:
            minimal = 0
        maximal = correction_by.rect.x + radius
        maximal = round(maximal)
        if maximal > screen_width:
            maximal = screen_width
        return randint(minimal, maximal)

    def generate_height(self) -> int:
        return randint(screen_height // 2 - 200, screen_height // 5 * 3)

    @property
    def edges(self) -> tuple:
        if not self._edges:
            left_edge = self.rect.x - self.width // 2
            right_edge = self.rect.x + self.width // 2
            self._edges = (left_edge, right_edge)
        return self._edges


class Hopalong(pg.sprite.Sprite):
    def __init__(self, *group: pg.sprite.Group):
        super().__init__(*group)
        self.jump_height = screen_height // 3 * 2
        self.move_length = screen_width // 2
        self.is_moving_up = None
        self.left_to_move_up = self.jump_height
        self.is_moving_right = None
        self.left_to_move_right = self.move_length
        self.tile = None
        image = load_image(sprite)
        self.image = pg.transform.scale(image, (100, 100))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = (self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.center = screen_height, screen_width // 2

    def update(self, group: pg.sprite.Group):
        for _ in range(10):
            self.move(group)

    def move(self, group: pg.sprite.Group):
        is_still = not self.is_moving_up
        is_colliding = self.is_having_collision(group)
        if is_still and is_colliding:
            self.left_to_move_up = self.jump_height
            self.is_moving_up = True
            self.tile = is_colliding
        if self.is_moving_right is True:
            self.rect.x += 10
        elif self.is_moving_right is False:
            self.rect.x -= 10
        if self.is_moving_right is not None:
            self.is_moving_right = None
        if self.tile:
            edge = self.tile.edges
            if edge[0] > self.rect.x or edge[1] < self.rect.x:
                self.tile = None
                self.is_moving_up = False
        if self.is_moving_up is True:
            if self.rect.y > 0:
                self.rect.y -= 1
            self.left_to_move_up -= 1
        elif self.is_moving_up is False:
            self.rect.y += 1
        if not self.left_to_move_up:
            if self.is_moving_up:
                self.is_moving_up = False
            else:
                self.is_moving_up = True
            self.left_to_move_up = self.jump_height
        print("left_to_move_up", self.left_to_move_up)

    def is_alive(self):
        if self.rect.y > screen_height:
            return False
        return True

    def is_having_collision(self, group: pg.sprite.Group) -> pg.sprite.Sprite:
        for sprite in group:
            if not (sprite.edges[0] < self.rect.x < sprite.edges[1]):
                continue
            difference_height = sprite.rect.y - self.rect.y
            print(difference_height)
            if difference_height != 20:
                continue
            return sprite


all_sprites = pg.sprite.Group()
hopalong = Hopalong(all_sprites)
tiles = pg.sprite.Group()
tile = Tile(tiles, hopalong)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_UP:
                if hopalong.is_moving_up is None:
                    hopalong.is_moving_up = True
    keys = pg.key.get_pressed()
    if keys[pg.K_RIGHT]:
        hopalong.is_moving_right = True
    elif keys[pg.K_LEFT]:
        hopalong.is_moving_right = False
    if hopalong.is_alive() is False:
        running = False
    all_sprites.update(tiles)
    tiles.update()
    measurer = hopalong.tile
    if measurer and not shift:
        value = screen_height - 200 - measurer.rect.y
        if value > 0:
            shift = value
    if shift:
        if not step:
            step = shift // 10
        round_step = round(step)
        for entity in tiles:
            entity.rect.y += round_step
        shift -= step
        if shift <= 0:
            newcomers = randint(1, 2)
            for _ in range(newcomers):
                tile = Tile(tiles, hopalong)
            shift = 0
    hopalong.tile = None
    screen.fill(black)
    all_sprites.draw(screen)
    tiles.draw(screen)
    pg.display.flip()
    pg.display.update()
    clock.tick(FPS)
pg.quit()

