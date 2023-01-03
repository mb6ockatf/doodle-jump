#!/usr/bin/env python3
import sys
import os
from random import randrange
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
print(screen_width, screen_height)
pg.display.set_caption("DOODLE JUMP")
black = pg.Color("black")
white = pg.Color("white")


def load_image(name: str):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        pg.quit()
    image = pg.image.load(fullname).convert_alpha()
    return image


class Hopalong(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.jump_height = screen_height // 2
        self.move_length = screen_width // 6
        self.is_moving_up = None
        self.left_to_move_up = self.jump_height
        self.is_moving_right = None
        self.left_to_move_right = self.move_length
        image = load_image(sprite)
        self.image = pg.transform.scale(image, (200, 200))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = (self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.center = screen_height, screen_width // 2

    def update(self):
        if self.is_moving_right is not None:
            if self.is_moving_right:
                self.rect.x += 10
            else:
                self.rect.x -= 10
            self.left_to_move_right -= 10
        if self.left_to_move_right == 0:
            self.is_moving_right = None
            self.left_to_move_right = self.move_length
        if self.is_moving_up is not None:
            if self.is_moving_up:
                self.rect.y -= 10
            else:
                self.rect.y += 10
            self.left_to_move_up -= 10
        if self.left_to_move_up == 0:
            if self.is_moving_up:
                self.is_moving_up = False
            else:
                self.is_moving_up = None
            self.left_to_move_up = self.jump_height


all_sprites = pg.sprite.Group()
hopalong = Hopalong(all_sprites)
running = True
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
    screen.fill(black)
    all_sprites.update()
    all_sprites.draw(screen)
    pg.display.flip()
    pg.display.update()
    clock.tick(FPS)
pg.quit()

