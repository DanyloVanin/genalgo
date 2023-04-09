import pytest

from coding import *
from codec import *
from population_factory import PopulationFactory
from functions import *
from evoalgorithm import *

@pytest.mark.parametrize("length, population_size", [
    (10, 10),
])
def test_evolution(length, population_size):
    func = Fx2()
    factory = PopulationFactory(func)
    population = factory.generate_binomial_chromosome_population(length, population_size)
    evolution = EvoAlgorithm(population, ExpScaledRWS_1_005K(), func)
    run = evolution.run(1, 'test_fx2', 5)
    assert len(population.individuals) == population_size