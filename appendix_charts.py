import os
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Appendix Output\NHBC 8x10\Lounge_Fire_1\Lounge_Fire_1_100_Results.xlsx
def run_appendix_charts(scen_dir_path=r'Appendix Output\NHBC 8x10\Lounge_Fire_1'):
    # TODO:get name of scenario from path
    # scen_name = os.path.basename(scen_dir_path)
    # # loop through charts 100 - 1million
    # # access workbooks
    # spreadsheets = [f for f in os.listdir(scen_dir_path) if "Results" in f][::-1]
    # pd_points = []
    # cc_points = []
    # for current_sheet in spreadsheets:
    #     workbook = openpyxl.load_workbook(f'{scen_dir_path}/{current_sheet}')
    #     # plot the upper and lower mean
    #     # worksheet = workbook.active
    #     # add cc1 and cc2 together?
    #     # just find max and min from bot
    #     # add pd
    #     pd_max = max(workbook['PD1']['AD3'].value, workbook['PD2']['AD3'].value)
    #     pd_min = min(workbook['PD1']['AD3'].value, workbook['PD2']['AD3'].value)
    #     pd_avg = (workbook['PD1']['AD3'].value + workbook['PD2']['AD3'].value) / 2
    #     pd_points.append({
    #         "max": pd_max,
    #         "min": pd_min,
    #         "average": pd_avg
    #     })
        
    #     cc_max = max(workbook['CC1']['AD3'].value, workbook['CC2']['AD3'].value)
    #     cc_min = min(workbook['CC1']['AD3'].value, workbook['CC2']['AD3'].value)
    #     cc_avg = (workbook['CC1']['AD3'].value + workbook['CC2']['AD3'].value) / 2
    #     cc_points.append({
    #         "max": cc_max,
    #         "min": cc_min,
    #         "average": cc_avg
    #     })

    # draw chart
    pd_points = [{'max': 1, 'min': 0.37, 'average': 0.685}, {'max': 1, 'min': 0.33, 'average': 0.665}, {'max': 1, 'min': 0.3297, 'average': 0.6648499999999999}, {'max': 1, 'min': 0.3321, 'average': {}}, {'max': 1, 'min': 0.332276, 'average': {}}]
    cc_points = [{'max': 0.61, 'min': 0.35, 'average': 0.48}, {'max': 0.55, 'min': 0.291, 'average': 0.4205}, {'max': 0.5571, 'min': 0.3009, 'average': 0.42900000000000005}, {'max': 0.55432, 'min': 0.29991, 'average': {}}, {'max': 0.554732, 'min': 0.299536, 'average': {}}]
    # plot chart
    # Extracting max and min values
    def extract_values(data):
        max_vals = [point['max'] for point in data]
        min_vals = [point['min'] for point in data]
        return max_vals, min_vals

    pd_max_vals, pd_min_vals = extract_values(pd_points)
    cc_max_vals, cc_min_vals = extract_values(cc_points)

    x_vals = ["100", "1000", "10000", "100000", "1000000"]

    # Plotting the values
    fig, ax = plt.subplots()

    # Plotting the pd_points
    ax.plot(x_vals, pd_max_vals, 'o-', label='PD Max', color='r') 
    ax.plot(x_vals, pd_min_vals, 'o-', label='PD Min', color='b') 
    ax.fill_between(x_vals, pd_max_vals, pd_min_vals, color='yellow')

    # Plotting the cc_points
    ax.plot(x_vals, cc_max_vals, 'o-', label='CC Max', color='g') 
    ax.plot(x_vals, cc_min_vals, 'o-', label='CC Min', color='c') 
    ax.fill_between(x_vals, cc_max_vals, cc_min_vals, color='cyan', alpha=0.5)

    # Displaying the legend
    ax.legend()

    # Displaying the plot
    plt.show()
        


    pass

run_appendix_charts()
