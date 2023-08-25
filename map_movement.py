# 160*150 is the mini window to move. Load all maps
import random
import pygame
import sys

from main import get_cropped_image, Game


def get_sprites_kid_gohan(game):
    """
    # Posizione iniziale del pupazzo
    pupazzo_rect = pupazzo_sprites[current_direction][current_frame].get_rect()
    pupazzo_rect.center = (game.screen_width // 2, game.screen_height // 2)
    :return: sorted_pupazzo_sprites, pupazzo_rect
    """
    # Caricamento degli sprite del pupazzo
    pupazzo_sprite_sheet = get_cropped_image("resources/images/Icons/All_map_player.png", 20, 23, 33, 73)
    pupazzo_sprite_sheet = pygame.transform.scale(pupazzo_sprite_sheet, (pupazzo_sprite_sheet.get_width() * 3.5,
                                                                         pupazzo_sprite_sheet.get_height() * 2))
    # game.draw_image_on_background_slowly(pupazzo_sprite_sheet, None, 0, 0, False,
    #                                    0, 0, 0.5)
    pupazzo_width = pupazzo_sprite_sheet.get_width() / 2
    pupazzo_height = pupazzo_sprite_sheet.get_height() / 4
    pupazzo_frames_per_direction = 2
    pupazzo_sprites = []
    # Aggiorna lo schermo
    pygame.display.flip()
    # Controllo dell'ordine delle direzioni
    valid_directions = [2, 0, 3, 1]  # su, giù, sinistra, destra
    for row in range(4):  # 4 righe per le 4 direzioni
        pupazzo_direction_sprites = []
        for col in range(pupazzo_frames_per_direction):
            sprite_rect = pygame.Rect(col * pupazzo_width, row * pupazzo_height, pupazzo_width, pupazzo_height)
            pupazzo_frame = pupazzo_sprite_sheet.subsurface(sprite_rect)
            pupazzo_direction_sprites.append(pupazzo_frame)

        # Memorizza le direzioni nell'ordine corretto
        current_direction = valid_directions[row]
        pupazzo_sprites.append(pupazzo_direction_sprites)

    # Creiamo una nuova lista ordinata degli sprite
    sorted_pupazzo_sprites = [
        pupazzo_sprites[1],  # Sprite di movimento verso l'alto
        pupazzo_sprites[3],  # Sprite di movimento verso il basso
        pupazzo_sprites[0],  # Sprite di movimento verso sinistra
        pupazzo_sprites[2],  # Sprite di movimento verso destra
    ]

    pupazzo_sprites = sorted_pupazzo_sprites
    # Inizializzazione delle variabili per l'animazione del pupazzo
    current_direction = 0  # 0: giù, 1: destra, 2: su, 3: sinistra
    current_frame = 0

    # Posizione iniziale del pupazzo
    pupazzo_rect = pupazzo_sprites[current_direction][current_frame].get_rect()
    pupazzo_rect.center = (game.screen_width // 2, game.screen_height // 2)
    return sorted_pupazzo_sprites, pupazzo_rect


def get_matrix_movementes_map(game, map_surface):
    """
    :param game:
    :param map_surface:
    :return: collision_matrix
    """
    # map_surface = game.draw_image_on_background_slowly(map_surface, None, 0, 0, True,
    #                                                   game.screen_width, game.screen_height, 0.5)
    # Creazione del livello di collisione (matrice di collisione 800x600)
    # Dimensioni delle celle per la matrice di collisione
    collision_matrix = [[0] * game.screen_width for _ in range(game.screen_height)]
    collision_matrix[game.screen_height - 1] = [1] * game.screen_width
    collision_matrix[game.screen_height - 2] = [1] * game.screen_width
    collision_matrix[game.screen_height - 3] = [1] * game.screen_width
    collision_matrix[game.screen_height - 4] = [1] * game.screen_width
    # Visualizza la matrice di collisione
    for y in range(len(collision_matrix)):
        for x in range(len(collision_matrix[0])):
            if collision_matrix[y][x] == 1:
                pygame.draw.rect(game.screen, (255, 0, 0),
                                 pygame.Rect(x, y, 1, 1))

    # Aggiornamento dello schermo
    pygame.display.flip()
    return collision_matrix


def load_background_sunny_land_map(game, background):
    if game is None:
        game = Game()
    # Caricamento degli sfondi
    cell_width = 1  # Sostituisci 'num_columns' con il numero di colonne della matrice
    cell_height = 1  # Sostituisci 'num_rows' con il numero di righe della matrice
    collision_matrix = get_matrix_movementes_map(game, background)
    pupazzo_speed = 5
    pupazzo_direction = [0, 0]
    frame_counter = 0
    animation_speed = 10
    pupazzo_frames_per_direction = 2
    sorted_pupazzo_sprites, pupazzo_rect = get_sprites_kid_gohan(game)
    pupazzo_sprites = sorted_pupazzo_sprites
    # Inizializzazione delle variabili per l'animazione del pupazzo
    current_direction = 0  # 0: giù, 1: destra, 2: su, 3: sinistra
    current_frame = 0
    # Posizione iniziale del pupazzo
    pupazzo_rect = pupazzo_sprites[current_direction][current_frame].get_rect()
    pupazzo_rect.center = (game.screen_width // 2, game.screen_height // 2)
    # Variabili per il controllo del movimento
    moving_up = False
    moving_down = False
    moving_left = False
    moving_right = False
    # Variabili per il controllo del tempo
    last_time = pygame.time.get_ticks()
    time_per_frame = 1000 / 60  # Tempo in millisecondi per ogni frame
    clock = pygame.time.Clock()
    is_first_time: bool = True
    first_time = game.screen.copy()  # Copia la superficie corrente
    # Ciclo di gioco
    while True:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        last_time = current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    moving_up = True
                elif event.key == pygame.K_DOWN:
                    moving_down = True
                elif event.key == pygame.K_LEFT:
                    moving_left = True
                elif event.key == pygame.K_RIGHT:
                    moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    moving_up = False
                elif event.key == pygame.K_DOWN:
                    moving_down = False
                elif event.key == pygame.K_LEFT:
                    moving_left = False
                elif event.key == pygame.K_RIGHT:
                    moving_right = False

        # Aggiornamento dell'animazione
        frame_counter += 1
        if frame_counter >= animation_speed:
            frame_counter = 0
            current_frame = (current_frame + 1) % pupazzo_frames_per_direction

        # Calcolo della velocità in base al tempo trascorso
        pupazzo_speed_x = 0
        pupazzo_speed_y = 0
        if moving_up:
            pupazzo_speed_y = -pupazzo_speed
            current_direction = 2  # Sprite di movimento verso l'alto
        elif moving_down:
            pupazzo_speed_y = pupazzo_speed
            current_direction = 0  # Sprite di movimento verso il basso
        if moving_left:
            pupazzo_speed_x = -pupazzo_speed
            current_direction = 3  # Sprite di movimento verso sinistra
        elif moving_right:
            pupazzo_speed_x = pupazzo_speed
            current_direction = 1  # Sprite di movimento verso destra

        # Aggiornamento della posizione del pupazzo in base alla velocità e al tempo
        new_x = pupazzo_rect.x + pupazzo_speed_x * (delta_time / time_per_frame)
        new_y = pupazzo_rect.y + pupazzo_speed_y * (delta_time / time_per_frame)

        # Verifica delle collisioni solo se la nuova posizione è all'interno dei limiti dello schermo
        if 0 <= new_x < game.screen_width - pupazzo_rect.width and 0 <= new_y < game.screen_height - pupazzo_rect.height:
            # Aggiornamento della posizione del pupazzo
            top_left_cell = (int(new_x // cell_width), int(new_y // cell_height))
            top_right_cell = (int((new_x + pupazzo_rect.width) // cell_width), int(new_y // cell_height))
            bottom_left_cell = (int(new_x // cell_width), int((new_y + pupazzo_rect.height) // cell_height))
            bottom_right_cell = (
                int((new_x + pupazzo_rect.width) // cell_width), int((new_y + pupazzo_rect.height) // cell_height))

            # Controlla se ci sono ostacoli nelle celle coinvolte
            if (
                    collision_matrix[top_left_cell[1]][top_left_cell[0]] == 0 and
                    collision_matrix[top_right_cell[1]][top_right_cell[0]] == 0 and
                    collision_matrix[bottom_left_cell[1]][bottom_left_cell[0]] == 0 and
                    collision_matrix[bottom_right_cell[1]][bottom_right_cell[0]] == 0
            ):
                pupazzo_rect.x = new_x
                pupazzo_rect.y = new_y

        # Limita la posizione del pupazzo all'interno della finestra
        pupazzo_rect.x = max(0, min(pupazzo_rect.x, game.screen_width - pupazzo_rect.width))
        pupazzo_rect.y = max(0, min(pupazzo_rect.y, game.screen_height - pupazzo_rect.height))

        if is_first_time:
            is_first_time = False
            game.screen.blit(first_time, (0, 0))
            pygame.display.flip()
        else:
            # Pulizia dello schermo
            game.screen.blit(background, (0, 0))
            game.screen.blit(pupazzo_sprites[current_direction][current_frame], pupazzo_rect)
            # Aggiornamento dello schermo
            pygame.display.flip()

        # Limita il framerate
        clock.tick(60)
