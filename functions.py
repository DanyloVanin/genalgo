import numpy as np

from codec import *
from individual import Individual
from population_factory import PopulationFactory
from constants import DELTA, SIGMA

class FConstALL:
    def __init__(self):
        self.factory = PopulationFactory(self)
        self.length = 100

    def estimate(self, _):
        return 100

    def get_genotype_value(self, chromosome_code):
        return 100

    def generate_optimal(self):
        # All chromosomes are good, no difference
        return Individual(np.zeros((self.length,), dtype=int), 100)

    def get_optimal(self):
        return self.generate_optimal()

    def generate_population(self, population_size):
        return self.factory.generate_binomial_chromosome_population(self.length, population_size)


class FHD:
    def __init__(self):
        self.delta = 100
        self.factory = PopulationFactory(self)
        self.length = 100

    def get_genotype_value(self, chromosome_code):
        return np.count_nonzero(chromosome_code)

    def estimate(self, chromosome):
        # k - number of non-zeroes
        k = len(chromosome) - np.count_nonzero(chromosome)
        return (len(chromosome) - k) + k * self.delta

    def generate_optimal(self):
        # optimal for FHD is all zeroes, genotype is length*delta
        return Individual('0'*self.length, self.length * self.delta)

    def get_optimal(self):
        return self.generate_optimal()

    def generate_population(self, population_size):
        return self.factory.generate_binomial_chromosome_population(self.length, population_size)


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
        return (abs(y - self.optimum_y) <= DELTA) and (abs(x - self.optimum_x)) <= SIGMA

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
        return (abs(y - self.optimum_y) <= DELTA) and (abs(x - self.optimum_x)) <= SIGMA