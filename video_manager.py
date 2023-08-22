def play_video(video_path, width, hight):
    import pygame
    from moviepy.editor import VideoFileClip
    # Load video
    clip = VideoFileClip(video_path)
    clip = clip.resize((width, hight))
    clip = clip.set_audio(clip.audio.set_duration(clip.duration))

    width, height = clip.size
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # Load audio and play it separately
    clip.preview()

    run = True
    start_time = pygame.time.get_ticks() / 1000
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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


def test():
    # Call the function to play a specific video
    video_path = "resources/videos/Dragon Ball Z - I Leggendari Super Guerrieri (ITA) - Capitolo 1.mp4"
    play_video(video_path, 800, 600)
