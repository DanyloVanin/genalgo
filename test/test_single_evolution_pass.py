import pytest

from evoalgorithm import *


@pytest.mark.parametrize("length, population_size", [
    (10, 10),
])
def test_evolution_rws(length, population_size):
    func = Fx2()
    factory = PopulationFactory(func)
    population = factory.generate_binomial_chromosome_population(length, population_size)
    evolution = EvoAlgorithm(population, WindowRWS_2H(), func)
    run = evolution.run(1, 'test_fx2', 5)
    assert len(population.individuals) == population_size


@pytest.mark.parametrize("length, population_size", [
    (10, 10),
])
def test_evolution_sus(length, population_size):
    func = Fx2(is_gray=False)
    factory = PopulationFactory(func)
    population = factory.generate_binomial_chromosome_population(length, population_size)
    evolution = EvoAlgorithm(population, ExpScaledSUS_1_005K(), func)
    run = evolution.run(1, 'test_fx2', 5)
    assert len(population.individuals) == population_size