#!/usr/bin/env python3
import sys
import pygame as pg
import pymunk.pygame_util


pymunk.pygame_util.positive_y_is_up = False
FPS = 120


class Hopalong(pg.sprite.Sprite):
    image =
    def __init__(self):
        ...

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.set_caption("DOODLE JUMP")

draw_options = pymunk.pygame_util.DrawOptions(screen)
space = pymunk.Space()
space.gravity = 0, 8000

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    space.step = 1 / FPS
    space.debug_draw(draw_options)
    screen.fill((0, 0, 0))
    pg.display.flip()
    clock.tick(FPS)
pg.quit()

