import os
from dataclasses import dataclass
import pygame


def load_image(name: str) -> pygame.Surface:
    """
    Loads image and creates pygame.Surface
    set_colorkey and convert_alpha to remove background on png images
    """
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"file '{fullname}' not found")
        pygame.quit()
    image = pygame.image.load(fullname)
    black = pygame.Color("Black")
    image.set_colorkey(black)
    image.convert_alpha()
    return image


def round_by_ten(number) -> int:
    """
    Returns number-like object rounded by ten
    """
    number = round(number, -1)
    number = int(number)
    return number

def write_record(value: int):
    """
    Writes new record value to file
    """
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

@dataclass
class InitDisplay:
    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    _info = pygame.display.Info()
    width = _info.current_w
    height = _info.current_h

