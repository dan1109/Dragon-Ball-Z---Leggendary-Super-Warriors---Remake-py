import pygame

from main import get_cropped_image
from obstacles import load_background_image, load_obstacle_rect

# Costanti
CHARACTER_WIDTH, CHARACTER_HEIGHT = 20, 20
CHARACTER_SPEED = 5
ACCELERATION = 0.5


class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.rect = pygame.Rect(self.x, self.y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self.second_character_rect = load_obstacle_rect()
        background_image = get_cropped_image("resources/images/Icons/All_maps.png", 18, 13, 255, 305).convert_alpha()
        self.background_image = load_background_image(background_image)
        self.greeting_displayed = False

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.speed_x = -CHARACTER_SPEED
        elif keys[pygame.K_RIGHT]:
            self.speed_x = CHARACTER_SPEED
        else:
            self.speed_x = 0

        if keys[pygame.K_UP]:
            self.speed_y = -CHARACTER_SPEED
        elif keys[pygame.K_DOWN]:
            self.speed_y = CHARACTER_SPEED
        else:
            self.speed_y = 0

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.topleft = (self.x, self.y)

    def handle_collision(self, obstacle_image, keys, greeting_displayed):
        self.x -= self.speed_x
        self.y -= self.speed_y

        if keys[pygame.K_a] and self.rect.colliderect(self.second_character_rect):
            if not greeting_displayed:
                print("Hello")
                self.greeting_displayed = True
        else:
            self.greeting_displayed = False

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.second_character_rect)
