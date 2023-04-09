import os
import random

import numpy as np
import seaborn as sns
from statistics import mean
import matplotlib.pyplot as plt
from chromosome import Chromosome
from constants import N, EPS


def all_the_same(elements):
    return len(elements) < 1 or len(elements) == elements.count(elements[0])


def verify_genes_homogeneity(chromosomes):
    num_individuals = len(chromosomes)
    for i in range(len(chromosomes[0].code)):
        genes = []
        for chromosome in chromosomes:
            genes.append(chromosome.code[i])
        ones = genes.count('1')
        if 0.99 > ones/num_individuals > 0.01:
            return False
    return True


mutation_table = {
    # L, N   : P_mutation
    # L = 10, N = ...
    (10, 100): 0.0005,
    (10, 200): 0.0005 / 2,
    (10, 300): 0.0005 / 3,
    (10, 400): 0.0005 / 4,
    (10, 500): 0.0005 / 5,
    (10, 1000): 0.00005,
    # L = 100, N = ..
    (100, 100): 0.00001,
    (100, 200): 0.00001 / 2,
    (100, 300): 0.00001 / 3,
    (100, 400): 0.00001 / 4,
    (100, 500): 0.00001 / 5,
    (100, 1000): 0.000001
}


class Population:
    def __init__(self, chromosomes, p_m, p_crossover):
        self.chromosomes = chromosomes
        self.fitness_list = [chromosome.fitness for chromosome in self.chromosomes]
        self.genotypes_list = [list(x.code) for x in self.chromosomes]
        self.p_m = p_m
        self.p_crossover = p_crossover

    def print_fenotypes_distribution(self, folder_name, func_name, run, iteration):
        path = 'stats/' + folder_name + '/' + str(N) + '/' + func_name + '/' + str(run) + '/fenotypes'

        if not os.path.exists(path):
            os.makedirs(path)

        sns.displot(self.fitness_list)
        plt.savefig(path + '/' + str(iteration) + '.png')
        plt.close()

    def print_genotypes_distribution(self, folder_name, func_name, run, iteration, fitness_func):
        path = 'stats/' + folder_name + '/' + str(N) + '/' + func_name + '/' + str(run) + '/genotypes'

        if not os.path.exists(path):
            os.makedirs(path)

        x_list = [fitness_func.get_genotype_value(code) for code in self.genotypes_list]
        sns.displot(x_list)
        plt.savefig(path + '/' + str(iteration) + '.png')
        plt.close()

    def estimate_convergence(self, avg_fitness_list=None, last_n=None):
        if self.p_m == 0:
            return all_the_same(self.genotypes_list)
        else:

            # TODO гомогенність популяції по кожному гену на 99%
            return verify_genes_homogeneity(self.chromosomes)
            #
            # if avg_fitness_list is None or last_n is None or len(avg_fitness_list) < last_n:
            #     return False
            #
            # last_n_avg_fitness_list = avg_fitness_list[-last_n:]
            # last_n_diff = []
            #
            # for i in range(1, len(last_n_avg_fitness_list)):
            #     curr = last_n_avg_fitness_list[i]
            #     prev = last_n_avg_fitness_list[i - 1]
            #     last_n_diff.append(abs(curr - prev))
            #
            # return all(x <= EPS for x in last_n_diff)

    def mutate(self, fitness_function):
        """
        Mutation logic
        Uses mutation_probability parameter - p_m
        :param fitness_function:
        :return:
        """
        # Check if mutation is enabled
        if self.p_m == 0:
            return

        # Get mutation probability
        code_length = len(self.chromosomes[0].code)  # L
        number_of_individuals = len(self.chromosomes)  # N
        mutation_probability = mutation_table[(code_length, number_of_individuals)]

        # randomly change bits in each chromosome
        for chromosome in self.chromosomes:
            for i in range(0, len(chromosome.code)):
                if random.random() < mutation_probability:
                    chromosome.code[i] = int(not chromosome.code[i])
                    chromosome.fitness = fitness_function.estimate(chromosome.code)
        self.update()

    # Perform crossover
    def crossover(self, fitness_function):
        # Skip crossover if probability 0
        if self.p_crossover == 0:
            return

        next_chromosomes = []

        chromosomes = self.chromosomes.copy()

        def pop_random_chromosome():
            index = random.randrange(0, len(chromosomes))
            return chromosomes.pop(index)

        while len(chromosomes) > 0:
            parent1 = pop_random_chromosome()
            parent2 = pop_random_chromosome()

            chromosome1_code = parent1.code
            chromosome2_code = parent2.code

            crossover_point = int(random.random() * len(chromosome1_code))
            child1_code = chromosome1_code[:crossover_point] + chromosome2_code[crossover_point:]
            child2_code = chromosome2_code[:crossover_point] + chromosome1_code[crossover_point:]

            next_chromosomes.append(
                Chromosome(child1_code, fitness_function.estimate(child1_code), len(next_chromosomes)))
            next_chromosomes.append(
                Chromosome(child2_code, fitness_function.estimate(child2_code), len(next_chromosomes)))

        assert (len(chromosomes) == len(next_chromosomes))
        self.chromosomes = next_chromosomes
        self.update()

    def get_mean_fitness(self):
        return mean(self.fitness_list)

    def get_max_fitness(self):
        return max(self.fitness_list)

    def get_best_genotype(self):
        max_value = self.get_max_fitness()
        best_list = list(filter(lambda x: self.fitness_list[x] == max_value, range(len(self.fitness_list))))
        return self.genotypes_list[best_list[0]]

    def get_fitness_std(self):
        return np.std(self.fitness_list)

    def get_unique_chromosomes_count(self):
        return len(set([chromosome.key for chromosome in self.chromosomes]))

    def get_keys_list(self):
        return list([chromosome.key for chromosome in self.chromosomes])

    def get_chromosomes_copies_count(self, chromosome_genotype):
        return self.genotypes_list.count(chromosome_genotype)

    def update(self):
        self.fitness_list = [chromosome.fitness for chromosome in self.chromosomes]
        self.genotypes_list = [list(x.code) for x in self.chromosomes]

    # TODO need to check this one, probably should be moved out of here
    def update_rws(self, probabilities):
        self.chromosomes = [np.random.choice(self.chromosomes, p=probabilities) for _ in
                            range(0, len(self.chromosomes))]
        self.update()

    def update_chromosomes(self, chromosomes):
        self.chromosomes = chromosomes
        self.update()

    def __copy__(self):
        return Population(self.chromosomes.copy(), self.p_m.copy())
# %%
