import pygame
import sys
from sound_manager import SoundManager


def execute_option(option_index):
    if option_index == 0:
        print("Avvia nuova partita")
    elif option_index == 1:
        print("Carica partita")
    elif option_index == 2:
        print("Apri opzioni")
    elif option_index == 3:
        pygame.quit()
        sys.exit()


class MenuState:
    def __init__(self):
        self.options = ["Nuova Partita", "Carica Partita", "Opzioni", "Esci"]
        self.selected_option = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                SoundManager.play_scroll_sound()
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                SoundManager.play_scroll_sound()
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                SoundManager.play_click_sound()
                execute_option(self.selected_option)
