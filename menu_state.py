import pygame
from sound_manager import SoundManager


class MenuState:
    ENTER_CHOICE = 2

    def __init__(self):
        self.selected_option = 0
        self.count_enter = 0

    def execute_option(self, options_list):
        if self.selected_option < len(options_list):
            print(str(options_list[self.selected_option]))
        self.count_enter = MenuState.ENTER_CHOICE

    def handle_menu(self, event, options_list):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                SoundManager.play_scroll_sound()
                self.selected_option = (self.selected_option - 1) % len(options_list)
            elif event.key == pygame.K_DOWN:
                SoundManager.play_scroll_sound()
                self.selected_option = (self.selected_option + 1) % len(options_list)
            elif event.key == pygame.K_RETURN:
                SoundManager.play_click_sound()
                self.execute_option(options_list)
