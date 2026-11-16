import pygame
from os.path import join
from os import walk
from pathlib import Path
import random
#https://telemost.yandex.ru/j/56751930442592 ссылка на занятие
#https://us06web.zoom.us/j/87561424651?pwd=yDlOuSVnXsQuan1Jacwq2gbxhzyrCH.1 запасная ссылка на занятие
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900 
FPS = 60
TILE_SIZE = 64
ROOT = Path(__file__).resolve().parent
# корень проекта: папка data лежит рядом с папкой game
PROJECT_ROOT = ROOT.parent

def asset(*parts):
    return join(ROOT, *parts)

def data(*parts):
    return join(PROJECT_ROOT, 'data', *parts)

