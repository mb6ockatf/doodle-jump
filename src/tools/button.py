"""Button class"""
import pygame


class Button:
    """
    Class representing a button, as there's no builtin button in pygame
    """
    def __init__(self, color: tuple, text_color: tuple, text: str, pos: tuple):
        """
        pos argument is a tuple, were 2 integers are pointing to left-top
        corner of the button, and other two are button's width and height.
        For instance,
        Button((0, 0, 0), (140, 140, 140), "something", (120, 120, 90, 90))
        will create a 90x90 button at 120x120.
        """
        self.rect_pos_data = pos
        self.text_color = text_color
        self.canvas_pos_data = self.get_canvas_pos(pos)
        self.color = color
        font_size = 144
        font = pygame.font.SysFont(None, font_size)  #type:ignore
        pic_size = font.size(text)
        while pic_size[0] > pos[-2] - 30 or pic_size[1] > pos[-1] - 30:
            font_size -= 10
            font = pygame.font.SysFont(None, font_size)  #type:ignore
            pic_size = font.size(text)
        self.image = font.render(text, True, text_color)
        image_x = pos[0] + (pos[2] - pic_size[0]) // 2
        image_y = pos[1] + (pos[3] - pic_size[1]) // 2
        self.image_coords = (image_x, image_y)

    def draw(self, screen: pygame.surface.Surface):
        """Draw text, color box and ..."""
        pygame.draw.rect(screen, self.color, self.rect_pos_data)
        pygame.draw.rect(screen, self.text_color, self.canvas_pos_data, 5)
        screen.blit(self.image, self.image_coords)

    def get_canvas_pos(self, pos: tuple) -> tuple:
        """Count canvas pos"""
        return pos[0] + 5, pos[1] + 5, pos[2] - 10, pos[3] - 10
