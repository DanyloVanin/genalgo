from constants import DEFAULT_POPULATION_SIZE, RUNS_TO_PLOT
import xlsxwriter
import math
import os


def save_to_excel_internal(sheet, dictionary, col_num=1, row_num=2, print_keys=True):
    for key, value in dictionary.items():
        if print_keys:
            sheet.write(row_num - 1, col_num, key)
        if value[0] is None:
            sheet.write(row_num, col_num, 'None')
        elif isinstance(value[0],str):
            sheet.write_column(row_num, col_num, value)
        elif math.isnan(value[0]):
            sheet.write(row_num, col_num, 'NaN')
        elif math.isinf(value[0]):
            sheet.write(row_num, col_num, 'Inf')
        else:
            sheet.write_column(row_num, col_num, value)
        col_num += 1

    return col_num


def save_to_excel(runs_dictionary, selection_func_name, calculate_noise=False):
    path = 'stats/' + selection_func_name + '_Stats/' + str(DEFAULT_POPULATION_SIZE)

    if not os.path.exists(path):
        os.makedirs(path)

    workbook = xlsxwriter.Workbook(path + '/' + selection_func_name + '_' + str(DEFAULT_POPULATION_SIZE) + '_data.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.name = str(DEFAULT_POPULATION_SIZE)
    func_num = 1
    items_len = len(runs_dictionary)
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'fg_color': 'yellow'})

    for func_key, runs_stats in runs_dictionary.items():
        # Generate function name
        func_name = func_key[0]
        func_name += '_mutation' if func_key[1] else ''
        func_name += '_crossover' if func_key[2] else ''

        worksheet.write(func_num + 1, 0, func_name)
        worksheet.write(func_num + items_len + 3, 0, func_name)
        last_col_num = 1
        i = 0

        for run in runs_stats.runs[:]:
            start_range = last_col_num
            if not calculate_noise:
                last_col_num = save_to_excel_internal(worksheet, run.pressure_stats.as_dict(), last_col_num, func_num + 1,
                                                      func_num == 1)
            last_col_num = save_to_excel_internal(worksheet, run.reproduction_stats.as_dict(), last_col_num,
                                                  func_num + 1, func_num == 1)
            if not calculate_noise:
                last_col_num = save_to_excel_internal(worksheet, run.selection_diff_stats.as_dict(), last_col_num,
                                                      func_num + 1, func_num == 1)
            if calculate_noise:
                last_col_num = save_to_excel_internal(worksheet, run.noise_stats.as_dict(), last_col_num,
                                                      func_num + 1, func_num == 1)
            i = i + 1
            if func_num == 1:
                worksheet.merge_range(0, start_range, 0, last_col_num - 1, 'Run ' + str(i), merge_format)

        start_range = last_col_num
        last_col_num = save_to_excel_internal(worksheet, runs_stats.as_dict(), last_col_num, func_num + 1,
                                              func_num == 1)
        if func_num == 1:
            worksheet.merge_range(0, start_range, 0, last_col_num - 1, 'Avg values', merge_format)
        last_col_num = save_to_excel_internal(worksheet, runs_stats.as_dict(), 1, func_num + items_len + 3,
                                              func_num == 1)
        if func_num == 1:
            worksheet.merge_range(func_num + items_len + 1, 1, func_num + items_len + 1, last_col_num - 1, 'Avg values',
                                  merge_format)

        func_num = func_num + 1

    workbook.close()


# def save_noise_to_excel(runs_dictionary, selection_func_name):
#     path = 'stats/' + selection_func_name + '/' + str(DEFAULT_POPULATION_SIZE)
#
#     if not os.path.exists(path):
#         os.makedirs(path)
#
#     workbook = xlsxwriter.Workbook(path + '/' + selection_func_name + '_' + str(DEFAULT_POPULATION_SIZE) + '_data.xlsx')
#     worksheet = workbook.add_worksheet()
#     worksheet.name = str(DEFAULT_POPULATION_SIZE)
#     func_num = 1
#     items_len = len(runs_dictionary)
#     merge_format = workbook.add_format({
#         'bold': 1,
#         'border': 1,
#         'align': 'center',
#         'fg_color': 'yellow'})
#
#     for func_name, runs_stats in runs_dictionary.items():
#         worksheet.write(func_num + 1, 0, func_name)
#         worksheet.write(func_num + items_len + 3, 0, func_name)
#         last_col_num = 1
#         i = 0
#
#         for run in runs_stats.runs:
#             start_range = last_col_num
#             last_col_num = save_to_excel_internal(worksheet, run.noise_stats.as_dict(), last_col_num, func_num + 1,
#                                                   func_num == 1)
#             i = i + 1
#             if func_num == 1:
#                 worksheet.merge_range(0, start_range, 0, last_col_num - 1, 'Run ' + str(i), merge_format)
#
#         start_range = last_col_num
#         last_col_num = save_to_excel_internal(worksheet, runs_stats.as_noise_dict(), last_col_num, func_num + 1,
#                                               func_num == 1)
#         if func_num == 1:
#             worksheet.merge_range(0, start_range, 0, last_col_num - 1, 'Avg values', merge_format)
#         last_col_num = save_to_excel_internal(worksheet, runs_stats.as_noise_dict(), 1, func_num + items_len + 3,
#                                               func_num == 1)
#         if func_num == 1:
#             worksheet.merge_range(func_num + items_len + 1, 1, func_num + items_len + 1, last_col_num - 1, 'Avg values',
#                                   merge_format)
#
#         func_num = func_num + 1
#
#     workbook.close()


def save_avg_to_excel(func_runs_dictionary):
    path = 'stats/AVG/' + str(DEFAULT_POPULATION_SIZE)
    if not os.path.exists(path):
        os.makedirs(path)
    workbook = xlsxwriter.Workbook(path + '/data.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.name = str(DEFAULT_POPULATION_SIZE)
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'fg_color': 'yellow'})
    row = 1
    for fitness_func, runs_dictionary in func_runs_dictionary.items():
        func_num = 1
        for func_name, runs_stats in runs_dictionary.items():
            worksheet.write(row + 1, 0, func_name)
            last_col_num = save_to_excel_internal(worksheet, runs_stats.as_dict(), 1, row + 1, func_num == 1)
            if func_num == 1:
                worksheet.merge_range(row - 1, 1, row - 1, last_col_num - 1, fitness_func, merge_format)
            func_num = func_num + 1
            row = row + 1
        row = row + 3
    # for fitness_func, runs_dictionary in noise_runs_dictionary.items():
    #     func_num = 1
    #     for func_name, runs_stats in runs_dictionary.items():
    #         worksheet.write(row + 1, 0, func_name)
    #         last_col_num = save_to_excel_internal(worksheet, runs_stats.as_noise_dict(), 1, row + 1, func_num == 1)
    #         if func_num == 1:
    #             worksheet.merge_range(row - 1, 1, row - 1, last_col_num - 1, fitness_func, merge_format)
    #         func_num = func_num + 1
    #         row = row + 1
    #     row = row + 3
    workbook.close()
# %%
