import matplotlib.pyplot as plt
from constants import chart_config, compute_y_axis_bounds
import math

def save_chart_high_res(name_of_chart, new_dir_path, dpi=1200):
    plt.savefig(f'{new_dir_path}/{name_of_chart}_chart.png', format='png', dpi=dpi)
    plt.close()

def plot_bounds(x_min_axis, x_max_axis, y_min_axis, y_max_axis, plot=plt):
    plot.xlim([x_min_axis, x_max_axis])    ## limits x axis bounds
    plot.ylim([y_min_axis, y_max_axis])    ## limits y axis bounds


def run_charts(
        name,
        No_Runs, 
        HRR_Time, 
        HRR, 
        prog_time, 
        prog_HRR, 
        Simulation_Time, 
        escape_times,
        plot_time,
        kitchen_vis,
        bedroom_vis,
        lounge_vis,
        results_dir,
        kitchen_temp,
        bedroom_temp,
        lounge_temp,
        kitchen_rad,
        bedroom_rad,
        lounge_rad
        ):
    with plt.rc_context(chart_config):
        # plt.figure(figsize=(6, 4))  ## size of output
        plt.plot(HRR_Time, HRR, color = 'blue', linewidth = 0.5,)  ## adds a line
        plt.plot(prog_time, prog_HRR, color = 'red', linewidth = 0.5, linestyle='dotted')   ## adds another line
        
        
        plt.title(f"{name} - Recorded and Programmed Heat Release Rate", fontname = 'Segoe UI', fontsize = 10) ## add title
        plt.xlabel("Time (Seconds)", fontname = 'Segoe UI', fontsize = 10) ## sets label and font for xaxis
        plt.xticks(fontname = 'Segoe UI', fontsize = 8)  # sets tick locations and font for xticks
        plt.ylabel("Heat Release Rate (kW)", fontname = 'Segoe UI', fontsize = 10)  ## sets label and font for y axis
        plt.yticks(fontname = 'Segoe UI', fontsize = 8)   # sets tick location font for y ticks
        plt.legend(["Recorded HRR", "Programmed HRR"], loc ="lower right", fontsize = 8)
        
        
        if name == "PD1":
            ylim = 300
        else:
            ylim = 2000
        y_temp_array = [HRR, prog_HRR]
        max_axis_array = [max(f) for f in y_temp_array]
        min_axis_array = [min(f) for f in y_temp_array]
        ax_ymax, ax_ymin = compute_y_axis_bounds(max_axis_array, min_axis_array)
        # ax1.set_ylim([ax1_ymin, ax1_ymax])        
        # scope if ylim > suggested limits
        plt.xlim([0,Simulation_Time])    ## limits x axis bounds
        plt.ylim([ax_ymin, max(ylim, ax_ymax)])    ## limits y axis bounds
        
        # export_pdf.savefig(bbox_inches = "tight")
        plt.tight_layout() 
        if __name__ != '__main__':
            save_chart_high_res(name_of_chart=f'{name}-HRR', new_dir_path=results_dir)
        else:
            # plt.show()
            pass
        plt.close()

    escape_time_dist = []
    escape_time_times = []
    t = 0
    while t <= Simulation_Time:
        escape_time_dist.append(len([1 for i in escape_times if i <= t])/No_Runs*100)
        escape_time_times.append(t)
        t = t + 1

    fig_height = 5
    with plt.rc_context(chart_config):
        fig, ax1 = plt.subplots(figsize=(6, fig_height))  ## size of output

        ax1.set_xlabel("Time (Seconds)", fontname='Segoe UI', fontsize=10)
        ax1.set_ylabel("Visibility (m)", fontname='Segoe UI', fontsize=10)
        ax1.plot(plot_time, kitchen_vis, 'orange', linewidth=1.0, linestyle='dashdot', label='Kitchen Escape Route')
        ax1.plot(plot_time, bedroom_vis, 'green', linewidth=0.5, linestyle='dotted', label='Bedroom Escape Route')
        ax1.plot(plot_time, lounge_vis, 'blue', linewidth=0.5, linestyle='dashed', label='Lounge Escape Route')
        ax1.axhline(y=5, color='black', linewidth=0.5, linestyle='solid', label='0.3m/s Walking Speed (All Occupants)')
        ax1.axhline(y=3, color='black', linewidth=0.5, linestyle='dotted', label='0m/s Walking Speed (30% of Occupants)')
        ax1.axhline(y=2, color='black', linewidth=0.5, linestyle='dashed', label='0m/s Walking Speed (All Occupants)')
        ax1.tick_params(axis='y')
        ax1.set_ylim([0, 30])
        ax1.set_xlim([0, Simulation_Time])

        ax2 = ax1.twinx()
        ax2.set_ylabel("Number of Occupants Escaped (%)", fontname='Segoe UI', fontsize=10)
        ax2.plot(plot_time, escape_time_dist, 'red', linewidth=0.5, label="Occupants Escaped (%)")
        ax2.tick_params(axis='y')
        ax2.set_ylim([0, 100])

        plt.rcParams['xtick.labelsize'] = 8
        plt.rcParams['ytick.labelsize'] = 8

        plt.title(f"{name} - Visibility and Probability of Escape", fontname='Segoe UI', fontsize=10)  ## add title

        # Combining legends from both subplots into one
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1 + h2, l1 + l2, loc="lower center", fontsize=8, bbox_to_anchor=(0.5, -0.55), frameon=False)

        plt.tight_layout()
        if __name__ != '__main__':
            save_chart_high_res(name_of_chart=f'{name}-Visibility 6x{fig_height}', new_dir_path=results_dir)
        else:
            save_chart_high_res(name_of_chart=f'{name}-Visibility 6x{fig_height}', new_dir_path=results_dir)
            plt.show()

        plt.close()    
    # TODO: later have legend moved down and chart less long in y direction
    for vis_fig_height in [6]:
        with plt.rc_context(chart_config):
            # plt.figure(figsize=(6, 4))  ## size of output

            fig1, ax1 = plt.subplots(figsize=(6, vis_fig_height))
        
            ax1.set_xlabel("Time (Seconds)", fontname = 'Segoe UI', fontsize = 10)
            ax1.set_ylabel("Visibility (m)", fontname = 'Segoe UI', fontsize = 10)
            ax1.plot(plot_time, kitchen_vis, 'orange', linewidth = 1.0, linestyle='dashdot', label = 'Kitchen Escape Route')
            ax1.plot(plot_time, bedroom_vis, 'green', linewidth = 0.5, linestyle='dotted', label = 'Bedroom Escape Route')
            ax1.plot(plot_time, lounge_vis, 'blue', linewidth = 0.5, linestyle='dashed', label = 'Lounge Escape Route')
            ax1.axhline(y = 5, color = 'black', linewidth = 0.5, linestyle='solid', label = '0.3m/s Walking Speed (All Occupants)')
            ax1.axhline(y = 3, color = 'black', linewidth = 0.5, linestyle='dotted', label = '0m/s Walking Speed (30% of Occupants)')
            ax1.axhline(y = 2, color = 'black', linewidth = 0.5, linestyle='dashed', label = '0m/s Walking Speed (All Occupants)')
            ax1.tick_params(axis = 'y')
            ax1.set_ylim([0, 30])
            ax1.set_xlim([0, Simulation_Time])

            
            ax2 = ax1.twinx()
            
            ax2.set_ylabel("Number of Occupants Escaped (%)", fontname = 'Segoe UI', fontsize = 10)
            ax2.plot(plot_time, escape_time_dist, 'red', linewidth = 0.5,  label = "Occupants Escaped (%)")
            ax2.tick_params(axis = 'y')
            ax2.set_ylim([0, 100])
            
            # ax1.rcParams['xtick.labelsize']=8
            # ax2.rcParams['ytick.labelsize']=8

            plt.title(f"{name} - Visibility and Probability of Escape", fontname = 'Segoe UI', fontsize = 10) ## add title
            h1, l1 = ax1.get_legend_handles_labels()
            h2, l2 = ax2.get_legend_handles_labels()
            ax1.legend(h1+h2, l1+l2, loc ="lower center", fontsize = 8, bbox_to_anchor=(0.3, -0.65), frameon=False)
            # plt.legend(bbox_to_anchor=(0.3, -0.55), loc='lower center', fontsize = 8, frameon=False)
            
            # export_pdf.savefig(bbox_inches = "tight")
            plt.tight_layout() 
            # plt.show()
            if __name__ != '__main__':
                save_chart_high_res(name_of_chart=f'{name}-Visibility 6x{fig_height}', new_dir_path=results_dir)
            else:
                save_chart_high_res(name_of_chart=f'{name}-Visibility 6x{vis_fig_height}', new_dir_path=results_dir)
                plt.show()

            plt.close()   

    # with PdfPages(f"{results_dir}/{name} - Temperature.pdf") as export_pdf: ### draws visibility graph
    with plt.rc_context(chart_config):
        # plt.figure(figsize=(6, 4))  ## size of output

        fig, ax1 = plt.subplots(figsize=(6, fig_height))
    
        ax1.set_xlabel("Time (Seconds)", fontname = 'Segoe UI', fontsize = 10)
        ax1.set_ylabel("Temperature (C)", fontname = 'Segoe UI', fontsize = 10)
        ax1.plot(plot_time, kitchen_temp, 'orange', linewidth = 1.0, linestyle='dashdot', label = 'Kitchen Escape Route')
        ax1.plot(plot_time, bedroom_temp, 'green', linewidth = 0.5, linestyle='dotted', label = 'Bedroom Escape Route')
        ax1.plot(plot_time, lounge_temp, 'blue', linewidth = 0.5, linestyle='dashed', label = 'Lounge Escape Route')
        ax1.axhline(y = 60, color = 'black', linewidth = 0.5, linestyle='dotted', label = 'Typical Tenability Limit (BS 7974-6)')

        ax1.tick_params(axis = 'y')
        y_temp_array = [kitchen_temp, bedroom_temp, lounge_temp]
        max_axis_array = [max(f) for f in y_temp_array]
        min_axis_array = [min(f) for f in y_temp_array]
        ax1_ymax, ax1_ymin = compute_y_axis_bounds(max_axis_array, min_axis_array)
        ax1.set_ylim([ax1_ymin, ax1_ymax])
        ax1.set_xlim([0, Simulation_Time])

        
        ax2 = ax1.twinx()
        
        ax2.set_ylabel("Number of Occupants Escaped (%)", fontname = 'Segoe UI', fontsize = 10)
        ax2.plot(plot_time, escape_time_dist, 'red', linewidth = 0.5,  label = "Occupants Escaped (%)")
        ax2.tick_params(axis = 'y')
        ax2.set_ylim([0, 100])
        
        plt.rcParams['xtick.labelsize']=8
        plt.rcParams['ytick.labelsize']=8

        plt.title(f"{name} - Temperature and Probability of Escape", fontname = 'Segoe UI', fontsize = 10) ## add title
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc ="lower center", fontsize = 8, bbox_to_anchor=(0.3, -0.45), frameon=False)
        # plt.legend(bbox_to_anchor=(0.3, -0.45), loc='lower center', fontsize = 8, frameon=False)
        
        # export_pdf.savefig(bbox_inches = "tight")
        plt.tight_layout() 
        if __name__ != '__main__':
            save_chart_high_res(name_of_chart=f'{name}-Temperature 6x{fig_height}', new_dir_path=results_dir)           
        else:
            save_chart_high_res(name_of_chart=f'{name}-Temperature 6x{fig_height}', new_dir_path=results_dir)
            plt.show()

        plt.close()   

    # with PdfPages(f"{results_dir}/{name} - RAD.pdf") as export_pdf: ### draws visibility graph
    with plt.rc_context(chart_config):
        # plt.figure(figsize=(6, 4))  ## size of output

        fig, ax1 = plt.subplots(figsize=(6, fig_height))
    
        ax1.set_xlabel("Time (Seconds)", fontname = 'Segoe UI', fontsize = 10)
        ax1.set_ylabel("Radiative Heat Flux (kW/m2)", fontname = 'Segoe UI', fontsize = 10)
        ax1.plot(plot_time, kitchen_rad, 'orange', linewidth = 1.0, linestyle='dashdot', label = 'Kitchen Escape Route')
        ax1.plot(plot_time, bedroom_rad, 'green', linewidth = 0.5, linestyle='dotted', label = 'Bedroom Escape Route')
        ax1.plot(plot_time, lounge_rad, 'blue', linewidth = 0.5, linestyle='dashed', label = 'Lounge Escape Route')
        ax1.axhline(y = 2.5, color = 'black', linewidth = 0.5, linestyle='dotted', label = 'Typical Tenability Limit (BS 7974-6)')
        ax1.tick_params(axis = 'y')
        y_temp_array = [kitchen_rad, bedroom_rad, lounge_rad]
        max_axis_array = [max(f) for f in y_temp_array]
        min_axis_array = [min(f) for f in y_temp_array]
        ax1_ymax, ax1_ymin = compute_y_axis_bounds(max_axis_array, min_axis_array)
        ax1.set_ylim([ax1_ymin, ax1_ymax])
        ax1.set_xlim([0, Simulation_Time])
        
        ax2 = ax1.twinx()
        
        ax2.set_ylabel("Number of Occupants Escaped (%)", fontname = 'Segoe UI', fontsize = 10)
        ax2.plot(plot_time, escape_time_dist, 'red', linewidth = 0.5,  label = "Occupants Escaped (%)")
        ax2.tick_params(axis = 'y')
        ax2.set_ylim([0, 100])
        
        plt.rcParams['xtick.labelsize']=8
        plt.rcParams['ytick.labelsize']=8

        plt.title(f"{name} - Radiative Heat Flux and Probability of Escape", fontname = 'Segoe UI', fontsize = 10) ## add title
        h1, l1 = ax2.get_legend_handles_labels()
        h2, l2 = ax1.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc ="lower center", fontsize = 8, bbox_to_anchor=(0.3, -0.45), frameon=False)
        # plt.legend(bbox_to_anchor=(0.3, -0.45), loc='lower center', fontsize = 8, frameon=False)
        # export_pdf.savefig(bbox_inches = "tight")
        plt.tight_layout() 
        if __name__ != '__main__':
            save_chart_high_res(name_of_chart=f'{name}-RAD 6x{fig_height}', new_dir_path=results_dir)   
        else:
            save_chart_high_res(name_of_chart=f'{name}-RAD 6x{fig_height}', new_dir_path=results_dir)  
            plt.show()
                    
        plt.close() 

if __name__ == '__main__':
    from final_chart_inputs import *
#         name, HRR_Time, HRR, prog_time, prog_HRR, 
    #     Simulation_Time, 
    #     escape_times,
    #     plot_time,
    #     kitchen_vis,
    #     bedroom_vis,
    #     lounge_vis,
    #     results_dir,
    #     kitchen_temp,
    #     bedroom_temp,
    #     lounge_temp,
    #     kitchen_rad,
    #     bedroom_rad,
    #     lounge_rad    
    run_charts(
        name,
        No_Runs, 
        HRR_Time, 
        HRR, 
        prog_time, 
        prog_HRR, 
        Simulation_Time, 
        escape_times,
        plot_time,
        kitchen_vis,
        bedroom_vis,
        lounge_vis,
        results_dir,
        kitchen_temp,
        bedroom_temp,
        lounge_temp,
        kitchen_rad,
        bedroom_rad,
        lounge_rad
        )