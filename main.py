#!/usr/bin/env python3
import os
from random import randint
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


pygame.init()
FPS = 70
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen_height_div_five = screen_height // 5
pygame.display.set_caption("DOODLE JUMP")
black = pygame.Color("black")
white = pygame.Color("white")
font = pygame.font.SysFont(None, 144)
score = 0


def load_image(name: str) -> pygame.Surface:
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"file '{fullname}' not found")
        pygame.quit()
    image = pygame.image.load(fullname)
    image.set_colorkey(black)
    image.convert_alpha()
    return image


def round_by_ten(number: int) -> int:
    number = round(number, -1)
    number = int(number)
    return number


def write_record(value: int):
    open("record.bin", "ab").close()
    with open("record.bin", "rb") as bytestream:
        current_record = bytestream.read().decode("utf-8")
        if current_record == "":
            current_record = 0
        current_record = int(current_record)
    if value > current_record:
        new_record = str(value).encode("utf-8")
        with open("record.bin", "wb") as file:
            file.write(new_record)


class Tile(pygame.sprite.Sprite):
    def __init__(self, is_broken: bool, group: pygame.sprite.Group,
                 player_height: tuple):
        super().__init__(group)
        self.is_broken = is_broken
        self.is_falling = False
        image_name = "tile.png"
        if self.is_broken:
            image_name = "broken_tile.png"
        self.image = load_image(image_name)
        self.image = pygame.transform.scale(self.image, (155, 35))
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.rect.y = self.generate_height(*player_height)
        x_value = randint(1, screen_width - 1)
        self.rect.x = round_by_ten(x_value)
        self._edges = None

    @staticmethod
    def generate_height(radius: int, edge: int, minimal_y: int) -> int:
        minimal = minimal_y - radius + edge * 1.5
        maximal = minimal_y + radius - edge * 1.5
        if minimal < 0:
            minimal = edge
        elif maximal > screen_height:
            maximal = screen_height - edge
        value = randint(minimal, maximal)
        value = round_by_ten(value)
        return value

    @property
    def edges(self) -> tuple:
        if not self._edges:
            x, half_width = self.rect.x, self.width // 2
            self._edges = (x - half_width, x + half_width)
        return self._edges

    def update(self):
        if self.is_broken and self.is_falling:
            self.rect.y += 50
        if self.rect.y >= screen_height:
            self.kill()


class Hopalong(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, name: str):
        super().__init__(group)
        self.jump_height = screen_height // 3 * 2
        self.jump_height = round_by_ten(self.jump_height)
        self.move_length = screen_width
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
            self.image = self.image_storage[self.name + "_left"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = (self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.center = screen_height, screen_width // 2

    def get_height_data(self) -> tuple:
        return self.jump_height, self.height, self.rect.y

    def update(self, group: pygame.sprite.Group) -> bool:
        if self.is_facing_right:
            image_name = self.name + "_right"
        else:
            image_name = self.name + "_left"
        self.image = self.image_storage[image_name]
        shifted = False
        is_still = not self.is_moving_up
        colliding_object = None
        for sprite in group:
            if not sprite.edges[0] < self.rect.x < sprite.edges[1]:
                continue
            if sprite.rect.y - self.rect.y != 80:
                continue
            colliding_object = sprite
            break
        if is_still and colliding_object:
            colliding_object.is_falling = colliding_object.is_broken
            self.left_to_move_up = self.jump_height
            self.is_moving_up = True
            shifted = True
        if self.is_moving_right is True:
            self.rect.x += 25
            self.is_facing_right = True
        elif self.is_moving_right is False:
            self.rect.x -= 25
            self.is_facing_right = False
        self.rect.x %= screen_width
        self.is_moving_right = None
        if self.is_moving_up is True:
            if self.rect.y > 0:
                self.rect.y -= 10
            self.left_to_move_up -= 10
        elif self.is_moving_up is False:
            self.rect.y += 10
        if self.rect.y % 10 != 0:
            self.rect.y = round_by_ten(self.rect.y)
        if not self.left_to_move_up:
            self.is_moving_up = not self.is_moving_up
            self.left_to_move_up = self.jump_height
        return shifted

    def is_alive(self) -> bool:
        if self.rect.y > screen_height:
            return False
        return True


is_opened = True
is_running = False
hopalong = None
is_paused = None
SHIFT = None
STEP = None
player_group = None
tiles_group = None
score_position = None
sprites = ["bird", "sprout"]
while is_opened:
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
                    if not is_paused:
                        is_paused = True
                    else:
                        is_paused = False
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
                SHIFT = round_by_ten(screen_height_div_five)
                STEP = SHIFT // 10
                STEP = round_by_ten(STEP)
            if SHIFT > 0:
                for entity in tiles_group:
                    entity.rect.y += STEP
                SHIFT -= STEP
                if SHIFT <= 0:
                    SHIFT = 0
                    player_height_data = hopalong.get_height_data()
                    Tile(False, tiles_group, player_height_data)
                    broken_newcomers = randint(0, 2)
                    for _ in range(broken_newcomers):
                        Tile(True, tiles_group, player_height_data)
                    score += 10
        screen.fill(black)
        player_group.draw(screen)
        tiles_group.draw(screen)
        screen.blit(score_img, score_position)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(FPS)
    else:
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
                    hopalong = Hopalong(player_group, sprite_name)
                    tiles_group = pygame.sprite.Group()
                    Tile(False, tiles_group, hopalong.get_height_data())
                    score = 0
                    SHIFT = 0
                    STEP = 0
                    score_width = round_by_ten(screen_width * 0.9)
                    score_height = screen_ehight // 10
                    score_position = (score_width, score_height)
                    is_paused = True
        screen.fill(black)
        pygame.display.flip()
        clock.tick(FPS)
pygame.quit()

