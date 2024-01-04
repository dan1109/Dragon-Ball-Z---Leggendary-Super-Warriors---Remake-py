import pygame

# Constants
CHARACTER_SPEED = 5
ACCELERATION = 0.5
ANIMATION_SPEED = 10


class CharacterMap:
    """
    A class representing a character on the game map.
    """

    # Dictionary of directions
    DIRECTIONS = {
        0: {'name': 'down', 'opposite': 2},
        1: {'name': 'right', 'opposite': 3},
        2: {'name': 'up', 'opposite': 0},
        3: {'name': 'left', 'opposite': 1}
    }

    def __init__(self, x, y, sprites):
        """
        Initialize the CharacterMap object.

        :param x: Initial x-coordinate
        :param y: Initial y-coordinate
        :param sprites: List of sprites for character animation
        """
        self.x = x
        self.y = y
        self.x_previous = self.x - 1
        self.y_previous = self.y - 1
        self.sprites = sprites[0]
        self.rect = sprites[1]
        self.direction = 0  # 0: down, 1: right, 2: up, 3: left
        self.current_frame = 0
        self.frames_per_direction = 2
        self.frame_counter = 0
        self.speed_x = CHARACTER_SPEED
        self.speed_y = CHARACTER_SPEED
        # Variables for movement control -> 0: down, 1: right, 2: up, 3: left
        self.directions = {0: False, 1: False, 2: False, 3: False}

    def reset_directions(self):
        """
        Reset the direction flags for character movement.
        """
        self.directions = {0: False, 1: False, 2: False, 3: False}

    def set_direction(self, direction):
        """
        Set the character's direction.

        :param direction: New direction (0: down, 1: right, 2: up, 3: left)
        """
        self.reset_directions()
        self.directions[direction] = True
        self.direction = direction

    def set_previous_coordinate(self):
        """
        Set the character's position to the previous coordinates.
        """
        self.x = self.x_previous
        self.y = self.y_previous

    def move_up(self):
        """
        Move the character upwards.
        """
        self.set_direction(2)  # Sprite moving upwards
        self.y_previous = self.y
        self.y -= 1 * self.speed_y

    def move_down(self):
        """
        Move the character downwards.
        """
        self.set_direction(0)  # Sprite moving downwards
        self.y_previous = self.y
        self.y += 1 * self.speed_y

    def move_left(self):
        """
        Move the character to the left.
        """
        self.set_direction(3)  # Sprite moving left
        self.x_previous = self.x
        self.x -= 1 * self.speed_x

    def move_right(self):
        """
        Move the character to the right.
        """
        self.set_direction(1)  # Sprite moving right
        self.x_previous = self.x
        self.x += 1 * self.speed_x

    def opposite_direction(self):
        """
        Get the opposite direction of the current character's direction.

        :return: Opposite direction (0: down, 1: right, 2: up, 3: left)
        """
        return self.DIRECTIONS[self.direction]['opposite']

    def update_frame(self, animation_speed):
        """
        Update the character's animation frame.

        :param animation_speed: Speed of animation frame updates
        """
        self.frame_counter += 1
        if self.frame_counter >= animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % self.frames_per_direction
        self.rect.topleft = (self.x, self.y)

    def blit(self, game):
        """
        Draw the character on the game screen.

        :param game: The game object
        """
        self.update_frame(ANIMATION_SPEED)
        game.screen.blit(self.sprites[self.direction][self.current_frame], self.rect)  # Draw the character

    def handle_pressed_movement(self, keys):
        """
        Handle character movement based on key presses.

        :param keys: Dictionary of pressed keys
        """
        if keys[pygame.K_UP]:
            self.move_up()
        if keys[pygame.K_DOWN]:
            self.move_down()
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()
        self.set_rect()

    def set_rect(self):
        """
        Set the character's rectangle for collision detection.
        """
        self.rect = pygame.Rect(self.x, self.y, self.sprites[0][0].get_width(), self.sprites[0][0].get_height())
