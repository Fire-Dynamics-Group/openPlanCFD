''' 
Stage 1 
this script outputs 1 of each door type
these door types can then be copied/deleted as required and placed by user in pyrosim

'''

#### This script defines the fixed variables for the study and saves 
# them to an excel file. It also sets up an FDS tools file to assist
# model building

import xlsxwriter
import os
import pathlib
import json

from constants import current_folder_path
from FDS_door_generator import return_doors_seals_fds

#### Database Entries
# TODO: have stage 1, 2 and 3 output folders
# user moves output from stage 1 -> should be 2; one backup; one to edit and bring to stage 2
# stage 2 should read but not overwrite the output from stage 1
# stage 3 should read but not overwrite output from stage 2

# TODO: RTI NEEDED, tActive

BS_9251_Category_1 = [2, "&PROP ID='BS 9251',","      QUANTITY='SPRINKLER LINK TEMPERATURE',", "      PART_ID='Water',", "      FLOW_RATE=49.05,", "      PARTICLE_VELOCITY=5.0,", "      SPRAY_ANGLE=60.0,75.0/", "BS 9251"]
Smartscan = [2, "&PROP ID='Automist Smartscan',","      QUANTITY='SPRINKLER LINK TEMPERATURE',", "      PART_ID='Water',", "      FLOW_RATE=6.0,", "      PARTICLE_VELOCITY=15.0,", "      SPRAY_ANGLE=0.0,25.0/", "Automist Smartscan"]
'''
Sam's notes on parameters
# # Property Details
# Project_Name = "Roneo Corner - Smallest Flat"
# Number_Of_Bedrooms = 2
# Number_Of_Lounges = 1
# Number_Of_Kitchens = 1
# Lounge_Fires = 0
# Lounge_Fires_Own_Door = [] # list of 1s and 0s, 1 being own door, 0 being use same door. List should have same number of entries as number of fires
# Bedroom_Fires = 0
# Bedroom_Fires_Own_Door = [] # list of 1s and 0s, 1 being own door, 0 being use same door. List should have same number of entries as number of fires
# Kitchen_Fires = 1
# Kitchen_Fires_Own_Door = [1] # list of 1s and 0s, 1 being own door, 0 being use same door. List should have same number of entries as number of fires
# TD_From_Bedrooms = [3.3]  ## a list of maximum TD's from bedrooms, measured from drawings
# TD_From_Kitchens = [2.7] ##  measured from drawings
# TD_From_Lounges = [2.7] ## measured from drawings
# Suppression_Type = BS_9251_Category_1  # options: "BS_9251_Category_1", "Plumis-Smartscan"
# Proposed_Detection = 1 # 1 = LD1, 2 = LD2 etc.
# CC_Detection = 3 # same
# Floor_To_Ceiling = 2.5
'''

