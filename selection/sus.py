from constants import MAX_ITERATIONS, ZERO
from population import Population
from numpy import random
from statistics import mean
import math
import numpy as np

# TODO a lot depends on validity of this method, have to check correctness
def basic_sus(population: Population, total_fitness, fitness_scale: []):
    mating_pool = []
    number_of_parents = len(population.individuals)
    fitness_step = total_fitness / number_of_parents
    random_offset = random.uniform(0, fitness_step)
    current_fitness_pointer = random_offset
    last_fitness_scale_position = 0

    for _ in range(len(population.individuals)):
        for fitness_scale_position in range(last_fitness_scale_position, len(fitness_scale)):
            if fitness_scale[fitness_scale_position] >= current_fitness_pointer:
                mating_pool.append(population.individuals[fitness_scale_position])
                last_fitness_scale_position = fitness_scale_position
                break
        current_fitness_pointer += fitness_step

    return mating_pool


class SUS:
    @staticmethod
    def select(population: Population):
        total_fitness = 0
        fitness_scale = []

        for index, individual in enumerate(population.individuals):
            total_fitness += individual.fitness
            if index == 0:
                fitness_scale.append(individual.fitness)
            else:
                fitness_scale.append(individual.fitness + fitness_scale[index - 1])

        mating_pool = basic_sus(population, total_fitness, fitness_scale)
        population.update_chromosomes(mating_pool)

        return population


class WindowSUS:
    def __init__(self, h: int):
        self.fh_worst_list = []
        self.h = h

    def window_sus(self, population: Population):
        total_fitness = 0
        fitness_scale = []

        if len(self.fh_worst_list) < self.h:
            self.fh_worst_list.append(min(population.fitness_list))
        else:
            # Should remove the first one and then append to the end
            self.fh_worst_list.pop(0)
            self.fh_worst_list.append(min(population.fitness_list))

        # Get the worst fitness from window
        fh_worst = min(self.fh_worst_list)
        all_same = all([x.fitness-fh_worst < ZERO for x in population.individuals])
        PADDING = 0.0001 if all_same else 0
        for index, individual in enumerate(population.individuals):
            individual_scaled_fitness = individual.fitness - fh_worst + PADDING
            total_fitness += individual_scaled_fitness
            if index == 0:
                fitness_scale.append(individual_scaled_fitness)
            else:
                # We are building numeric line, where we will then use points to indicate probability ranges
                fitness_scale.append(individual_scaled_fitness + fitness_scale[index - 1])


        mating_pool = basic_sus(population, total_fitness, fitness_scale)

        population.update_chromosomes(mating_pool)

        return population

    def select(self, population):
        return self.window_sus(population)


class ExpScaledSUS:
    def __init__(self, k: int):
        self.k = k

    def exp_scaled_sus(self, population: Population):
        total_fitness = 0
        fitness_scale = []

        for index, individual in enumerate(population.individuals):
            individual_scaled_fitness = math.pow(individual.fitness, self.k)
            total_fitness += individual_scaled_fitness
            if index == 0:
                fitness_scale.append(individual_scaled_fitness)
            else:
                # We are building numeric line, where we will then use points to indicate probability ranges
                fitness_scale.append(individual_scaled_fitness + fitness_scale[index - 1])

        mating_pool = basic_sus(population, total_fitness, fitness_scale)
        population.update_chromosomes(mating_pool)

        return population

    def select(self, population):
        return self.exp_scaled_sus(population)


# %%

class WindowSUS_2H(WindowSUS):
    def __init__(self, h=2):
        super().__init__(h)


class WindowSUS_10H(WindowSUS):
    def __init__(self, h=10):
        super().__init__(h)


class ExpScaledSUS_1_005K(ExpScaledSUS):

    def __init__(self, k=1.005):
        super().__init__(k)


class ExpScaledSUS_1_05K(ExpScaledSUS):

    def __init__(self, k=1.05):
        super().__init__(k)
