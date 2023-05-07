from constants import *
from population import Population
from run import Run
from statlib.noise_stats import NoiseStats
from statlib.pressure_stats import PressureStats
from statlib.reproduction_stats import ReproductionStats
from statlib.selection_diff_stats import SelectionDiffStats


class EvoAlgorithm:
    def __init__(self, initial_population: Population, selection_function, fitness_function, mutation_enabled=False,
                 crossover_enabled=False):
        self.population: Population = initial_population
        self.population.mutation_enabled = mutation_enabled
        self.population.crossover_enabled = crossover_enabled
        self.selection_function = selection_function
        self.fitness_function = fitness_function
        # self.optimal = optimal
        self.iteration = 0

        # Statistics
        self.pressure_stats = PressureStats()
        self.reproduction_stats = ReproductionStats()
        self.selection_diff_stats = SelectionDiffStats()
        self.noise_stats = NoiseStats()
        # FIXME ! Assumption that first element of population list is the optimal one
        self.best = self.population.genotypes_list[0]
        self.pressure_stats.num_of_best.append(self.population.genotypes_list.count(self.best))
        self.pressure_stats.f_best.append(self.population.get_max_fitness())

    def run(self, run_number, folder_name, iterations_to_plot):
        is_const_function = 'FConstALL' in self.fitness_function.__class__.__name__
        if is_const_function:
            return self._run_noise(run_number, folder_name, iterations_to_plot)
        avg_fitness_list = [self.population.get_mean_fitness()]
        std_fitness_list = [self.population.get_fitness_std()]
        best_fitness_list = [self.population.get_max_fitness()]

        converged = self.population.is_converged()

        while not converged and self.iteration < MAX_ITERATIONS:
            if self.iteration < iterations_to_plot and run_number < RUNS_TO_PLOT:
                # Print genotypes and fenotypes distribution plots
                self.fitness_function.draw_histograms(
                    population=self.population,
                    folder_name=folder_name,
                    func_name=self.selection_function.__class__.__name__,
                    run=run_number + 1,
                    iteration=self.iteration + 1,
                )

            keys_before_selection = self.population.get_keys_list()
            # best_genotype = self.population.get_best_genotype()
            f = avg_fitness_list[self.iteration]

            # Selecting next population using the selection function
            self.population = self.selection_function.select(self.population)

            # Різниця відбору
            fs_parents = self.population.get_mean_fitness()
            if not is_const_function:
                self.selection_diff_stats.s_list.append(fs_parents - f)

            # Keys after selection
            keys_after_selection = self.population.get_keys_list()
            not_selected_chromosomes = set(keys_before_selection) - set(keys_after_selection)

            # Швидкість репродукції або коефіцієнт плідності RR – частка особин популяції, яких було обрано до
            # батьківського пулу.
            number_of_individuals = len(self.population.individuals)
            self.reproduction_stats.rr_list.append(1 - (len(not_selected_chromosomes) / number_of_individuals))

            # Інтенсивність відбору
            f_std_parent = std_fitness_list[self.iteration]
            self.pressure_stats.intensities.append(
                PressureStats.calculate_intensity(self.population.get_mean_fitness(), f, f_std_parent))

            # Mutation and crossover
            self.population.crossover(self.fitness_function)
            self.population.mutate(self.fitness_function)

            # Fitness STD
            f_std = self.population.get_fitness_std()
            std_fitness_list.append(f_std)
            # Average fitness
            fs = self.population.get_mean_fitness()
            avg_fitness_list.append(fs)


            # кількість (частка) копій найкращої (!!!ОПТИМАЛЬНОЇ!!!) особини.
            num_of_optimal = self.population.get_chromosomes_copies_count(self.best)
            best_genotype_not_optimal = self.population.get_best_genotype()

            self.pressure_stats.num_of_best.append(self.population.get_chromosomes_copies_count(best_genotype_not_optimal))
            self.pressure_stats.num_of_optimal.append(num_of_optimal)

            # найкраще значення здоров’я популяції. (важливо бачити, чи втрачався оптимальний розв’язок)
            self.pressure_stats.f_best.append(self.population.get_max_fitness())
            # Max fitness
            best_fitness_list.append(self.population.get_max_fitness())

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
            best_genotype = self.best
            num_best_genotype = self.population.get_chromosomes_copies_count(best_genotype)
            self.reproduction_stats.best_rr_list.append(num_best_genotype / number_of_individuals)
            if num_best_genotype >= number_of_individuals / 2 and self.pressure_stats.grl is None:
                self.pressure_stats.grli = self.iteration
                self.pressure_stats.grl = self.pressure_stats.grs[-1]
            converged = self.population.is_converged()

        # NI – кількість ітерацій до популяції, в якій всі особини однакові
        if converged:
            self.pressure_stats.NI = self.iteration

        # Print genotypes and fenotypes after the finish
        if run_number < RUNS_TO_PLOT:
            self.fitness_function.draw_histograms(
                population=self.population,
                folder_name=folder_name,
                func_name=self.selection_function.__class__.__name__,
                run=run_number + 1,
                iteration=self.iteration + 1,
            )

        # Час поглинання (takeover time) τ – мінімальна кількість поколінь, за якої ГА, застосовуючи тільки оператор
        # відбору, перетворює початкову популяцію на однорідну популяцію копій найкращої особини (початкова популяція
        # має містити одну копію цієї особини).
        self.pressure_stats.takeover_time = self.iteration
        # F_found – коефіцієнт пристосованості найкращого ланцюжка в фінальній популяції
        self.pressure_stats.f_found = self.population.get_max_fitness()
        # F_avg – середній коефіцієнт пристосованості в фінальній популяції
        self.pressure_stats.f_avg = self.population.get_mean_fitness()

        # Calculating pressure, reproduction and selection data
        self.pressure_stats.calculate()
        self.reproduction_stats.calculate()
        self.selection_diff_stats.calculate()

        # Check if Run was successful
        is_successful = self.check_success()

        return Run(avg_fitness_list, std_fitness_list, best_fitness_list, self.pressure_stats, self.reproduction_stats,
                   self.selection_diff_stats, None, is_successful)

    def check_success(self):
        ff_name = self.fitness_function.__class__.__name__
        # Для функції бінарного ланцюжка прогін є успішним, якщо
        if ff_name == 'FConstALL' or ff_name == 'FHD':
            # за наявності мутації: ідентифіковано збіжність алгоритму ТА >=90% особин фінальної популяції є копіями оптимального ланцюжка.
            if self.population.mutation_enabled:
                return self.population.is_converged() and 100*self.population.get_chromosomes_copies_count(
                    self.fitness_function.get_optimal().code) / len(
                    self.population.individuals) >= SUCCESSFUL_RUN_OPTIMAL_GENOTYPE_RATE
            else:
            # за відсутності мутації: всі особини є копіями оптимального ланцюжка
                return self.population.get_chromosomes_copies_count(self.fitness_function.get_optimal().code) == len(
                    self.population.individuals)
        else:
            # Для функцій дійсного аргумента прогін є успішним, якщо ідентифіковано збіжність алгоритму
            # та знайдеться хоча б одна особина фінальної популяції, коефіцієнт пристосованості якої є не
            # меншим за δ від його реального значення
            return self.population.is_converged() and any(
                [self.fitness_function.check_chromosome_success(p) for p in self.population.individuals])

    def _run_noise(self, run_number, folder_name, iterations_to_plot):

        converged = False

        avg_fitness_list = [self.population.get_mean_fitness()]
        std_fitness_list = [self.population.get_fitness_std()]
        best_fitness_list = [self.population.get_max_fitness()]

        while not converged and self.iteration < MAX_ITERATIONS:
            if self.iteration < iterations_to_plot and run_number < RUNS_TO_PLOT:
                # Print genotypes and fenotypes distribution plots
                self.fitness_function.draw_histograms(
                    population=self.population,
                    folder_name=folder_name,
                    func_name=self.selection_function.__class__.__name__,
                    run=run_number + 1,
                    iteration=self.iteration + 1,
                )

            keys_before_selection = self.population.get_keys_list()

            # Selecting next population using the selection function
            self.population = self.selection_function.select(self.population)

            # Keys after selection
            keys_after_selection = self.population.get_keys_list()
            not_selected_chromosomes = set(keys_before_selection) - set(keys_after_selection)

            # Швидкість репродукції або коефіцієнт плідності RR – частка особин популяції, яких було обрано до
            # батьківського пулу.
            number_of_individuals = len(self.population.individuals)
            self.reproduction_stats.rr_list.append(1 - (len(not_selected_chromosomes) / number_of_individuals))

            # Mutation and crossover
            self.population.mutate(self.fitness_function)
            self.population.crossover(self.fitness_function)

            # Max fitness
            best_fitness_list.append(self.population.get_max_fitness())

            self.iteration += 1

            converged = self.population.is_all_same_genotype()

        # NI – кількість ітерацій до популяції, в якій всі особини однакові
        if converged:
            self.noise_stats.NI = self.iteration
            self.noise_stats.conv_to = self.population.genotypes_list[0]

        self.reproduction_stats.calculate()

        # Print genotypes and fenotypes after the finish
        self.fitness_function.draw_histograms(
            population=self.population,
            folder_name=folder_name,
            func_name=self.selection_function.__class__.__name__,
            run=run_number + 1,
            iteration=self.iteration + 1,
        )

        # Check if Run was successful
        is_successful = converged

        return Run(avg_fitness_list, std_fitness_list, best_fitness_list, self.pressure_stats, self.reproduction_stats,
                   self.selection_diff_stats, self.noise_stats, is_successful)

    def calculate_noise(self, initial_population: Population, selection_function, fitness_function,
                        mutation_enabled=False, crossover_enabled=False):
        # TODO finish the function
        # Enable/disable mutation and crossover
        initial_population.mutation_enabled = mutation_enabled
        initial_population.crossover_enabled = crossover_enabled

        iteration = 0
        while not initial_population.is_converged() and iteration < MAX_RUNS:
            initial_population = selection_function.select(initial_population)
            # Mutation and convergence
            initial_population.mutate(fitness_function)
            initial_population.crossover(fitness_function)
            iteration += 1

        # Gather noise statistics
        ns = NoiseStats()

        if initial_population.is_converged():
            ns.NI = iteration
            ns.conv_to = initial_population.chromosomes[0].code[0]

        return ns
# %%
