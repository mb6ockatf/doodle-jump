from random import randint
import pygame
from tools import round_by_five, load_image


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        is_broken: bool,
        group: pygame.sprite.Group,
        player_height: tuple,
        screen_sizes: tuple,
    ):
        super().__init__(group)
        self.screen_sizes = screen_sizes
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
        x_value = randint(1, screen_sizes[0] - self.width)
        self.rect.x = round_by_five(x_value)

    def generate_height(self, radius: int, edge: int, minimal_y: int) -> int:
        minimal = round(minimal_y - radius + edge * 1.5)
        maximal = round(minimal_y + radius - edge * 1.5)
        if minimal < 0:
            minimal = edge
        elif maximal > self.screen_sizes[1]:
            maximal = self.screen_sizes[1] - edge
        value = randint(minimal, maximal)
        return round_by_five(value)

    def update(self):
        if self.is_broken and self.is_falling:
            self.rect.y += 50  # type:ignore
        if self.rect.y >= self.screen_sizes[1]:  # type:ignore
            self.kill()

    @property
    def edges(self) -> tuple:
        return self.rect.x - self.width // 2, self.rect.x + self.width // 2


class MovingTile(Tile):
    def __init__(self, *stuff):
        super().__init__(*stuff)
        self.moving_direction = "right"

    def update(self):
        self.move()
        if self.is_broken and self.is_falling:
            self.rect.y += 50  # type:ignore
        if self.rect.y >= self.screen_sizes[1]:  # type:ignore
            self.kill()
    
    def move(self):
        if self.rect.x + 5 > self.screen_sizes[0]:
            self.moving_direction = "left"
        elif self.rect.x - 5 < 0:
            self.moving_direction = "right"
        if self.moving_direction == "right":
            self.rect.x += 5
        else:
            self.rect.x -= 5