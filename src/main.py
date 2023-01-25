#!/usr/bin/env python3
import os
from random import randint

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from database import DatabaseConnection
from sprites import Hopalong, Tile
from tools import Button, Colors, InputBox, round_by_five


class Gamekeeper:
    """
    Data handler to control game cycle variables
    """

    NAME = "your name"

    def __init__(self):
        self._score = 0
        self.db_connection = DatabaseConnection()
        name = Gamekeeper.NAME
        self.current_record = self.set_current_record(name)
        self.shift = 0
        self.step = 0
        self.is_opened = True
        self.is_running = False
        self.is_paused = True
        self.tiles = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        sprite_name = sprites[randint(0, 1)]
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
        score_width = round_by_five(display_sizes[0] * 0.9)
        score_height = display_sizes[1] // 10
        self.score_position = (score_width, score_height)

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int):
        self._score = value
        if self._score % 100 == 0 and self.score != 0:
            self.hopalong.difficulty *= 1.25

    def set_current_record(self, name: str):
        """
        Get record for current user and handle its type
        """
        current_record = self.db_connection.select(name)
        if current_record == []:
            current_record = 0
        else:
            current_record = current_record[0][0]
        return str(current_record)


    def run(self):
        """
        Set variables to start the game
        """
        Gamekeeper.NAME = self.nickname_box.text
        self.is_running = True
        self.shift = 0
        self.step = 0

    def quit(self):
        """
        Write the record into database and set variables to close the game
        """
        self.db_connection.insert(Gamekeeper.NAME, self.score)
        self.score = 0
        self.is_running = False
        self.is_opened = False
        self.is_paused = False
        self.db_connection.close()


if __name__ == "__main__":
    pygame.init()
    FPS = 120
    colors = Colors()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    _info = pygame.display.Info()
    display_sizes = (_info.current_w, _info.current_h)
    pygame.display.set_caption("DOODLE JUMP")
    font = pygame.font.SysFont(None, 144) #type:ignore
    sprites = ["bird", "sprout"]
    gamekeeper = Gamekeeper()
    while gamekeeper.is_opened:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamekeeper.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gamekeeper.quit()
                elif event.key in (pygame.K_UP, pygame.K_SPACE):
                    gamekeeper.run()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                btn_pos = gamekeeper.start_btn.rect_pos_data
                if btn_pos[0] < mouse[0] < btn_pos[0] + btn_pos[2]:
                    if btn_pos[1] < mouse[1] < btn_pos[1] + btn_pos[3]:
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamekeeper.quit()
                        gamekeeper = Gamekeeper()
                    if event.key in (pygame.K_UP, pygame.K_SPACE):
                        if gamekeeper.hopalong.is_moving_up is None:
                            gamekeeper.hopalong.is_moving_up = True
                        gamekeeper.is_paused = not gamekeeper.is_paused
            keys = pygame.key.get_pressed()
            score_color = colors["white"]
            score_image = font.render(str(gamekeeper.score), True, score_color)
            if not gamekeeper.is_paused:
                if keys[pygame.K_RIGHT]:
                    gamekeeper.hopalong.is_moving_right = True
                elif keys[pygame.K_LEFT]:
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
                        entity.rect.y += gamekeeper.step #type:ignore
                    gamekeeper.shift -= gamekeeper.step
                    if gamekeeper.shift <= 0:
                        gamekeeper.shift = 0
                        player_height = gamekeeper.hopalong.get_height_data()
                        tile_data = [False,
                                    gamekeeper.tiles,
                                    player_height,
                                    display_sizes]
                        Tile(*tile_data)
                        tile_data[0] = True
                        for _ in range(randint(0, 2)):
                            Tile(*tile_data)
                        gamekeeper.score += 10
            display.fill(colors["black"])
            gamekeeper.players.draw(display)
            gamekeeper.tiles.draw(display)
            display.blit(score_image, gamekeeper.score_position)
            pygame.display.update()
            clock.tick(FPS)
    pygame.quit()
