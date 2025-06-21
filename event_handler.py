import pygame
from wormy import showInstructions, display_scores

def main_menu_event_handler(terminate_callback, levels, configuration, selected_level, mode_selected):
    """Obsługuje zdarzenia w menu głównym."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate_callback()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_level = (selected_level - 1) % len(levels)
            elif event.key == pygame.K_DOWN:
                selected_level = (selected_level + 1) % len(levels)
            elif event.key == pygame.K_LEFT:
                mode_selected = (mode_selected - 1) % len(configuration.mode_names)
            elif event.key == pygame.K_RIGHT:
                mode_selected = (mode_selected + 1) % len(configuration.mode_names)
            elif event.key == pygame.K_i:
                showInstructions()
            elif event.key == pygame.K_s:
                display_scores(configuration.mode_names[mode_selected])
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                pygame.mixer.music.stop()
                result = dict(levels[selected_level])
                result['mode'] = configuration.mode_names[mode_selected]
                return result
    return None, selected_level, mode_selected