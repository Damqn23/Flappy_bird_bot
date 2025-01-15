# main.py
import pygame
from bird import Bird
from genetic_algorithm import select_parents, create_next_generation
from game import Game
import pickle  # For saving and loading the best genome
import os  # For checking file existence

def main():
    # Initialize Pygame
    pygame.init()
    print("Pygame initialized.")

    # Set up display
    screen_width = 500
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Flappy Bird AI")
    print("Pygame display set.")

    # Initialize population
    population_size = 50
    best_genome = None

    # Check if a saved best genome file exists
    if os.path.exists('best_genome.pkl'):
        with open('best_genome.pkl', 'rb') as f:
            best_genome = pickle.load(f)
        print("Loaded best genome from file.")

    # Create initial population
    if best_genome:
        # Start with one elite bird (best bird from previous session) and the rest random
        population = [Bird(x=100, y=350, genome=best_genome)] + [Bird(x=100, y=350) for _ in range(population_size - 1)]
    else:
        # If no saved genome, start with a fully random population
        population = [Bird(x=100, y=350) for _ in range(population_size)]

    print(f"Initialized population of {population_size} birds.")

    # Create Game instance with the screen and population
    game = Game(population, screen)

    # Run generations
    generations = 1000
    num_parents = 20  # Number of parents to select each generation

    for generation in range(generations):
        print(f"\n--- Generation {generation + 1} ---")

        # Run the game for the current population
        game.run_generation()

        # Get fitness scores
        fitness_scores = game.get_fitness_scores()
        print(f"Fitness scores: {fitness_scores}")

        # Identify the best bird
        best_fitness = max(fitness_scores)
        best_index = fitness_scores.index(best_fitness)
        best_bird = population[best_index]
        print(f"Best bird in Generation {generation + 1}: Score = {best_fitness}")

        # Save the best genome if it's better than the previous best
        best_genome = best_bird.get_genome()
        with open('best_genome.pkl', 'wb') as f:
            pickle.dump(best_genome, f)
        print("Best genome saved.")

        # Select parents based on fitness
        parents = select_parents(population, num_parents)
        print(f"Selected top {num_parents} parents.")

        # Create next generation with elitism
        population = create_next_generation(parents, population_size, elite_genome=best_genome)
        print(f"Created new generation of {population_size} birds.")

        # Reset the game with the new population
        game.reset(population)

    print("\nTraining completed.")

if __name__ == "__main__":
    main()
