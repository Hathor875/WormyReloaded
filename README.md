WormyReloaded is a modernized version of the classic Wormy game written in Python with Pygame.

## Features

- Main menu with difficulty and mode selection
- Two game modes: **Portal Mode** (edge teleportation) and **Wall Death** (game over on wall hit)
- Random obstacles, power-ups, and the WORM word collection mechanic
- Sound effects and music (menu and in-game)
- Highscore system (separate for each mode)
- GUI bar with score, WORM word, and super-apple counter
- All configuration in `configuration.py`

## Project structure

- `wormy.py` – main game logic and loop
- `configuration.py` – game constants and settings
- `highscores.py` – highscore management (YAML files)
- `load_assets.py` – loading music and sound effects
- `music_player.py` – advanced music playback (pydub)
- `assets/` – sound and music files
- `requirements.txt` – dependencies

## How to run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the game:
   ```bash
   python wormy.py
   ```

## Controls

- Arrow keys / WASD – move the worm
- SPACE – turbo mode (if available)
- ESC – exit or return to menu

## Highscores

Highscores are saved in YAML files (`highscores_portal.yml`, `highscores_wall.yml`) for each mode separately. Only the top 10 scores are kept.

## Assets

All music and sound effects are in the `assets/` directory. You can replace them with your own `.ogg` files if you wish.

---

If you want to split the code into smaller files, see the suggested structure in the issues or ask the author for a modular version.



