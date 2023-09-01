import numpy as np
import matplotlib.pyplot as plt

from constants import chart_config

def save_chart_high_res(name_of_chart, new_dir_path, dpi=1200):
    plt.savefig(f'{new_dir_path}/{name_of_chart}_chart.png', format='png', dpi=dpi)
# TODO: send in real figures from results
# save figure as png
def run_bar_chart(pd, cc, results_path='Report Template'):
    with plt.rc_context(chart_config):

        escaped = [(pd["escaped"])*100, (cc["escaped"])*100]
        trapped = [(pd["trapped"])*100, (cc["trapped"])*100] # need to minus trapped and harmed from this
        trapped_and_harmed = [pd["trapped_and_harmed"]*100, cc["trapped_and_harmed"]*100]
        # menMeans = (20, 35)
        # womenMeans = (25, 32)
        N = len(escaped)

        trapped_bottom = []
        for idx, f in enumerate(escaped):
            trapped_bottom.append(f)        
        t_h_bottom = []
        for idx, f in enumerate(escaped):
            t_h_bottom.append(f + trapped[idx])

        ind = np.arange(N) # the x locations for the groups
        width = 0.35
        fig = plt.figure()
        ax = fig.add_axes([0.1,0.175,0.8,0.8])
        ax.bar(ind, escaped, width, color='cornflowerblue')
        ax.bar(ind, trapped, width,bottom=trapped_bottom, color='gray')
        ax.bar(ind, trapped_and_harmed, width,bottom=t_h_bottom, color='darkorange')
        ax.set_ylabel('Percentage (%)')
        # ax.set_title('Scores by group and gender')
        ax.set_xticks(ind, ('Proposed Design', 'Code Compliant Design'))
        ax.set_yticks(np.arange(0, 110, 10))

        cols = 3
        bbox_position = (0.5,-0.2)
        ax.legend(bbox_to_anchor =bbox_position, ncol=cols,loc='lower center', fontsize = 8, frameon=False, labels=['Escaped', 'Trapped', 'Trapped and Harmed'])
        # ax.legend()
        plt.tight_layout() 
        chart_name = 'bar_chart'
        save_chart_high_res(chart_name, results_path)
        if __name__ == '__main__':
            plt.show()
        plt.close()

        return f'{results_path}/{chart_name}_chart.png'

if __name__ == '__main__':
    pd = {
        "escaped": 60,
        "trapped": 2,
        "trapped_and_harmed": 10
    }
    cc = {
        "escaped": 50,
        "trapped": 8,
        "trapped_and_harmed": 15
    }
    run_bar_chart(pd, cc)