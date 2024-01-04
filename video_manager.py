import numpy as np
import sounddevice as sd


def play_video(video_path, width, hight):
    import pygame
    from moviepy.editor import VideoFileClip
    # Load video
    pygame.display.set_caption("Dragon Ball Z : I Leggendari Super Guerrieri")
    clip = VideoFileClip(video_path)
    clip = clip.resize((width, hight))
    clip = clip.set_audio(clip.audio.set_duration(clip.duration))

    width, height = clip.size
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # Extract audio and load it into sounddevice
    audio_clip = clip.audio
    audio_data = audio_clip.to_soundarray(fps=44100)  # Adjust FPS as needed
    audio_mono = audio_data[:, 0]  # Take one channel (mono)

    sd.play(audio_mono, 44100)  # Play audio using sounddevice

    run = True
    start_time = pygame.time.get_ticks() / 1000
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sd.stop()  # Ferma la riproduzione dell'audio alla fine

        elapsed_time = (pygame.time.get_ticks() / 1000) - start_time
        frame = clip.get_frame(elapsed_time)
        pygame_frame = pygame.surfarray.make_surface(frame)

        rotated_frame = pygame.transform.rotate(pygame_frame, 270)
        flipped_frame = pygame.transform.flip(rotated_frame, True, False)

        screen.blit(flipped_frame, (0, 0))
        pygame.display.flip()
        clock.tick(30)
        if elapsed_time > clip.duration:
            run = False
            sd.stop()  # Ferma la riproduzione dell'audio alla fine


def test():
    # Call the function to play a specific video
    video_path = "resources/videos/Dragon Ball Z - I Leggendari Super Guerrieri (ITA) - Capitolo 1.mp4"
    play_video(video_path, 800, 600)
