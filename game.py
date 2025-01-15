import pygame
import numpy as np
from bird import Bird
from pipe import Pipe

class Game:
    best_record = 0
    def __init__(self, population, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.clock = pygame.time.Clock()
        self.population = population
        self.gap = 200  # Distance between pipes
        self.gaps_passed = 0
        

        # We'll load images (including base) first
        self.load_images()

        # Now that self.base is loaded, we can pass its height to Pipe
        self.pipes = [Pipe(self.screen_width + 200, self.screen_height, self.base.get_height())]

        # Base movement variables
        self.base_x = 0
        self.base_speed = 5  # Speed at which the base moves

        # Font for displaying stats
        self.font = pygame.font.SysFont('Arial', 24)
        self.current_generation = 1
        self.best_fitness = 0

    def load_images(self):
        """Load background and base images without scaling."""
        try:
            self.bg = pygame.image.load('imgs/bg.png').convert()
            # Ensure the background fits the screen
            self.bg = pygame.transform.scale(self.bg, (self.screen_width, self.screen_height))
            print("Loaded background image.")
        except pygame.error as e:
            print(f"Unable to load background image: {e}")
            self.bg = pygame.Surface((self.screen_width, self.screen_height))
            self.bg.fill((135, 206, 235))  # Sky blue fallback

        try:
            self.base = pygame.image.load('imgs/base.png').convert_alpha()
            # Scale base to match screen width
            self.base = pygame.transform.scale(self.base, (self.screen_width, self.base.get_height()))
            print("Loaded base image.")
        except pygame.error as e:
            print(f"Unable to load base image: {e}")
            self.base = pygame.Surface((self.screen_width, 100), pygame.SRCALPHA)
            pygame.draw.rect(self.base, (222, 184, 135), self.base.get_rect())  # Sandy brown fallback

    def reset(self, population):
        self.population = population
        self.gaps_passed = 0
        # Recreate pipes, passing base height
        self.pipes = [Pipe(self.screen_width + 200, self.screen_height, self.base.get_height())]
        self.base_x = 0
        for bird in self.population:
            bird.y = 350
            bird.velocity = 0
            bird.is_alive = True
            bird.score = 0
        print("Game reset with new population.")

    def run_generation(self):
        run = True
        while run and any(bird.is_alive for bird in self.population):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Draw background
            self.screen.blit(self.bg, (0, 0))

            # Draw and move base
            self.screen.blit(self.base, (self.base_x, self.screen_height - self.base.get_height()))
            self.screen.blit(self.base, (self.base_x + self.base.get_width(),
                                         self.screen_height - self.base.get_height()))
            self.base_x -= self.base_speed
            if self.base_x <= -self.base.get_width():
                self.base_x = 0

            # Move and draw pipes
            add_pipe = False
            remove_pipes = []
            for pipe in self.pipes:
                pipe.move()
                pipe.draw(self.screen)
                for bird in self.population:
                    if bird.is_alive and pipe.collide(bird):
                        bird.is_alive = False
                        print(f"Bird at y: {bird.y} collided with pipe.")
                if pipe.off_screen():
                    remove_pipes.append(pipe)
                if not pipe.passed and pipe.x < self.screen_width // 2:
                    pipe.passed = True
                    add_pipe = True
                    # Increment score for each alive bird
                    for bird in self.population:
                        if bird.is_alive:
                            bird.score += 1
                            print(f"Bird at y: {bird.y} passed a pipe. Score: {bird.score}")

            if add_pipe:
                print("Adding new pipe.")
                self.gaps_passed += 1
                if self.gaps_passed > Game.best_record:  # Update class-level best record
                    Game.best_record = self.gaps_passed
                
                # Pass the base height here too
                self.pipes.append(Pipe(self.screen_width + 200, self.screen_height, self.base.get_height()))

            for pipe in remove_pipes:
                self.pipes.remove(pipe)

            # Update and draw birds
            for bird in self.population:
                if bird.is_alive:
                    # Find the closest pipe
                    closest_pipe = None
                    for pipe in self.pipes:
                        if pipe.x + pipe.WIDTH > bird.x:
                            closest_pipe = pipe
                            break
                    if closest_pipe:
                        # Prepare AI inputs
                        inputs = np.array([
                            bird.y / self.screen_height,
                            (closest_pipe.x - bird.x) / self.screen_width,
                            closest_pipe.top_pipe_height / self.screen_height,
                            closest_pipe.bottom_pipe_height / self.screen_height
                        ])
                        bird.decide(inputs)
                    bird.update()

                    # Check collision with ground or ceiling
                    if (bird.rect.bottom > self.screen_height - self.base.get_height()
                            or bird.rect.top < 0):
                        bird.is_alive = False
                        print(f"Bird at y: {bird.y} collided with ground or ceiling.")

                    # Draw bird
                    bird.draw(self.screen)

            # Render stats
            self.render_stats()

            pygame.display.flip()
            self.clock.tick(60)

    def render_stats(self):
        """Render generation and fitness statistics on the screen."""
        
        gaps_passed_text = self.font.render(f"Gaps Passed: {self.gaps_passed}", True, (0, 0, 0))
        best_record_text = self.font.render(f"Best Record: {Game.best_record}", True, (0, 0, 0))  # Use class-level attribute



        
        self.screen.blit(gaps_passed_text, (10, 10))
        self.screen.blit(best_record_text,(10, 40))


        
        

    def get_fitness_scores(self):
        return [bird.score for bird in self.population]
