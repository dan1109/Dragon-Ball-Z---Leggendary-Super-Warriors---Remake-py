import pygame
import sys


def play_sound(music_path):
    pygame.mixer.Sound(music_path).play()


class SoundManager:
    MENU_SOUND = "resources/sounds/03 BGM #03.wav"
    SCROLL_MENU_SOUND = "resources/sounds/direction.wav"
    A_SOUND = "resources/sounds/A.wav"

    @staticmethod
    def play_menu_sound():
        pygame.mixer.init()
        pygame.mixer.Sound(SoundManager.MENU_SOUND).play(-1)  # -1 indica il loop infinito

    @staticmethod
    def play_scroll_sound():
        pygame.mixer.init()
        pygame.mixer.Sound(SoundManager.SCROLL_MENU_SOUND).play()

    @staticmethod
    def play_click_sound():
        pygame.mixer.init()
        pygame.mixer.Sound(SoundManager.A_SOUND).play()

    @staticmethod
    def load_sound(music_path):
        pygame.mixer.init()
        return pygame.mixer.music.load(music_path)

    @staticmethod
    def stop_music(music_path):
        pygame.mixer.Sound(music_path).stop()

    @staticmethod
    def stop_current_music():
        pygame.mixer.pause()

    @staticmethod
    def play_sound(music_path, is_infinite: bool):
        if is_infinite:
            pygame.mixer.Sound(music_path).play(-1)
        else:
            pygame.mixer.Sound(music_path).play()
