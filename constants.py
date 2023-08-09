import pathlib
import math

current_folder_path = pathlib.Path(__file__).parent.resolve() # needs to be sent in as base folder

growthRateObject = {
    "slow": 0.0029,
    "medium": 0.0117,
    "fast": 0.047,
    "ultraFast": 0.188 
  }

# sprinklers activation constants
tAmb = 293
E = 0.20 
g = 9.81
rho = 1.1
cp = 1.04

font_name_light = 'Segoe UI Light'
font_name_normal = 'Segoe UI'
light_text_color = (0.59,0.56,0.56)
chart_config = {        
        "xtick.color": light_text_color,
        "ytick.color": light_text_color,
        "axes.titlecolor": light_text_color,
        "axes.labelcolor": light_text_color,
        "axes.edgecolor": light_text_color,
        "legend.labelcolor": light_text_color,
        "figure.figsize": [6, 4],
        'axes.grid': True,
        'grid.linewidth': '0.05',
        "grid.color": light_text_color
        }


def compute_y_axis_bounds(max_axis_array, min_axis_array, to_the_nearest=10):

    def get_min_bound(element):
        if element ==0 or 0.01 > element > -0.01: # or within 0.01
            return 0
        else:
            return element-10

    max_bounds = [element+10 for element in max_axis_array]
    min_bounds = [get_min_bound(element) for element in min_axis_array]
    max_from_lines = max(max_bounds)
    min_from_lines = min(min_bounds)
    max_axis = math.floor(max_from_lines/to_the_nearest) * to_the_nearest
    min_axis = math.ceil(min_from_lines/to_the_nearest) * to_the_nearest
    return max_axis, min_axis