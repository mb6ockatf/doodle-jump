import pygame
from tools import round_by_ten, load_image


class Hopalong(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, name: str,
                 screen_width: int, screen_height: int):
        super().__init__(group)
        self.screen_height = screen_height
        self.screen_width = screen_width
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
        """
        returns all the hopalong height data for calculations
        """
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
        self.rect.x %= self.screen_width
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
        """
        Check if sprite is still visible on the screen
        """
        if self.rect.y > self.screen_height:
            return False
        return True

