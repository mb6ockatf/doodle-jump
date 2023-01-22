"""
input box class
"""
import pygame


class InputBox:
    """
    Nickname input box class
    changes color to active if has been clicked on or any key pressed
    to passive - if other place was clicked
    """
    def __init__(self, pos: tuple, text: str, colors: tuple, font):
        self.rect = pygame.Rect(pos)
        self.passive_color = colors[0]
        self.active_color = colors[1]
        self.color = self.passive_color
        self.text = text
        self.font = font
        self.text_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        """
        Insert text and render it if key has been pressed
        change active or passive state
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            if self.active:
                self.color = self.active_color
            else:
                self.color = self.passive_color
        if event.type == pygame.KEYDOWN:
            self.active = True
            self.color = self.active_color
            if event.key == pygame.K_RETURN:
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.text_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        """
        Draw frame rectangle and textbox
        """
        width = max(200, self.text_surface.get_width() + 10)
        self.rect.w = width
        text_pos = (self.rect.x + 5, self.rect.y + 5)
        screen.blit(self.text_surface, text_pos)
        pygame.draw.rect(screen, self.color, self.rect, 2)
