import time
from multiprocessing import Pool

from constants import *
from functions import *
from program import main
from selection.rws import RWS, WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K
from selection.sus import SUS, WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K
from statlib.excel import save_avg_to_excel
from statlib.plots import *

release_sm = [WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K, RWS,
              WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K, SUS]
testing_sm = [RWS, SUS]
selection_methods = testing_sm if env == 'test' else release_sm

test_functions = [
    # (FConstALL(), selection_methods, 'FConstALL', DEFAULT_POPULATION_SIZE),
    # (FHD(), selection_methods, 'FHD_100', DEFAULT_POPULATION_SIZE),
    # (Fx2(), selection_methods, 'Fx2_gray', DEFAULT_POPULATION_SIZE),
    (F5122subx2(), selection_methods, 'F5122subx2_gray', DEFAULT_POPULATION_SIZE),
    # (Fx2(is_gray=False), selection_methods, 'Fx2_bin', DEFAULT_POPULATION_SIZE),
    (F5122subx2(is_gray=False), selection_methods, 'F5122subx2_bin', DEFAULT_POPULATION_SIZE),
]

functions = test_functions


if __name__ == '__main__':
    p_start = time.time()
    results = {}
    noise_results = {}

    with Pool(2) as p:
        res_list = p.starmap(main, functions)

        for res in res_list:
            results[res[0]] = res[1]

        save_avg_to_excel(results)

    p_end = time.time()
    print('Program calculation (in sec.): ' + str((p_end - p_start)))
#%%
