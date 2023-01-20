#!/usr/bin/env python3
import os
from random import randint
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from tile import Tile
from hopalong import Hopalong
from tools import InitDisplay, round_by_ten, write_record


pygame.init()
FPS = 70
clock = pygame.time.Clock()
screen = InitDisplay()
pygame.display.set_caption("DOODLE JUMP")
black = pygame.Color("black")
white = pygame.Color("white")
font = pygame.font.SysFont(None, 144)
score = 0
is_opened = True
is_running = False
is_paused = True
SHIFT = 0
STEP = 0
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
hopalong = None
score_position = None
sprites = ["bird", "sprout"]
while is_opened:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_opened = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_opened = False
            elif event.key in (pygame.K_UP, pygame.K_SPACE):
                is_running = True
                pygame.mouse.set_visible(False)
                sprite_name = sprites[randint(0, 1)]
                player_group = pygame.sprite.Group()
                hopalong = Hopalong(player_group, sprite_name, screen.width, screen.height)
                tiles_group = pygame.sprite.Group()
                Tile(False, tiles_group, hopalong.get_height_data(), screen.height, screen.width)
                score = 0
                SHIFT = 0
                STEP = 0
                score_width = round_by_ten(screen.width * 0.9)
                score_height = screen.height // 10
                score_position = (score_width, score_height)
                is_paused = True
    screen.display.fill(black)
    pygame.display.flip()
    clock.tick(FPS)
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_opened = False
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
                    is_paused = False
                    pygame.mouse.set_visible(True)
                if event.key in (pygame.K_UP, pygame.K_SPACE):
                    if hopalong.is_moving_up is None:
                        hopalong.is_moving_up = True
                    is_paused = not is_paused
        keys = pygame.key.get_pressed()
        score_img = font.render(str(score), True, white)
        if not is_paused:
            if keys[pygame.K_RIGHT]:
                hopalong.is_moving_right = True
            elif keys[pygame.K_LEFT]:
                hopalong.is_moving_right = False
            if hopalong.is_alive() is False:
                is_running = False
                write_record(score)
            tiles_group.update()
            is_shifting = hopalong.update(tiles_group)
            if not SHIFT and is_shifting:
                heights = [element.rect.y for element in tiles_group]
                heights.sort()
                SHIFT = round_by_ten(screen.height // 5)
                STEP = SHIFT // 10
            if SHIFT > 0:
                for entity in tiles_group:
                    entity.rect.y += STEP
                SHIFT -= STEP
                if SHIFT <= 0:
                    SHIFT = 0
                    player_height_data = hopalong.get_height_data()
                    Tile(False, tiles_group, player_height_data, screen.width, screen.height)
                    for _ in range(randint(0, 2)):
                        Tile(True, tiles_group, player_height_data, screen.width, screen.height)
                    score += 10
        screen.display.fill(black)
        player_group.draw(screen.display)
        tiles_group.draw(screen.display)
        screen.display.blit(score_img, score_position)
        pygame.display.update()
        clock.tick(FPS)
pygame.quit()

