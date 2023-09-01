import pygame
import sys

from main import get_cropped_image

# Inizializza Pygame
pygame.init()

# Imposta le dimensioni della finestra
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Scrollable Image Viewer")
clock = pygame.time.Clock()


def main(image_path):
    image = pygame.image.load(image_path)
    image_width, image_height = image.get_size()

    scroll_x, scroll_y = 0, 0
    scroll_speed = 50  # Velocità di scrolling
    scroll_multiplier = 0.1  # Moltiplicatore per lo scroll con la rotella del mouse

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Gestisci lo scrolling con i tasti
        if keys[pygame.K_LEFT]:
            scroll_x += scroll_speed
        if keys[pygame.K_RIGHT]:
            scroll_x -= scroll_speed
        if keys[pygame.K_UP]:
            scroll_y += scroll_speed
        if keys[pygame.K_DOWN]:
            scroll_y -= scroll_speed

        # Gestisci lo scrolling con la rotella del mouse
        scroll_x -= pygame.mouse.get_rel()[0] * scroll_multiplier
        scroll_y -= pygame.mouse.get_rel()[1] * scroll_multiplier

        # Limita lo scrolling alla grandezza dell'immagine
        scroll_x = max(-(image_width - width), min(0, scroll_x))
        scroll_y = max(-(image_height - height), min(0, scroll_y))

        # Ottieni le coordinate del mouse all'interno dell'immagine
        mouse_x, mouse_y = pygame.mouse.get_pos()
        relative_x = mouse_x - scroll_x
        relative_y = mouse_y - scroll_y

        # Pulisci lo schermo
        screen.fill((255, 255, 255))

        # Disegna l'immagine nella posizione corrente dello scrolling
        screen.blit(image, (scroll_x, scroll_y))

        # Aggiorna lo schermo
        pygame.display.flip()

        # Stampa le coordinate nella console
        print("Coordinates (Image):", relative_x, relative_y)

        clock.tick(60)  # Limita il frame rate

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # image_path = "resources/images/Icons/All_faces.png"
    image_path = "resources/images/Icons/All_maps.png"
    main(image_path)
