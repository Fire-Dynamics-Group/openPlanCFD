''''
TODO: visibility critera chart for each model - compare to actual data
TODO: starting position (max TD) chart for each model - compare to actual data
LATER: need to access prob data 
'''
import numpy as np
import matplotlib.pyplot as plt
# TODO: save all 4 charts with model name
def visibility_chart(model_data, model_name='PD1', output_dir='CFD Test Output\Roneo Corner - Smallest Flat\Kitchen_Fire_1'):
    # read from excel
    N = 2
    ind = np.arange(N) # the x locations for the groups
    width = 0.35
    fig = plt.figure()
    ax = fig.add_axes([0.1,0.175,0.8,0.8])
    ax.bar(0, round(len([f for f in model_data['Visibility Tenability Limit'] if f == 2])/100), width, color='cornflowerblue')
    ax.bar(1, round(len([f for f in model_data['Visibility Tenability Limit'] if f == 3])/100), width, color='cornflowerblue')
    ax.hlines(y=70, xmin=-0.25, xmax=0.25, color='red', linestyle='--')
    ax.hlines(y=30, xmin=0.75, xmax=1.25, color='red', linestyle='--')
    ax.set_ylabel('%', rotation=90)
    ax.set_xticks(ind, ('2m', '3m'))
    ax.set_yticks(np.arange(0, 120, 20))
    title = f'Visibility - {model_name}'
    chart_path = f'{output_dir}/{title}_chart.png'
    plt.savefig(chart_path, format='png', dpi=1200)
    if __name__ == "__main__":
        plt.show()  
    plt.close()

    return chart_path
    # read from orange line - not sure how to get what it 'should' be?
    pass
from collections import Counter
def start_room_chart(model_data, model_name='PD1', output_dir='CFD Test Output\Roneo Corner - Smallest Flat\Kitchen_Fire_1'):
    # read from excel
    # TODO: yellow lines 70% 2; 30% 3
    N = 2
    room_col = model_data['Starting Location']
    room_list = list(set(room_col))
    room_count = Counter(room_col)
    ind = np.arange(len(room_list)) # the n*rooms locations for the groups

    num_kitchens = len([f for f in room_list if 'Kitchen' in f])
    num_bedrooms = len([f for f in room_list if 'Bedroom' in f])
    num_lounges = len([f for f in room_list if 'Living' in f])
    # Kit_Prob
    Kit_Prob = round(0.03 / num_kitchens, 2)
    # Bed_Prob
    Bed_Prob = round(0.51 / num_bedrooms, 2)
    # Liv_Prob
    Liv_Prob = round(0.46 / num_lounges, 2)
    width = 0.2
    fig = plt.figure()
    ax = fig.add_axes([0.1,0.175,0.8,0.8])
    for idx, room in enumerate(room_list):
        ax.bar(ind[idx], round(room_count[room]/100), width, color='cornflowerblue')
        if 'Kitchen' in room:
            prob = Kit_Prob
        elif 'Bedroom' in room:
            prob = Bed_Prob
        else:
            prob = Liv_Prob
        ax.hlines(y=prob*100, xmin=ind[idx]-0.25, xmax=ind[idx]+0.25, color='red', linestyle='--')
    ax.set_ylabel('%', rotation=90)
    ax.set_xticks(ind, room_list)
    ax.set_yticks(np.arange(0, 120, 20))
    title = f'Starting Location - {model_name}'
    chart_path = f'{output_dir}/{title}_chart.png'
    plt.savefig(chart_path, format='png', dpi=1200)
    # if __name__ == "__main__":
    #     plt.show()  
    plt.close() 

    return chart_path 
    # plt.show()
    # read from orange line - not sure how to get what it 'should' be?
    pass



from stage_three_read_data import return_scen_excel
import os
def run_scen_misc_charts(output_dir='CFD Test Output\Roneo Corner - Smallest Flat\Kitchen_Fire_1'):
    # output_dir='CFD Test Output\Roneo Corner - Smallest Flat\Kitchen_Fire_1'
    # path_to_results_file='CFD Test Output\Roneo Corner - Smallest Flat\Kitchen_Fire_1\Kitchen_Fire_1_Results.xlsx'
    scen_name = os.path.basename(output_dir)
    scen_object, scen_workbook = return_scen_excel(path_to_results_file=f'{output_dir}/{scen_name}_Results.xlsx')
    chart_paths = {}
    chart_paths['start_room'] = {}
    chart_paths['vis'] = {}
    for model in ['PD1', 'PD2', 'CC1', 'CC2']:
        chart_paths['start_room'][model] = start_room_chart(scen_object[model], model_name=model, output_dir=output_dir)
        chart_paths['vis'][model] = visibility_chart(scen_object[model], model_name=model, output_dir=output_dir)

    return chart_paths

if __name__ == "__main__":
    run_scen_misc_charts()
# from escape_probability import generate_dataset_from_curve
# pre_movement_numbers, population, weights, list_of_numbers = generate_dataset_from_curve()
