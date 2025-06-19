import pygame
import configuration
import os

# przywrócona funkcja do ładowania muzyki przez pygame

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
    fx = {
        'powerup': pygame.mixer.Sound(configuration.FX_PATH_POWERUP),
        'whoosh': pygame.mixer.Sound(configuration.FX_PATH_WHOOSH),
        'laser': pygame.mixer.Sound(configuration.FX_PATH_LASER),
        'kick': pygame.mixer.Sound(configuration.FX_PATH_KICK),
        'dnb9': pygame.mixer.Sound(configuration.FX_PATH_DNB9),
    }
    return fx
