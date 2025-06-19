WormyReloaded is a modernized version of the classic Wormy game written in Python with Pygame.
Includes new features, bug fixes, and gameplay improvements over the original.


## Main changes and new features

### New features:

- Main menu with difficulty selection, score multipliers, and music.
- Game mode selection: **Portal Mode** (edge teleportation) or **Wall Death** (game over on wall hit, red borders).
- Randomly generated obstacles that never overlap with the worm or apple.
- Power-up after collecting the **WORM** word: collect letters in order, blinking current letter, super-apple counter.
- Semi-transparent cross effect during power-up, permanently removing obstacles.
- Power-up effect stacks: collecting another WORM while active increases the super-apple counter.
- GUI bar with WORM word, super-apple counter, and clear score display.

### Sound effects and music:

- Music in the menu and during gameplay (different tracks for each difficulty).
- Sound effects:
  - "whoosh" when the worm actually turns,
  - "laser" when collecting an apple,
  - "powerup" when activating the power-up,
  - "kick" on game over.

### Fixes and refactoring:

- All constants moved to `configuration.py`.
- Improved collision logic, apple generation, obstacle handling, and teleportation.
- The worm never appears on the GUI bar during teleportation.
- Red borders in Wall Death mode are drawn exactly on the game edge.
- Code refactored for clarity and modularity.



