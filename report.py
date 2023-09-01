import os
import datetime
from pathlib import Path
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
from constants import growthRateObject
from bar_chart import run_bar_chart
from stage_three_read_data import return_scen_excel

'''
# TODO: drop in text here
is contained over multiple storeys{% endif %} 
features open kitchens when the area of the apartment exceeds 8m x 4m, 
a floor area greater than 12m x 16m.

'''

# document_name = 'Event Tree.docx'
document_path = Path(__file__).parent /"Report Template"/"Template_Open_Plan_Report.docx"
# Report Template\Template_Open_Plan_Report.docx
doc = DocxTemplate(document_path)
# c:\Users\IanShaw\Fire Dynamics Group Dropbox\Thomas O'Driscoll\R&D\NHBC 8x10_1000x1000.json
def create_inline_image(image_file, template=doc, width=Inches(6), height=Inches(4)):
    return InlineImage(template, image_descriptor=image_file, width=width, height=height)
'''
TODO: is fire size calculated from sprinkler positions?
TODO: calc blue chart from data
sprinkler activation time PD1
peak hrr in pd1
fire growth rate

'''
from misc_charts import run_scen_misc_charts
def input_report_variables(
                            has_area_above_12x16,
                            has_kitchen_above_8x4,
                            is_multi_storey, 
                            num_kitchens, # from excel sheet
                            num_bedrooms,
                            num_lounges,
                            fire_locations, # from excel sheet
                            TD_From_Bedrooms,
                            TD_From_Lounges,
                            TD_From_Kitchens,
                            Project_Name,
                            Scenarios,
                            Proposed_Detection, 
                            CC_Detection,
                            Suppression_Type,
                            # LATER: should access all scenarios
                            # TODO: pass in base folder and access scenarios from there
                            base_path = r'C:\Users\IanShaw\localProgramming\fd\open plan 2\openPlanCFD\CFD Test Output\Roneo Corner - Smallest Flat',
                            output_filename=Path(__file__).parent /"Report Template"/'test output report2.docx',
                            ):
    today = datetime.datetime.today()
    # TODO: pull data from excel
    for scenario in Scenarios:
        results_path = f'{base_path}/{scenario}'
    
    scen_data, scen_workbook = return_scen_excel(path_to_results_file=f'{results_path}\{scenario}_Results.xlsx')
    misc_chart_paths = run_scen_misc_charts(output_dir=results_path) 
    # read sprinkler area from txt file

    import json
    path_txt = f'{base_path}\{Project_Name} Variables.txt'
    if os.path.exists(path_txt):
        with open(path_txt, 'r') as f:
            lines = json.loads(f.readlines()[0])
            sprinklered_room_area = lines['sprinklered_room_area']
    else:
        sprinklered_room_area = 30     # TODO: CHECK If this exists in excel

    pd1_path = f'{results_path}/PD1/PD1.fds'
    with open(pd1_path, 'r') as f:
        lines = f.readlines()

    pass
    # {{PD1_START_ROOM}}
    PD1_START_ROOM = create_inline_image(image_file=misc_chart_paths['start_room']['PD1'])
    # {{PD1_VIS}}
    PD1_VIS = create_inline_image(image_file=misc_chart_paths['vis']['PD1'])

    # model_res_col = ['AD'][0]
    pd1_trapped = scen_workbook['PD1']['AD'][0].value
    pd1_trapped_and_harmed = scen_workbook['PD1']['AD'][1].value
    pd1_escaped = scen_workbook['PD1']['AD'][2].value

    pd2_trapped = scen_workbook['PD2']['AD'][0].value
    pd2_trapped_and_harmed = scen_workbook['PD2']['AD'][1].value
    pd2_escaped = scen_workbook['PD2']['AD'][2].value 

    ps1_trapped = 0.23 * 0.89 * pd1_trapped
    ps2_trapped = 0.23 * 0.11 * pd2_trapped


    ps1_trapped_and_harmed = 0.23 * 0.89 * pd1_trapped_and_harmed
    ps2_trapped_and_harmed = 0.23 * 0.11 * pd2_trapped_and_harmed

    FAIL1_PD = round((ps1_trapped + ps2_trapped)*100, 1)
    FAIL2_PD = round((ps1_trapped_and_harmed + ps2_trapped_and_harmed)*100, 1)
    PASS1_PD = 100 - FAIL1_PD 
    PASS2_PD = 100 - FAIL2_PD

    cc1_trapped = scen_workbook['CC1']['AD'][0].value
    cc1_trapped_and_harmed = scen_workbook['CC1']['AD'][1].value
    cc1_escaped = scen_workbook['CC1']['AD'][2].value

    cc2_trapped = scen_workbook['CC2']['AD'][0].value
    cc2_trapped_and_harmed = scen_workbook['CC2']['AD'][1].value
    cc2_escaped = scen_workbook['CC2']['AD'][2].value 
    CC2_HARMED = cc2_trapped_and_harmed


    cs1_trapped = 0.23 * 0.6 * cc1_trapped
    cs2_trapped = 0.23 * 0.4 * cc2_trapped


    cs1_trapped_and_harmed = 0.23 * 0.6 * cc1_trapped_and_harmed
    cs2_trapped_and_harmed = 0.23 * 0.4 * cc2_trapped_and_harmed

    FAIL1_CC = round((cs1_trapped + cs2_trapped)*100, 1)
    FAIL2_CC = round((cs1_trapped_and_harmed + cs2_trapped_and_harmed)*100, 1)
    PASS1_CC = 100 - FAIL1_CC
    PASS2_CC = 100 - FAIL2_CC


    pd_escaped = round((100 - (FAIL1_PD + FAIL2_PD)) / 100, 3)
    pd_trapped = round(FAIL1_PD / 100, 3) # FAIL1_PD
    pd_trapped_and_harmed = round(FAIL2_PD / 100, 3)

    cc_escaped = round((100 - (FAIL1_CC + FAIL2_CC)) / 100, 3)
    cc_trapped = round(FAIL1_CC / 100, 3)
    cc_trapped_and_harmed = round(FAIL2_CC / 100, 3)

    # run bar chart
    bar_chart = run_bar_chart(
                    pd={
                        "escaped": pd_escaped,
                        "trapped": pd_trapped,
                        "trapped_and_harmed": pd_trapped_and_harmed
                    },
                    cc={
                        "escaped": cc_escaped,
                        "trapped": cc_trapped,
                        "trapped_and_harmed": cc_trapped_and_harmed
                    },
                    results_path=results_path
    )

    BAR_CHART = create_inline_image(image_file=bar_chart)

    harmed_ratio = round(FAIL2_CC / FAIL1_CC, 2)

    ''' REASONS_FOR_STUDY variable logic '''
    is_multi_storey_text = 'is contained over multiple storeys'
    if num_kitchens > 1:
        singular_article_kitchen = ''
        plural_kitchens = 's'
    else:
        singular_article_kitchen = 'an '
        plural_kitchens = ''
    has_kitchen_above_8x4_text = f'features {singular_article_kitchen}open kitchen{plural_kitchens} where the area of the apartment exceeds 8m x 4m'
    has_area_above_12x16_text = f'comprises of a floor area greater than 12m x 16m'

    reasons_for_study_text_list = []
    reasons_for_study_text = ''
    # if x add text for x to list
    if is_multi_storey:
        reasons_for_study_text_list.append(is_multi_storey_text)
        protected_area = 'stair'
    else:
        protected_area = 'entrance hall'
    if has_area_above_12x16:
        reasons_for_study_text_list.append(has_area_above_12x16_text)
    if has_kitchen_above_8x4:
        reasons_for_study_text_list.append(has_kitchen_above_8x4_text)
    # add and between last two
    if len(reasons_for_study_text_list) > 1:
        reasons_for_study_text = 'and ' + reasons_for_study_text_list[-1]
         # and comma between others
        if len(reasons_for_study_text_list) > 2:
            reasons_for_study_text = ', '.join(reasons_for_study_text_list[:-1]) + " " + reasons_for_study_text
    else:
        reasons_for_study_text = reasons_for_study_text_list[0]

    only_open_kitchen = False
    if has_kitchen_above_8x4 and len(reasons_for_study_text_list) == 1:
        only_open_kitchen = True

    '''CC1'''
    CC1
    '''CC2'''

    summary_statement = f'{protected_area} but with the provision of a suppression system, provides a level of safety which is at least as high as a code compliant design with a protected {protected_area} but no suppression' 
    
    trial_chart = create_inline_image(image_file=f'{results_path}\_premovement_chart.png', template=doc)
    # 1.5 x 1 for smaller charts
    if 'Kitchen' in fire_locations: 
        fgr = growthRateObject['fast'] 
    else: 
        fgr = growthRateObject['medium']
    # Kit_Prob
    Kit_Prob = round(0.03 / num_kitchens, 2)
    # Bed_Prob
    Bed_Prob = round(0.51 / num_bedrooms, 2)
    # Liv_Prob
    Liv_Prob = round(0.46 / num_lounges, 2)

    # TD's
    list_td_bedrooms = [
        'remove row!!' for f in range(6)
    ]
    for idx, td in enumerate(TD_From_Bedrooms):
        list_td_bedrooms[idx] = td

    list_td_liv = [
        'remove row!!' for f in range(2)
    ]    
    for idx, td in enumerate(TD_From_Lounges):
        list_td_liv[idx] = td

    list_td_kit = [
        'remove row!!' for f in range(2)
    ]    
    for idx, td in enumerate(TD_From_Kitchens):
        list_td_kit[idx] = td
        
    context = {
        "Kit_Prob": Kit_Prob,
        "Bed_Prob": Bed_Prob,
        "Liv_Prob": Liv_Prob,
        "P1PD": PASS1_PD,
        "P2PD": PASS2_PD,
        "F1PD": FAIL1_PD,
        "F2PD": FAIL2_PD,
        "P1CC": PASS1_CC,
        "P2CC": PASS2_CC,
        "F1CC": FAIL1_CC,
        "F2CC": FAIL2_CC,

        "P1A": round(pd1_trapped, 2),
        "P1B": round(ps1_trapped, 2),
        "P2A": round(pd1_trapped_and_harmed, 2),
        "P2B": round(ps1_trapped_and_harmed, 2),

        "P1C": round(pd2_trapped, 2),
        "P1D": round(ps2_trapped, 2),
        "P2C": round(pd2_trapped_and_harmed, 2),
        "P2D": round(ps2_trapped_and_harmed, 2),

        "C1A": round(cc1_trapped, 2),
        "C1B": round(cs1_trapped, 2),
        "C2A": round(cc1_trapped_and_harmed, 2),
        "C2B": round(cs1_trapped_and_harmed, 2),

        "C1C": round(cc2_trapped, 2),
        "C1D": round(cs2_trapped, 2),
        "C2C": round(cc2_trapped_and_harmed, 2),
        "C2D": round(cs2_trapped_and_harmed, 2),

        "CC2_HARMED": CC2_HARMED,
        "HARMED_RATIO": harmed_ratio,
        "ONE_STOREY": not is_multi_storey,
        "AUTHOR_NAME": "Test Author", # TODO: include in gui stage 3
        "CLIENT_NAME": "Test Client", # TODO: include in gui stage 3
        "TODAYS_DATE": today,
        "PROJECT_NAME": Project_Name,
        "IS_MULTI_STOREY": is_multi_storey, 
        "REASONS_FOR_STUDY": reasons_for_study_text,
        "ONLY_OPEN_KITCHEN": only_open_kitchen,
        # use first location of fire for now
        "FIRE_LOCATION": fire_locations[0],
        "F_LO": fire_locations[0],
        "HAS_KITCHEN_FIRE": 'Kitchen' in fire_locations,
        "SUMMARY_STATEMENT": summary_statement,
        "FGR": fgr, 
        "PD1_Area": sprinklered_room_area, 
        "Other_Area": 3.24, # TODO: include in gui stage 3
        "PD1_HRR": 402, 
        "P1_H": 402,
        "Other_HRR": 1500,
        "PD1_HPUA": 500,
        "Other_HPUA": 445,
        "PD1_peak_time": 185,
        "P1_T": 185,
        "Other_peak_time": 358,
        "is_HRR_custom": False, # needs to be added to excel or scope if x
        "FLOW_RATE": 49.05,
        "PARTICLE_VEL": 5.0,
        "CC_IS_LD3": CC_Detection == 3,
        "CC_IS_LD2": CC_Detection == 2,
        "DIST": 2,
        "C_H": 2.5,
        "SP_A": 25.0,
        "PD1_PRE_MOVE": create_inline_image(image_file=f'{results_path}\_premovement_chart.png', template=doc, width=Inches(2), height=Inches(1.5)),
        "PRE_MOVE_CHART": trial_chart,
        "BAR_CHART": BAR_CHART,
        "PD1_START_ROOM": PD1_START_ROOM,
        "PD1_VIS": PD1_VIS,
        "TD_B1": list_td_bedrooms[0],
        "TD_B2": list_td_bedrooms[1],
        "TD_B3": list_td_bedrooms[2],
        "TD_B4": list_td_bedrooms[3],
        "TD_B5": list_td_bedrooms[4],
        "TD_B6": list_td_bedrooms[5],
        "TD_L1": list_td_liv[0],
        "TD_L2": list_td_liv[1],
        "TD_K1": list_td_kit[0],
        "TD_K2": list_td_kit[1],

    }



    doc.render(context)

    doc.save(output_filename)    

