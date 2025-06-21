import pygame
import configuration

def load_music():
    pygame.mixer.init()
    music_tracks = {
        'menu': configuration.MUSIC_PATH_1,
        'game_easy': configuration.MUSIC_PATH_2,
        'game_normal': configuration.MUSIC_PATH_3,
        'game_hard': configuration.MUSIC_PATH_4
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

def play_fx(sound):
    if sound:
        sound.play()
