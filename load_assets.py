import pygame
import configuration
import os

# added: funkcja do ładowania muzyki z podziałem na menu i różne poziomy gry

def load_music():
    pygame.mixer.init()
    music_tracks = {
        'menu': configuration.MUSIC_PATH_1,  # muzyka do menu głównego
        'game_easy': configuration.MUSIC_PATH_2,   # muzyka do gry - łatwy
        'game_normal': configuration.MUSIC_PATH_3, # muzyka do gry - normalny
        'game_hard': configuration.MUSIC_PATH_4    # muzyka do gry - trudny
    }
    return music_tracks

def load_fx():
    # fix: ładowanie efektów dźwiękowych na podstawie ścieżek z configuration.py
    fx = {
        'powerup': pygame.mixer.Sound(configuration.FX_PATH_POWERUP),
        'whoosh': pygame.mixer.Sound(configuration.FX_PATH_WHOOSH),
        'laser': pygame.mixer.Sound(configuration.FX_PATH_LASER),
        'kick': pygame.mixer.Sound(configuration.FX_PATH_KICK),
    }
    return fx
