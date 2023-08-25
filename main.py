import sys
import time

import pygame
from pygame import Surface

import messages
import save_load
import video_manager
from colors import Colors
from menu_state import MenuState
from sound_manager import SoundManager
from start_state import StartState


def get_cropped_image(image_path, x, y, width, height) -> pygame.Surface:
    image = pygame.image.load(image_path)
    # Definisci il rettangolo di ritaglio (x, y, larghezza, altezza)
    crop_rect = pygame.Rect(x, y, width, height)
    # Ritaglia l'immagine secondo il rettangolo definito
    # Crea una nuova immagine con sfondo trasparente
    cropped_image = pygame.Surface((crop_rect.width, crop_rect.height), pygame.SRCALPHA)
    cropped_image.blit(image, (0, 0), crop_rect)
    return cropped_image


class Game:
    def __init__(self):
        pygame.init()
        self.fade_opacity = 0  # Opacità iniziale del rettangolo di dissolvenza
        self.running = True
        self.state = MenuState()
        self.screen = pygame.display
        self.background = pygame.image
        self.custom_font = pygame.font
        self.start_state = None
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dragon Ball Z : I Leggendari Super Guerrieri")
        self.enter_pressed = False
        self.menu_options_img = None

    def draw_image_on_background(self, image_path, x, y, is_upscale: bool, width, height):
        # Disegna l'immagine sulla superficie temporanea alle coordinate (x, y)
        if is_upscale:
            image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        else:
            image = pygame.image.load(image_path)
        self.erase_screen(x, y)
        self.screen.blit(image, (x, y))
        pygame.display.flip()

    def draw_image_on_background_slowly(self, image_type, image_path, x, y, is_upscale: bool, r_width, r_height,
                                        dur_sec):
        max_opacity = 255
        frames_per_sec = 30
        total_frames = int(frames_per_sec * dur_sec)
        if image_type is not None:
            image = image_type
        else:
            image = pygame.image.load(image_path)
        if is_upscale:
            image = pygame.transform.scale(image, (r_width, r_height))
        for frame in range(total_frames):
            current_opacity = int((frame / total_frames) * max_opacity)  # Calcola l'opacità corrente
            image.set_alpha(current_opacity)  # Imposta l'opacità dell'immagine
            # self.screen.fill((0, 0, 0))  # Pulisce lo schermo
            self.screen.blit(image, (x, y))
            pygame.display.flip()

            time.sleep(1 / frames_per_sec)  # Ritardo tra le iterazioni

        self.screen.blit(image, (x, y))  # Mostra l'immagine con opacità massima
        pygame.display.flip()
        return image

    def draw_font(self, text, color, x, y):
        start_text = self.custom_font.render(text, True, color)
        start_text_rect = start_text.get_rect(center=(x, y))
        self.screen.blit(start_text, start_text_rect)

    def erase_screen(self, screen_width, screen_height):
        if screen_width is None or screen_height is None:
            screen_width = self.screen_width
            screen_height = self.screen_height
        while self.fade_opacity < 255:  # Assicurati di non superare l'opacità massima
            self.fade_opacity += 0.35  # Aumenta gradualmente l'opacità
            # Disegna il rettangolo di dissolvenza
            fade_surface = pygame.Surface((screen_width, screen_height))
            fade_surface.set_alpha(self.fade_opacity)
            fade_surface.fill(Colors.WHITE)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
        pygame.display.flip()

    def menu_options(self, options_list, screen_width, screen_height):
        # Pulizia dello schermo
        self.screen.blit(self.background, (0, 0))
        for i, option in enumerate(options_list):
            temp_color = Colors.BLACK
            self.draw_font(option, temp_color,
                           screen_width // 2, screen_height // 2 + i * 50)
        pygame.display.flip()
        self.menu_options_img = self.screen.copy()  # Copia la superficie corrente

    def menu(self, menu_image: str, menu_sound, options_list, is_double_check: bool, screen_width, screen_height):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dragon Ball Z : I Leggendari Super Guerrieri")
        self.erase_screen(None, None)
        # Caricamento e ridimensionamento dell'immagine di sfondo
        self.background = pygame.image.load(menu_image)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        # Caricamento del font personalizzato
        font_path = "resources/Fonts/pkmn rbygsc.ttf"  # Sostituisci con il percorso del tuo file di font
        self.custom_font = pygame.font.Font(font_path, 36)
        SoundManager.play_sound(menu_sound, True)
        if is_double_check:
            self.start_state = StartState()  # Nuovo stato di avvio
        if screen_width is None or screen_height is None:
            screen_width = self.screen_width
            screen_height = self.screen_height
        self.running = True
        while self.running:
            dt = pygame.time.Clock().tick(60) / 1000  # Calcola il tempo trascorso
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    SoundManager.stop_music()  # stop menu music
                    self.running = False
                elif is_double_check and self.enter_pressed is False:

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            SoundManager.play_click_sound()
                            self.enter_pressed = True
                            self.state = MenuState()
                            self.state.count_enter += 1
                            self.menu_options(options_list, screen_width, screen_height)
                else:
                    self.state.handle_menu(event, options_list)  # Gestisci la voce di menu
            if is_double_check:
                self.start_state.update(dt)  # Aggiorna lo stato di avvio
                # Mostra il messaggio di start solo se "ENTER" non è stato premuto
                if not self.enter_pressed:
                    # Pulizia dello schermo
                    self.screen.blit(self.background, (0, 0))
                    time.sleep(0.5)
                    pygame.display.flip()
                    # disegno dello schermo START
                    self.draw_font(self.start_state.message, Colors.BLACK, self.screen_width // 2,
                                   self.screen_height // 2)
                    time.sleep(0.9)
            else:
                if not self.enter_pressed:
                    self.enter_pressed = True
                    self.state = MenuState()
                    self.state.count_enter += 1
                    self.menu_options(options_list, screen_width, screen_height)

            # Mostra le opzioni del menu solo se "ENTER" è stato premuto o visualizzare il menu
            if self.enter_pressed:
                # disegna sfondo con menu, font e scelta
                self.screen.blit(self.menu_options_img, (0, 0))
                self.draw_font(options_list[self.state.selected_option], Colors.WHITE,
                               screen_width // 2, screen_height // 2 + self.state.selected_option * 50)
                self.draw_image_on_background("resources/images/Icons/select.PNG",
                                              (screen_width // 2) - 0.35 * screen_width,
                                              screen_height // 2 + self.state.selected_option * 45, False, 0, 0)
                pygame.display.flip()
            pygame.display.flip()
            if self.state.count_enter == MenuState.ENTER_CHOICE:
                self.running = False

        print("Uscito dal menu - " + str(options_list[self.state.selected_option]))
        self.erase_screen(None, None)
        SoundManager.stop_current_music()  # stop menu music
        return self.state.selected_option

    def run(self):
        from story import story_01
        video_manager.play_video("resources/videos/Gameboy Color - Boot Up Screen.mp4", 800, 600)
        self.menu("resources/images/Icons/menu.png", SoundManager.MENU_SOUND, messages.Messages.INIT_MENU_OPTION, True,
                  None, None)
        if self.state.selected_option == 0:  # new
            story_01(self)
        if self.state.selected_option == 1:  # load
            json_save = save_load.choose_slot(False)
        print("")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
