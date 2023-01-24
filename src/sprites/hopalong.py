"""
Hopalong - player's sprite class
"""
import pygame
from tools import round_by_five, load_image


class Hopalong(pygame.sprite.Sprite):
    """
    PLayer's sprite
    can jump for self.jump_height value
    start falling after reaching the maximum jump height
    can land onto something, and start jumping again
    dies when falls out of the lower side of the screen
    """
    def __init__(self, group: pygame.sprite.Group, name: str,
                screen_sizes: tuple):
        super().__init__(group)
        self.screen_sizes = screen_sizes
        self.jump_height = screen_sizes[1] // 3 * 2
        self.jump_height = round_by_five(self.jump_height)
        self.move_length = screen_sizes[0]
        self.is_moving_up = None
        self.left_to_move_up = self.jump_height
        self._is_moving_right = None
        self.is_facing_right = False
        self.on_tile_edges = None
        self.name = name
        self.image_storage = {}
        self.image = None
        if self.name == "ghost":
            size = (110, 110)
        elif self.name in ("sprout", "bird"):
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
        self.rect.center = screen_sizes[1], screen_sizes[0] // 2

    def get_height_data(self) -> tuple:
        """
        returns all the hopalong height data for calculations
        """
        return self.jump_height, self.height, self.rect.y  # type:ignore

    def update(self, group: pygame.sprite.Group) -> bool:
        """
        Check collisions and change movement direction
        """
        if self.is_facing_right:
            image_name = self.name + "_right"
        else:
            image_name = self.name + "_left"
        self.image = self.image_storage[image_name]
        shifted = False
        is_still = not self.is_moving_up
        colliding_object = None
        for sprite in group:
            if not sprite.edges[0] < self.rect.x < sprite.edges[1]:  # type: ignore
                continue
            if sprite.rect.y - self.rect.y != 80:#type:ignore
                continue
            colliding_object = sprite
            break
        if is_still and colliding_object:
            colliding_object.is_falling = colliding_object.is_broken #type:ignore
            self.left_to_move_up = self.jump_height
            self.is_moving_up = True
            shifted = True
        if self.is_moving_right is True:
            self.rect.x += 20 #type:ignore
            self.is_facing_right = True
        elif self.is_moving_right is False:
            self.rect.x -= 20 #type:ignore
            self.is_facing_right = False
        self.rect.x %= self.screen_sizes[0] #type:ignore
        self.is_moving_right = None #type:ignore
        if self.is_moving_up is True:
            if self.rect.y > 0: #type:ignore
                self.rect.y -= 5 #type:ignore
            self.left_to_move_up -= 5
        elif self.is_moving_up is False:
            self.rect.y += 5 #type:ignore
        if self.rect.y % 5 != 0: #type:ignore
            self.rect.y = round_by_five(self.rect.y) #type:ignore
        if not self.left_to_move_up:
            self.is_moving_up = not self.is_moving_up
            self.left_to_move_up = self.jump_height
        return shifted

    def is_alive(self) -> bool:
        """
        Check if sprite is still visible on the screen
        """
        if self.rect.y > self.screen_sizes[1]: #type:ignore
            return False
        return True

    @property
    def is_moving_right(self):
        """
        Property to isolate is_moving_right variable
        """
        return self._is_moving_right

    @is_moving_right.setter
    def is_moving_right(self, value):
        self._is_moving_right = value
