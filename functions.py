import numpy as np
from chromosome import Chromosome
from constants import DELTA, SIGMA
from population import Population
from population_factory import PopulationFactory
from coding import *


# TODO add needed functions

class FHD:
    def __init__(self, delta):
        self.delta = delta

    @staticmethod
    def get_genotype_value(chromosome_code):
        return np.count_nonzero(chromosome_code)

    def estimate(self, chromosome):
        # k - number of non-zeroes
        k = len(chromosome) - np.count_nonzero(chromosome)
        return (len(chromosome) - k) + k * self.delta

    def generate_optimal(self, length):
        # optimal for FHD is all zeroes, genotype is length*delta
        return Chromosome(np.zeros((length,), dtype=int), length * self.delta)

    def get_optimal(self, n, l, p_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, i):
        return PopulationFactory(self).generate_population_fhd(n, l, p_m, i)


class FConstALL:
    @staticmethod
    def estimate(chromosome):
        return 100

    @staticmethod
    def generate_optimal(length):
        # All chromosomes are good, no difference
        return [Chromosome(np.zeros((length,), dtype=int), length)]

    def generate_population(self, n, l, p_m):
        chromosomes = self.generate_optimal(l) * int(n / 2) #TODO need to look into it
        return Population(chromosomes, p_m)


class Fx:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def estimate(self, chromosome):
        return decode(chromosome, self.a, self.b, len(chromosome))

    def get_genotype_value(self, chromosome_code):
        return decode(chromosome_code, self.a, self.b, len(chromosome_code))

    def generate_optimal(self, length):
        gray_code = encode(self.b, self.a, self.b, length)
        return Chromosome(gray_code, self.b)

    def get_optimal(self, n, l, p_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, i):
        return PopulationFactory(self).generate_population_fx(n, l, p_m, i)

    def check_chromosome_success(self, ch: Chromosome):
        return ((self.b - ch.fitness) <= DELTA) and (decode(ch.code, self.a, self.b, len(ch.code)) - self.b) <= SIGMA


class Fx2(Fx):
    def estimate(self, chromosome):
        return math.pow(decode(chromosome, self.a, self.b, len(chromosome)), 2)

    def generate_optimal(self, length):
        gray_code = encode(self.b, self.a, self.b, length)
        return Chromosome(gray_code, math.pow(self.b, 2))

    def get_optimal(self, n, l, p_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, i):
        return PopulationFactory(self).generate_population_fx2(n, l, p_m, i)

    def check_chromosome_success(self, ch: Chromosome):
        return ((self.b ** 2 - ch.fitness) <= DELTA) and (
                decode(ch.code, self.a, self.b, len(ch.code)) - self.b) <= SIGMA


class Fx4(Fx):
    def estimate(self, chromosome):
        return math.pow(decode(chromosome, self.a, self.b, len(chromosome)), 4)

    def generate_optimal(self, length):
        gray_code = encode(self.b, self.a, self.b, length)
        return Chromosome(gray_code, math.pow(self.b, 4))

    def get_optimal(self, n, l, p_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, i):
        return PopulationFactory(self).generate_population_fx4(n, l, p_m, i)

    def check_chromosome_success(self, ch: Chromosome):
        return ((self.b ** 4 - ch.fitness) <= DELTA) and (
                decode(ch.code, self.a, self.b, len(ch.code)) - self.b) <= SIGMA


class F2x2(Fx):
    def estimate(self, chromosome):
        return 2 * math.pow(decode(chromosome, self.a, self.b, len(chromosome)), 2)

    def generate_optimal(self, length):
        gray_code = encode(self.b, self.a, self.b, length)
        return Chromosome(gray_code, math.pow(self.b, 2))

    def get_optimal(self, n, l, p_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, i):
        return PopulationFactory(self).generate_population_f2x2(n, l, p_m, i)

    def check_chromosome_success(self, ch: Chromosome):
        return ((2 * self.b ** 2 - ch.fitness) <= DELTA) and (
                decode(ch.code, self.a, self.b, len(ch.code)) - self.b) <= SIGMA


class F5122subx2:
    @staticmethod
    def estimate(chromosome):
        return math.pow(5.12, 2) - math.pow(decode(chromosome, -5.11, 5.12, len(chromosome)), 2)

    @staticmethod
    def get_genotype_value(chromosome_code):
        return decode(chromosome_code, -5.11, 5.12, len(chromosome_code))

    @staticmethod
    def get_optimal(n, l, p_m, i):
        return F5122subx2.generate_optimal(l)

    @staticmethod
    def generate_optimal(length):
        x = 0
        gray_code = encode(x, -5.11, 5.12, length)
        return Chromosome(gray_code, math.pow(5.12, 2))

    def generate_population(self, n, l, p_m, i):
        return PopulationFactory(self).generate_population_f512(n, l, p_m, i)

    @staticmethod
    def check_chromosome_success(ch: Chromosome):
        return ((math.pow(5.12, 2) - ch.fitness) <= DELTA) and abs(decode(ch.code, -5.11, 5.12, len(ch.code))) <= SIGMA


class F5124subx4:
    @staticmethod
    def estimate(chromosome):
        return math.pow(5.12, 4) - math.pow(decode(chromosome, -5.11, 5.12, len(chromosome)), 4)

    @staticmethod
    def get_genotype_value(chromosome_code):
        return decode(chromosome_code, -5.11, 5.12, len(chromosome_code))

    @staticmethod
    def get_optimal(n, l, p_m, i):
        return F5124subx4.generate_optimal(l)

    @staticmethod
    def generate_optimal(length):
        x = 0
        gray_code = encode(x, -5.11, 5.12, length)
        return Chromosome(gray_code, math.pow(5.12, 4))

    def generate_population(self, n, l, p_m, i):
        return PopulationFactory(self).generate_population_f514(n, l, p_m, i)

    @staticmethod
    def check_chromosome_success(ch: Chromosome):
        return ((math.pow(5.12, 4) - ch.fitness) <= DELTA) and abs(decode(ch.code, -5.11, 5.12, len(ch.code))) <= SIGMA
# %%
