# import openpyxl
import pandas as pd
from collections import Counter

def generate_dataset_from_curve(path_to_file, number_of_runs):

    df = pd.read_excel(path_to_file)

    weights = list(df['Probability'].values)
    population = list(df['Time'].values)
    n = 0
    list_of_numbers = [] # adjusted counts
    
    for i in weights:
        list_of_numbers.append(round(i*number_of_runs))
        n = n+1

    if sum(list_of_numbers) > number_of_runs:
        difference = sum(list_of_numbers) - number_of_runs
        upper = round(difference/2)
        lower = difference - upper
        index = 1
        while upper > 0:
            if list_of_numbers[-index] == 0:
                index = index + 1
            else:
                list_of_numbers[-index] = list_of_numbers[-index]-1
                index = index + 1
                upper = upper - 1
        index = 0
        while lower > 0:
            if list_of_numbers[index] == 0:
                index = index + 1
            else:
                list_of_numbers[index] = list_of_numbers[index]-1
                index = index + 1
                lower = lower - 1   
    elif sum(list_of_numbers) < number_of_runs:
        difference = number_of_runs - sum(list_of_numbers)
        upper = round(difference/2)
        lower = difference - upper
        index = 50
        while upper > 0:
            list_of_numbers[index] = list_of_numbers[index]+1
            index = index + 1
            upper = upper - 1
        index = 49
        while lower > 0:
            list_of_numbers[index] = list_of_numbers[index]+1
            index = index - 1
            lower = lower - 1  

    

    index = 0
    pre_movement_numbers =[] # list of time values based on curve
    for i in population:
        n = list_of_numbers[index]
        while n > 0:
            pre_movement_numbers.append(i)
            n = n-1
        index=index+1

    return pre_movement_numbers, population, weights, list_of_numbers

def chart_dataset_from_curve(pre_movement_numbers, population, weights, list_of_numbers):
    import matplotlib.pyplot as plt
    from constants import chart_config, compute_y_axis_bounds
    
    with plt.rc_context(chart_config):
        # TODO: legend and ticks to be cleaned
        fig, ax1 = plt.subplots()

        ax1.hist(pre_movement_numbers, bins=len(population))
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Frequency')
        ax1.set_xlim([0, max(population)])
        maxY_ax1, minY_ax1 = compute_y_axis_bounds(max_axis_array=[max(list_of_numbers)], min_axis_array=[0], to_the_nearest=10)
        diff = max(list_of_numbers) / maxY_ax1
        ax1.set_ylim([0, maxY_ax1])      
        ax2 = ax1.twinx()
        ax2.set_ylim([0, max(weights) / diff])
        ax2.set_ylabel('Probability')
        ax2.plot(population, weights, 'orange', linewidth=1.0)
        plt.tight_layout()
        plt.show()

def return_dataset_dict_from_curve(path_to_file='data\escapeProbability.xlsx', number_of_runs=100): # should be specific to current folder!
    pre_movement_numbers, population, weights, list_of_numbers = generate_dataset_from_curve(path_to_file, number_of_runs)
    return dict(Counter(pre_movement_numbers))


if __name__ == '__main__':
    # path_to_file = 'data\escapeProbability.xlsx'
    # pre_movement_numbers, population, weights, list_of_numbers = generate_dataset_from_curve(path_to_file, 10000) #100000
    # print(dict(Counter(pre_movement_numbers)))
    # # pop
    # chart_dataset_from_curve(pre_movement_numbers, population, weights, list_of_numbers)
    print(return_dataset_dict_from_curve(path_to_file='data\escapeProbability.xlsx', number_of_runs=100))
