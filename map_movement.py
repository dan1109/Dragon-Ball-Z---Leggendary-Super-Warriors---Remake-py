# 160*150 is the mini window to move. Load all maps
import random

import numpy as np
import pygame
import sys

from main import get_cropped_image, Game


def flip_collision_matrix(game, collision_matrix):
    """
    debug purpose
    :param game:
    :param collision_matrix:
    :return:
    """
    # Visualizza la matrice di collisione
    for y in range(len(collision_matrix)):
        for x in range(len(collision_matrix[0])):
            if collision_matrix[y][x] == 1:
                pygame.draw.rect(game.screen, (255, 0, 0),
                                 pygame.Rect(x, y, 1, 1))

    # Aggiornamento dello schermo
    pygame.display.flip()


def add_obstacles_to_collision_matrix(collision_matrix, background_image: pygame.Surface,
                                      obstacle_image: pygame.Surface):
    obstacle_width = obstacle_image.get_width()
    obstacle_height = obstacle_image.get_height()

    background_array = pygame.surfarray.array3d(background_image)
    obstacle_array = pygame.surfarray.array3d(obstacle_image)

    for y in range(background_image.get_height() - obstacle_height + 1):
        for x in range(background_image.get_width() - obstacle_width + 1):
            cropped_area = pygame.Rect(x, y, obstacle_width, obstacle_height)
            cropped_surface = background_image.subsurface(cropped_area)
            cropped_array = pygame.surfarray.array3d(cropped_surface)

            if np.array_equal(cropped_array, obstacle_array):
                for i in range(obstacle_height):
                    for j in range(obstacle_width):
                        if 0 <= y + i < len(collision_matrix) and 0 <= x + j < len(collision_matrix[0]):
                            if obstacle_image.get_at((j, i)) != (0, 0, 0, 0):
                                collision_matrix[y + i][x + j] = 1
    return collision_matrix


def common_parts_matrix(common_matrix, image1: pygame.Surface, image2: pygame.Surface):
    width = min(image1.get_width(), image2.get_width())
    height = min(image1.get_height(), image2.get_height())

    array1 = pygame.surfarray.array3d(image1.subsurface(pygame.Rect(0, 0, width, height)))
    array2 = pygame.surfarray.array3d(image2.subsurface(pygame.Rect(0, 0, width, height)))

    common_matrix = np.all(array1 == array2, axis=2).astype(int)

    return common_matrix.tolist()


def upscale_matrix(collision_matrix, map_surface: pygame.Surface, background: pygame.Surface):
    """
    :param collision_matrix: Matrice di collisioni originale
    :param map_surface: Superficie della mappa
    :param background: Superficie dello sfondo
    :return: collision_matrix_game
    """
    # Fattori di scala
    scale_x = background.get_width() / map_surface.get_width()
    scale_y = background.get_height() / map_surface.get_height()

    collision_matrix_game = []

    for y in range(background.get_height()):
        collision_row = []
        for x in range(background.get_width()):
            # Calcola gli indici sulla matrice originale in base alle coordinate nell'immagine ingrandita
            original_y = int(y / scale_y)
            original_x = int(x / scale_x)

            # Accedi alla matrice di collisioni originale con gli indici calcolati
            if 0 <= original_y < len(collision_matrix) and 0 <= original_x < len(collision_matrix[0]):
                collision_value = collision_matrix[original_y][original_x]
            else:
                collision_value = 0

            collision_row.append(collision_value)
        collision_matrix_game.append(collision_row)

    return collision_matrix_game


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
    pupazzo_rect.center = (game.screen_width // 3, game.screen_height // 3)
    return sorted_pupazzo_sprites, pupazzo_rect


def load_background_sunny_land_map(game, background):
    if game is None:
        game = Game()
    # Caricamento degli sfondi
    stone_obstacle = get_cropped_image("resources/images/Icons/All_maps obstacles.png", 18, 13, 255, 305)
    # Crea una matrice di collisioni vuota con la mappa originale
    collision_matrix = [[0 for _ in range(background.get_width())] for _ in
                        range(background.get_height())]
    # tutte le collisioni in map
    # collision_matrix = add_obstacles_to_collision_matrix(collision_matrix, background, stone_obstacle)
    collision_matrix = common_parts_matrix(collision_matrix, background, stone_obstacle)
    collision_matrix = upscale_matrix(collision_matrix, background, game.screen)
    is_first_time: bool = True
    sorted_pupazzo_sprites, pupazzo_rect = get_sprites_kid_gohan(game)
    background = game.draw_image_on_background_slowly(background, None, 0, 0, True,
                                                      game.screen_width, game.screen_height, 0)
    pupazzo_frames_per_direction = 2
    pupazzo_sprites = sorted_pupazzo_sprites
    # Inizializzazione delle variabili per l'animazione del pupazzo
    current_direction = 0  # 0: giù, 1: destra, 2: su, 3: sinistra
    current_frame = 0
    game.screen.blit(pupazzo_sprites[current_direction][current_frame], pupazzo_rect)
    first_time = game.screen.copy()  # Copia la superficie corrente
    game.screen.blit(first_time, (0, 0))
    # Aggiornamento dello schermo
    pygame.display.flip()
    flip_collision_matrix(game, collision_matrix)
    # Aggiornamento dello schermo
    pygame.display.flip()
    cell_width = 1  # Sostituisci 'num_columns' con il numero di colonne della matrice
    cell_height = 1  # Sostituisci 'num_rows' con il numero di righe della matrice
    pupazzo_speed = 5
    pupazzo_direction = [0, 0]
    frame_counter = 0
    animation_speed = 10
    # Variabili per il controllo del movimento
    moving_up = False
    moving_down = False
    moving_left = False
    moving_right = False
    # Variabili per il controllo del tempo
    last_time = pygame.time.get_ticks()
    time_per_frame = 1000 / 60  # Tempo in millisecondi per ogni frame
    clock = pygame.time.Clock()
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
