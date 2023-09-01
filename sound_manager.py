import pygame


def initialize_if_not_mixer():
    if not pygame.mixer.get_init():
        pygame.mixer.init()


def play_sound(music_path):
    pygame.mixer.Sound(music_path).play()


class SoundManager:
    MENU_SOUND = "resources/sounds/03 BGM #03.wav"
    SCROLL_MENU_SOUND = "resources/sounds/direction.wav"
    A_SOUND = "resources/sounds/A.wav"

    @staticmethod
    def play_menu_sound():
        initialize_if_not_mixer()
        pygame.mixer.Sound(SoundManager.MENU_SOUND).play(-1)  # -1 indica il loop infinito

    @staticmethod
    def play_scroll_sound():
        initialize_if_not_mixer()
        pygame.mixer.Sound(SoundManager.SCROLL_MENU_SOUND).play()

    @staticmethod
    def play_click_sound():
        initialize_if_not_mixer()
        pygame.mixer.Sound(SoundManager.A_SOUND).play()

    @staticmethod
    def load_sound(music_path):
        initialize_if_not_mixer()
        return pygame.mixer.music.load(music_path)

    @staticmethod
    def stop_music(music_path):
        pygame.mixer.Sound(music_path).stop()

    @staticmethod
    def stop_current_music():
        pygame.mixer.pause()
        pygame.mixer.stop()  # ferma i canali

    @staticmethod
    def play_sound(music_path, is_infinite: bool):
        initialize_if_not_mixer()
        volume_level = 0.2
        pygame.mixer.set_reserved(1)  # Imposta un canale riservato
        music = pygame.mixer.Sound(music_path)  # Crea l'oggetto Sound
        music.set_volume(volume_level)  # Imposta il volume
        if is_infinite:
            music.play(loops=-1)  # Riproduci in loop infinito
        else:
            music.play()  # Riproduci una sola volta

    @staticmethod
    def play_sound_volume(music_path, volume_level, is_infinite):
        initialize_if_not_mixer()
        pygame.mixer.set_reserved(1)  # Imposta un canale riservato
        music = pygame.mixer.Sound(music_path)  # Crea l'oggetto Sound
        music.set_volume(volume_level)  # Imposta il volume
        if is_infinite:
            music.play(loops=-1)  # Riproduci in loop infinito
        else:
            music.play()  # Riproduci una sola volta

    @staticmethod
    def get_audio_duration(music_path):
        initialize_if_not_mixer()
        audio = pygame.mixer.Sound(music_path)
        duration_in_seconds = audio.get_length()
        return duration_in_seconds
