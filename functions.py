import numpy as np
import os

from codec import *
import matplotlib.pyplot as plt
from individual import Individual
from population_factory import PopulationFactory
from constants import DELTA, SIGMA, N
from population import Population


def _draw_fitness_histogram(
        population: Population,
        folder_name: str,
        func_name: str,
        run: int,
        iteration: int,
) -> None:
    dir_path = f"stats/{folder_name}/{N}/{func_name}/{run}/fitness"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    plt.figure()
    plt.hist(population.fitness_list, bins=100, color="green", histtype="bar", rwidth=1)

    # x-axis label
    plt.xlabel("Health")
    # frequency label
    plt.ylabel("Num of individuals")
    # plot title

    plt.title("Fitness of individuals")
    plt.savefig(f"{dir_path}/{iteration}.png")
    plt.close()


def _draw_phenotype_histogram(
        a: float,
        b: float,
        population: Population,
        folder_name: str,
        func_name: str,
        run: int,
        iteration: int,
        phenotypes
) -> None:
    dir_path = f"stats/{folder_name}/{N}/{func_name}/{run}/genotypes"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    plt.figure()
    plt.hist(phenotypes, bins=100, color="red", histtype="bar", rwidth=None)

    # x-axis label
    plt.xlabel("Genotype value")
    # frequency label
    plt.ylabel("Num of individual")
    # plot title

    plt.title("Genotypes of individuals")

    plt.savefig(f"{dir_path}/{iteration}.png")
    plt.close()


def _draw_count_ones_in_genotype_histogram(
        population: Population,
        folder_name: str,
        func_name: str,
        run: int,
        iteration: int,
) -> None:
    dir_path = f"stats/{folder_name}/{N}/{func_name}/{run}/ones_in_genotypes"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    ones = [
        chromosome.code.count('1')
        for chromosome in population.individuals
    ]
    bins = 100

    plt.figure()
    plt.hist(
        ones, bins, color="red", histtype="bar", rwidth=1
    )

    # x-axis label
    plt.xlabel("Ones in genotype")
    # frequency label
    plt.ylabel("Num of individual")
    # plot title
    plt.title("Number of ones in chromosome")

    plt.savefig(f"{dir_path}/{iteration}.png")
    plt.close()


class FConstALL:
    def __init__(self):
        self.factory = PopulationFactory(self)
        self.length = 100

    def estimate(self, _):
        return 100

    def get_genotype_value(self, _):
        return 100

    def generate_optimal(self):
        # All chromosomes are good, no difference
        return Individual('0'*self.length, 100)

    def get_optimal(self):
        return self.generate_optimal()

    def generate_population(self, population_size):
        return self.factory.generate_binomial_chromosome_population(self.length, population_size)

    def draw_histograms(
            self,
            population: Population,
            folder_name: str,
            func_name: str,
            run: int,
            iteration: int,
    ) -> None:
        _draw_count_ones_in_genotype_histogram(
            population, folder_name, func_name, run, iteration
        )

class FHD:
    def __init__(self):
        self.delta = 100.
        self.factory = PopulationFactory(self)
        self.length = 100

    def get_genotype_value(self, chromosome_code):
        return np.count_nonzero(chromosome_code)

    def estimate(self, chromosome):
        # k - number of non-zeroes
        nonzero = chromosome.count('1')
        k = len(chromosome) - nonzero
        return (len(chromosome) - k) + k * self.delta

    def generate_optimal(self):
        # optimal for FHD is all zeroes, genotype is length*delta
        return Individual('0' * self.length, self.length * self.delta)

    def get_optimal(self):
        return self.generate_optimal()

    def generate_population(self, population_size):
        return self.factory.generate_binomial_chromosome_population(self.length, population_size)

    def draw_histograms(
            self,
            population: Population,
            folder_name: str,
            func_name: str,
            run: int,
            iteration: int,
    ) -> None:
        _draw_count_ones_in_genotype_histogram(
            population, folder_name, func_name, run, iteration
        )


