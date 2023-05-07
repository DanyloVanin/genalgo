import time

from functions import *
from program import main
from selection.rws import WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K, RWS
from selection.sus import WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K, SUS
from statlib.plots import *

# WindowSUS_2H, WindowSUS_10H,
all_functions = [WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K, RWS,
                 WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K, SUS]

all_functions = [SUS]

if __name__ == '__main__':
    p_start = time.time()
    results = {}
    noise_results = {}

    results = main(FConstALL(), all_functions, 'Single_FHD_bin', DEFAULT_POPULATION_SIZE)

    # noise_results['FConst'] = main_noise(selection_methods)
    # save_avg_to_excel(results, noise_results)

    p_end = time.time()
    print('Program calculation (in sec.): ' + str((p_end - p_start)))
# %%
