#!/usr/bin/env python3
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from random import randint, choice
import pygame
from argparse import ArgumentParser
from database import DatabaseConnection
from sprites import Hopalong, Tile, MovingTile
from tools import Button, Colors, InputBox, round_by_five


class Gamekeeper:
    NAME = "your name"

    def __init__(self):
        pygame.mouse.set_visible(True)
        self._score, self.stage = 0, 0
        self.db_connection = DatabaseConnection()
        name = Gamekeeper.NAME
        self.current_record = self.set_current_record(name)
        self.shift, self.step = 0, 0
        self.is_opened, self.is_running, self.is_paused = True, False, True
        self.tiles, self.players = pygame.sprite.Group(), pygame.sprite.Group()
        sprite_name = choice(sprites)
        self.hopalong = Hopalong(self.players, sprite_name, display_sizes)
        Tile(False, self.tiles, self.hopalong.get_height_data(), display_sizes)
        self.background_color = colors.get_random_paint(colors.dark)
        start_pos = display_sizes[0] // 2, display_sizes[1] // 2, 300, 100
        text_color = colors.get_random_paint(colors.vivid)
        btn_color = colors.get_random_paint(colors.light)
        self.start_btn = Button(btn_color, text_color, "START", start_pos)
        name_pos = display_sizes[0] // 6, display_sizes[1] // 2, 300, 100
        name_colors = (colors["grey"], colors["brown"])
        self.nickname_box = InputBox(name_pos, name, name_colors, font)
        score_width = round_by_five(display_sizes[0] * 0.8)
        score_height = display_sizes[1] // 10
        self.score_position = (score_width, score_height)

    @property
    def score(self) -> int:
        return round(self._score)

    @score.setter
    def score(self, value: int):
        score_boost = (value - self._score) * self.hopalong.difficulty
        self._score = self._score + score_boost
        current_stage = self._score // 100
        if current_stage > self.stage:
            self.stage = current_stage
            self.hopalong.difficulty *= 1.01

    def set_current_record(self, name: str):
        current_record = self.db_connection.select(name)
        if current_record == []:
            current_record = 0
        else:
            current_record = current_record[0][0]
        return str(current_record)

    def run(self):
        Gamekeeper.NAME = self.nickname_box.text
        pygame.mouse.set_visible(False)
        self.is_running, self.shift, self.step = True, 0, 0

    def quit(self):
        self.db_connection.insert(Gamekeeper.NAME, self.score)
        self.score = 0
        self.is_running, self.is_opened, self.is_paused = False, False, False
        self.hopalong, self.players = None, None
        self.db_connection.close()


def finish_frame():
    display.fill(colors["black"])
    gamekeeper.players.draw(display)
    gamekeeper.tiles.draw(display)
    display.blit(score_image, gamekeeper.score_position)
    pygame.display.update()
    clock.tick(FPS)


pygame.init()
FPS = 60
colors = Colors()
clock = pygame.time.Clock()
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
_info = pygame.display.Info()
display_sizes = (_info.current_w, _info.current_h)
pygame.display.set_caption("DOODLE JUMP")
font = pygame.font.SysFont(None, 144)
sprites = ["ghost", "sprout", "bird"]
gamekeeper = Gamekeeper()
while gamekeeper.is_opened:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamekeeper.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gamekeeper.quit()
            elif event.key in (pygame.K_UP, pygame.K_SPACE, pygame.K_RETURN):
                gamekeeper.run()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            btn_pos = gamekeeper.start_btn.rect_pos_data
            if (
                btn_pos[0] < mouse[0] < btn_pos[0] + btn_pos[2]
                and btn_pos[1] < mouse[1] < btn_pos[1] + btn_pos[3]
            ):
                gamekeeper.run()
        gamekeeper.nickname_box.handle_event(event)
    display.fill(gamekeeper.background_color)
    score_color = colors["white"]
    value = str(gamekeeper.current_record)
    score_image = font.render(value, True, score_color)
    display.blit(score_image, gamekeeper.score_position)
    gamekeeper.nickname_box.draw(display)
    gamekeeper.start_btn.draw(display)
    clock.tick(FPS)
    pygame.display.update()
    while gamekeeper.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamekeeper.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                gamekeeper.quit()
                gamekeeper = Gamekeeper()
            elif event.type == pygame.KEYDOWN and event.key in (
                pygame.K_UP,
                pygame.K_SPACE,
                pygame.K_w,
            ):
                if gamekeeper.hopalong.is_moving_up is None:
                    gamekeeper.hopalong.is_moving_up = True
                gamekeeper.is_paused = not gamekeeper.is_paused
        keys = pygame.key.get_pressed()
        score_color = colors["white"]
        score_image = font.render(str(gamekeeper.score), True, score_color)
        if gamekeeper.is_paused:
            finish_frame()
            continue
        if any((keys[pygame.K_RIGHT], keys[pygame.K_d])):
            gamekeeper.hopalong.is_moving_right = True
        elif any((keys[pygame.K_LEFT], keys[pygame.K_a])):
            gamekeeper.hopalong.is_moving_right = False
        if gamekeeper.hopalong.is_alive() is False:
            gamekeeper.quit()
            gamekeeper = Gamekeeper()
        gamekeeper.tiles.update()
        SHIFTING = gamekeeper.hopalong.update(gamekeeper.tiles)
        if not gamekeeper.shift and SHIFTING:
            gamekeeper.shift = round_by_five(display_sizes[1] // 5)
            gamekeeper.step = gamekeeper.shift // 10
        if gamekeeper.shift > 0:
            for entity in gamekeeper.tiles:
                entity.rect.y += gamekeeper.step  # type:ignore
            gamekeeper.shift -= gamekeeper.step
            if gamekeeper.shift <= 0:
                gamekeeper.shift = 0
                player_height = gamekeeper.hopalong.get_height_data()
                tile_data = [
                    False,
                    gamekeeper.tiles,
                    player_height,
                    display_sizes,
                ]
                Tile(*tile_data)
                tile_data[0] = True
                for _ in range(randint(0, 2)):
                    Tile(*tile_data)
                for _ in range(randint(0, 2)):
                    MovingTile(*tile_data)
                gamekeeper.score += 10
        finish_frame()
pygame.quit()