from stage_three_read_data import return_excel_data
def prep_for_report_variables(
                                cfd_output_path, 
                                has_area_above_12x16,
                                has_kitchen_above_8x4,
                                is_multi_storey
                            ):
    project_name = os.path.basename(cfd_output_path)
    Number_Of_Bedrooms, Number_Of_Lounges, Number_Of_Kitchens, Kitchen_Fires, Suppression_Type, Lounge_Fires, Bedroom_Fires, No_Scenarios, Proposed_Detection, CC_Detection, Floor_To_Ceiling, Scenario_Names, Project_Name, TD_From_Bedrooms, TD_From_Lounges, TD_From_Kitchens = return_excel_data(cfd_output_path, project_name)
    # num_kitchens = Number_Of_Kitchens
    fire_locations = []
    for k_fire in range(Kitchen_Fires):
        fire_locations.append('Kitchen')
    for l_fire in range(Lounge_Fires):
        fire_locations.append('Lounge')
    for b_fire in range(Bedroom_Fires):
        fire_locations.append('Bedroom')
    # atm only one fire taken forward in the report variables
    # Project_Name, 
    # TODO: add further parameters needed for report from excel sheet
    input_report_variables(
                            has_area_above_12x16,
                            has_kitchen_above_8x4,
                            is_multi_storey, 
                            Number_Of_Kitchens, # from excel sheet
                            Number_Of_Bedrooms, 
                            Number_Of_Lounges,
                            fire_locations, # from excel sheet
                            TD_From_Bedrooms, 
                            TD_From_Lounges, 
                            TD_From_Kitchens,
                            Project_Name,
                            Scenario_Names,
                            Proposed_Detection, 
                            CC_Detection,
                            Suppression_Type,
                            base_path=cfd_output_path,
                            )



if __name__ == "__main__":
    # TODO: get data from excel sheet
    prep_for_report_variables(
                                    cfd_output_path=r'C:\Users\IanShaw\localProgramming\fd\open plan 2\openPlanCFD\CFD Test Output\Roneo Corner - Smallest Flat', 
                                    has_area_above_12x16 = True,
                                    has_kitchen_above_8x4 = True,
                                    is_multi_storey = False
                                )