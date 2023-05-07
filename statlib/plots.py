import matplotlib.pyplot as plt
from constants import DEFAULT_POPULATION_SIZE
import os


def save_line_plot(fitness_func_name, func_name, data, file_name, y_label, iteration):
    # TODO should pass population size dynamically
    path = 'stats/' + fitness_func_name + '/' + str(DEFAULT_POPULATION_SIZE) + '/' + func_name + '/' + str(iteration)

    if not os.path.exists(path):
        os.makedirs(path)

    x = list(range(1, len(data) + 1))

    x_ticks_step = None
    if len(data) <= 10:
        x_ticks_step = 2
    if 10 < len(data) < 100:
        x_ticks_step = 5
    elif 100 <= len(data) < 1000:
        x_ticks_step = 20
    elif 1000 <= len(data) < 1200:
        x_ticks_step = 50
    elif 1200 <= len(data) < 3000:
        x_ticks_step = 250
    
    plt.figure(figsize=(20, 10))
    plt.plot(x, data, label=func_name)
    plt.ylabel(y_label)
    plt.xlabel('generation')
    
    if x_ticks_step is not None:
        x_ticks = list(range(1, len(data) + 1, x_ticks_step))
        x_ticks.append(len(data) + 1)
        plt.xticks(x_ticks)
        
    plt.legend()
    plt.savefig(path + '/' + file_name + '.png')
    plt.close()


def save_lines_plot(fitness_func_name, func_name, data_arr, label_arr, file_name, y_label, iteration):
    # TODO should pass population size dynamically
    path = 'stats/' + fitness_func_name + '/' + str(DEFAULT_POPULATION_SIZE) + '/' + func_name + '/' + str(iteration)

    if not os.path.exists(path):
        os.makedirs(path)

    plt.figure(figsize=(20, 10))

    x_ticks_step = None
    if len(data_arr[0]) <= 10:
        x_ticks_step = 2
    if 10 < len(data_arr[0]) < 100:
        x_ticks_step = 5
    elif 100 <= len(data_arr[0]) < 1000:
        x_ticks_step = 20
    elif 1000 <= len(data_arr[0]) < 1200:
        x_ticks_step = 50
    elif 1200 <= len(data_arr[0]) < 3000:
        x_ticks_step = 250

    for i in range(0, len(data_arr)):
        data = data_arr[i]
        label = label_arr[i]
        x = list(range(1, len(data) + 1))
        plt.plot(x, data, label=label)

    plt.ylabel(y_label)
    plt.xlabel('generation')

    if x_ticks_step is not None:
        x_ticks = list(range(1, len(data) + 1, x_ticks_step))
        x_ticks.append(len(data) + 1)
        plt.xticks(x_ticks)

    plt.legend()
    plt.savefig(path + '/' + file_name + '.png')
    plt.close()
# %%
