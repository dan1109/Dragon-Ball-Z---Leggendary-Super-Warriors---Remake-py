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
        SoundManager.stop_current_music()
        pygame.mixer.init()
        # Imposta il volume_level (0.0 - 1.0, dove 0.0 è muto e 1.0 è il massimo volume)
        volume_level = 0.2
        if is_infinite:
            pygame.mixer.Sound(music_path).play(-1).set_volume(volume_level)
        else:
            pygame.mixer.Sound(music_path).play().set_volume(volume_level)

    @staticmethod
    def play_sound_volume(music_path, volume_level, is_infinite: bool):
        SoundManager.stop_current_music()
        pygame.mixer.stop()
        pygame.mixer.init()
        # Imposta il volume_level (0.0 - 1.0, dove 0.0 è muto e 1.0 è il massimo volume)
        if is_infinite:
            pygame.mixer.Sound(music_path).play(-1).set_volume(volume_level)
        else:
            pygame.mixer.Sound(music_path).play().set_volume(volume_level)

    @staticmethod
    def get_audio_duration(music_path):
        pygame.mixer.init()
        audio = pygame.mixer.Sound(music_path)
        duration_in_seconds = audio.get_length()
        return duration_in_seconds
