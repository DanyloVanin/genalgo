from population import Population
from statlib.pressure_stats import PressureStats
from statlib.noise_stats import NoiseStats
from selection.rws import WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_005K, ExpScaledRWS_1_05K
from selection.sus import WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_005K, ExpScaledSUS_1_05K
from statlib.selection_diff_stats import SelectionDiffStats
from statlib.reproduction_stats import ReproductionStats
from run import Run
from functions import *
from constants import *


class EvoAlgorithm:
    def __init__(self, initial_population: Population, selection_function, fitness_function):
        self.population: Population = initial_population
        self.selection_function = selection_function
        self.fitness_function = fitness_function
        # self.optimal = optimal
        self.iteration = 0

        # Statistics
        self.pressure_stats = PressureStats()
        self.reproduction_stats = ReproductionStats()
        self.selection_diff_stats = SelectionDiffStats()
        # TODO ! Assumption that first element of population list is the optimal one
        self.best = self.population.genotypes_list[0]
        self.pressure_stats.num_of_best.append(self.population.genotypes_list.count(self.best))
        self.pressure_stats.f_best.append(self.population.get_max_fitness())

    def run(self, run_number, folder_name, iterations_to_plot):
        avg_fitness_list = [self.population.get_mean_fitness()]
        std_fitness_list = [self.population.get_fitness_std()]

        converged = self.population.is_converged()

        while not converged and self.iteration < MAX_ITERATIONS:
            if self.iteration < iterations_to_plot:
                # Print genotypes and fenotypes distribution plots
                # TODO look deeper into logic
                self.population.print_fenotypes_distribution(folder_name, self.selection_function.__class__.__name__,
                                                             run_number + 1, self.iteration + 1)
                self.population.print_genotypes_distribution(folder_name, self.selection_function.__class__.__name__,
                                                             run_number + 1, self.iteration + 1, self.fitness_function)

            keys_before_selection = self.population.get_keys_list()
            best_genotype = self.population.get_best_genotype()
            f = avg_fitness_list[self.iteration]
            # Selecting next population using the selection function
            self.population = self.selection_function.select(self.population)
            # Keys after selection
            keys_after_selection = self.population.get_keys_list()
            not_selected_chromosomes = set(keys_before_selection) - set(keys_after_selection)
            # TODO check if working
            self.population.mutate(self.fitness_function)
            self.population.crossover(self.fitness_function)
            # Fitness STD
            f_std = self.population.get_fitness_std()
            std_fitness_list.append(f_std)
            # Average fitness
            fs = self.population.get_mean_fitness()
            avg_fitness_list.append(fs)
            # Різниця відбору
            # TODO Досліджуємо на всіх функціях, крім FconstALL
            self.selection_diff_stats.s_list.append(fs - f)
            # Get number of individuals with the best genotype
            num_of_best = self.population.get_chromosomes_copies_count(best_genotype)
            # Швидкість репродукції або коефіцієнт плідності RR – частка особин популяції, яких було обрано до батьківського пулу.
            number_of_individuals = len(self.population.individuals)
            self.reproduction_stats.rr_list.append(1 - (len(not_selected_chromosomes) / number_of_individuals))
            # TODO find out more about the next statistics
            self.reproduction_stats.best_rr_list.append(num_of_best / number_of_individuals)
            # Інтенсивність відбору
            self.pressure_stats.intensities.append(
                PressureStats.calculate_intensity(self.population.get_mean_fitness(), f, f_std))
            # найкраще значення здоров’я популяції. (важливо бачити, чи втрачався оптимальний розв’язок)
            self.pressure_stats.f_best.append(self.population.get_max_fitness())
            # кількість (частка) копій найкращої (!!!ОПТИМАЛЬНОЇ!!!) особини.
            self.pressure_stats.num_of_best.append(num_of_best)
            self.iteration += 1
            # Growth Rate
            # Швидкість росту (growth rate) визначають як відношення кількості копій найкращої особини
            # в двох послідовних популяціях (якщо кілька особин є найкращими, враховуємо всіх).
            self.pressure_stats.grs.append(
                PressureStats.calculate_growth_rate(self.pressure_stats.num_of_best[self.iteration],
                                                    self.pressure_stats.num_of_best[self.iteration - 1],
                                                    self.pressure_stats.f_best[self.iteration],
                                                    self.pressure_stats.f_best[self.iteration - 1]))
            # Growth rate
            # пізню (обчислюється, коли кількість копій найкращої особини сягає 50%) швидкість росту.
            if num_of_best >= number_of_individuals / 2 and self.pressure_stats.grl is None:
                self.pressure_stats.grli = self.iteration
                self.pressure_stats.grl = self.pressure_stats.grs[-1]
            converged = self.population.is_converged()

        # NI – кількість ітерацій до популяції, в якій всі особини однакові
        if converged:
            self.pressure_stats.NI = self.iteration

        # Print genotypes and fenotypes after the finish
        self.population.print_fenotypes_distribution(folder_name, self.selection_function.__class__.__name__, run_number + 1,
                                                     self.iteration)
        self.population.print_genotypes_distribution(folder_name, self.selection_function.__class__.__name__, run_number + 1,
                                                     self.iteration + 1, self.fitness_function)
        # Час поглинання (takeover time) τ – мінімальна кількість поколінь, за якої ГА, застосовуючи тільки оператор відбору,
        # перетворює початкову популяцію на однорідну популяцію копій найкращої особини (початкова популяція має містити одну копію цієї особини).
        self.pressure_stats.takeover_time = self.iteration
        # F_found – коефіцієнт пристосованості найкращого ланцюжка в фінальній популяції
        self.pressure_stats.f_found = self.population.get_max_fitness()
        # F_avg – середній коефіцієнт пристосованості в фінальній популяції
        self.pressure_stats.f_avg = self.population.get_mean_fitness()
        self.pressure_stats.calculate()
        self.reproduction_stats.calculate()
        self.selection_diff_stats.calculate()
        is_successful = self.check_success() if converged else False
        return Run(avg_fitness_list, std_fitness_list, self.pressure_stats, self.reproduction_stats,
                   self.selection_diff_stats, None, is_successful)

    def check_success(self):
        ff_name = self.fitness_function.__class__.__name__
        if ff_name == 'FConstALL' or ff_name == 'FHD':
            if self.population.mutation_enabled:
                # TODO could possibly not be working because of strange list logic for genotypes
                return self.population.is_converged() and self.population.get_chromosomes_copies_count(self.fitness_function.get_optimal().code) / len(self.population.individuals) >= SUCCESSFUL_RUN_OPTIMAL_GENOTYPE_RATE
            else:
                return self.population.is_converged()
        else:
            self.population.is_converged() and any([self.fitness_function.check_chromosome_success(p) for p in self.population.individuals])


    # @staticmethod
    # def calculate_noise(sf):
    #     pop = Fconst().generate_population(N, 100, 0)
    #     population = Population(pop.chromosomes.copy(), pop.p_m)
    #     iteration = 0
    #     stop = 1000 if 'Disruptive' in sf.__class__.__name__ else G
    #
    #     if type(sf) == BlendedRWS or type(sf) == BlendedSUS:
    #         sf.attempts = 0
    #     elif type(sf) == WindowRWS or type(sf) == WindowSUS:
    #         sf.fh_worst_list = []
    #
    #     while not population.estimate_convergence() and iteration < stop:
    #         population = sf.select(population)
    #         iteration += 1
    #
    #     ns = NoiseStats()
    #
    #     if population.estimate_convergence():
    #         ns.NI = iteration
    #         ns.conv_to = population.chromosomes[0].code[0]
    #
    #     return ns
# %%
