# 160*150 is the mini window to move. Load all maps

import numpy as np
import pygame
import sys

import dialogue_system
import messages
from Character_map import CharacterMap
from main import get_cropped_image, Game
from sound_manager import SoundManager
from test_obstacles import is_collision

# Costanti
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CHARACTER_WIDTH, CHARACTER_HEIGHT = 20, 20

# Posizione del secondo personaggio fisso
SECOND_CHARACTER_X, SECOND_CHARACTER_Y = 700, 80
SECOND_CHARACTER_WIDTH, SECOND_CHARACTER_HEIGHT = 20, 20


def update_map(game, screen, obstacles, background, arr_characters):
    """
    Update the game map by clearing the screen, drawing the background, obstacles,
    and characters, and refreshing the display.

    :param game: The game object
    :param screen: The game screen surface
    :param obstacles: The image representing obstacles on the map
    :param background: The background image of the game map
    :param arr_characters: List of character objects to be drawn on the map
    """
    # -- aggiornamento dell'immagine a prescindere dalla scelta degli fi
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))  # Disegna l'immagine di sfondo
    screen.blit(obstacles, (0, 0))  # Disegna l'immagine degli ostacoli
    for character in arr_characters:
        character.blit(game)
    pygame.display.flip()


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
    # 30 e 75 sono le grandezz estandard degli sprites
    pupazzo_sprite_sheet = get_cropped_image("resources/images/Icons/All_map_player.png", start_x, start_y,
                                             30, 75)
    # see_img(pupazzo_sprite_sheet) # only for testing
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


def draw_visible_map_portion(screen, background, background_x, window_width, window_height):
    """
    Draws only the visible portion of the map on the screen.

    Args:
        screen (pygame.Surface): The surface to draw the map on.
        background (pygame.Surface or str or None): Either a Pygame Surface object representing
            the complete background image, a file path to the background image, or None.
            If None, no background is drawn.
        background_x (int): The X-coordinate of the background to start drawing from.
        window_width (int): Width of the viewing window.
        window_height (int): Height of the viewing window.

    Raises:
        ValueError: If `background` is not a valid Pygame Surface, a valid file path, or None.
    """
    if background is not None:
        if isinstance(background, pygame.Surface):
            background_image = background
        elif isinstance(background, str):
            try:
                background_image = pygame.image.load(background).convert()
            except pygame.error:
                raise ValueError("Invalid file path provided for background image.")
        else:
            raise ValueError("Invalid background argument. Please provide a Pygame Surface, a file path, or None.")

        screen.blit(background_image, (0, 0), (background_x, 0, window_width, window_height))


def rendering_img(img):
    """
    Load and convert an image to an optimal format for rendering in Pygame. This can improve game performance,
    as the image will be stored in a format more suitable for on-screen rendering. Pygame supports different color
    modes for images, such as "RGB" and "RGBA." When you use .convert(), Pygame will attempt to convert the image to
    the most appropriate color format for your display, reducing the need for costly format conversions during rendering
    and improving overall performance.
    Args:
        img (str or pygame.Surface): Either a file path to the image or a Pygame Surface object representing the image.
    Returns:
        pygame.Surface: The loaded and converted Pygame image.
    Raises:
        ValueError: If `img` is not a valid Pygame Surface, a valid file path, or None.
    """
    if img is not None:
        if isinstance(img, pygame.Surface):
            return img.convert()
        elif isinstance(img, str):
            try:
                return pygame.image.load(img).convert()
            except pygame.error:
                raise ValueError("Invalid file path provided for background image.")
        else:
            raise ValueError("Invalid background argument. Please provide a Pygame Surface, a file path, or None.")


def map_story_01(game, background, obstacles, main_character, second_character):
    if game is None:
        game = Game()
    # Caricamento degli sfondi
    screen = game.screen
    # Caricamento immagini - Ridimensiona le immagini per adattarle alla finestra
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    obstacles = pygame.transform.scale(obstacles, (SCREEN_WIDTH, SCREEN_HEIGHT))
    greeting_displayed = False  # Per evitare di visualizzare il saluto "Hello" più di una volta
    main_character.blit(game)
    second_character.blit(game)
    # Aggiornamento dello schermo
    pygame.display.flip()
    # Variabili per il controllo del tempo
    last_time = pygame.time.get_ticks()
    time_per_frame = 1000 / 60  # Tempo in millisecondi per ogni frame
    clock = pygame.time.Clock()
    # Ciclo di gioco --
    first_time = game.screen.copy()  # Copia la superficie corrente
    game.screen.blit(first_time, (0, 0))
    pygame.display.flip()
    end_map_story_01 = False
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        pygame.event.clear()  # Clear the current RETURN
        keys = pygame.key.get_pressed()  # Gestione degli eventi e input utente
        # Gestione degli input diretti
        if keys[pygame.K_RETURN]:
            pygame.event.clear()  # Clear the current RETURN
            running = False  # exit and return call again function to interupt thread
        main_character.handle_pressed_movement(keys)
        if is_collision(main_character.rect, obstacles):
            main_character.set_previous_coordinate()
        elif main_character.rect.colliderect(second_character.rect):
            main_character.set_previous_coordinate()
            if keys[pygame.K_a] and main_character.rect.colliderect(second_character.rect):
                if not greeting_displayed:
                    greeting_displayed = True
                    second_character.direction = main_character.opposite_direction()
                    update_map(game, screen, obstacles, background, [main_character, second_character])
                    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_25.txt", "Piccolo", False)
                    dialogue_system.dialogue_box_win_card(game, "Attacco L.3",
                                                          False)  # todo a list of cards in memory
                    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_26.txt", "", False)
                    # answer = dialogue_system.dialogue_with_yes_no(game,
                    # "resources/Dialogue/Story_01/Story_01_25.txt", "Piccolo", False, True, True)

                    print("")
                    end_map_story_01 = True
            else:
                greeting_displayed = False
        update_map(game, screen, obstacles, background, [main_character, second_character])
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # -- aggiornamento dell'immagine
    choice_menu_map = game.menu("resources/images/Icons/save_state.png", "", messages.Messages.MAP_MENU_OPTION,
                                False, 300, 100)
    dialogue_system.screen_white_and_empty_box_seconds(game, 0.3)
    print("running false")
    return [game, background, obstacles, main_character, second_character, end_map_story_01]
