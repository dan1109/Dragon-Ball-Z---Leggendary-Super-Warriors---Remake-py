import pygame
import sys


class SoundManager:
    pygame.mixer.init()
    MENU_SOUND: pygame.mixer.Sound = pygame.mixer.Sound("resources/sounds/03 BGM #03.wav")
    SCROLL_MENU_SOUND: pygame.mixer.Sound = pygame.mixer.Sound("resources/sounds/direction.wav")
    A_SOUND: pygame.mixer.Sound = pygame.mixer.Sound("resources/sounds/A.wav")

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.init(frequency=44100)

    @staticmethod
    def play_menu_sound():
        SoundManager.MENU_SOUND.play()

    @staticmethod
    def play_scroll_sound():
        SoundManager.SCROLL_MENU_SOUND.play()

    @staticmethod
    def play_click_sound():
        SoundManager.A_SOUND.play()

    @staticmethod
    def load_sound(music_path):
        return pygame.mixer.music.load(music_path)