# TODO: add parameters for user input
# TODO: add single internal door, double internal door, and flat door
def create_fds_base_model(Project_Name, 
                          Number_Of_Bedrooms, 
                          Number_Of_Lounges, 
                          Number_Of_Kitchens, 
                          Lounge_Fires, 
                        #   Lounge_Fires_Own_Door, 
                          Bedroom_Fires, 
                        #   Bedroom_Fires_Own_Door, 
                          Kitchen_Fires, 
                        #   Kitchen_Fires_Own_Door,
                          TD_From_Bedrooms,
                          TD_From_Kitchens,
                          TD_From_Lounges,
                          Suppression_Type,
                          Proposed_Detection,
                          CC_Detection,
                          Floor_To_Ceiling,
                          rti, # needs to write to excel
                          sprinklered_room_area, # need to write to excel
                          tActive, # need to save to excel or json
                          output_path = ""
                          ):
    #### Variables

    # # Tenabiity Limits
    # FED_Tenability_Limit = 1  # Needs more work
    # Temp_Tenability_Limit_NS = 120 ## Temperature Tenability limit when moisture is < moisture_laden
    # Temp_Tenability_Limit_S = 60 # Temperature tenability Limit when moisture > Moiture Laden 
    # Moisture_Laden = 0.1  # As per BS 7974:6
    # Probability_Of_High_Visibility_Tenability_Limit = 0.3 # as per BS 7974:6
    # High_Visibility_Tenability_Limit = 3
    # Low_Visibility_Tenability_Limit = 2
    # TODO: have chosen output file
    current_folder_path = pathlib.Path(__file__).parent.resolve()

    y_move_down = 2.1

    if len(output_path) > 0:
        current_folder_path = output_path
    # Calculated Variables

    No_Scenarios = Bedroom_Fires + Kitchen_Fires + Lounge_Fires  ## works out number of scenarios
    Scenario_Names = [] # creates a list of scenario names
    n=1
    while n <= Lounge_Fires: # creates list of all scenarios for later use 
        Scenario_Names.append(f"Lounge_Fire_{n}")
        n=n+1
    n=1
    while n <= Kitchen_Fires:
        Scenario_Names.append(f"Kitchen_Fire_{n}")
        n=n+1
    n=1
    while n <= Bedroom_Fires:
        Scenario_Names.append(f"Bedroom_Fire_{n}")
        n=n+1
    # Probabilities

    Probability_Occupant_in_Kitchen = 0.02 ## All as per NHBC Open Plan Report
    Probability_Occupant_in_Lounge = 0.38
    Probability_Occupant_in_Bedroom = 0.6  


    #### Create Spreadsheet
    # try: 
    # does this work for other folder location??
    if Project_Name not in os.listdir(current_folder_path):
        os.mkdir(f"{current_folder_path}/{Project_Name}") 
    # except: 
    #     print()  
    model_object = {}
    for item in [
        Project_Name, 
        Number_Of_Bedrooms, 
        Number_Of_Lounges, 
        Number_Of_Kitchens,
        Lounge_Fires,
        Bedroom_Fires,
        Kitchen_Fires,
        TD_From_Bedrooms,
        TD_From_Kitchens,
        TD_From_Lounges, 
        Suppression_Type,
        No_Scenarios,
        Scenario_Names,
        Proposed_Detection,
        CC_Detection,
        Floor_To_Ceiling,
        rti,
        sprinklered_room_area,
        tActive
        # ....
        ]:
        var_name = [ i for i, a in locals().items() if a == item][0]
        model_object[var_name] = item
        # model_object[f'']
    sub_path = f'{current_folder_path}/{Project_Name}'
    filename = f'{Project_Name} Variables.txt'
    # create and save to a txt file
    with open(f'{sub_path}/{filename}', 'w') as f:
        # Write the dictionary to the file in JSON format
        json.dump(model_object, f)
    workbook = xlsxwriter.Workbook(f"{current_folder_path}/{Project_Name}/{Project_Name} Variables.xlsx") # create spreadsheet and worksheet. This will be on the drive so other parts of the program can read it. 
    worksheet = workbook.add_worksheet("Variables")

    worksheet.write(0,0,"Project_Name") ##information dump to spreadsheet
    worksheet.write(0,1,Project_Name)
    worksheet.write(1,0,"Number_Of_Bedrooms")
    worksheet.write(1,1,Number_Of_Bedrooms)
    worksheet.write(2,0,"Number_Of_Lounges")
    worksheet.write(2,1,Number_Of_Lounges)
    worksheet.write(3,0,"Number_Of_Kitchens")
    worksheet.write(3,1,Number_Of_Kitchens)
    worksheet.write(4,0,"Lounge_Fires")
    worksheet.write(4,1,Lounge_Fires)
    worksheet.write(5,0,"Lounge_Fires_Own_Door")
    worksheet.write(5,1,'n/a')
    worksheet.write(6,0,"Bedroom_Fires")
    worksheet.write(6,1,Bedroom_Fires)
    worksheet.write(7,0,"Bedroom_Fires_Own_Door")
    worksheet.write(7,1,'n/a')
    worksheet.write(8,0,"Kitchen_Fires")
    worksheet.write(8,1,Kitchen_Fires)
    worksheet.write(9,0,"Kitchen_Fires_Own_Door")
    worksheet.write(9,1,'n/a')
    worksheet.write(10,0,"TD_From_Bedrooms")
    worksheet.write(10,1,str(TD_From_Bedrooms))
    worksheet.write(11,0,"TD_From_Kitchens")
    worksheet.write(11,1,str(TD_From_Kitchens))
    worksheet.write(12,0,"TD_From_Lounges")
    worksheet.write(12,1,str(TD_From_Lounges))
    worksheet.write(13,0,"Suppression_Type")
    worksheet.write(13,1,str(Suppression_Type))
    worksheet.write(14,0,"No_Scenarios")
    worksheet.write(14,1,No_Scenarios)
    worksheet.write(15,0,"Scenario_Names")
    worksheet.write(15,1,str(Scenario_Names))
    worksheet.write(16,0,"No_Openable_Doors")
    # worksheet.write(16,1,No_Openable_Doors)
    worksheet.write(16,1,"n/a")
    worksheet.write(17,0,"Default_Door")
    # worksheet.write(17,1,Default_Door)
    worksheet.write(17,1,"n/a")
    worksheet.write(18,0,"Scenario_Doors")
    # worksheet.write(18,1,str(Scenario_Doors))
    worksheet.write(18,1,"n/a")
    worksheet.write(19,0,"Proposed_Detection")
    worksheet.write(19,1,Proposed_Detection)
    worksheet.write(20,0,"CC_Detection")
    worksheet.write(20,1,CC_Detection)
    worksheet.write(21,0,"Floor_To_Ceiling")
    worksheet.write(21,1,Floor_To_Ceiling)


    workbook.close()


    #####  generate Base FDS file

    string = Project_Name.replace(" ", "_")
    filename = f"{current_folder_path}/{Project_Name}/{string}_Base_Model.fds" # creates / finds FDS file to write
    file = open(filename, "w") # opens "filename" as a file that can be written "w"

    file.write(f"&HEAD CHID='{filename}_Base_Model'/\n") # inserts code header for fds model - names model with underscores so file name has underscores
    file.write("""
    &TIME T_END=1200.0/ 
    &DUMP DT_DEVC=1, DT_RESTART=400.0, DT_SL3D=1/

    &SPEC ID='WATER VAPOR'/

    &PART ID='Water',
        SPEC_ID='WATER VAPOR',
        DIAMETER=500.0,
        MONODISPERSE=.TRUE.,
        AGE=60.0,
        SAMPLING_FACTOR=1/

    &MATL ID='GYPSUM PLASTER',
        FYI='Quintiere',
        SPECIFIC_HEAT=0.84,
        CONDUCTIVITY=0.48,
        DENSITY=1440.0/

    &SURF ID='Gypsum',
        RGB=146,202,166,
        DEFAULT=.TRUE.,
        BACKING='INSULATED',
        MATL_ID(1,1)='GYPSUM PLASTER',
        MATL_MASS_FRACTION(1,1)=1.0,
        THICKNESS(1)=0.025/
        
    &PROP ID='Cleary Photoelectric P1',
        QUANTITY='CHAMBER OBSCURATION',
        ALPHA_E=1.8,
        BETA_E=-1.0,
        ALPHA_C=1.0,
        BETA_C=-0.8/

    &REAC ID='Fire',
        FUEL='REAC_FUEL',
        C=3.434,
        H=6.19,
        O=2.483,
        N=0.017,
        AUTO_IGNITION_TEMPERATURE=0.0,
        CO_YIELD=0.00640,
        SOOT_YIELD=0.016
        HCN_YIELD=0.00005,
        HEAT_OF_COMBUSTION=18075.636/


        """)

    file.write(f"&DEVC ID='Smoke detector LD{Proposed_Detection}_00', PROP_ID='Cleary Photoelectric P1', XYZ=0.0,{-y_move_down},{Floor_To_Ceiling-0.1}/\n") ## inserts smoke detector whch can be copied

    if Proposed_Detection != CC_Detection:
        file.write(f"&DEVC ID='Smoke detector LD{CC_Detection}_00', PROP_ID='Cleary Photoelectric P1', XYZ=1.0,{-y_move_down},{Floor_To_Ceiling-0.1}/\n") # if CC has different detection category, creates detection for CC only

    n = 1
    while n <= 10.0:
        file.write(f"&DEVC ID='CD{n}',QUANTITY='DENSITY', SPEC_ID='CARBON DIOXIDE' XYZ=2.0,{1-n-y_move_down},1.7/\n") # inserts 10 x Carbon Dioxide measurement at correct height - this needs to be better. 
        n = n+1

    n = 1
    while n <= 10.0:
        file.write(f"&DEVC ID='CM{n}',QUANTITY='DENSITY', SPEC_ID='CARBON MONOXIDE' XYZ=2.0,{1-n-y_move_down},1.7/\n") # inserts 10 x Carbon Monoxide measurement at correct height - this needs to be better. 
        n = n+1

    n = 1
    while n <= 10.0:
        file.write(f"&DEVC ID='HCN{n}',QUANTITY='DENSITY', SPEC_ID='HYDROGEN CYANIDE' XYZ=2.0,{1-n-y_move_down},1.7/\n") # inserts 10 x HCN measurement at correct height - this needs to be better. 
        n = n+1

    n = 1
    while n <= 10.0:
        file.write(f"&DEVC ID='VIS{n}', QUANTITY='VISIBILITY', XYZ=2.0,{1-n-y_move_down},1.7/\n") # inserts 10 x vis measurement at correct height...etc
        n = n+1

    n = 1
    while n <= 10.0:
        file.write(f"&DEVC ID='TEMP{n}', QUANTITY='TEMPERATURE', XYZ=2.0,{1-n-y_move_down},1.7/\n")
        n = n+1

    n = 1
    while n <= 10.0:
        file.write(f"&DEVC ID='RAD{n}', QUANTITY='RADIATIVE HEAT FLUX GAS', XYZ=2.0,{1-n-y_move_down},1.7/\n")
        n = n+1

    n = 1
    while n <= 10.0:
        file.write(f"&DEVC ID='WATER{n}', QUANTITY='VOLUME FRACTION', SPEC_ID='WATER VAPOR' XYZ=2.0,{1-n-y_move_down},1.7/\n") # not sure if this is correct
        n = n+1

    x = 3.0

    n = 1

    while n <= No_Scenarios:
        file.write(f"&OBST ID='{Scenario_Names[n-1]}', COLOR='RED', XB={x},{x+1.8},{-1.8-y_move_down},{-y_move_down},0.0,0.1, SURF_ID='Gypsum'/\n") # creates an obstruction to denote the fire location for each scenario 445kw/m2
        x = x + 4
        n = n+1
    

    # doors = list(Scenario_Doors.values())
    # doors = list(dict.fromkeys(doors))   #creates a list of names of doors for the model

    # just paste in 3 doors
    door_names = ["Internal_Flat_Door_Single", "Internal_Flat_Door_Double", "Flat_Entrance_Door"]
    door_types = {
        "Internal_Flat_Door_Single":
{
            "x": 0.8,
            "y": 0.1,
            "z": 2.1                       
                       },


        "Internal_Flat_Door_Double":
{
            "x": 1.6,
            "y": 0.1,
            "z": 2.1                       
                       },


        "Flat_Entrance_Door":
{
            "x": 0.8,
            "y": 0.0,
            "z": 2.1                       
                       }

        
    }

    for door in door_names: # pastes in a door for every different openable door.
        if "Double" in door:
            y1 = 1
        else:
            y1 = 0
        file.write(f"&OBST ID='{door}', COLOR='GREEN', XB={x},{x+door_types[door]['x']},{y1-y_move_down},{y1 + door_types[door]['y']-y_move_down},0.0,{door_types[door]['z']}, SURF_ID='Gypsum'/\n")
        x = x + 1

    file.write(f"&OBST ID='CC_WALL', XB={x},{x+2},{-0.1-y_move_down},{0.0-y_move_down},0.0,2.5, SURF_ID='Gypsum'/\n") ## inserts some template code compliant walls with the correct name so they can be removed later. 
    x = x+3
    file.write(f"&OBST ID='CC_WALL', XB={x},{x+0.1},{-3.0-y_move_down},{0.0-y_move_down},0.0,2.5, SURF_ID='Gypsum'/\n")
    x = x+1


    n = 1

    while n <= No_Scenarios:
        file.write(f"&OBST ID='{Scenario_Names[n-1]}_Inlet_Air', COLOR='YELLOW', XB={x},{x+2.5},{-1.0-y_move_down},{0.0-y_move_down},0.0,1.0, SURF_ID='Gypsum'/\n") # creates an obstruction to denote the inlet air
        x = x + 1
        n = n+1


    file.write(f"{Suppression_Type[1]}\n")
    file.write(f"{Suppression_Type[2]}\n")
    file.write(f"{Suppression_Type[3]}\n")
    file.write(f"{Suppression_Type[4]}\n")
    file.write(f"{Suppression_Type[5]}\n")
    file.write(f"{Suppression_Type[6]}\n")

    y = 1
    while y <= No_Scenarios:
        n = 1
        while n <= Suppression_Type[0]:
            if "Kitchen" in Scenario_Names[y-1]:
                act = 73
            else:
                act = 147
            file.write(f"&DEVC ID='{Scenario_Names[y-1]}_SPRK{n}', PROP_ID='{Suppression_Type[7]}', XYZ={x},{-y_move_down},{Floor_To_Ceiling-0.1}, QUANTITY='TIME', SETPOINT={act}/\n")
            x = x + 1
            n = n + 1
        y = y+1


    file.write("&SLCF QUANTITY='TEMPERATURE', PBZ=1.7/\n")
    file.write("&SLCF QUANTITY='VISIBILITY', PBZ=1.7/\n")
    file.write("&SLCF QUANTITY='TEMPERATURE', PBX=2.0/\n")
    file.write("&SLCF QUANTITY='VISIBILITY', PBX=2.0/\n")
    file.write("&SLCF QUANTITY='TEMPERATURE', PBY=2.0/\n")
    file.write("&SLCF QUANTITY='VISIBILITY', PBY=2.0/\n")



    
    print(f"file saved to {filename}")

    file.close() 

