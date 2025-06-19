import os

# Stałe konfiguracyjne do gry Wormy

FPS = 60  # liczba klatek na sekundę (płynność gry)
SNAKE_MOVE_DELAY = 4  # co ile klatek wąż się przesuwa (im mniejsza wartość, tym szybciej)
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# Kolory
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK
LIGHTBLUE  = (100, 200, 255)  # added: jasno-niebieski do power-upa
YELLOW = (255, 255, 0)  # added: kolor żółty do wykorzystania przy trybie turbo

# Kierunki
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

# added: ścieżki do plików muzycznych
MUSIC_PATH_1 = os.path.join(os.path.dirname(__file__), 'assets', 'music', 'bgm_action_1.ogg')
MUSIC_PATH_2 = os.path.join(os.path.dirname(__file__), 'assets', 'music', 'bgm_action_2.ogg')
MUSIC_PATH_3 = os.path.join(os.path.dirname(__file__), 'assets', 'music', 'bgm_action_3.ogg')
MUSIC_PATH_4 = os.path.join(os.path.dirname(__file__), 'assets', 'music', 'bgm_action_4.ogg')

# fix: ścieżki do plików efektów dźwiękowych
FX_PATH_POWERUP = os.path.join(os.path.dirname(__file__), 'assets', 'fx', '404721__owlstorm__retro-video-game-sfx-powerup-2.ogg')
FX_PATH_WHOOSH = os.path.join(os.path.dirname(__file__), 'assets', 'fx', '802464__sadiquecat__stick-whoosh-6.ogg')
FX_PATH_LASER = os.path.join(os.path.dirname(__file__), 'assets', 'fx', '811933__justwatson64__laser-1.ogg')
FX_PATH_KICK = os.path.join(os.path.dirname(__file__), 'assets', 'fx', '812065__logicogonist__fat-kick-2b.ogg')
FX_PATH_DNB9 = os.path.join(os.path.dirname(__file__), 'assets', 'fx', '189928__cqbcqb__dnb9.ogg')

# Upewnij się, że jest eksportowany
__all__ = [
    'FPS', 'SNAKE_MOVE_DELAY', 'WINDOWWIDTH', 'WINDOWHEIGHT', 'CELLSIZE', 'CELLWIDTH', 'CELLHEIGHT',
    'WHITE', 'BLACK', 'RED', 'GREEN', 'DARKGREEN', 'DARKGRAY', 'BGCOLOR',
    'UP', 'DOWN', 'LEFT', 'RIGHT', 'HEAD',
    'MUSIC_PATH_1', 'MUSIC_PATH_2', 'MUSIC_PATH_3', 'MUSIC_PATH_4',
    'FX_PATH_POWERUP', 'FX_PATH_WHOOSH', 'FX_PATH_LASER', 'FX_PATH_KICK', 'FX_PATH_DNB9',
    'LIGHTBLUE', 'YELLOW'
]
