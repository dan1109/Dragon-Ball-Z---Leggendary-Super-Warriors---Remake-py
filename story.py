import pygame

import dialogue_system
import map_movement
from dialogue_system import screen_white_and_empty_box
from main import Game, get_cropped_image
from sound_manager import SoundManager


def temp_test(game):
    if game is None:
        game = Game()
    # map
    mini_background = get_cropped_image("resources/images/Icons/All_maps.png", 18, 13, 255, 305)
    pupazzo_sprites, pupazzo_rect = map_movement.get_sprites_character(20, 23, True)
    # Posizione iniziale del pupazzo
    pupazzo_rect.topleft = (100, 100)
    # Inizializzazione delle variabili per l'animazione del pupazzo
    current_direction = 0  # 0: giù, 1: destra, 2: su, 3: sinistra
    current_frame = 0
    screen_white_and_empty_box(game)
    SoundManager.play_sound_volume("resources/sounds/17 BGM #13.wav", 0.2, True)
    game.draw_image_on_background_slowly(mini_background, None, 0, 0, True,
                                         game.screen_width, game.screen_height, 0.5)
    obstacles = get_cropped_image("resources/images/Icons/All_maps obstacles.png", 18, 13, 255, 305)
    game.screen.blit(pupazzo_sprites[current_direction][current_frame], pupazzo_rect)
    # Aggiornamento dello schermo
    pygame.display.flip()
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_24.txt", "Gohan", False)
    # map_movement.load_background_sunny_land_map(game, mini_background)
    map_movement.new_load_background_sunny_land_map(game, mini_background, obstacles)
    print("")


