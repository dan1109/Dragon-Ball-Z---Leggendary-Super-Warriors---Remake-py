# 160*150 is the mini window to move. Load all maps
import random

import numpy as np
import pygame
import sys

from main import get_cropped_image, Game
from test_obstacles import is_collision

# Costanti
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CHARACTER_WIDTH, CHARACTER_HEIGHT = 20, 20
CHARACTER_SPEED = 5
ACCELERATION = 0.5

# Posizione del secondo personaggio fisso
SECOND_CHARACTER_X, SECOND_CHARACTER_Y = 700, 80
SECOND_CHARACTER_WIDTH, SECOND_CHARACTER_HEIGHT = 20, 20


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


def see_img(pupazzo_sprite_sheet):
    schermo = pygame.display.set_mode((800, 600))
    schermo.blit(pupazzo_sprite_sheet, (0, 0))
    # Aggiorna lo schermo
    pygame.display.flip()


def get_sprites_character(start_x: int, start_y: int, double_frames: bool):
    """
    # Posizione iniziale del pupazzo
    pupazzo_rect = pupazzo_sprites[current_direction][current_frame].get_rect()
    pupazzo_rect.center = (game.screen_width // 2, game.screen_height // 2)
    :return: sorted_pupazzo_sprites, pupazzo_rect
    """
    # Caricamento degli sprite del pupazzo 30+73
    pupazzo_sprite_sheet = get_cropped_image("resources/images/Icons/All_map_player.png", start_x, start_y,
                                             30, 75)
    see_img(pupazzo_sprite_sheet)
    # Scala lo sprite sheet
    scale_factor = 2 if double_frames else 1  # Imposta il fattore di scala corretto
    pupazzo_sprite_sheet = pygame.transform.scale(pupazzo_sprite_sheet,
                                                  (pupazzo_sprite_sheet.get_width() * scale_factor,
                                                   pupazzo_sprite_sheet.get_height() * 1.2))

    pupazzo_width = pupazzo_sprite_sheet.get_width() // (2 if double_frames else 1)
    pupazzo_height = pupazzo_sprite_sheet.get_height() // 4

    pupazzo_frames_per_direction = 2 if double_frames else 1  # Imposta il numero corretto di frame per direzione

    pupazzo_sprites = []
    # Aggiorna lo schermo
    # pygame.display.flip()
    # Controllo dell'ordine delle direzioni
    valid_directions = [2, 0, 3, 1]  # su, giù, sinistra, destra
    for row in range(4):  # 4 righe per le 4 direzioni
        pupazzo_direction_sprites = []
        for col in range(pupazzo_frames_per_direction):
            sprite_rect = pygame.Rect(col * pupazzo_width, row * pupazzo_height, pupazzo_width, pupazzo_height)
            pupazzo_frame = pupazzo_sprite_sheet.subsurface(sprite_rect)
            pupazzo_direction_sprites.append(pupazzo_frame)
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
    pupazzo_rect = pupazzo_sprites[current_direction][current_frame].get_rect()
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
    sorted_pupazzo_sprites, pupazzo_rect = get_sprites_character(game)
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


def new_load_background_sunny_land_map(game, background, obstacles):
    if game is None:
        game = Game()
    # Caricamento degli sfondi
    screen = game.screen

    # Ridimensiona le immagini per adattarle alla finestra
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    obstacles = pygame.transform.scale(obstacles, (SCREEN_WIDTH, SCREEN_HEIGHT))

    character_x, character_y = 100, 100
    sorted_pupazzo_sprites, character_rect = get_sprites_character(20, 23, True)
    second_character_sprites, second_character_rect = get_sprites_character(69, 23, True)
    # Posizione iniziale del second_character_rect
    second_character_rect.topleft = (character_x + 500, character_y - 50)
    greeting_displayed = False  # Per evitare di visualizzare il saluto "Hello" più di una volta

    pupazzo_frames_per_direction = 2
    pupazzo_sprites = sorted_pupazzo_sprites
    # Inizializzazione delle variabili per l'animazione del pupazzo
    current_direction = 0  # 0: giù, 1: destra, 2: su, 3: sinistra
    second_character_direction = 0
    current_frame = 0
    game.screen.blit(pupazzo_sprites[current_direction][current_frame], character_rect)
    first_time = game.screen.copy()  # Copia la superficie corrente
    game.screen.blit(first_time, (0, 0))
    # Aggiornamento dello schermo
    pygame.display.flip()
    # Aggiornamento dello schermo
    pygame.display.flip()
    pupazzo_speed = 5
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
    running = True
    # Ciclo di gioco
    while running:
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
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
        # quale movimento ha fatto?
        frame_counter += 1
        if frame_counter >= animation_speed:
            frame_counter = 0
            current_frame = (current_frame + 1) % pupazzo_frames_per_direction
        if moving_up:
            current_direction = 2  # Sprite di movimento verso l'alto
        elif moving_down:
            current_direction = 0  # Sprite di movimento verso il basso
        if moving_left:
            current_direction = 3  # Sprite di movimento verso sinistra
        elif moving_right:
            current_direction = 1  # Sprite di movimento verso destra
        if keys[pygame.K_LEFT]:
            character_speed_x = -CHARACTER_SPEED
        elif keys[pygame.K_RIGHT]:
            character_speed_x = CHARACTER_SPEED
        else:
            character_speed_x = 0
        if keys[pygame.K_UP]:
            character_speed_y = -CHARACTER_SPEED
        elif keys[pygame.K_DOWN]:
            character_speed_y = CHARACTER_SPEED
        else:
            character_speed_y = 0
        character_x += character_speed_x
        character_y += character_speed_y
        character_rect.topleft = (character_x, character_y)
        if is_collision(character_rect, background, obstacles) or character_rect.colliderect(second_character_rect):
            character_x -= character_speed_x
            character_y -= character_speed_y
            if keys[pygame.K_a] and character_rect.colliderect(second_character_rect):
                if not greeting_displayed:
                    print("Hello")
                    greeting_displayed = True
            else:
                greeting_displayed = False
        # -- aggiornamento dell'immagine
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))  # Disegna l'immagine di sfondo
        screen.blit(obstacles, (0, 0))  # Disegna l'immagine degli ostacoli
        game.screen.blit(pupazzo_sprites[current_direction][current_frame], character_rect)  # Disegna il primo pers.
        # Disegna il secondo personaggio (ostacolo)
        game.screen.blit(second_character_sprites[second_character_direction][current_frame], second_character_rect)
        pygame.display.flip()
        clock.tick(60)
        # -- aggiornamento dell'immagine
