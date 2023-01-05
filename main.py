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
running = True


def load_image(name: str):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        pg.quit()
    image = pg.image.load(fullname)
    image.set_colorkey(black)
    image.convert_alpha()
    return image


class Tile(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        image = load_image("tile.png")
        self.image = pg.transform.scale(image, (310, 70))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = (self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.center = self.generate(), screen_height - 200
        self._edges = None

    def generate(self):
        x = randint(0, screen_width)
        return x

    @property
    def edges(self):
        if not self._edges:
            left_edge = self.rect.x - self.width // 2
            right_edge = self.rect.x + self.width // 2
            self._edges = (left_edge, right_edge)
        return self._edges


class Hopalong(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.jump_height = screen_height // 2
        self.move_length = screen_width // 6
        self.is_moving_up = None
        self.left_to_move_up = self.jump_height
        self.is_moving_right = None
        self.left_to_move_right = self.move_length
        self.tile = None
        image = load_image(sprite)
        self.image = pg.transform.scale(image, (200, 200))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = (self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.center = screen_height, screen_width // 2

    def update(self, group):
        for _ in range(10):
          self.move(group)

    def move(self, group):
        if not self.is_moving_up:
            if pg.sprite.spritecollideany(self, group):
                for element in group:
                    if self.rect.y - element.rect.y == -199:
                        self.left_to_move_up = self.jump_height
                        self.is_moving_up = None
                        self.tile = element
                        break
        if self.is_moving_right is not None:
            if self.is_moving_right:
                self.rect.x += 1
                if self.tile:
                    edge = self.tile.edges[1]
                    if edge < self.rect.x:
                        self.tile = None
                        self.is_moving_up = False
            else:
                self.rect.x -= 1
                if self.tile:
                    edge = self.tile.edges[0]
                    if edge > self.rect.x:
                        self.tile = None
                        self.is_moving_up = False
            self.left_to_move_right -= 1
        if not self.left_to_move_right:
            self.is_moving_right = None
            self.left_to_move_right = self.move_length
        if self.is_moving_up is not None:
            if self.is_moving_up:
                self.rect.y -= 1
                self.left_to_move_up -= 1
            else:
                self.rect.y += 1
        if not self.left_to_move_up:
            if self.is_moving_up:
                self.is_moving_up = False
            else:
                self.is_moving_up = None
            self.left_to_move_up = self.jump_height

    def is_alive(self):
        if self.rect.y > screen_height:
            return False
        return True


all_sprites = pg.sprite.Group()
hopalong = Hopalong(all_sprites)
tiles = pg.sprite.Group()
tile = Tile(tiles)
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
    screen.fill(black)
    turn_result = all_sprites.update(tiles)
    all_sprites.draw(screen)
    tiles.draw(screen)
    pg.display.flip()
    pg.display.update()
    clock.tick(FPS)
pg.quit()

