import matplotlib.pyplot as plt
# import matplotlib.patches as patches

def prep_data(data):
    # max([f['PD']['trapped_fraction'] for f in data[100]])
    # min([f['PD']['trapped_fraction'] for f in data[100]])
    # get keys from data
    # create object with min, max for each key
    keys = list(data.keys())
    obj = {}
    for key in sorted(keys):
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

    x_vals = [f"{f}" for f in list(points_object.keys())]
    pd_max_vals = [points_object[f]['PD']['max']*100 for f in list(points_object.keys())]
    pd_min_vals = [points_object[f]['PD']['min']*100 for f in list(points_object.keys())]
    cc_max_vals = [points_object[f]['CC']['max']*100 for f in list(points_object.keys())]
    cc_min_vals = [points_object[f]['CC']['min']*100 for f in list(points_object.keys())] 

    pd_avg_vals = [(points_object[f]['PD']['max'] + points_object[f]['PD']['min'])/2*100 for f in list(points_object.keys())]
    cc_avg_vals = [(points_object[f]['CC']['max'] + points_object[f]['CC']['min'])/2*100 for f in list(points_object.keys())]   

    fig, ax = plt.subplots()

    ax.fill_between(x_vals, pd_max_vals, pd_min_vals, color='lime', alpha=0.5, label='PD')

    ax.fill_between(x_vals, cc_max_vals, cc_min_vals, color='cyan', alpha=0.5, label='CC')
    ax.plot(x_vals, pd_avg_vals, color='black', linestyle='--')
    ax.plot(x_vals, cc_avg_vals, color='black', linestyle='--')

    ax.legend()
    plt.tight_layout()
    if __name__ == "__main__":
        plt.show()
    else:
        plt.show()
        # should save locally
        


    pass
def compare_appendix_charts(sets_of_points_object):
    def return_chart_vals(points_object):
        x_vals = [f"{f}" for f in list(points_object.keys())]
        pd_max_vals = [points_object[f]['PD']['max']*100 for f in list(points_object.keys())]
        pd_min_vals = [points_object[f]['PD']['min']*100 for f in list(points_object.keys())]
        cc_max_vals = [points_object[f]['CC']['max']*100 for f in list(points_object.keys())]
        cc_min_vals = [points_object[f]['CC']['min']*100 for f in list(points_object.keys())] 

        pd_avg_vals = [(points_object[f]['PD']['max'] + points_object[f]['PD']['min'])/2*100 for f in list(points_object.keys())]
        cc_avg_vals = [(points_object[f]['CC']['max'] + points_object[f]['CC']['min'])/2*100 for f in list(points_object.keys())]   
        return x_vals, pd_max_vals, pd_min_vals, cc_max_vals, cc_min_vals, pd_avg_vals, cc_avg_vals

    fig, ax = plt.subplots()

    pd_cols = ['blue', 'lime']   
    cc_cols = ['red', 'cyan'] 

    for idx, points_object in enumerate(sets_of_points_object):
        x_vals, pd_max_vals, pd_min_vals, cc_max_vals, cc_min_vals, pd_avg_vals, cc_avg_vals = return_chart_vals(points_object)

        ax.fill_between(x_vals, pd_max_vals, pd_min_vals, color=pd_cols[idx], alpha=0.5, label=f'PD {idx + 1}')

        ax.fill_between(x_vals, cc_max_vals, cc_min_vals, color=cc_cols[idx], alpha=0.5, label=f'CC {idx + 1}')

        # ax.plot(x_vals, pd_avg_vals, color='black', linestyle='--')
        # ax.plot(x_vals, cc_avg_vals, color='black', linestyle='--')

    ax.legend()
    plt.tight_layout()
    if __name__ == "__main__":
        plt.show()
    else:
        plt.show()
        # should save locally
        


    pass

if __name__ == "__main__":
    from appendix_data import data, one_k_data
    from NHBC_8x10_50000x1000 import data_1k_8x10
    from NHBC_12x16_10000x1000 import data_1k_12x16
    data = prep_data(data)
    # run_appendix_charts(data)
    # data_1k_8x10
    compare_appendix_charts(sets_of_points_object= [data, data_1k_8x10])
    # run_appendix_charts(data_1k_8x10)
    # run_appendix_charts(data_1k_12x16)
