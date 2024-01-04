import pygame
import sys

from map_movement import get_sprites_character

# Inizializza Pygame
pygame.init()

# Imposta le dimensioni della finestra
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Imposta il titolo della finestra
pygame.display.set_caption("Debug dei sprites del personaggio")

# Carica i tuoi sprites del personaggio 20 piccolo 65
sprites, pupazzo_rect = get_sprites_character(65, 22, True)

# Imposta la posizione iniziale del personaggio
pupazzo_rect.center = (screen_width // 2, screen_height // 2)

# Imposta una velocità di aggiornamento
clock = pygame.time.Clock()
current_frame = 0
current_direction = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pulisce lo schermo
    screen.fill((0, 0, 0))

    # Disegna il frame corrente del personaggio
    screen.blit(sprites[current_direction][current_frame], pupazzo_rect)

    # Aggiorna lo schermo
    pygame.display.flip()

    # Aggiungi un ritardo di 1 secondo tra i frame
    pygame.time.delay(500)  # 1000 millisecondi (1 secondo)

    # Aggiorna il frame del personaggio
    current_frame += 1
    if current_frame >= len(sprites[current_direction]):
        current_frame = 0

    # Controlla gli eventi della tastiera per cambiare la direzione del personaggio
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        current_direction = 2
    elif keys[pygame.K_DOWN]:
        current_direction = 0
    elif keys[pygame.K_LEFT]:
        current_direction = 3
    elif keys[pygame.K_RIGHT]:
        current_direction = 1

    # Limita la velocità di aggiornamento
    clock.tick(20)  # Puoi regolare questa velocità a tuo piacimento

# Chiudi Pygame
pygame.quit()
sys.exit()