class Fx2:
    def __init__(self, is_gray=True):
        self.is_gray = is_gray
        self.a = 0
        self.b = 10.23
        self.optimum_x = 10.23
        self.optimum_y = 10.23 ** 2
        self.precision = 2
        self.chromosome_length = calculate_genome_length(self.a, self.b, self.precision)
        self.factory = PopulationFactory(self)

    def get_genotype_value(self, chromosome_code):
        if self.is_gray:
            binary = convert_grey_to_binary(chromosome_code)
            decimal = convert_binary_to_decimal(binary, self.a, self.precision)
            return decimal
        else:
            decimal = convert_binary_to_decimal(chromosome_code, self.a, self.precision)
            return decimal

    def estimate(self, chromosome_code):
        if self.is_gray:
            binary = convert_grey_to_binary(chromosome_code)
            decimal = convert_binary_to_decimal(binary, self.a, self.precision)
            return math.pow(decimal, 2)
        else:
            decimal = convert_binary_to_decimal(chromosome_code, self.a, self.precision)
            return math.pow(decimal, 2)

    def generate_optimal(self):
        if self.is_gray:
            binary = convert_decimal_to_binary(self.optimum_x, self.a, self.b, self.precision)
            gray = convert_binary_to_grey(binary)
            return Individual(gray, self.optimum_y)
        else:
            binary = convert_decimal_to_binary(self.optimum_x, self.a, self.b, self.precision)
            return Individual(binary, self.optimum_y)

    def get_optimal(self):
        return self.generate_optimal()

    def generate_population(self, population_size):
        return self.factory.generate_binomial_chromosome_population(self.chromosome_length, population_size)

    def check_chromosome_success(self, individual: Individual):
        x = self.get_genotype_value(individual.code)
        y = self.estimate(individual.code)
        return (abs(y - self.optimum_y) <= DELTA) and (abs(x - self.optimum_x) <= SIGMA)

    def draw_histograms(
            self,
            population: Population,
            folder_name: str,
            func_name: str,
            run: int,
            iteration: int,
    ) -> None:
        _draw_count_ones_in_genotype_histogram(
            population, folder_name, func_name, run, iteration
        )
        _draw_fitness_histogram(population, folder_name, func_name, run, iteration)
        phenotypes = [
            self.get_genotype_value(chromosome.code)
            for chromosome in population.individuals
        ]
        _draw_phenotype_histogram(
            self.a, self.b, population, folder_name, func_name, run, iteration, phenotypes
        )

class F5122subx2:

    def __init__(self, is_gray=True):
        self.is_gray = is_gray
        self.a = -5.12
        self.b = 5.11
        self.precision = 2
        self.optimum_x = 0
        self.optimum_y = 5.12 ** 2
        self.chromosome_length = calculate_genome_length(self.a, self.b, self.precision)
        self.factory = PopulationFactory(self)

    def estimate(self, chromosome_code):
        if self.is_gray:
            binary = convert_grey_to_binary(chromosome_code)
            decimal = convert_binary_to_decimal(binary, self.a, self.precision)
            return math.pow(5.12, 2) - math.pow(decimal, 2)
        else:
            decimal = convert_binary_to_decimal(chromosome_code, self.a, self.precision)
            return math.pow(5.12, 2) - math.pow(decimal, 2)

    def get_genotype_value(self, chromosome_code):
        if self.is_gray:
            binary = convert_grey_to_binary(chromosome_code)
            decimal = convert_binary_to_decimal(binary, self.a, self.precision)
            return decimal
        else:
            decimal = convert_binary_to_decimal(chromosome_code, self.a, self.precision)
            return decimal

    def get_optimal(self):
        return self.generate_optimal()

    def generate_optimal(self):
        if self.is_gray:
            binary = convert_decimal_to_binary(self.optimum_x, self.a, self.b, self.precision)
            gray = convert_binary_to_grey(binary)
            return Individual(gray, self.optimum_y)
        else:
            binary = convert_decimal_to_binary(self.optimum_x, self.a, self.b, self.precision)
            return Individual(binary, self.optimum_y)

    def generate_population(self, population_size):
        return self.factory.generate_binomial_chromosome_population(self.chromosome_length, population_size)

    def check_chromosome_success(self, individual: Individual):
        x = self.get_genotype_value(individual.code)
        y = self.estimate(individual.code)
        return (abs(y - self.optimum_y) <= DELTA) and (abs(x - self.optimum_x) <= SIGMA)

    def draw_histograms(
            self,
            population: Population,
            folder_name: str,
            func_name: str,
            run: int,
            iteration: int,
    ) -> None:
        _draw_count_ones_in_genotype_histogram(
            population, folder_name, func_name, run, iteration
        )
        _draw_fitness_histogram(population, folder_name, func_name, run, iteration)
        phenotypes = [
            self.get_genotype_value(chromosome.code)
            for chromosome in population.individuals
        ]
        _draw_phenotype_histogram(
            self.a, self.b, population, folder_name, func_name, run, iteration, phenotypes
        )