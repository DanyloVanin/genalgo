from numpy import random

from individual import Individual
from population import Population
"""
Constructor accepts fitness_function class
"""


class PopulationFactory:
    def __init__(self, fitness_function):
        self.fitness_function = fitness_function

    def generate_binomial_chromosome_population(self, length, population_size):
        chromosomes = [self.fitness_function.generate_optimal()]
        for j in range(population_size-1):
            chromosome = random.binomial(n=1, p=.5, size=length)
            # turning numpy array into string
            chromosome_str = ''.join(map(str, chromosome))
            fitness = self.fitness_function.estimate(chromosome_str)
            chromosomes.append(Individual(chromosome_str, fitness, j + 2))

        return Population(chromosomes)
# %%
