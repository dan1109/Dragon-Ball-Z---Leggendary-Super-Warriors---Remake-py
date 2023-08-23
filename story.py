import pygame

import dialogue_system
from dialogue_system import screen_white_and_empty_box
from sound_manager import SoundManager


def story_01(game):
    screen_white_and_empty_box(game)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_blue.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 1)
    dialogue_system.dialogue_box(game, "resources/Dialogue/Story_01/Story_01_00.txt", False)
    dialogue_system.screen_white_and_empty_box(game)
    SoundManager.play_sound("resources/sounds/01 BGM #01.wav", True)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/Dragon Balls.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 1)
    dialogue_system.dialogue_box(game, "resources/Dialogue/Story_01/Story_01_01.txt", False)
    screen_white_and_empty_box(game)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_01_01.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 1)
    dialogue_system.dialogue_box(game, "resources/Dialogue/Story_01/Story_01_02.txt", False)
    screen_white_and_empty_box(game)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_blue.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 1)
    SoundManager.stop_current_music()
    dialogue_system.dialogue_box(game, "resources/Dialogue/Story_01/Story_01_03.txt", False)
    dialogue_system.box_face(game, 22, 34, True, None)  # radittz face
    SoundManager.play_sound("resources/sounds/11 BGM #07.wav", True)
    dialogue_system.dialogue_box(game, "resources/Dialogue/Story_01/Story_01_04.txt", False)
    game.draw_image_on_background_slowly(None, "resources/images/Icons/story_blue.png", 0, 0, True,
                                         game.screen_width, game.screen_height - 200, 0.5)
    dialogue_system.box_face(game, 22, 34, False, True)  # radittz face
    dialogue_system.box_face(game, 64, 34, False, False)  # goku face
    dialogue_system.dialogue_box(game, "resources/Dialogue/Story_01/Story_01_05.txt", False)
