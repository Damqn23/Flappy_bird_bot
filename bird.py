# bird.py
import pygame
import numpy as np
from neural_network import NeuralNetwork

class Bird:
    def __init__(self, x, y, genome=None):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 0.5
        self.flap_strength = -10
        self.is_alive = True
        self.score = 0

        # Load bird animation frames without scaling
        self.load_images(['imgs/bird1.png', 'imgs/bird2.png', 'imgs/bird3.png'])
        self.current_frame = 0
        self.animation_speed = 0.2  # Adjust for animation speed
        self.animation_timer = 0

        # Initialize neural network genome
        if genome:
            self.brain = NeuralNetwork(genome['w1'], genome['b1'], genome['w2'], genome['b2'])
        else:
            self.brain = NeuralNetwork()

        # Get the rect based on the first image
        self.image = self.bird_frames[self.current_frame]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Flap cooldown to prevent excessive flapping
        self.flap_cooldown = 0  # Frames until next flap

    def load_images(self, image_paths):
        """Load bird images without scaling."""
        self.bird_frames = []
        for path in image_paths:
            try:
                image = pygame.image.load(path).convert_alpha()
                self.bird_frames.append(image)
                print(f"Loaded bird image: {path}")
            except pygame.error as e:
                print(f"Unable to load bird image {path}: {e}")
                # Create a placeholder if image fails to load
                placeholder = pygame.Surface((34, 24), pygame.SRCALPHA)
                pygame.draw.circle(placeholder, (255, 255, 0), (17, 12), 12)  # Yellow circle
                self.bird_frames.append(placeholder)
                print(f"Added placeholder for bird image: {path}")

    def flap(self):
        if self.flap_cooldown == 0:
            self.velocity = self.flap_strength
            self.flap_cooldown = 20  # 20 frames cooldown (~0.33 seconds at 60 FPS)
            print(f"Bird flapped! New velocity: {self.velocity}")
        else:
            print(f"Flap on cooldown: {self.flap_cooldown} frames remaining.")

    def update(self):
        # Handle flap cooldown
        if self.flap_cooldown > 0:
            self.flap_cooldown -= 1

        # Apply gravity
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.centery = self.y
        print(f"Bird updated to y: {self.y}, velocity: {self.velocity}")

        # Update animation
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.bird_frames)
            self.image = self.bird_frames[self.current_frame]
            print(f"Switched to bird frame: {self.current_frame + 1}")

    def decide(self, inputs):
        output = self.brain.forward(inputs)
        print(f"Bird decision inputs: {inputs}, output: {output}")
        if output > 0.5:
            self.flap()

    def get_genome(self):
        return self.brain.get_parameters()

    def mutate(self, mutation_rate=0.1):
        self.brain.mutate(mutation_rate)
        print("Bird genome mutated.")

    def draw(self, screen):
        """Draw the bird with its current animation frame."""
        screen.blit(self.image, self.rect)
        # Optional: Draw rect for debugging
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
