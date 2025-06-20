# Wormy, by Al Sweigart al@inventwithpython.com
# (Pygame) Lead the green snake around the screen eating red apples.



import random, pygame, sys
import math
import configuration
import load_assets  # added: import ładowania assetów
import highscores

# fix: jawny import stałych z configuration.py
assert configuration.WINDOWWIDTH % configuration.CELLSIZE == 0, "Window width must be a multiple of cell size."
assert configuration.WINDOWHEIGHT % configuration.CELLSIZE == 0, "Window height must be a multiple of cell size."

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
LIGHTBLUE  = (100, 200, 255)  # added: jasno-niebieski do power-upa
YELLOW    = (255, 255, 0)  # added: kolor żółty
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

LETTERS = ['W', 'O', 'R', 'M']

def display_scores(mode):
    """Wyświetl tabelę wyników dla danego trybu."""
    font = pygame.font.Font('freesansbold.ttf', 32)
    smallfont = pygame.font.Font('freesansbold.ttf', 24)
    scores = highscores.read_highscores(mode)
    
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        
        # Tytuł
        title = font.render(f'Najlepsze wyniki - {mode}', True, YELLOW)
        titleRect = title.get_rect(center=(configuration.WINDOWWIDTH//2, 50))
        DISPLAYSURF.blit(title, titleRect)
        
        # Tabela wyników
        if not scores:
            noScores = smallfont.render('Brak wyników', True, WHITE)
            noScoresRect = noScores.get_rect(center=(configuration.WINDOWWIDTH//2, configuration.WINDOWHEIGHT//2))
            DISPLAYSURF.blit(noScores, noScoresRect)
        else:
            for i, score in enumerate(scores):
                y_pos = 120 + i * 35
                # Miejsce i nazwa
                place_name = smallfont.render(f"{i+1}. {score['name']}", True, WHITE)
                DISPLAYSURF.blit(place_name, (80, y_pos))
                
                # Wynik
                score_text = smallfont.render(str(score['score']), True, YELLOW)
                score_rect = score_text.get_rect(right=configuration.WINDOWWIDTH-200, top=y_pos)
                DISPLAYSURF.blit(score_text, score_rect)
                
                # Poziom trudności
                diff_text = smallfont.render(score['difficulty'], True, LIGHTBLUE)
                DISPLAYSURF.blit(diff_text, (configuration.WINDOWWIDTH-180, y_pos))
        
        # Instrukcja wyjścia
        exitText = smallfont.render('ESC - Powrót do menu', True, DARKGRAY)
        exitRect = exitText.get_rect(center=(configuration.WINDOWWIDTH//2, configuration.WINDOWHEIGHT-40))
        DISPLAYSURF.blit(exitText, exitRect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def mainMenu():
    # added: proste menu główne z wyborem poziomu trudności, mnożnikami punktów i kluczem muzyki
    menuFont = pygame.font.Font('freesansbold.ttf', 40)
    infoFont = pygame.font.Font('freesansbold.ttf', 24)
    mode_selected = 0  # 0: Portal Mode, 1: Wall Death
    mode_names = ["Portal Mode", "Wall Death"]
    selected = 1  # 0: łatwy, 1: normalny, 2: trudny
    levels = [
        {"name": "EASY", "delay": 9, "multiplier": 1, "music": "game_easy", "super_apples": 3},
        {"name": "MID", "delay": 6, "multiplier": 2, "music": "game_normal", "super_apples": 2},
        {"name": "HARD", "delay": 4, "multiplier": 3, "music": "game_hard", "super_apples": 1}
    ]
    # przywrócone odtwarzanie muzyki menu przez pygame
    pygame.mixer.music.load(MUSIC['menu'])
    pygame.mixer.music.play(-1)
    while True:
        DISPLAYSURF.fill(configuration.BGCOLOR)
        titleSurf = menuFont.render('WormyReloaded - Menu', True, configuration.WHITE)
        titleRect = titleSurf.get_rect(center=(configuration.WINDOWWIDTH//2, 80))
        DISPLAYSURF.blit(titleSurf, titleRect)
        # tryb gry
        for i, mode in enumerate(mode_names):
            color = configuration.RED if i == mode_selected else configuration.WHITE
            surf = infoFont.render(f"Tryb: {mode}", True, color)
            rect = surf.get_rect(center=(configuration.WINDOWWIDTH//2, 140 + i*30))
            DISPLAYSURF.blit(surf, rect)
        # poziomy trudności
        for i, level in enumerate(levels):
            color = configuration.GREEN if i == selected else configuration.WHITE
            surf = infoFont.render(f'{level["name"]} (x{level["multiplier"]})', True, color)
            rect = surf.get_rect(center=(configuration.WINDOWWIDTH//2, 220 + i*50))
            DISPLAYSURF.blit(surf, rect)
        # Dodaj opcję instrukcji
        instrSurf = infoFont.render('I - Instructions', True, configuration.LIGHTBLUE)
        instrRect = instrSurf.get_rect(center=(configuration.WINDOWWIDTH//2, configuration.WINDOWHEIGHT-120))
        DISPLAYSURF.blit(instrSurf, instrRect)
        
        scoreSurf = infoFont.render('S - High Scores', True, configuration.LIGHTBLUE)
        scoreRect = scoreSurf.get_rect(center=(configuration.WINDOWWIDTH//2, configuration.WINDOWHEIGHT-90))
        DISPLAYSURF.blit(scoreSurf, scoreRect)
        
        infoSurf = infoFont.render('Arrows up/down - level, left/right - mode, Enter - start', True, configuration.DARKGRAY)
        infoRect = infoSurf.get_rect(center=(configuration.WINDOWWIDTH//2, configuration.WINDOWHEIGHT-60))
        DISPLAYSURF.blit(infoSurf, infoRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(levels)
                elif event.key == pygame.K_LEFT:
                    mode_selected = (mode_selected - 1) % len(mode_names)
                elif event.key == pygame.K_RIGHT:
                    mode_selected = (mode_selected + 1) % len(mode_names)
                elif event.key == pygame.K_i:
                    showInstructions()
                elif event.key == pygame.K_s:
                    display_scores(mode_names[mode_selected])
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    pygame.mixer.music.stop()
                    result = dict(levels[selected])
                    result['mode'] = mode_names[mode_selected]
                    return result

# fix: wysokość paska GUI
UI_HEIGHT = 40

# fix: powiększenie okna gry o pasek GUI
WINDOWHEIGHT_WITH_UI = configuration.WINDOWHEIGHT + UI_HEIGHT

# Załaduj efekty dźwiękowe jako globalną zmienną FX
FX = None

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, MUSIC, FX
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((configuration.WINDOWWIDTH, WINDOWHEIGHT_WITH_UI))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')
    # fix: załaduj muzykę do obiektu MUSIC przed wywołaniem mainMenu
    MUSIC = load_assets.load_music()
    # załaduj efekty dźwiękowe do FX
    FX = load_assets.load_fx()    # showStartScreen() tylko na samym początku gry
    showStartScreen()
    
    while True:
        level = mainMenu()
        score = runGame(level)  # Odbieramy wynik z gry
        if score is None:
            score = 0
        showGameOverScreen(score, level['mode'], level['name'])


def generate_obstacles(wormCoords, apple, num_obstacles=10):
    # added: generowanie losowych przeszkód, nie kolidujących z wężem i jabłkiem
    obstacles = []
    occupied = set((seg['x'], seg['y']) for seg in wormCoords)
    occupied.add((apple['x'], apple['y']))
    while len(obstacles) < num_obstacles:
        x = random.randint(0, configuration.CELLSIZE - 1)
        y = random.randint(0, configuration.CELLSIZE - 1)
        if (x, y) not in occupied:
            obstacles.append({'x': x, 'y': y})
            occupied.add((x, y))
    return obstacles

def getRandomLetterLocation(wormCoords, apple, obstacles, letter_pos=None):
    occupied = set((seg['x'], seg['y']) for seg in wormCoords)
    occupied.add((apple['x'], apple['y']))
    for obs in obstacles:
        occupied.add((obs['x'], obs['y']))
    if letter_pos:
        occupied.add((letter_pos['x'], letter_pos['y']))
    while True:
        x = random.randint(0, configuration.CELLSIZE - 1)
        y = random.randint(0, configuration.CELLSIZE - 1)
        if (x, y) not in occupied:
            return {'x': x, 'y': y}

def runGame(level):
    # przywrócone odtwarzanie muzyki do gry przez pygame
    pygame.mixer.music.load(MUSIC[level['music']])
    pygame.mixer.music.play(-1)
    # Set a random start point.
    startx = random.randint(5, configuration.CELLSIZE - 6)
    starty = random.randint(5, configuration.CELLSIZE - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = configuration.RIGHT
    # fix: dodano zmienną do przechowywania nowego kierunku
    new_direction = direction
    obstacles = []  # fix: inicjalizacja obstacles przed użyciem
    apple = getRandomLocation(wormCoords, obstacles)
    obstacles = generate_obstacles(wormCoords, apple, num_obstacles=10)
    # added: losowa litera na planszy i lista zebranych
    letter_char = random.choice(LETTERS)
    letter_pos = getRandomLetterLocation(wormCoords, apple, obstacles)
    collected_letters = []
    powerup_active = False
    powerup_timer = 0
    move_counter = 0
    removed_obstacles = []  # added: lista tymczasowo usuniętych przeszkód
    super_apples_left = 0  # fix: efekt krzyża domyślnie wyłączony, aktywuje się dopiero po zebraniu napisu WORM
    UI_HEIGHT = 40  # added: wysokość paska UI na górze
    mode = level.get('mode', 'Portal Mode')
    turbo = False
    turbo_turns = 0
    turbo_multiplier = 2  # mnożnik dla turbo
    turbo_delay = max(1, level['delay'] // 2)  # przyspieszenie w turbo
    score = 0  # nowy licznik punktów
    turbo_fx_channel = None
    turbo_fx_playing = False
    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                # fix: zmiana kierunku zapisywana do new_direction
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != configuration.RIGHT:
                    if new_direction != configuration.LEFT:
                        new_direction = configuration.LEFT
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != configuration.LEFT:
                    if new_direction != configuration.RIGHT:
                        new_direction = configuration.RIGHT
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != configuration.DOWN:
                    if new_direction != configuration.UP:
                        new_direction = configuration.UP
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != configuration.UP:
                    if new_direction != configuration.DOWN:
                        new_direction = configuration.DOWN
                elif event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_SPACE:
                    turbo = True
                    if not turbo_fx_playing:
                        pygame.mixer.music.stop()
                        turbo_fx_channel = pygame.mixer.find_channel()
                        if turbo_fx_channel:
                            turbo_fx_channel.play(FX['dnb9'], loops=-1)
                            turbo_fx_playing = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    turbo = False
                    if turbo_fx_channel:
                        turbo_fx_channel.stop()
                        turbo_fx_channel = None
                        turbo_fx_playing = False
                    # po wyjściu z turbo przywróć muzykę gry
                    pygame.mixer.music.play(-1)

        # fix: przesuwamy węża tylko co configuration.SNAKE_MOVE_DELAY klatek
        move_counter += 1
        current_delay = turbo_delay if turbo else level['delay']
        if move_counter >= current_delay:
            move_counter = 0
            if direction != new_direction:
                if FX: FX['whoosh'].play()
                if turbo:
                    turbo_turns += 1
            direction = new_direction

            head = wormCoords[configuration.HEAD]
            teleported = False            # obsługa trybu Wall Death
            if mode == 'Wall Death':
                if head['x'] < 0 or head['x'] >= configuration.CELLWIDTH or head['y'] < 0 or head['y'] >= configuration.CELLHEIGHT:
                    base_score = score * level['multiplier']
                    turbo_score = turbo_turns * turbo_multiplier
                    return base_score + turbo_score  # game over przy uderzeniu w ścianę
            else:  # Portal Mode
                if head['y'] < 0:
                    new_y = configuration.CELLHEIGHT - 1
                    for seg in wormCoords:
                        seg['x'] = head['x']
                        seg['y'] = new_y
                    head['y'] = new_y
                    teleported = True
                elif head['y'] >= configuration.CELLHEIGHT:
                    new_y = 0
                    for seg in wormCoords:
                        seg['x'] = head['x']
                        seg['y'] = new_y
                    head['y'] = new_y
                    teleported = True
                if head['x'] < 0:
                    head['x'] = configuration.CELLWIDTH - 1
                elif head['x'] >= configuration.CELLWIDTH:
                    head['x'] = 0
            # fix: pomiń sprawdzanie kolizji z samym sobą jeśli była teleportacja
            if not teleported:
                for wormBody in wormCoords[1:]:
                    if wormBody['x'] == head['x'] and wormBody['y'] == head['y']:
                        base_score = score * level['multiplier']
                        turbo_score = turbo_turns * turbo_multiplier
                        return base_score + turbo_score  # game over

            # fix: kolizja z przeszkodą = game over
            for obs in obstacles:
                if wormCoords[configuration.HEAD]['x'] == obs['x'] and wormCoords[configuration.HEAD]['y'] == obs['y']:
                    base_score = score * level['multiplier']
                    turbo_score = turbo_turns * turbo_multiplier
                    return base_score + turbo_score  # game over

            # check if the worm has eaten an apply
            # fix: zebranie jabłka zmniejsza liczbę super-jabłek
            if wormCoords[configuration.HEAD]['x'] == apple['x'] and wormCoords[configuration.HEAD]['y'] == apple['y']:
                # dźwięk zebrania jabłka
                if FX: FX['laser'].play()
                apple = getRandomLocation(wormCoords, obstacles) # set a new apple somewhere
                letter_char = random.choice(LETTERS)
                letter_pos = getRandomLetterLocation(wormCoords, apple, obstacles)
                if super_apples_left > 0:
                    super_apples_left -= 1
                score += 100  # +100 za jabłko
            else:
                del wormCoords[-1] # remove worm's tail segment

            # move the worm by adding a segment in the direction it is moving
            if direction == configuration.UP:
                newHead = {'x': wormCoords[configuration.HEAD]['x'], 'y': wormCoords[configuration.HEAD]['y'] - 1}
            elif direction == configuration.DOWN:
                newHead = {'x': wormCoords[configuration.HEAD]['x'], 'y': wormCoords[configuration.HEAD]['y'] + 1}
            elif direction == configuration.LEFT:
                newHead = {'x': wormCoords[configuration.HEAD]['x'] - 1, 'y': wormCoords[configuration.HEAD]['y']}
            elif direction == configuration.RIGHT:
                newHead = {'x': wormCoords[configuration.HEAD]['x'] + 1, 'y': wormCoords[configuration.HEAD]['y']}
            wormCoords.insert(0, newHead)

        # added: zbieranie litery
        # fix: kolejność liter ma znaczenie, zła litera resetuje kolekcję
        if wormCoords[configuration.HEAD]['x'] == letter_pos['x'] and wormCoords[configuration.HEAD]['y'] == letter_pos['y']:
            expected_letter = LETTERS[len(collected_letters)]
            if letter_char == expected_letter:
                collected_letters.append(letter_char)
                if len(collected_letters) == len(LETTERS):
                    collected_letters = []
                    super_apples_left += level['super_apples']  # sumowanie efektu, a nie nadpisywanie
                    # dźwięk powerup
                    if FX: load_assets.play_fx(FX['powerup'])
            else:
                collected_letters = []  # reset
            letter_char = random.choice(LETTERS)
            letter_pos = getRandomLetterLocation(wormCoords, apple, obstacles)
        # added: obsługa powerupa (np. nieśmiertelność)
        if powerup_active:
            # wyznacz pola krzyża wokół jabłka
            cross = [
                {'x': apple['x'], 'y': apple['y'] - 1},
                {'x': apple['x'], 'y': apple['y'] + 1},
                {'x': apple['x'] - 1, 'y': apple['y']},
                {'x': apple['x'] + 1, 'y': apple['y']}
            ]
            # usuwanie przeszkód z krzyża
            if not removed_obstacles:
                for c in cross:
                    for obs in obstacles[:]:
                        if obs['x'] == c['x'] and obs['y'] == c['y']:
                            removed_obstacles.append(obs)
                            obstacles.remove(obs)
            powerup_timer -= 1
            if powerup_timer <= 0:
                powerup_active = False
                # przywróć przeszkody
                obstacles.extend(removed_obstacles)
                removed_obstacles = []

        # fix: czarne tło na górze planszy na napisy
        DISPLAYSURF.fill(configuration.BGCOLOR)
        pygame.draw.rect(DISPLAYSURF, configuration.BLACK, (0, 0, configuration.WINDOWWIDTH, UI_HEIGHT))
        drawGrid(offset_y=UI_HEIGHT, mode=mode)
        drawWorm(wormCoords, offset_y=UI_HEIGHT, turbo=turbo)
        drawApple(apple, offset_y=UI_HEIGHT)
        drawObstacles(obstacles, offset_y=UI_HEIGHT)
        if super_apples_left > 0:
            drawFullPowerupCross(apple, offset_y=UI_HEIGHT)
        drawLetter(letter_char, letter_pos, offset_y=UI_HEIGHT)
        drawCollectedLetters(collected_letters, super_apples_left > 0, super_apples_left)
        # Dodanie punktów za turbo zakręty
        base_score = score * level['multiplier']
        turbo_score = turbo_turns * turbo_multiplier
        drawScore(base_score + turbo_score)
        drawSnakeLength(len(wormCoords))  # Dodaj licznik długości węża
        pygame.display.update()
        FPSCLOCK.tick(configuration.FPS)




def checkForKeyPress():
    if len(pygame.event.get(pygame.QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(pygame.KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == pygame.K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    # Nowy, efektowny ekran startowy WormyReloaded
    titleFont = pygame.font.Font('freesansbold.ttf', 80)
    subtitleFont = pygame.font.Font('freesansbold.ttf', 40)
    infoFont = pygame.font.Font('freesansbold.ttf', 28)
    clock = pygame.time.Clock()
    angle = 0
    color_shift = 0
    wormy_colors = [configuration.GREEN, configuration.LIGHTBLUE, configuration.RED, configuration.DARKGREEN]
    logo_points = [
        (120, 320), (160, 300), (200, 320), (240, 300), (280, 320), (320, 300), (360, 320)
    ]
    while True:
        DISPLAYSURF.fill((10, 10, 30))
        # Efektowne logo WormyReloaded
        titleSurf = titleFont.render('Wormy', True, (255, 255, 255))
        titleRect = titleSurf.get_rect(center=(configuration.WINDOWWIDTH / 2, 120))
        DISPLAYSURF.blit(titleSurf, titleRect)
        subtitleSurf = subtitleFont.render('Reloaded', True, (0, 255, 180))
        subtitleRect = subtitleSurf.get_rect(center=(configuration.WINDOWWIDTH / 2, 190))
        DISPLAYSURF.blit(subtitleSurf, subtitleRect)
        # Animowany wąż pod napisem
        for i, (x, y) in enumerate(logo_points):
            color = wormy_colors[(i + color_shift) % len(wormy_colors)]
            pygame.draw.circle(DISPLAYSURF, color, (x + 120, y), 18)
            pygame.draw.circle(DISPLAYSURF, (0, 0, 0), (x + 120, y), 18, 2)
        # Efekt świetlny na napisie
        glowSurf = titleFont.render('Wormy', True, (0, 255, 180))
        glowSurf.set_alpha(80 + int(60 * abs(math.sin(angle))))
        DISPLAYSURF.blit(glowSurf, titleRect.move(0, 0))
        # Instrukcja
        infoSurf = infoFont.render('Naciśnij dowolny klawisz, aby rozpocząć', True, (200, 200, 200))
        infoRect = infoSurf.get_rect(center=(configuration.WINDOWWIDTH / 2, configuration.WINDOWHEIGHT - 80))
        DISPLAYSURF.blit(infoSurf, infoRect)
        pygame.display.update()
        angle += 0.05
        color_shift = (color_shift + 1) % len(wormy_colors)
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        clock.tick(30)


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation(wormCoords=None, obstacles=None):
    # fix: jabłko nie może się pojawiać na wężu ani na przeszkodach
    occupied = set()
    if wormCoords:
        occupied.update((seg['x'], seg['y']) for seg in wormCoords)
    if obstacles:
        occupied.update((obs['x'], obs['y']) for obs in obstacles)
    while True:
        x = random.randint(0, configuration.CELLWIDTH - 1)
        y = random.randint(0, configuration.CELLHEIGHT - 1)
        if (x, y) not in occupied:
            return {'x': x, 'y': y}


def showGameOverScreen(score=0, mode="Portal Mode", difficulty="EASY"):
    # zatrzymaj wszystkie dźwięki i muzykę
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    # odtwórz dźwięk kick (game over)
    if FX: FX['kick'].play()
    
    # Sprawdź, czy wynik kwalifikuje się do tablicy wyników
    current_scores = highscores.read_highscores(mode)
    qualifies = len(current_scores) < 10 or score > min(score['score'] for score in current_scores)
    
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    infoFont = pygame.font.Font('freesansbold.ttf', 32)
    
    # Oblicz pozycje elementów
    window_center_x = configuration.WINDOWWIDTH / 2
    window_center_y = configuration.WINDOWHEIGHT / 2
    
    # Renderuj "Game Over"
    gameSurf = gameOverFont.render('Game Over', True, configuration.WHITE)
    gameRect = gameSurf.get_rect()
    gameRect.center = (window_center_x, window_center_y - 100)
    
    # Wyświetl końcowy wynik
    scoreSurf = infoFont.render(f'Final Score: {score}', True, configuration.WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.center = (window_center_x, window_center_y)
    
    DISPLAYSURF.fill(configuration.BGCOLOR)
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    
    if qualifies:
        name = ""
        nameEntered = False
        cursor_visible = True
        cursor_time = pygame.time.get_ticks()
        
        while not nameEntered:
            current_time = pygame.time.get_ticks()
            
            # Miganie kursora co 530ms
            if current_time - cursor_time > 530:
                cursor_visible = not cursor_visible
                cursor_time = current_time
            
            DISPLAYSURF.fill(configuration.BGCOLOR)
            DISPLAYSURF.blit(gameSurf, gameRect)
            DISPLAYSURF.blit(scoreSurf, scoreRect)
            
            # Komunikat o nowym rekordzie
            promptSurf = infoFont.render('New High Score!', True, configuration.YELLOW)
            promptRect = promptSurf.get_rect()
            promptRect.center = (window_center_x, window_center_y + 50)
            
            # Instrukcja wpisywania imienia
            enterSurf = infoFont.render('Enter your name (4 chars):', True, configuration.WHITE)
            enterRect = enterSurf.get_rect()
            enterRect.center = (window_center_x, window_center_y + 90)
            
            # Pole do wpisywania imienia z migającym kursorem
            if len(name) < 4:
                display_name = name + ("▋" if cursor_visible else " ")
            else:
                display_name = name
            
            nameSurf = infoFont.render(display_name, True, 
                                     configuration.YELLOW if len(name) == 4 else configuration.WHITE)
            nameRect = nameSurf.get_rect()
            nameRect.center = (window_center_x, window_center_y + 130)
            
            # Ramka wokół pola wprowadzania
            input_bg_rect = pygame.Rect(0, 0, 150, 40)
            input_bg_rect.center = nameRect.center
            pygame.draw.rect(DISPLAYSURF, configuration.DARKGRAY, input_bg_rect, 1)
            
            # Instrukcja zatwierdzenia i licznik znaków
            if len(name) == 4:
                confirmSurf = infoFont.render('Press Enter to continue', True, 
                                            configuration.YELLOW if cursor_visible else configuration.DARKGRAY)
                confirmRect = confirmSurf.get_rect()
                confirmRect.center = (window_center_x, window_center_y + 170)
                DISPLAYSURF.blit(confirmSurf, confirmRect)
            else:
                # Licznik wprowadzonych znaków
                counterSurf = infoFont.render(f'{len(name)}/4', True, configuration.DARKGRAY)
                counterRect = counterSurf.get_rect()
                counterRect.center = (window_center_x, window_center_y + 170)
                DISPLAYSURF.blit(counterSurf, counterRect)
            
            DISPLAYSURF.blit(promptSurf, promptRect)
            DISPLAYSURF.blit(enterSurf, enterRect)
            DISPLAYSURF.blit(nameSurf, nameRect)
            
            pygame.display.update()
            FPSCLOCK.tick(30)  # Limit FPS dla płynnej animacji
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) == 4:
                        if FX: FX['laser'].play()
                        nameEntered = True
                    elif event.key == pygame.K_BACKSPACE and len(name) > 0:
                        name = name[:-1]
                        if FX: FX['whoosh'].play()
                    elif len(name) < 4 and event.unicode.isalnum():
                        name += event.unicode.upper()
                        if FX: FX['powerup'].play()
        
        # Zapisz wynik
        highscores.save_highscore(mode, score, name, difficulty)
    else:
        # Wyświetl informację o naciśnięciu klawisza
        pressKeySurf = infoFont.render('Press any key to continue', True, configuration.DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.center = (window_center_x, window_center_y + 50)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
        pygame.display.update()
        
        pygame.time.wait(500)
        checkForKeyPress() # clear out any key presses in the event queue
        
        while True:
            if checkForKeyPress():
                pygame.event.get() # clear event queue
                return
    
    return

def drawScore(score, multiplier=1):
    # fix: nie wyświetlaj mnożnika
    scoreSurf = BASICFONT.render(f'Score: {score}', True, configuration.WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (configuration.WINDOWWIDTH - 220, 5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, offset_y=0, turbo=False):
    for coord in wormCoords:
        # nie rysuj segmentów poza planszą (np. y < 0)
        if coord['y'] < 0:
            continue
        x = coord['x'] * configuration.CELLSIZE
        y = coord['y'] * configuration.CELLSIZE + offset_y
        wormSegmentRect = pygame.Rect(x, y, configuration.CELLSIZE, configuration.CELLSIZE)
        if turbo:
            pygame.draw.rect(DISPLAYSURF, configuration.YELLOW, wormSegmentRect)
        else:
            pygame.draw.rect(DISPLAYSURF, configuration.DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, configuration.CELLSIZE - 8, configuration.CELLSIZE - 8)
        if turbo:
            pygame.draw.rect(DISPLAYSURF, configuration.YELLOW, wormInnerSegmentRect)
        else:
            pygame.draw.rect(DISPLAYSURF, configuration.GREEN, wormInnerSegmentRect)


def drawApple(coord, offset_y=0):
    x = coord['x'] * configuration.CELLSIZE
    y = coord['y'] * configuration.CELLSIZE + offset_y
    appleRect = pygame.Rect(x, y, configuration.CELLSIZE, configuration.CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, configuration.RED, appleRect)


def drawGrid(offset_y=0, mode='Portal Mode'):
    # Rysuj siatkę
    for x in range(0, configuration.WINDOWWIDTH, configuration.CELLSIZE):
        pygame.draw.line(DISPLAYSURF, configuration.DARKGRAY, (x, offset_y), (x, configuration.WINDOWHEIGHT + offset_y))
    for y in range(0, configuration.WINDOWHEIGHT, configuration.CELLSIZE):
        pygame.draw.line(DISPLAYSURF, configuration.DARKGRAY, (0, y + offset_y), (configuration.WINDOWWIDTH, y + offset_y))
    # Rysuj czerwone ramki na krawędziach w trybie Wall Death
    if mode == 'Wall Death':
        border_color = configuration.RED
        border_rect = pygame.Rect(0, offset_y, configuration.WINDOWWIDTH, configuration.WINDOWHEIGHT)
        pygame.draw.rect(DISPLAYSURF, border_color, border_rect, 2)  # grubość 2 px


def drawObstacles(obstacles, offset_y=0):
    # added: rysowanie przeszkód jako szare kwadraty
    for obs in obstacles:
        x = obs['x'] * configuration.CELLSIZE
        y = obs['y'] * configuration.CELLSIZE + offset_y
        rect = pygame.Rect(x, y, configuration.CELLSIZE, configuration.CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, configuration.DARKGRAY, rect)

def drawLetter(char, pos, offset_y=0):
    font = pygame.font.Font('freesansbold.ttf', 28)
    surf = font.render(char, True, configuration.RED)
    rect = surf.get_rect(center=(pos['x'] * configuration.CELLSIZE + configuration.CELLSIZE//2, pos['y'] * configuration.CELLSIZE + configuration.CELLSIZE//2 + offset_y))
    DISPLAYSURF.blit(surf, rect)

def drawCollectedLetters(collected, powerup_active, super_apples_left=0):
    # fix: usunięcie lokalnego importu pygame, użycie globalnego
    font = pygame.font.Font('freesansbold.ttf', 24)
    blink = (pygame.time.get_ticks() // 300) % 2 == 0
    for i, l in enumerate(LETTERS):
        if i < len(collected):
            color = configuration.GREEN
        elif i == len(collected):
            color = configuration.RED if blink else configuration.DARKGRAY
        else:
            color = configuration.DARKGRAY
        surf = font.render(l, True, color)
        rect = surf.get_rect(topleft=(20 + i*30, 5))
        DISPLAYSURF.blit(surf, rect)
    if powerup_active or super_apples_left > 0:
        text = f'  POWER-UP! ({super_apples_left})'
        surf = font.render(text, True, configuration.GREEN)
        rect = surf.get_rect(topleft=(20 + len(LETTERS)*30 + 10, 5))
        DISPLAYSURF.blit(surf, rect)

def drawFullPowerupCross(apple, offset_y=0):
    # fix: rysowanie półprzezroczystego krzyża na całą planszę
    overlay = pygame.Surface((configuration.WINDOWWIDTH, configuration.WINDOWHEIGHT), pygame.SRCALPHA)
    alpha = 150  # przezroczystość (0-255)
    x = apple['x'] * configuration.CELLSIZE
    rect_v = pygame.Rect(x, 0, configuration.CELLSIZE, configuration.WINDOWHEIGHT)
    pygame.draw.rect(overlay, (100, 200, 255, alpha), rect_v)
    y = apple['y'] * configuration.CELLSIZE
    rect_h = pygame.Rect(0, y, configuration.WINDOWWIDTH, configuration.CELLSIZE)
    pygame.draw.rect(overlay, (100, 200, 255, alpha), rect_h)
    DISPLAYSURF.blit(overlay, (0, offset_y))


def showInstructions():
    font = pygame.font.Font('freesansbold.ttf', 22)
    smallfont = pygame.font.Font('freesansbold.ttf', 16)
    instructions = [
        'Instructions:',
        '- Arrows/WASD: control the worm',
        '- Space: TURBO (speed up, yellow worm, points for turns)',
        '- Collect apples (100 pts each)',
        '- Collect WORM letters to activate super-apples',
        '- Modes: Portal (wrap around) or Wall Death (wall = game over)',
        '',
        'Press any key to return to menu.'
    ]
    while True:
        DISPLAYSURF.fill(configuration.BGCOLOR)
        for i, line in enumerate(instructions):
            surf = font.render(line, True, configuration.WHITE) if i == 0 else smallfont.render(line, True, configuration.LIGHTBLUE)
            rect = surf.get_rect(center=(configuration.WINDOWWIDTH//2, 80 + i*28))
            DISPLAYSURF.blit(surf, rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return

def drawSnakeLength(length):
    """Wyświetla długość węża na pasku UI."""
    lengthSurf = BASICFONT.render(f'Length: {length}', True, configuration.YELLOW)
    lengthRect = lengthSurf.get_rect()
    lengthRect.topleft = (configuration.WINDOWWIDTH - 350, 5)
    DISPLAYSURF.blit(lengthSurf, lengthRect)

if __name__ == '__main__':
    main()