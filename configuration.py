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

# Kierunki
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

# added: ścieżki do plików muzycznych
MUSIC_PATH_1 = os.path.join(os.path.dirname(__file__), 'assets', 'music', 'bgm_action_1.mp3')
MUSIC_PATH_2 = os.path.join(os.path.dirname(__file__), 'assets', 'music', 'bgm_action_2.mp3')
MUSIC_PATH_3 = os.path.join(os.path.dirname(__file__), 'assets', 'music', 'bgm_action_3.mp3')
MUSIC_PATH_4 = os.path.join(os.path.dirname(__file__), 'assets', 'music', 'bgm_action_4.mp3')

# fix: ścieżki do plików efektów dźwiękowych
FX_PATH_POWERUP = os.path.join(os.path.dirname(__file__), 'assets', 'fx', '404721__owlstorm__retro-video-game-sfx-powerup-2.wav')
FX_PATH_WHOOSH = os.path.join(os.path.dirname(__file__), 'assets', 'fx', '802464__sadiquecat__stick-whoosh-6.wav')
FX_PATH_LASER = os.path.join(os.path.dirname(__file__), 'assets', 'fx', '811933__justwatson64__laser-1.wav')
FX_PATH_KICK = os.path.join(os.path.dirname(__file__), 'assets', 'fx', '812065__logicogonist__fat-kick-2b.wav')
