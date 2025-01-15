# genetic_algorithm.py
import numpy as np
from bird import Bird
import pickle

def select_parents(population, num_parents):
    """
    Select the top-performing birds as parents based on their scores.
    """
    # Sort the population based on scores in descending order
    sorted_population = sorted(population, key=lambda bird: bird.score, reverse=True)
    # Select the top 'num_parents' birds
    parents = sorted_population[:num_parents]
    return parents

def create_next_generation(parents, population_size, elite_genome=None):
    """
    Create the next generation of birds.
    - Parents are used to breed new birds.
    - Optionally, an elite genome can be added to preserve the best bird.
    """
    next_generation = []

    # If elite_genome is provided, create an elite bird and add to next_generation
    if elite_genome is not None:
        elite_bird = Bird(x=100, y=350, genome=elite_genome)
        next_generation.append(elite_bird)
        print("Elite bird added to the next generation.")

    # Calculate how many birds to create
    remaining_population = population_size - len(next_generation)

    # Breed new birds to fill the remaining population
    for _ in range(remaining_population):
        # Randomly select two parents
        parent1, parent2 = np.random.choice(parents, 2, replace=False)
        # Crossover their genomes
        child_genome = crossover(parent1.get_genome(), parent2.get_genome())
        # Mutate the child's genome
        child_genome = mutate(child_genome, mutation_rate=0.1)
        # Create a new bird with the child's genome
        child_bird = Bird(x=100, y=350, genome=child_genome)
        next_generation.append(child_bird)

    return next_generation

def crossover(genome1, genome2):
    """
    Perform crossover between two genomes to produce a child's genome.
    Assumes genome1 and genome2 are dictionaries with 'w1', 'b1', 'w2', 'b2' as keys.
    """
    child_genome = {}
    for key in genome1.keys():
        # Get the shape of the parameter
        shape = genome1[key].shape
        # Flatten the arrays to perform crossover
        flat1 = genome1[key].flatten()
        flat2 = genome2[key].flatten()
        # Choose a random crossover point
        if len(flat1) > 1:
            crossover_point = np.random.randint(1, len(flat1))
        else:
            crossover_point = 0
        # Create child parameter by combining parent parameters
        child_flat = np.concatenate((flat1[:crossover_point], flat2[crossover_point:]))
        # Reshape back to original shape
        child_genome[key] = child_flat.reshape(shape)
    return child_genome

def mutate(genome, mutation_rate=0.1):
    """
    Mutate the genome by adding small random values to weights and biases.
    """
    for key in genome.keys():
        mutation_mask = np.random.rand(*genome[key].shape) < mutation_rate
        random_values = np.random.randn(*genome[key].shape) * mutation_mask
        genome[key] += random_values
    return genome