if __name__ == '__main__':

    # create_fds_base_model(Project_Name= "NHBC 8x10 - Copy", 
    #                         Number_Of_Bedrooms = 2, 
    #                         Number_Of_Lounges = 1, 
    #                         Number_Of_Kitchens = 1, 
    #                         Lounge_Fires = 1, 
    #                         # Lounge_Fires_Own_Door = [], 
    #                         Bedroom_Fires = 0, 
    #                         # Bedroom_Fires_Own_Door = [], 
    #                         Kitchen_Fires = 0, 
    #                         # Kitchen_Fires_Own_Door = [1],
    #                         TD_From_Bedrooms = [3,4.7],
    #                         TD_From_Kitchens = [1.4],
    #                         TD_From_Lounges = [3.8],
    #                         Suppression_Type = BS_9251_Category_1,
    #                         Proposed_Detection = 1,
    #                         CC_Detection = 3,
    #                         Floor_To_Ceiling = 2.3
    #                         )
        create_fds_base_model(Project_Name= "NHBC 12x16", 
                            Number_Of_Bedrooms = 3, 
                            Number_Of_Lounges = 1, 
                            Number_Of_Kitchens = 1, 
                            Lounge_Fires = 1, 
                            Bedroom_Fires = 0, 
                            Kitchen_Fires = 0, 
                            TD_From_Bedrooms = [4,8.2,9.8],
                            TD_From_Kitchens = [5],
                            TD_From_Lounges = [4.9],
                            Suppression_Type = BS_9251_Category_1,
                            Proposed_Detection = 1,
                            CC_Detection = 3,
                            Floor_To_Ceiling = 2.3,
                            rti=90,
                            sprinklered_room_area=25,
                            tActive= 68
                            )