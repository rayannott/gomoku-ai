from enum import Enum
from typing import Literal
from os.path import join
import json
import pygame

FieldCell = Literal[0, 1, -1]
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FIELD_SIZE = SCREEN_HEIGHT
STONE_RADIUS = 14
THEME_PATH = join('theme.json')
with open(THEME_PATH) as fr:
    THEME = json.load(fr)

Pos = tuple[int, int]
pygame.font.init()
FONT = pygame.font.SysFont('comic sans', 32)
FONT_SMALL = pygame.font.SysFont('comic sans', 20)
