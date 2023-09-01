import pygame
import sys

from main import get_cropped_image

# Costanti
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CHARACTER_WIDTH, CHARACTER_HEIGHT = 20, 20
CHARACTER_SPEED = 5
ACCELERATION = 0.5

# Posizione del secondo personaggio fisso
SECOND_CHARACTER_X, SECOND_CHARACTER_Y = 700, 80
SECOND_CHARACTER_WIDTH, SECOND_CHARACTER_HEIGHT = 20, 20


def load_images():
    image1 = get_cropped_image("resources/images/Icons/All_maps.png", 18, 13, 255, 305).convert_alpha()
    image2 = get_cropped_image("resources/images/Icons/All_maps obstacles.png", 18, 13, 255, 305).convert_alpha()

    # Ridimensiona le immagini per adattarle alla finestra
    image1 = pygame.transform.scale(image1, (SCREEN_WIDTH, SCREEN_HEIGHT))
    image2 = pygame.transform.scale(image2, (SCREEN_WIDTH, SCREEN_HEIGHT))

    return image1, image2


def rect_overlap(rect1, rect2):
    return rect1.colliderect(rect2)


def is_collision(character_rect, image1, image2):
    character_mask = character_rect
    image2_mask = image2.get_rect()

    if rect_overlap(character_mask, image2_mask):
        for x in range(character_mask.left, character_mask.right):
            for y in range(character_mask.top, character_mask.bottom):
                if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
                    return True  # Uscito dai limiti della finestra
                pixel_alpha = image2.get_at((x, y))[3]  # Ottieni il canale alfa (trasparenza)
                if pixel_alpha > 0:
                    return True  # Collisione con un'area non trasparente di image2
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    image1, image2 = load_images()

    character_x, character_y = 100, 100
    character_speed_x, character_speed_y = 0, 0
    character_rect = pygame.Rect(character_x, character_y, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    second_character_rect = pygame.Rect(SECOND_CHARACTER_X, SECOND_CHARACTER_Y, SECOND_CHARACTER_WIDTH,
                                        SECOND_CHARACTER_HEIGHT)

    greeting_displayed = False  # Per evitare di visualizzare il saluto "Hello" più di una volta

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            character_speed_x = -CHARACTER_SPEED
        elif keys[pygame.K_RIGHT]:
            character_speed_x = CHARACTER_SPEED
        else:
            character_speed_x = 0

        if keys[pygame.K_UP]:
            character_speed_y = -CHARACTER_SPEED
        elif keys[pygame.K_DOWN]:
            character_speed_y = CHARACTER_SPEED
        else:
            character_speed_y = 0

        character_x += character_speed_x
        character_y += character_speed_y

        character_rect.topleft = (character_x, character_y)

        if is_collision(character_rect, image1, image2) or character_rect.colliderect(second_character_rect):
            character_x -= character_speed_x
            character_y -= character_speed_y

            if keys[pygame.K_a] and character_rect.colliderect(second_character_rect):
                if not greeting_displayed:
                    print("Hello")
                    greeting_displayed = True
            else:
                greeting_displayed = False

        screen.fill((0, 0, 0))
        screen.blit(image1, (0, 0))  # Disegna l'immagine di sfondo
        screen.blit(image2, (0, 0))  # Disegna l'immagine degli ostacoli

        pygame.draw.rect(screen, (0, 0, 255), character_rect)
        pygame.draw.rect(screen, (255, 0, 0), second_character_rect)  # Disegna il secondo personaggio (ostacolo)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()