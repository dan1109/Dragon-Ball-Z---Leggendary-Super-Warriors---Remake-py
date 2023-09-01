import pygame
import sys
from character import Character
from main import get_cropped_image
from obstacles import load_obstacle_image, is_collision

# Costanti
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    character = Character(100, 100)
    obstacle_imag = get_cropped_image("resources/images/Icons/All_maps obstacles.png", 18, 13, 255, 305).convert_alpha()
    obstacle_image = load_obstacle_image(obstacle_imag)

    greeting_displayed = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        character.handle_input(keys)
        character.update()

        if is_collision(character.rect, obstacle_image) or character.rect.colliderect(character.second_character_rect):
            character.handle_collision(obstacle_image, keys, greeting_displayed)

        screen.fill((0, 0, 0))
        screen.blit(character.background_image, (0, 0))
        screen.blit(obstacle_image, (0, 0))
        character.draw(screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
