#!/usr/bin/env python3
import sys
import os
from random import randrange
import pygame as pg
import pymunk
import pymunk.pygame_util

pg.init()
pymunk.pygame_util.positive_y_is_up = False
FPS = 120
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
draw_options = pymunk.pygame_util.DrawOptions(screen)  # type: ignore
space = pymunk.Space()
space.gravity = 0, 8000


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
        image = load_image(sprite)
        self.image = pg.transform.scale(image, (200, 200))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = (self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.center = screen_height, screen_width // 2
        self.set_physics()

    def set_physics(self):
        self.mass = 1
        self.moment = pymunk.moment_for_box(self.mass, self.size)
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.moment = self.moment
        point_a = (self.width // 2 + self.rect.x,
                    self.height // 2 - self.rect.y)
        point_b = (self.width + self.rect.x,
                    self.height + self.rect.y)
        self.shape = pymunk.Segment(self.body, (point_a), (point_b), 100)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        space.add(self.body, self.shape)

    def update(self):
        self.body.apply_impulse_at_local_point((self.rect.x + self.width // 2,
        10), (0, 0))



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
    screen.fill(black)
    all_sprites.update()
    all_sprites.draw(screen)
    space.step(1 / FPS)
    space.debug_draw(draw_options)
    pg.display.flip()
    pg.display.update()
    clock.tick(FPS)
pg.quit()
