import time
from constants import *
from functions import *
from selection.rws import RWS, WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K
from selection.sus import SUS, WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K
from statlib.plots import *
from program import main, main_noise
from statlib.excel import save_avg_to_excel

all_functions = [WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K,
                 WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K]


if __name__ == '__main__':
    p_start = time.time()
    results = {}
    noise_results = {}

    results = main(FHD(), all_functions, 'Single_FH100', DEFAULT_POPULATION_SIZE)

    # noise_results['FConst'] = main_noise(selection_methods)
    # save_avg_to_excel(results, noise_results)

    p_end = time.time()
    print('Program calculation (in sec.): ' + str((p_end - p_start)))
#%%
