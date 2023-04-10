from constants import MAX_RUNS
from run import Run
from statlib.runs_stats import RunsStats
from selection.rws import WindowRWS
from evoalgorithm import EvoAlgorithm
from population import Population
from statlib.excel import save_to_excel, save_noise_to_excel
from selection.sus import WindowSUS
from statlib.plots import *
import time
import copy

def save_run_plots(ff_name, sf_name, run, run_number):
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
    save_lines_plot(ff_name, sf_name, [run.reproduction_stats.rr_list,
                                       [1 - rr for rr in run.reproduction_stats.rr_list]],
                    ['Reproduction rate', 'Loss of diversity'],
                    'repro_rate_and_loss_of_diversity' + str(run_number + 1), 'Reproduction rate + Loss of diversity',
                    run_number + 1)
    save_line_plot(ff_name, sf_name, run.reproduction_stats.best_rr_list, 'best_rr' + str(run_number + 1),
                   'best chromosome rate', run_number + 1)


def main(fitness_function, selection_functions: [], file_name, population_size, mutation_enabled=False, crossover_enabled=False):
    p_start = time.time()
    runs_dict = {}
    ff_name = fitness_function.__class__.__name__

    for selection_function in selection_functions:
        runs_dict[selection_function.__name__] = RunsStats()

    for i in range(0, MAX_RUNS):
        p = fitness_function.generate_population(population_size)

        for selection_function in selection_functions:
            sf_name = selection_function.__name__

            folder_name = file_name if file_name is not None else ff_name
            folder_name += '_mutation' if mutation_enabled else ''
            folder_name += '_crossover' if crossover_enabled else ''
            current_run = EvoAlgorithm(copy.copy(p), selection_function(), fitness_function,
                                       mutation_enabled, crossover_enabled).run(i, folder_name, 5)
            save_run_plots(folder_name, sf_name, current_run, i)
            runs_dict[sf_name].runs.append(current_run)

    for selection_function in selection_functions:
        runs_dict[selection_function.__name__].calculate()

    excel_name = file_name if file_name is not None else ff_name
    excel_name += '_mutation' if mutation_enabled else ''
    excel_name += '_crossover' if crossover_enabled else ''
    save_to_excel(runs_dict, excel_name)

    p_end = time.time()
    print('Program ' + file_name + ' calculation (in sec.): ' + str((p_end - p_start)))

    return file_name, runs_dict


def main_noise(selection_functions: []):
    p_start = time.time()
    runs_dict = {}
    file_name = 'FConstAll'

    for selection_function in selection_functions:
        runs_dict[selection_function.__name__] = RunsStats()

    for i in range(0, MAX_RUNS):
        for selection_function in selection_functions:
            sf_name = selection_function.__name__

            #ns = EvoAlgorithm.calculate_noise(sf)
            # runs_dict[sf_name].runs.append(Run(noise_stats=ns))

    for selection_function in selection_functions:
        runs_dict[selection_function.__name__].calculate_noise_stats()

    save_noise_to_excel(runs_dict, file_name)

    p_end = time.time()
    print('Noise ' + file_name + ' calculation (in sec.): ' + str((p_end - p_start)))

    return runs_dict
# %%
