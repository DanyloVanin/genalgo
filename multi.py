import time
from multiprocessing import Pool
from constants import fh_pm, fhd_pm, fx2_pm, env
from functions import *
from selection.rws import RWS, WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K
from selection.sus import SUS, WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K
from statlib.plots import *
from program import main, main_noise
from statlib.excel import save_avg_to_excel


release_sm = [WindowRWS_2H, WindowRWS_10H, ExpScaledRWS_1_05K, ExpScaledRWS_1_005K, WindowSUS_2H, WindowSUS_10H, ExpScaledSUS_1_05K, ExpScaledSUS_1_005K]
testing_sm = [RWS, SUS]
selection_methods = testing_sm if env == 'test' else release_sm
release_functions = [
    (FHD(10), selection_methods, 'FHD_10', N, 100, 0),
    (FHD(100), selection_methods, 'FHD_10_pm', N, 100, fhd_pm),
    (Fx(0, 10.23), selection_methods, 'Fx', N, 10, 0),
    (Fx2(0, 10.23), selection_methods, 'Fx2', N, 10, 0),
    (Fx2(0, 10.23), selection_methods, 'Fx2_pm', N, 10, fx2_pm),
    (F5122subx2(-5.12, 5.11), selection_methods, '5_12_sub_X2', N, 10, 0),
    (F5122subx2(-5.12, 5.11), selection_methods, '5_12_sub_X2_pm', N, 10, fx2_pm)
]

test_functions = [
    # (FH(), selection_methods, 'FH', N, 100, 0),
    # (FH(), selection_methods, 'FH_pm', N, 100, fh_pm),
    (Fx2(0, 10.23), selection_methods, 'Fx2', N, 10, 0),
    (Fx2(0, 10.23), selection_methods, 'Fx2_pm', N, 10, fx2_pm),
]
functions = test_functions if env == 'test' else release_functions


if __name__ == '__main__':
    p_start = time.time()
    results = {}
    noise_results = {}

    with Pool(12) as p:
        res_list = p.starmap(main, functions)

        for res in res_list:
            results[res[0]] = res[1]

        noise_results['FConst'] = main_noise(selection_methods)
        save_avg_to_excel(results, noise_results)

    p_end = time.time()
    print('Program calculation (in sec.): ' + str((p_end - p_start)))
#%%
