import os
import random
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from constants import DESIRED_GENE_HOMOGENEITY_LEVEL
from individual import Individual


def all_the_same(elements):
    # Works by counting how many times the first item appears in the list
    return len(elements) < 1 or len(elements) == elements.count(elements[0])


def verify_genes_homogeneity(chromosomes):
    num_individuals = len(chromosomes)
    for i in range(len(chromosomes[0].code)):
        genes = []
        for chromosome in chromosomes:
            genes.append(chromosome.code[i])
        ones = genes.count('1')
        if DESIRED_GENE_HOMOGENEITY_LEVEL > ones / num_individuals > (1.0 - DESIRED_GENE_HOMOGENEITY_LEVEL):
            return False
    return True


MUTATION_TABLE = {
    # L, N   : P_mutation
    # L = 10, N = ...
    (10, 10): 0.01,  # TODO remove, used just for test
    (10, 100): 0.0001,
    (10, 200): 0.0001 / 2,
    (10, 300): 0.0001 / 3,
    (10, 400): 0.0001 / 4,
    (10, 500): 0.0001 / 5,
    (10, 1000): 0.00001,
    # L = 100, N = ..
    (100, 100): 0.00001,
    (100, 200): 0.00001 / 2,
    (100, 300): 0.00001 / 3,
    (100, 400): 0.00001 / 4,
    (100, 500): 0.00001 / 5,
    (100, 1000): 0.000001
}


class Population:
    def __init__(self, chromosomes, mutation_enabled=False, crossover_enabled=False):
        self.individuals = chromosomes
        self.fitness_list = [chromosome.fitness for chromosome in self.individuals]
        self.genotypes_list = [x.code for x in self.individuals]
        self.mutation_enabled = mutation_enabled
        self.crossover_enabled = crossover_enabled

    def print_fenotypes_distribution(self, folder_name, func_name, run, iteration):
        path = 'stats/' + folder_name + '/' + str(len(self.individuals)) + '/' + func_name + '/' + str(
            run) + '/fenotypes'

        if not os.path.exists(path):
            os.makedirs(path)

        sns.displot(self.fitness_list)
        plt.savefig(path + '/' + str(iteration) + '.png')
        plt.close()

    def print_genotypes_distribution(self, folder_name, func_name, run, iteration, fitness_func):
        path = 'stats/' + folder_name + '/' + str(len(self.individuals)) + '/' + func_name + '/' + str(
            run) + '/genotypes'

        if not os.path.exists(path):
            os.makedirs(path)

        # TODO temporary fix for genotype being list and not str
        x_list = [(fitness_func.get_genotype_value(code)) for code in self.genotypes_list]
        sns.displot(x_list)
        plt.savefig(path + '/' + str(iteration) + '.png')
        plt.close()

    def all_phenotypes_same(self):
        phenotypes = [individual.code for individual in self.individuals]
        return all_the_same(phenotypes)

    def is_all_same_genotype(self):
        return all_the_same(self.genotypes_list)

    def is_converged(self):
        # За відсутності мутації: збіжність популяції в одну точку або проведення 10 000 000 ітерацій.
        if not self.mutation_enabled:
            return all_the_same(self.genotypes_list)
        else:
            # за наявності мутації гомогенність популяції по кожному гену на 99%
            return verify_genes_homogeneity(self.individuals)

    def mutate(self, fitness_function):
        # Check if mutation is enabled
        if not self.mutation_enabled:
            return

        # Get mutation probability
        code_length = len(self.individuals[0].code)  # L
        number_of_individuals = len(self.individuals)  # N
        mutation_probability = MUTATION_TABLE[(code_length, number_of_individuals)]

        # randomly change bits in each chromosome
        for chromosome in self.individuals:
            chromosome_code_list = list(chromosome.code)
            for i in range(0, len(chromosome.code)):
                if random.random() < mutation_probability:
                    # had to play around with the list, because cannot assign to specific index of str
                    chromosome_code_list[i] = "0" if chromosome_code_list[i] == "1" else "1"
                    chromosome.code = ''.join(chromosome_code_list)
                    chromosome.fitness = fitness_function.estimate(chromosome.code)

        self.update()

    # Perform crossover
    def crossover(self, fitness_function):
        # Skip crossover if probability 0
        if not self.crossover_enabled:
            return

        next_individuals = []

        chromosomes = self.individuals.copy()

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
            assert (len(parent1.code) == len(child1_code))
            assert (len(parent2.code) == len(child2_code))

            next_individuals.append(
                Individual(child1_code, fitness_function.estimate(child1_code), len(next_individuals) + 1))
            next_individuals.append(
                Individual(child2_code, fitness_function.estimate(child2_code), len(next_individuals) + 1))

        assert (len(self.individuals) == len(next_individuals))
        self.individuals = next_individuals
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
        return len(set([chromosome.key for chromosome in self.individuals]))

    def get_keys_list(self):
        return list([chromosome.key for chromosome in self.individuals])

    def get_chromosomes_copies_count(self, chromosome_genotype):
        return self.genotypes_list.count(chromosome_genotype)

    def update(self):
        self.fitness_list = [chromosome.fitness for chromosome in self.individuals]
        self.genotypes_list = [x.code for x in self.individuals]

    def update_rws(self, probabilities):
        new_individuals = []
        for _ in range(0, len(self.individuals)):
            random_individual = np.random.choice(self.individuals, p=probabilities)
            new_individual = Individual(random_individual.code, random_individual.fitness, random_individual.key)
            new_individuals.append(new_individual)
        self.individuals = new_individuals
        self.update()

    def update_chromosomes(self, chromosomes):
        self.individuals = chromosomes
        self.update()

    def create_copy(self):
        copy_individuals = []
        for i in self.individuals:
            copy_individual = Individual(i.code, i.fitness, i.key)
            copy_individuals.append(copy_individual)
        return Population(copy_individuals, self.mutation_enabled, self.crossover_enabled)

    # def __copy__(self):
    #     return Population(self.individuals.copy(), self.mutation_enabled, self.crossover_enabled)
# %%
