import pygame
import random

class Pipe:
    VELOCITY = 5
    WIDTH = 52      # Pipe image width
    COLOR = (0, 255, 0)  # Fallback color if image fails to load

    def __init__(self, x, screen_height, base_height):
        self.x = x
        self.screen_height = screen_height
        self.base_height = base_height  # New: store how tall the base is
        self.gap = 180                  # Distance between top and bottom pipes
        self.passed = False

        # Load pipe image
        self.load_image('imgs/pipe.png')

        # Randomly set how high or low to place the gap, respecting the base
        self.set_height()

    def load_image(self, path):
        """Load the pipe image and scale it to make it bigger."""
        try:
            original_image = pygame.image.load(path).convert_alpha()

            # Define the scale factor (e.g., 1.5 for 150% size increase)
            scale_factor = 1.7
            scaled_width = int(original_image.get_width() * scale_factor)
            scaled_height = int(original_image.get_height() * scale_factor)

            # Scale the images
            self.top_image = pygame.transform.flip(
                pygame.transform.scale(original_image, (scaled_width, scaled_height)),
                False,
                True
            )
            self.bottom_image = pygame.transform.scale(original_image, (scaled_width, scaled_height))

            # Update width and height attributes
            self.WIDTH = scaled_width
            self.image_height = scaled_height

            print("Loaded and scaled pipe image.")
        except pygame.error as e:
            print(f"Unable to load pipe image {path}: {e}")
            self.top_image = None
            self.bottom_image = None
            self.image_height = 320  # Fallback
            print("Using colored rectangles as placeholders.")

    def set_height(self):
        """
        Clamp the gap so the bottom of the gap doesn't go below the base.
        The top of the gap won't go above the top of the screen.
        """
        half_gap = self.gap // 2

        # The lowest valid center for the gap is half_gap from the top
        min_center = half_gap
        # The highest valid center: (screen_height - base_height) - half_gap
        # so the gap won't go into the base.
        max_center = (self.screen_height - self.base_height) - half_gap

        if max_center < min_center:
            # If this happens, your gap + base is too big for the screen
            gap_center = (self.screen_height - self.base_height) // 2
            print("Warning: gap + base too large. Using fallback center.")
        else:
            gap_center = random.randint(min_center, max_center)

        # The top pipe's bottom is at (gap_center - half_gap),
        # so its top is that minus the pipe height.
        self.top = (gap_center - half_gap) - self.image_height

        # The bottom pipe starts at (gap_center + half_gap).
        self.bottom = gap_center + half_gap

        # For AI or debug: how high is the top pipe, how high is the bottom pipe
        self.top_pipe_height = (gap_center - half_gap)  # y-pos of top pipe's bottom
        self.bottom_pipe_height = self.screen_height - (gap_center + half_gap)

        print(f"[DEBUG] gap_center={gap_center}, top={self.top}, bottom={self.bottom}, "
              f"top_pipe_height={self.top_pipe_height}, bottom_pipe_height={self.bottom_pipe_height}")

    def move(self):
        """Move the pipe to the left."""
        self.x -= self.VELOCITY

    def draw(self, screen):
        """Draw top and bottom pipes."""
        if self.top_image and self.bottom_image:
            screen.blit(self.top_image, (self.x, self.top))
            screen.blit(self.bottom_image, (self.x, self.bottom))
        else:
            # Fallback: draw rectangles
            top_rect = pygame.Rect(self.x, self.top, self.WIDTH, self.image_height)
            bottom_rect = pygame.Rect(self.x, self.bottom, self.WIDTH, self.image_height)
            pygame.draw.rect(screen, self.COLOR, top_rect)
            pygame.draw.rect(screen, self.COLOR, bottom_rect)

    def collide(self, bird):
        """Check if the bird collides with either pipe."""
        bird_rect = bird.rect

        if self.top_image and self.bottom_image:
            top_pipe_rect = pygame.Rect(self.x, self.top, self.WIDTH, self.image_height)
            bottom_pipe_rect = pygame.Rect(self.x, self.bottom, self.WIDTH, self.image_height)
        else:
            top_pipe_rect = pygame.Rect(self.x, self.top, self.WIDTH, self.image_height)
            bottom_pipe_rect = pygame.Rect(self.x, self.bottom, self.WIDTH, self.image_height)

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            print(f"Collision detected: bird={bird_rect}, pipe_x={self.x}")
            return True
        return False

    def off_screen(self):
        """Check if the pipe is off the left edge of the screen."""
        off = self.x < -self.WIDTH
        if off:
            print(f"Pipe at x={self.x} is off-screen.")
        return off
