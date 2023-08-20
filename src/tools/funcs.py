from os import path
import pygame


def load_image(name: str) -> pygame.surface.Surface:
    fullname = path.join("data", name)
    if not path.isfile(fullname):
        print(f"file '{fullname}' not found")
    image = pygame.image.load(fullname)
    black = pygame.Color("Black")
    image.set_colorkey(black)
    image.convert_alpha()
    return image


def round_by_five(number) -> int:
    last_num = round(number % 10)
    if last_num >= 5:
        number += 10 - last_num
    else:
        number -= last_num
    number = round(number)
    return number


def write_record(value: int) -> None:
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
