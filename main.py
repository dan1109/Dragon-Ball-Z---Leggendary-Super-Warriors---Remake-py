import sys
import time

import pygame

from colors import Colors
from menu_state import MenuState
from sound_manager import SoundManager
from start_state import StartState


class Game:
    def __init__(self):
        self.enter_pressed = False
        self.state = MenuState()
        pygame.init()
        SoundManager.play_menu_sound()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dragon Ball Z : I Leggendari Super Guerrieri")

        # Caricamento e ridimensionamento dell'immagine di sfondo
        self.background = pygame.image.load("resources/images/Icons/menu.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

        # Caricamento del font personalizzato
        font_path = "resources/Fonts/pkmn rbygsc.ttf"  # Sostituisci con il percorso del tuo file di font
        self.custom_font = pygame.font.Font(font_path, 36)
        self.start_state = StartState()  # Nuovo stato di avvio
        self.enter_pressed = False

    def draw_image_on_background(self, image_path, x, y):
        # Disegna l'immagine sulla superficie temporanea alle coordinate (x, y)
        self.screen.blit(pygame.image.load(image_path), (x, y))

    def draw_font(self, text, color, x, y):
        start_text = self.custom_font.render(text, True, color)
        start_text_rect = start_text.get_rect(center=(x, y))
        self.screen.blit(start_text, start_text_rect)

    def run(self):
        running = True
        start_text_rect = ""
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        new_selection = 0
        while running:
            dt = pygame.time.Clock().tick(60) / 1000  # Calcola il tempo trascorso

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.enter_pressed is False:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.enter_pressed = True
                            SoundManager.play_click_sound()  # Suono di click
                            # Pulizia dello schermo
                            self.screen.blit(self.background, (0, 0))
                            self.state = MenuState()
                else:
                    self.state.handle_input(event)  # Gestisci l'input

            self.start_state.update(dt)  # Aggiorna lo stato di avvio

            # Mostra il messaggio di start solo se "ENTER" non è stato premuto
            if not self.enter_pressed:
                # Pulizia dello schermo
                self.screen.blit(self.background, (0, 0))
                pygame.display.flip()
                # disegno dello schermo START
                time.sleep(0.5)
                self.draw_font(self.start_state.message, Colors.GRAY, self.screen_width // 2, self.screen_height // 2)
                time.sleep(0.5)

            # Mostra le opzioni del menu solo se "ENTER" è stato premuto
            if self.enter_pressed:
                for i, option in enumerate(self.state.options):
                    temp_color = (Colors.WHITE if i == self.state.selected_option else Colors.GRAY)
                    if temp_color == Colors.WHITE:
                        # disegna sfondo, font e le altre voci di menu
                        self.screen.blit(self.background, (0, 0))
                        self.draw_font(option, temp_color,
                                       self.screen_width // 2, self.screen_height // 2 + i * 50)
                        self.draw_image_on_background("resources/images/Icons/select.PNG", (self.screen_width // 2)-200,
                                                      self.screen_height // 2 + i * 50)
                    else:
                        self.draw_font(option, temp_color,
                                       self.screen_width // 2, self.screen_height // 2 + i * 50)
                    pygame.display.flip()
            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