def story_01(game):
    if game is None:
        game = Game()
    raditz_goku_img = get_cropped_image("resources/images/Icons/All_story.png", 498, 11, 160, 95)
    sun_mountain = get_cropped_image("resources/images/Icons/All_story.png", 661, 11, 160, 95)
    game.draw_image_on_background_slowly(None, "resources/Dialogue/dialogue_sx.png", 0, 0, True,
                                         0, 0, 0.5)
    screen_white_and_empty_box(game)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_blue.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 1)
    dialogue_system.narration_box(game, "resources/Dialogue/Story_01/Story_01_00.txt", False)
    dialogue_system.screen_white_and_empty_box(game)
    SoundManager.play_sound("resources/sounds/01 BGM #01.wav", True)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/Dragon Balls.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 1)
    dialogue_system.narration_box(game, "resources/Dialogue/Story_01/Story_01_01.txt", False)
    screen_white_and_empty_box(game)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_01_01.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 1)
    dialogue_system.narration_box(game, "resources/Dialogue/Story_01/Story_01_02.txt", False)
    screen_white_and_empty_box(game)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_blue.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 1)
    SoundManager.stop_current_music()
    dialogue_system.narration_box(game, "resources/Dialogue/Story_01/Story_01_03.txt", False)
    dialogue_system.box_face(game, 22, 33, True, None)  # radittz face
    SoundManager.play_sound("resources/sounds/11 BGM #07.wav", True)
    dialogue_system.narration_box(game, "resources/Dialogue/Story_01/Story_01_04.txt", False)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_blue.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 0.5)
    dialogue_system.box_face(game, 22, 33, False, False)  # radittz face
    dialogue_system.box_face(game, 64, 33, False, True)  # goku face
    dialogue_system.narration_box(game, "resources/Dialogue/Story_01/Story_01_05.txt", False)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_blue.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 0.5)
    screen_white_and_empty_box(game)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_blue.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 0.5)
    SoundManager.stop_current_music()
    SoundManager.play_sound("resources/sounds/20 BGM #16.wav", True)
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_06.txt", "???", False)
    dialogue_system.box_face(game, 106, 33, True, None)  # gohan face
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_07.txt", "Gohan", False)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_blue.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 0.5)
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_08.txt", "???", False)
    dialogue_system.box_face(game, 106, 33, True, None)  # gohan face
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_09.txt", "Gohan", False)
    SoundManager.stop_current_music()
    screen_white_and_empty_box(game)
    SoundManager.play_sound_volume("resources/sounds/loose_shot.wav", 1.0, False)
    game.draw_image_on_background_slowly(raditz_goku_img, None, 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 0.5)
    dialogue_system.dialogue_dx(game, "resources/Dialogue/Story_01/Story_01_10.txt", "Goku", False)
    dialogue_system.box_face(game, 148, 33, True, None)  # gohan face angry
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_11.txt", "Gohan", False)
    dialogue_system.chapter(game, 1)
    game.draw_image_on_background_slowly(sun_mountain, None, 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 0.5)
    dialogue_system.box_face(game, 106, 33, False, True)  # gohan face
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_12.txt", "Gohan", False)
    dialogue_system.box_face(game, 190, 33, False, False)  # piccolo face
    dialogue_system.dialogue_dx(game, "resources/Dialogue/Story_01/Story_01_13.txt", "Piccolo", False)
    dialogue_system.box_face(game, 106, 33, False, True)  # gohan face
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_14.txt", "Gohan", False)
    game.draw_image_on_background_slowly(sun_mountain, None, 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 0.5)
    SoundManager.play_sound_volume("resources/sounds/12 BGM #08.wav", 1.0, True)
    dialogue_system.narration_box(game, "resources/Dialogue/Story_01/Story_01_15.txt", False)
    dialogue_system.box_face(game, 190, 33, False, False)  # piccolo face
    dialogue_system.dialogue_dx(game, "resources/Dialogue/Story_01/Story_01_16.txt", "Piccolo", False)
    dialogue_system.box_face(game, 106, 33, False, True)  # gohan face
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_17.txt", "Gohan", False)
    dialogue_system.box_face(game, 190, 33, False, False)  # piccolo face
    dialogue_system.dialogue_dx(game, "resources/Dialogue/Story_01/Story_01_18.txt", "Piccolo", False)
    dialogue_system.box_face(game, 106, 33, False, True)  # gohan face
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_19.txt", "Gohan", False)
    dialogue_system.box_face(game, 190, 33, False, False)  # piccolo face
    dialogue_system.dialogue_dx(game, "resources/Dialogue/Story_01/Story_01_20.txt", "Piccolo", False)
    dialogue_system.box_face(game, 232, 33, False, True)  # gohan face happy
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_21.txt", "Gohan", False)
    dialogue_system.box_face(game, 274, 33, False, True)  # gohan face ouch
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_22.txt", "Gohan", False)
    dialogue_system.box_face(game, 190, 33, False, False)  # piccolo face
    dialogue_system.dialogue_dx(game, "resources/Dialogue/Story_01/Story_01_23.txt", "Piccolo", False)
    dialogue_system.game_transiction(game)
    # map
    mini_background = get_cropped_image("resources/images/Icons/All_maps.png", 18, 13, 255, 305)
    pupazzo_sprites, pupazzo_rect = map_movement.get_sprites_character(20, 23, True)
    # Posizione iniziale del pupazzo
    pupazzo_rect.topleft = (100, 100)
    # Inizializzazione delle variabili per l'animazione del pupazzo
    current_direction = 0  # 0: giù, 1: destra, 2: su, 3: sinistra
    current_frame = 0
    screen_white_and_empty_box(game)
    SoundManager.stop_current_music()
    SoundManager.play_sound_volume("resources/sounds/17 BGM #13.wav", 0.2, True)
    game.draw_image_on_background_slowly(mini_background, None, 0, 0, True,
                                         game.screen_width, game.screen_height, 0.5)
    obstacles = get_cropped_image("resources/images/Icons/All_maps obstacles.png", 18, 13, 255, 305)
    game.screen.blit(pupazzo_sprites[current_direction][current_frame], pupazzo_rect)
    # Aggiornamento dello schermo
    pygame.display.flip()
    dialogue_system.dialogue_sx(game, "resources/Dialogue/Story_01/Story_01_24.txt", "Gohan", False)
    # map_movement.load_background_sunny_land_map(game, mini_background)
    map_movement.new_load_background_sunny_land_map(game, mini_background, obstacles)
    print("")


if __name__ == "__main__":
    game = Game()
    temp_test(game)
    # story_01(game)
