# import openpyxl
import pandas as pd
import matplotlib.pyplot as plt
from constants import chart_config, compute_y_axis_bounds

# with open(excel_file, 'r') as:
def generate_dataset_from_curve(path_to_file, number_of_runs):

    df = pd.read_excel(path_to_file)

    weights = list(df['Probability'].values)
    population = list(df['Time'].values)
    n = 0
    list_of_numbers = []
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
    pre_movement_numbers =[]
    for i in population:
        n = list_of_numbers[index]
        while n > 0:
            pre_movement_numbers.append(i)
            n = n-1
        index=index+1

    def find_multiplier_more_than_one(start):
        multiplier = 1
        current = start
        
        while current <= 1:
            multiplier *= 10
            current = start * multiplier
        return multiplier
    
    with plt.rc_context(chart_config):
        # TODO: legend and ticks to be cleaned
        fig, ax1 = plt.subplots()


        ax1.hist(pre_movement_numbers, bins=len(df['Time']))
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Frequency')
        ax1.set_xlim([0, df['Time'].max()])
        # find_multiplier_more_than_one(start=max(list_of_numbers))
        maxY_ax1, minY_ax1 = compute_y_axis_bounds(max_axis_array=[max(list_of_numbers)], min_axis_array=[0], to_the_nearest=10)
        diff = max(list_of_numbers) / maxY_ax1
        ax1.set_ylim([0, maxY_ax1])
        
        ax2 = ax1.twinx()

        ax2.set_ylim([0, max(weights) / diff])
        ax2.set_ylabel('Probability')
        ax2.plot(population, weights, 'orange', linewidth=1.0)
        plt.tight_layout()
        # plt.savefig(f'data/escape_prob_chart.png', format='png', dpi=1200)
        plt.show()
        pass




path_to_file = 'data\escapeProbability.xlsx'
generate_dataset_from_curve(path_to_file, 1000) #100000
