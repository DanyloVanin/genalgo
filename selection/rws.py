from population import Population
from statistics import mean
from constants import MAX_ITERATIONS
import math


class RWS:
    @staticmethod
    def rws(population):
        population_fitness = sum(population.fitness_list)

        if population_fitness == 0:
            return population

        probabilities = [chromosome.fitness / population_fitness for chromosome in population.individuals]
        population.update_rws(probabilities)

        return population

    def select(self, population):
        return self.rws(population)


class WindowRWS:
    def __init__(self, h: int):
        self.fh_worst_list = []
        self.h = h

    def window_rws(self, population: Population):
        population_fitness = sum(population.fitness_list)

        if population_fitness == 0:
            return population

        if len(self.fh_worst_list) < self.h:
            self.fh_worst_list.append(min(population.fitness_list))
        else:
            self.fh_worst_list.pop(0)
            self.fh_worst_list.append(min(population.fitness_list))

        fh_worst = min(self.fh_worst_list)
        scaled_fitness = []

        for chromosome in population.individuals:
            scaled_value = chromosome.fitness - fh_worst
            scaled_fitness.append(scaled_value)

        sf_sum = sum(scaled_fitness)

        if sf_sum > 0:
            probabilities = [sf / sf_sum for sf in scaled_fitness]
        else:
            population_fitness = sum(population.fitness_list)
            probabilities = [chromosome.fitness / population_fitness for chromosome in population.individuals]

        population.update_rws(probabilities)

        return population

    def select(self, population):
        return self.window_rws(population)


class ExpScaledRWS:
    def __init__(self, k: float):
        self.k = k

    def exp_scaled_rws(self, population: Population):
        population_fitness = sum(population.fitness_list)

        if population_fitness == 0:
            return population

        scaled_fitness = []

        for chromosome in population.individuals:
            scaled_value = chromosome.fitness ** self.k
            scaled_fitness.append(scaled_value)

        sf_sum = sum(scaled_fitness)

        if sf_sum > 0:
            probabilities = [sf / sf_sum for sf in scaled_fitness]
        else:
            # TODO for some reason we do not scale if sum is 0
            population_fitness = sum(population.fitness_list)
            probabilities = [chromosome.fitness / population_fitness for chromosome in population.individuals]

        assert abs(sum(probabilities) - 1.0) <= 0.000001
        # TODO should probably move that method out of Population class
        population.update_rws(probabilities)

        return population

    def select(self, population):
        return self.exp_scaled_rws(population)


class WindowRWS_2H(WindowRWS):
    def __init__(self, h=2):
        super().__init__(h)


class WindowRWS_10H(WindowRWS):
    def __init__(self, h=10):
        super().__init__(h)


class ExpScaledRWS_1_005K(ExpScaledRWS):

    def __init__(self, k=1.005):
        super().__init__(k)


class ExpScaledRWS_1_05K(ExpScaledRWS):

    def __init__(self, k=1.05):
        super().__init__(k)
# %%
