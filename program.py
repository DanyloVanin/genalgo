import time

from constants import MAX_RUNS, ITERATIONS_TO_PLOT, RUNS_TO_PLOT, LOG
from evoalgorithm import EvoAlgorithm
from statlib.excel import save_to_excel
from statlib.plots import *
from statlib.runs_stats import RunsStats


def save_run_plots(ff_name, sf_name, run, run_number):
    if 'FConstALL' not in ff_name:
        save_line_plot(ff_name, sf_name, run.avg_fitness_list, 'f_avg' + str(run_number + 1), 'f avg', run_number + 1)
        save_line_plot(ff_name, sf_name, run.std_fitness_list, 'f_std' + str(run_number + 1), 'f std', run_number + 1)
        save_line_plot(ff_name, sf_name, run.pressure_stats.intensities, 'intensity' + str(run_number + 1), 'intensity',
                       run_number + 1)
        save_line_plot(ff_name, sf_name, run.selection_diff_stats.s_list, 'selection_diff' + str(run_number + 1),
                       'selection difference', run_number + 1)
        save_lines_plot(ff_name, sf_name, [run.pressure_stats.intensities, run.selection_diff_stats.s_list],
                        ['Intensity', 'EvoAlgorithm diff'],
                    'intensity_and_sel_diff' + str(run_number + 1), 'Intensity + EvoAlgorithm diff', run_number + 1)
        save_line_plot(ff_name, sf_name, run.pressure_stats.grs, 'gr' + str(run_number + 1), 'growth rate', run_number + 1)
        save_line_plot(ff_name, sf_name, run.reproduction_stats.best_rr_list, 'best_rr' + str(run_number + 1),
                       'best chromosome rate', run_number + 1)
    save_lines_plot(ff_name, sf_name, [run.reproduction_stats.rr_list,
                                       [1 - rr for rr in run.reproduction_stats.rr_list]],
                    ['Reproduction rate', 'Loss of diversity'],
                    'repro_rate_and_loss_of_diversity' + str(run_number + 1), 'Reproduction rate + Loss of diversity',
                    run_number + 1)
    save_line_plot(ff_name, sf_name, run.best_fitness_list, 'f_best' + str(run_number + 1), 'f best', run_number + 1)

def main(fitness_function, selection_functions: [], file_name, population_size):
    p_start = time.time()
    runs_dict = {}
    ff_name = fitness_function.__class__.__name__
    calculate_noise = 'FConstALL' in ff_name
    print(f"Starting evolution for function: [Function]={ff_name}")

    # Initializing run statistics
    for selection_function in selection_functions:
        for mutation_enabled in [True, False]:
            for crossover_enabled in [True, False]:
                key = (selection_function.__name__, mutation_enabled, crossover_enabled)
                runs_dict[key] = RunsStats()

    for i in range(0, MAX_RUNS):
        p = fitness_function.generate_population(population_size)

        for selection_function in selection_functions:
            sf_name = selection_function.__name__
            for mutation_enabled in [False, True]:
                for crossover_enabled in [False, True]:
                    key = (selection_function.__name__, mutation_enabled, crossover_enabled)
                    # Creating file_name
                    folder_name = file_name if file_name is not None else ff_name
                    folder_name += '_mutation' if mutation_enabled else ''
                    folder_name += '_crossover' if crossover_enabled else ''

                    # Running the algorithm
                    population_copy = p.create_copy()
                    if LOG:
                        print(f'Run #{i}: [{ff_name}]-[{sf_name}]-[mutate: {mutation_enabled}]-[crossover: {crossover_enabled}]')
                    current_run = EvoAlgorithm(population_copy, selection_function(), fitness_function,
                                               mutation_enabled, crossover_enabled).run(i, folder_name, ITERATIONS_TO_PLOT)

                    if i < RUNS_TO_PLOT:
                        # TODO rewrite for proper and consistent scaling
                        save_run_plots(folder_name, sf_name, current_run, i)
                    runs_dict[key].runs.append(current_run)

    for selection_function in selection_functions:
        for mutation_enabled in [True, False]:
            for crossover_enabled in [True, False]:
                # TODO add assertion for number of runs being equal to number of runs
                key = (selection_function.__name__, mutation_enabled, crossover_enabled)

                runs_dict[key].calculate(calculate_noise)

    # Generating filename
    excel_name = file_name if file_name is not None else ff_name
    # TODO check this method
    save_to_excel(runs_dict, excel_name, calculate_noise)

    p_end = time.time()
    print('Program ' + file_name + ' calculation (in sec.): ' + str((p_end - p_start)))

    return file_name, runs_dict
