import matplotlib.pyplot as plt
# import matplotlib.patches as patches

def prep_data(data):
    # max([f['PD']['trapped_fraction'] for f in data[100]])
    # min([f['PD']['trapped_fraction'] for f in data[100]])
    # get keys from data
    # create object with min, max for each key
    keys = list(data.keys())
    obj = {}
    for key in keys:
        obj[key] = {}
        for scen in ['PD', 'CC']:
            key_max = max([f[scen]['trapped_fraction'] for f in data[key]])
            key_min = min([f[scen]['trapped_fraction'] for f in data[key]])
            obj[key][scen] = {'max': key_max, 'min': key_min}
    pass
    return obj
# Appendix Output\NHBC 8x10\Lounge_Fire_1\Lounge_Fire_1_100_Results.xlsx
# TODO: send in object with run data
def run_appendix_charts(points_object):

    # draw chart
    # pd_points = [{'max': 1, 'min': 0.37, 'average': 0.685}, {'max': 1, 'min': 0.33, 'average': 0.665}, {'max': 1, 'min': 0.3297, 'average': 0.6648499999999999}, {'max': 1, 'min': 0.3321, 'average': {}}, {'max': 1, 'min': 0.332276, 'average': {}}]
    # cc_points = [{'max': 0.61, 'min': 0.35, 'average': 0.48}, {'max': 0.55, 'min': 0.291, 'average': 0.4205}, {'max': 0.5571, 'min': 0.3009, 'average': 0.42900000000000005}, {'max': 0.55432, 'min': 0.29991, 'average': {}}, {'max': 0.554732, 'min': 0.299536, 'average': {}}]
    # plot chart
    # Extracting max and min values
    def extract_values(data):
        max_vals = [point['max'] for point in data]
        min_vals = [point['min'] for point in data]
        return max_vals, min_vals

    x_vals = [f"{f}" for f in list(points_object.keys())]
    pd_max_vals = [points_object[f]['PD']['max']*100 for f in list(points_object.keys())]
    pd_min_vals = [points_object[f]['PD']['min']*100 for f in list(points_object.keys())]
    cc_max_vals = [points_object[f]['CC']['max']*100 for f in list(points_object.keys())]
    cc_min_vals = [points_object[f]['CC']['min']*100 for f in list(points_object.keys())]    
    # pd_max_vals, pd_min_vals = extract_values(pd_points)
    # cc_max_vals, cc_min_vals = extract_values(cc_points)

    # x_vals = ["100", "1000", "10000", "100000", "1000000"] # get from keys

    # Plotting the values
    fig, ax = plt.subplots()

    # Plotting the pd_points
    # ax.plot(x_vals, pd_max_vals, 'o', label='PD Max', color='r') 
    # ax.plot(x_vals, pd_min_vals, 'o', label='PD Min', color='b') 
    ax.fill_between(x_vals, pd_max_vals, pd_min_vals, color='lime', label='PD')

    # Plotting the cc_points
    # ax.plot(x_vals, cc_max_vals, 'o-', label='CC Max', color='g') 
    # ax.plot(x_vals, cc_min_vals, 'o-', label='CC Min', color='c') 
    ax.fill_between(x_vals, cc_max_vals, cc_min_vals, color='cyan', alpha=0.5, label='CC')


    # Displaying the legend
    ax.legend()
    plt.tight_layout()
    # Displaying the plot
    plt.show()
        


    pass

if __name__ == "__main__":
    from appendix_data import data
    data = prep_data(data)
    run_appendix_charts(data)
