import time

from functions import *
from program import main
from selection.rws import WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K
from selection.sus import WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K
from statlib.plots import *

# WindowSUS_2H, WindowSUS_10H,
all_functions = [ WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K,
                  WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K]

# all_functions = [ExpScaledRWS_1_05K, ExpScaledRWS_1_005K]


if __name__ == '__main__':
    p_start = time.time()
    results = {}
    noise_results = {}

    results = main(F5122subx2(is_gray=True), all_functions, 'Single_F5122subx2', DEFAULT_POPULATION_SIZE)

    # noise_results['FConst'] = main_noise(selection_methods)
    # save_avg_to_excel(results, noise_results)

    p_end = time.time()
    print('Program calculation (in sec.): ' + str((p_end - p_start)))
#%%
