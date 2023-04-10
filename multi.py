import time
from multiprocessing import Pool
from constants import *
from functions import *
from selection.rws import RWS, WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K
from selection.sus import SUS, WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K
from statlib.plots import *
from program import main, main_noise
from statlib.excel import save_avg_to_excel


release_sm = [WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K, WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K]
testing_sm = [RWS, SUS]
selection_methods = testing_sm if env == 'test' else release_sm
test_functions = [
    (FHD(), selection_methods, 'FHD_100', DEFAULT_POPULATION_SIZE, False, False),
    (FHD(), selection_methods, 'FHD_100', DEFAULT_POPULATION_SIZE, True, False),
    (FHD(), selection_methods, 'FHD_100', DEFAULT_POPULATION_SIZE, False, True),
    (FHD(), selection_methods, 'FHD_100', DEFAULT_POPULATION_SIZE, True, True),
    (Fx2(), selection_methods, 'Fx2', DEFAULT_POPULATION_SIZE, False, False),
    (Fx2(), selection_methods, 'Fx2', DEFAULT_POPULATION_SIZE, True, False),
    (Fx2(), selection_methods, 'Fx2', DEFAULT_POPULATION_SIZE, False, True),
    (Fx2(), selection_methods, 'Fx2', DEFAULT_POPULATION_SIZE, True, True),
    (F5122subx2(), selection_methods, 'F5122subx2', DEFAULT_POPULATION_SIZE, False, False),
    (F5122subx2(), selection_methods, 'F5122subx2', DEFAULT_POPULATION_SIZE, True, False),
    (F5122subx2(), selection_methods, 'F5122subx2', DEFAULT_POPULATION_SIZE, False, True),
    (F5122subx2(), selection_methods, 'F5122subx2', DEFAULT_POPULATION_SIZE, True, True),
]
functions = test_functions


if __name__ == '__main__':
    p_start = time.time()
    results = {}
    noise_results = {}

    with Pool(12) as p:
        res_list = p.starmap(main, functions)

        for res in res_list:
            results[res[0]] = res[1]

        # noise_results['FConst'] = main_noise(selection_methods)
        # save_avg_to_excel(results, noise_results)

    p_end = time.time()
    print('Program calculation (in sec.): ' + str((p_end - p_start)))
#%%
