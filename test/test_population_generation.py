import pytest

from functions import *


@pytest.mark.parametrize("length, population_size", [
    (100, 10),
    (10, 10),
    (10, 100),
])
def test_fconst_population(length, population_size):
    func = FConstALL()
    factory = PopulationFactory(func)
    population = factory.generate_binomial_chromosome_population(length, population_size)
    assert len(population.individuals) == population_size


@pytest.mark.parametrize("length, population_size", [
    (100, 10),
    (10, 10),
    (10, 100),
])
def test_fhd_population(length, population_size):
    func = FHD()
    factory = PopulationFactory(func)
    population = factory.generate_binomial_chromosome_population(length, population_size)
    assert len(population.individuals) == population_size


@pytest.mark.parametrize("length, population_size", [
    (10, 10),
    (10, 100),
])
def test_fx2_population_binary(length, population_size):
    func = Fx2(is_gray=False)
    factory = PopulationFactory(func)
    population = factory.generate_binomial_chromosome_population(length, population_size)
    assert len(population.individuals) == population_size


@pytest.mark.parametrize("length, population_size", [
    (10, 10),
    (10, 100),
])
def test_fx2_population_gray(length, population_size):
    func = Fx2()
    factory = PopulationFactory(func)
    population = factory.generate_binomial_chromosome_population(length, population_size)
    assert len(population.individuals) == population_size


@pytest.mark.parametrize("length, population_size", [
    (10, 10),
    (10, 100),
])
def test_f5122subx2_population_binary(length, population_size):
    func = F5122subx2(is_gray=False)
    factory = PopulationFactory(func)
    population = factory.generate_binomial_chromosome_population(length, population_size)
    assert len(population.individuals) == population_size


@pytest.mark.parametrize("length, population_size", [
    (10, 10),
    (10, 100),
])
def test_f5122subx2_population_gray(length, population_size):
    func = F5122subx2()
    factory = PopulationFactory(func)
    population = factory.generate_binomial_chromosome_population(length, population_size)
    assert len(population.individuals) == population_size