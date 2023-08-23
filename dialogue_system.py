import time

import pygame

from colors import Colors
from sound_manager import SoundManager


def box_face(game, start_w, start_h, is_center: bool, is_sx: bool):
    end_w = 40
    end_h = 53
    if start_w == 22 and start_h == 34:
        raditz_face = game.get_cropped_image("resources/images/Icons/All_faces.png", 22, 34, end_w, end_h)
        face = raditz_face
    if start_w == 64 and start_h == 34:
        goku_face = game.get_cropped_image("resources/images/Icons/All_faces.png", 64, 34, end_w, end_h)
        face = goku_face
    if is_center:
        game.draw_image_on_background_slowly(face, None, game.screen_width / 2.7, game.screen_height / 4.5, True,
                                             game.screen_width / 4, game.screen_height / 2.5, 0.5)
    elif is_sx:
        game.draw_image_on_background_slowly(face, None, game.screen_width / 8, game.screen_height / 4.5, True,
                                             game.screen_width / 4, game.screen_height / 2.5, 0.5)
    elif not is_sx:
        game.draw_image_on_background_slowly(face, None, game.screen_width / 1.5, game.screen_height / 4.5, True,
                                             game.screen_width / 4, game.screen_height / 2.5, 0.5)



# Clear only the dialog box area by drawing a white rectangle
def create_empty_box(screen, screen_width, screen_height):
    dialog_box_rect = pygame.Rect(0, screen_height - 201, screen_width, 201)
    pygame.draw.rect(screen, Colors.WHITE, dialog_box_rect)
    pygame.display.flip()
    # Disegna il box del dialogo
    # Caricamento del font personalizzato
    font_path = "resources/Fonts/pkmn rbygsc.ttf"  # Sostituisci con il percorso del tuo file di font
    font = pygame.font.Font(font_path, 36)
    line_surface = font.render("", True, Colors.BLACK)
    pygame.draw.rect(screen, Colors.BLACK, (0, screen_height - 200, screen_width, 200), 2)
    screen.blit(line_surface, (20, screen_height - 180 + 1 * 40))
    pygame.display.flip()
    # Capture the current screen content


def screen_white_and_empty_box(game):
    screen_white_transition(game.screen, game.screen_width, game.screen_height, 1)
    create_empty_box(game.screen, game.screen_width, game.screen_height)


def screen_white_transition(screen, screen_width, screen_height, duration_sec):
    white_surface = pygame.Surface((screen_width, screen_height))
    white_surface.set_alpha(0)  # Opacità iniziale
    white_color = (255, 255, 255)
    white_surface.fill(white_color)

    frames_per_sec = 30
    total_frames = int(frames_per_sec * duration_sec)

    for frame in range(total_frames):
        current_opacity = int((frame / total_frames) * 255)  # Calcola l'opacità corrente
        white_surface.set_alpha(current_opacity)  # Imposta l'opacità della superficie
        screen.blit(white_surface, (0, 0))
        pygame.display.flip()

        time.sleep(1 / frames_per_sec)  # Ritardo tra le iterazioni

    # Mostra la superficie con opacità massima
    white_surface.set_alpha(255)
    screen.blit(white_surface, (0, 0))
    pygame.display.flip()


def image_suspend(screen, triangle_image, triangle_rect, screen_height, triangle_y_offset, triangle_movement_speed):
    # Aggiorna la posizione del triangolo
    triangle_rect.y = screen_height - 30 + triangle_y_offset
    triangle_y_offset += triangle_movement_speed
    if triangle_y_offset > 10 or triangle_y_offset < -10:
        triangle_movement_speed *= -1

    # Ruota l'immagine del triangolo di 90 gradi
    rotated_triangle = pygame.transform.rotate(triangle_image, 270)
    rotated_triangle_rect = rotated_triangle.get_rect(center=triangle_rect.center)

    # Disegna l'immagine del triangolo ruotata
    screen.blit(rotated_triangle, rotated_triangle_rect)


# 200 è il dialogo di altezza
def dialogue_box(game, txt_path, erase_all_screen: bool):
    # Impostazioni dello schermo
    screen_width = game.screen_width
    screen_height = game.screen_height
    screen = game.screen
    # Colori
    white = (255, 255, 255)
    black = (0, 0, 0)
    # Carica il testo da un file di testo
    with open(txt_path, "r") as file:
        dialogue_text = file.read()

    dialogue_lines = split_text(dialogue_text, 30)  # 50 è la lunghezza massima della riga

    # Impostazioni per lo scorrimento del testo
    current_line_index = 0
    lines_per_box = 2  # Quante righe di testo mostrare in un box

    # Caricamento del font personalizzato
    font_path = "resources/Fonts/pkmn rbygsc.ttf"  # Sostituisci con il percorso del tuo file di font
    font = pygame.font.Font(font_path, 36)

    # Caricamento dell'immagine del triangolo
    triangle_image = pygame.image.load("resources/images/Icons/select.PNG")
    original_triangle_rect = triangle_image.get_rect()
    triangle_rect = original_triangle_rect.copy()
    triangle_rect.bottomright = (screen_width - 10, screen_height - 50)  # Posiziona in basso a destra

    triangle_y_offset = 0
    triangle_movement_speed = 0.3

    clock = pygame.time.Clock()
    running = True
    # Pulisci lo schermo riempiendolo di bianco se richiesto
    if erase_all_screen:
        screen.fill(white)
    # Clear only the dialog box area by drawing a white rectangle
    dialog_box_rect = pygame.Rect(0, screen_height - 200, screen_width, 200)
    pygame.draw.rect(screen, white, dialog_box_rect)
    pygame.display.flip()
    # Disegna il box del dialogo
    line_surface = font.render("", True, black)
    pygame.draw.rect(screen, black, (0, screen_height - 200, screen_width, 200), 2)
    screen.blit(line_surface, (20, screen_height - 180 + 1 * 40))
    pygame.display.flip()
    # Capture the current screen content
    screen_copy = screen.copy()
    time.sleep(1)
    print("")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    SoundManager.play_click_sound()
                    # Aggiungi il seguente codice per "pulire" il triangolo quando premi ENTER
                    screen.blit(screen_copy, (0, 0))
                    pygame.display.flip()
                    # pausa
                    time.sleep(0.5)
                    current_line_index += lines_per_box
                    if current_line_index >= len(dialogue_lines):
                        running = False

        if running:
            # Mostra il testo nel box
            for i in range(lines_per_box):
                line_index = current_line_index + i
                # Mostra il triangolo solo dopo il riempimento del testo
                if line_index >= len(dialogue_lines):
                    triangle_rect.y = screen_height - 50
                else:
                    triangle_rect.y = screen_height - 50 + triangle_y_offset
                    triangle_y_offset += triangle_movement_speed
                    if triangle_y_offset > 10 or triangle_y_offset < -10:
                        triangle_movement_speed *= -1
                    line_surface = font.render(dialogue_lines[line_index], True, black)  # le scritte
                    screen.blit(line_surface, (20, screen_height - 150 + i * 40))

            image_suspend(screen, triangle_image, triangle_rect, screen_height, triangle_y_offset,
                          triangle_movement_speed)
            pygame.display.flip()
        clock.tick(60)


# Divide il testo in righe gestibili
def split_text(text, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_width:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "

    if current_line:
        lines.append(current_line)
    return lines

# dialogue_box("resources/Dialogue/Story_01_00.txt", True)
