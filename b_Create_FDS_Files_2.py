''' 
Step 2 
Step 1 dropped placeholder obstructions into fds script

Doors:
User should have copied/deleted door types and located where needed
This script looks for all doors of each type and attaches appropriate leakage vents to each door
Only front door to remain for proposed design (pd) -> no internal protected corridor unline code compliant (cc)

Fire:
User should have placed fire obstruction in appropriate location
This script converts the placeholder fire into a ringed fire

Sensors:
user should have placed in appropriate locations 10 sensors

Slices:
Script to locate slices at the escape route doors, fire and all sensor locations for the x, y and z directions; and for velocity, temp and visibility parameters. 
Z slices to be placed at 1.7m above finished floor level, in accordance with BRE study
Script to remove any duplicate slices.

'''

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 15:05:19 2020

@author: SamBennett
"""

#### 1. Import Modules

import openpyxl
import math 
import os
import shutil

from constants import current_folder_path, growthRateObject
from helper_function import Get_Coords_from_FDS_Code, find_centre_coords, find_dist, computeActivationTime
from FDS_door_generator import return_door_object_and_cc_escape_door, return_doors_seals_fds
from sprinkler_functions import return_sprinklered_fire_fds
#### 2. Functions


def Delete_Line_Containing_String(string, fdsfile):
    file = open(fdsfile, "r+")
    lines = file.readlines()
    file.close() 
    file = open(fdsfile, "w")
    n = 1
    for line in lines:
        if string in line:
            n=n+1
        else:
            file.write(line)
    print(f"{n} instances of {string} deleted from {fdsfile}")
    file.close()



def search_string_in_file(string_to_search, fdsfile): ## this returns a lines which feature a particular bit of code as long as there is only one bit in there. 
    file = open(fdsfile, "r")
    list_of_results = []
    # Open the file in read only mode
    lines = file.readlines()
    
    for index, line in enumerate(lines):
        if string_to_search in line:
            # If yes, then add the line number & line as a tuple in the list
            list_of_results.append((line.strip()))
    # Return list of tuples containing line numbers and lines where string is found
    file.close
    return list_of_results[0]  # return first item in list as a string


def string_to_list_and_clean(string):  ## it reads the lists in the excel sheet as a string, this cleans it up as intended
    list1 = string.split()
    list2 = []
    for i in list1:
        temp = i
        temp = temp.translate({ord(c): None for c in """,'[]"""})
        list2.append(temp)
    return list2

def write_unsprinklered_fire(x_org, y_org, z_org, Scenario_Name, fdsfile, cell_size, peak_fs=1500):
    file = open(fdsfile, "a")
    time_step = 1
    fire_height = 0.1
    if "Kitchen" in Scenario_Name:
        fgr = 0.0469
    else:
        fgr = 0.0117
    
    HRRPUA = 445 # constant
    # should reducing fire size from 2.5 to 1.5 be done by reducing HRR to 1.5MW/5.76?
    # peak_fs = 1500
    target_fire_area = round(peak_fs / HRRPUA, 3) # correct

    no_rings = 12    
 
    t = 0
    ring = 1
    
    ring_peak = (cell_size*2)**2*HRRPUA
    
    file.write("\n")
    file.write("\n")
    
    file.write(f"&OBST ID='Fire Ring {ring}', XB={x_org - cell_size}, {x_org + cell_size}, {y_org - cell_size}, {y_org + cell_size}, {z_org}, {z_org + fire_height}, SURF_IDS='Ring {ring}','Gypsum','Gypsum'/\n")
    file.write(f"&SURF ID='Ring {ring}',\n")
    file.write("    COLOR='RED',\n")
    file.write(f"    HRRPUA={HRRPUA},\n")
    file.write(f"    RAMP_Q='RAMP_{ring}',\n")
    file.write("    TMP_FRONT=300.0/\n")
    
    HRR = 0
    while HRR <= ring_peak:
        HRR = min(t*t*fgr, peak_fs)
        file.write(f"&RAMP ID='RAMP_{ring}', T={t}, F={round((HRR)/ring_peak,7)},/\n")
        t = min(t + time_step, math.sqrt(ring_peak/fgr)+0.000000001)
    centre_square_fire_area = (cell_size*2)**2
    ring_peak_prev = ring_peak
    current_fire_area = centre_square_fire_area
    
    ring = ring + 1
    
    # while ring <= no_rings:
    # calc required rings
    while current_fire_area < target_fire_area:
        ring_area = ((ring*cell_size*2)**2) - current_fire_area
        current_fire_area = ((ring*cell_size*2)**2)

        # if current_fire_area > target_fire_area:
        #     pass

        ring_peak = ring_area * HRRPUA 
        
        HRR = 0
        
        file.write(f"&OBST ID='Fire Ring {ring}', XB={x_org - (ring*cell_size)}, {x_org + (ring * cell_size)}, {y_org - (ring * cell_size)}, {y_org - (ring * cell_size)+ cell_size}, {z_org}, {z_org + fire_height},SURF_IDS='Ring {ring}','Gypsum','Gypsum'/\n")
        file.write(f"&OBST ID='Fire Ring {ring}', XB={x_org - (ring*cell_size)}, {x_org + (ring * cell_size)}, {y_org + (ring * cell_size) - cell_size}, {y_org + (ring * cell_size)}, {z_org}, {z_org + fire_height},SURF_IDS='Ring {ring}','Gypsum','Gypsum'/\n")
        file.write(f"&OBST ID='Fire Ring {ring}', XB={x_org - (ring*cell_size)}, {x_org - (ring * cell_size) + cell_size}, {y_org - (ring * cell_size) + cell_size}, {y_org + (ring * cell_size)- cell_size}, {z_org}, {z_org + fire_height},SURF_IDS='Ring {ring}','Gypsum','Gypsum'/\n")
        file.write(f"&OBST ID='Fire Ring {ring}', XB={x_org + (ring*cell_size) - cell_size}, {x_org + (ring * cell_size)}, {y_org - (ring * cell_size) + cell_size}, {y_org + (ring * cell_size)- cell_size}, {z_org}, {z_org + fire_height},SURF_IDS='Ring {ring}','Gypsum','Gypsum'/\n")
        file.write(f"&SURF ID='Ring {ring}',\n")
        file.write("    COLOR='RED',\n")
        file.write(f"    HRRPUA={HRRPUA},\n")
        file.write(f"    RAMP_Q='RAMP_{ring}',\n")
        file.write("    TMP_FRONT=300.0/\n")
        file.write(f"&RAMP ID='RAMP_{ring}', T={t}, F=0,/\n")
        t = t + 0.0001
        while HRR/ring_peak < 0.9999:
            HRR = min((t*t*fgr)-ring_peak_prev, peak_fs-ring_peak_prev)
            file.write(f"&RAMP ID='RAMP_{ring}', T={t}, F={round((HRR)/ring_peak,7)},/\n")
            t = min(t + time_step, math.sqrt((ring_peak+ring_peak_prev)/fgr))
            if ((t*t*fgr)-ring_peak_prev > peak_fs-ring_peak_prev):
                break
        ring_peak_prev = ring_peak +ring_peak_prev
        ring = ring+1
    file.close


def Draw_Closed_Door(x1, x2, y1, y2, z1, z2, fdsfile): ### codes the required vents and HVAC inputs for a non-smoke sealed closed door for the cc2 models
    file = open(fdsfile, "a")    
    bottom_gap = 0.01
    other_gaps = 0.004

    file.write("\n")
    file.write("\n")

    if x2-x1>y2-y1:
        door = "v"
    else:
        door = "h"
  
    if door == "v":
    
        file.write(f"&VENT ID='top vent 1', SURF_ID='INERT', XB={x1},{x2},{y1},{y1},{z2-0.1},{z2}  , RGB=200,200,200 / Top Vent 1/\n")
        file.write(f"&VENT ID='top vent 2', SURF_ID='INERT', XB={x1},{x2},{y2},{y2},{z2-0.1},{z2}  , RGB=200,200,200 / Top Vent 2/\n")
        
        file.write(f"&VENT ID='left vent 1', SURF_ID='INERT', XB={x1},{x1+0.1},{y1},{y1},{z1+0.1},{z2-0.1}  , RGB=200,200,200 / Left Vent 1/\n")
        file.write(f"&VENT ID='left vent 2', SURF_ID='INERT', XB={x1},{x1+0.1},{y2},{y2},{z1+0.1},{z2-0.1}  , RGB=200,200,200 / Left Vent 2/\n")   
        
        file.write(f"&VENT ID='right vent 1', SURF_ID='INERT', XB={x2-0.1},{x2},{y1},{y1},{z1+0.1},{z2-0.1}  , RGB=200,200,200 / Right Vent 1/\n")
        file.write(f"&VENT ID='right vent 2', SURF_ID='INERT', XB={x2-0.1},{x2},{y2},{y2},{z1+0.1},{z2-0.1}  , RGB=200,200,200 / Right Vent 2/\n") 
        
        file.write(f"&VENT ID='bottom vent 1', SURF_ID='INERT', XB={x1},{x2},{y1},{y1},{z1},{z1+0.1}  , RGB=200,200,200 / Bottom Vent 1/\n")
        file.write(f"&VENT ID='bottom vent 2', SURF_ID='INERT', XB={x1},{x2},{y2},{y2},{z1},{z1+0.1}  , RGB=200,200,200 / Bottom Vent 2/\n")
        
        file.write(f"&HVAC ID='top leak', TYPE_ID='LEAK', VENT_ID='top vent 1', VENT2_ID='top vent 2', AREA={(x2-x1)*other_gaps}, LEAK_ENTHALPY=.TRUE. / top leak /\n" )
        file.write(f"&HVAC ID='left leak', TYPE_ID='LEAK', VENT_ID='left vent 1', VENT2_ID='left vent 2', AREA={(z2-z1)*other_gaps}, LEAK_ENTHALPY=.TRUE. / left leak /\n" )
        file.write(f"&HVAC ID='right leak', TYPE_ID='LEAK', VENT_ID='right vent 1', VENT2_ID='right vent 2', AREA={(z2-z1)*other_gaps}, LEAK_ENTHALPY=.TRUE. / left leak /\n" )
        file.write(f"&HVAC ID='bottom leak', TYPE_ID='LEAK', VENT_ID='bottom vent 1', VENT2_ID='bottom vent 2', AREA={(x2-x1)*bottom_gap}, LEAK_ENTHALPY=.TRUE. / left leak /\n" )
        
    else:
        
        file.write(f"&VENT ID='top vent 1', SURF_ID='INERT', XB={x1},{x1},{y1},{y2},{z2-0.1},{z2}  , RGB=200,200,200 / Top Vent 1/\n")
        file.write(f"&VENT ID='top vent 2', SURF_ID='INERT', XB={x2},{x2},{y1},{y2},{z2-0.1},{z2}  , RGB=200,200,200 / Top Vent 2/\n")
        
        file.write(f"&VENT ID='left vent 1', SURF_ID='INERT', XB={x1},{x1},{y1},{y1+0.1},{z1+0.1},{z2-0.1}  , RGB=200,200,200 / Left Vent 1/\n")
        file.write(f"&VENT ID='left vent 2', SURF_ID='INERT', XB={x2},{x2},{y1},{y1+0.1},{z1+0.1},{z2-0.1}  , RGB=200,200,200 / Left Vent 2/\n")   
        
        file.write(f"&VENT ID='right vent 1', SURF_ID='INERT', XB={x1},{x1},{y2-0.1},{y2},{z1+0.1},{z2-0.1}  , RGB=200,200,200 / Right Vent 1/\n")
        file.write(f"&VENT ID='right vent 2', SURF_ID='INERT', XB={x2},{x2},{y2-0.1},{y2},{z1+0.1},{z2-0.1}  , RGB=200,200,200 / Right Vent 2/\n") 
        
        file.write(f"&VENT ID='bottom vent 1', SURF_ID='INERT', XB={x1},{x1},{y1},{y2},{z1},{z1+0.1}  , RGB=200,200,200 / Bottom Vent 1/\n")
        file.write(f"&VENT ID='bottom vent 2', SURF_ID='INERT', XB={x2},{x2},{y1},{y2},{z1},{z1+0.1}  , RGB=200,200,200 / Bottom Vent 2/\n")       
        
        file.write(f"&HVAC ID='top leak', TYPE_ID='LEAK', VENT_ID='top vent 1', VENT2_ID='top vent 2', AREA={(y2-y1)*other_gaps}, LEAK_ENTHALPY=.TRUE. / top leak /\n" )
        file.write(f"&HVAC ID='left leak', TYPE_ID='LEAK', VENT_ID='left vent 1', VENT2_ID='left vent 2', AREA={(z2-z1)*other_gaps}, LEAK_ENTHALPY=.TRUE. / left leak /\n" )
        file.write(f"&HVAC ID='right leak', TYPE_ID='LEAK', VENT_ID='right vent 1', VENT2_ID='right vent 2', AREA={(z2-z1)*other_gaps}, LEAK_ENTHALPY=.TRUE. / left leak /\n" )
        file.write(f"&HVAC ID='bottom leak', TYPE_ID='LEAK', VENT_ID='bottom vent 1', VENT2_ID='bottom vent 2', AREA={(y2-y1)*bottom_gap}, LEAK_ENTHALPY=.TRUE. / left leak /\n" )
    file.close

def Draw_Door_Hole(x1, x2, y1, y2, z1, z2, fdsfile): ### codes the required vents and HVAC inputs for a non-smoke sealed closed door for the cc2 models
    file = open(fdsfile, "a")    

    file.write("\n")
    file.write("\n")

    if x2-x1>y2-y1:
        door = "v"
    else:
        door = "h"
  
    if door == "v":
        file.write(f"&HOLE ID='Open Door', XB={x1},{x2},{y1-0.1},{y2+0.1},{z1},{z2} /\n")
    else:
        file.write(f"&HOLE ID='Open Door', XB={x1-0.1},{x2+0.1},{y1},{y2},{z1},{z2} /\n")
    file.close

''' TODO: build an array for the fds file '''

# todo -> send in sprinkler params -> later from user input
def Amend_FDS_File(
                scenario, 
                model, 
                fn, 
                Scenario_Names, 
                dest_dir, 
                fds_file_name, 
                cell_size, 
                Proposed_Detection, 
                CC_Detection, 
                sprinklerRoomArea, 
                roomHeight, 
                growthRate, 
                rTI, 
                tActive, 
                peak_fs_non_sprinkler,
                custom_fs_sprinkler,
                custom_sprinkler_distance
                  # either chosen, custom or sprinklered & to be calculated (None)
                ):
    
    #1. delete tail
    Delete_Line_Containing_String("&TAIL /", fn)  ## deletes "tail" from FDS file, to be added at the end. 
    
    #2 add fire
    # if fire already ring skip

    firecoords = search_string_in_file(f"'{scenario}'", fn) ## gets line of FDS code for temporary fire obstruction
    firecoords = Get_Coords_from_FDS_Code(firecoords)  ## gets coordinates of temporary fire obstruction from line of fds code, returns as a list of six floats
    for i in Scenario_Names: ## deletes all base fire obstructions from the model
        Delete_Line_Containing_String(f"&OBST ID='{i}'", fn)

    import re
    def extract_nums_from_string(string):
        return re.findall(r"[-+]?\d*\.\d+|\d+", string)

    fire_array = []
    #3. sort sprinklers
    if model != "PD1": ## if an unsprinklered scenario, delete al sprinklers from the model
        Delete_Line_Containing_String("SPRK", fn)
        write_unsprinklered_fire((firecoords[0]+(firecoords[1]-firecoords[0])/2), (firecoords[2]+(firecoords[3]-firecoords[2])/2), firecoords[4], scenario, fn, cell_size, peak_fs_non_sprinkler)
    else:   ##else delete all sprinklers which shouldnt be in this model. - not sure if I follow this?
        file = open(fn, "a") # a for append
        for i in Scenario_Names:
            if i != scenario:
                Delete_Line_Containing_String(f"{i}_SPRK", fn)
            else:
                # find activation time
                # need room dimensions, ceiling height and distance from fire to sprinkler head 
                # find previous sprk lines
                # TODO: allow for no time set -> just add to line
                sprk_lines = [f for f in open(fn, "r").readlines() if "SPRK" in f]
                # get parts with xyz co-ords => compare with fire co-ords
                # ceiling height taken from sprinkler z?? or mesh max height
                sprk_co_ords = [extract_nums_from_string(f)[-4:-1] for f in sprk_lines]
                fire_centre = find_centre_coords(firecoords)

                if custom_sprinkler_distance:
                    min_dist = custom_sprinkler_distance
                else:
                    # calc min_distance 
                    min_dist = None
                    
                    point2 = fire_centre[0:2]
                    for current_sprk in sprk_co_ords:
                        current_sprk = [float(f) for f in current_sprk]
                        point1 = current_sprk[0:2]
                        
                        current_distance = round(find_dist(point1, point2), 2)
                        if min_dist == None or current_distance < min_dist: # TBC if min distance from sprinklers to be used?
                            min_dist = current_distance


                if custom_fs_sprinkler:
                    activation_time = round(math.sqrt(custom_fs_sprinkler / growthRate))
                else:
                    activation_time = computeActivationTime(min_dist, sprinklerRoomArea, roomHeight, growthRate, rTI, tActive)


                new_sprk_lines = []
                for index, current_sprk_line in enumerate(sprk_lines):
                    temp_split = current_sprk_line.split(",")[-1]
                    temp_nums = extract_nums_from_string(temp_split)
                    prev_val = temp_nums[-1]
                    # insert new number to temp_split
                    temp_split = temp_split.replace(prev_val,f"{activation_time}")
                    updated_line = ",".join(current_sprk_line.split(",")[:-1]) + temp_split
                    new_sprk_lines.append(updated_line)

                Delete_Line_Containing_String(f"{i}_SPRK", fn)
                # add lines with timings
                
                for row in new_sprk_lines:
                    file.write(f"{row}\n") 

        fire_array = return_sprinklered_fire_fds((firecoords[0]+(firecoords[1]-firecoords[0])/2), (firecoords[2]+(firecoords[3]-firecoords[2])/2), firecoords[4], scenario, fn, cell_size, activation_time)



    fds_lines = open(f"{dest_dir}/{fds_file_name}", "r").readlines()
    
    

    # used to view co-ords of all doors 
    smoke_seal_fds_list = []

    if model == "PD1":
        ameneded_line = [line.replace("2", "8") for line in fds_lines if "T_END" in line]
        Delete_Line_Containing_String(f"T_END", fn) 
        smoke_seal_fds_list.append(ameneded_line)

    doors_object, cc_escape_door = return_door_object_and_cc_escape_door(firecoords, fds_lines)
    cc_escape_door_coords = doors_object[cc_escape_door["type"]][cc_escape_door["index"]] 
    door_types = list(doors_object.keys())
    # add flat entrance door seals for all
    front_door_coords = doors_object['Flat_Entrance_Door'][0] 
    smoke_seal_fds_list.append(return_doors_seals_fds(cell_size, smoke_sealed=True, number_of_doors=1, door_coords=front_door_coords, Door_Number=0))    
    
    '''     
            look for each occurrence of each door type 
            add leakages
            find fire room door -> needs to be open in CC2
            front door vents already added
            add to all other protected corridor doors
            Can add to all protected corridors at first
    '''
    for door_type in door_types:
        if '_Entrance' not in door_type:
            is_single_door = "Double" not in door_type
            for index, current_door_coords in enumerate(doors_object[door_type]):
                if current_door_coords != cc_escape_door_coords: # added for CC2 below
                    smoke_seal_fds_list.append(return_doors_seals_fds(cell_size, smoke_sealed=False, number_of_doors=1, door_coords=current_door_coords, Door_Number=index, single_door=is_single_door))

    #4. sort code compliant obstructions
    if "PD" in model: ## for all PD models, remove code compliant only obstructions and doors
        Delete_Line_Containing_String("&OBST ID='CC_WALL'", fn)
        Delete_Line_Containing_String("Internal_Flat_Door", fn) # removes all doors but front entrance to flat    
    else:
        # Code Compliant
        ''' 
            vents added to cc_escape_door only for CC2
        '''
        if model == "CC2": ## if CC2 model, add vents around closed door
            # draw seals around all doors
            smoke_seal_fds_list.append(return_doors_seals_fds(cell_size, smoke_sealed=False, number_of_doors=1, door_coords=cc_escape_door_coords, Door_Number=cc_escape_door["index"]))
            # Draw_Closed_Door(cc_escape_door_coords[0], cc_escape_door_coords[1], cc_escape_door_coords[2], cc_escape_door_coords[3], cc_escape_door_coords[4], cc_escape_door_coords[5], fn)
        else:  ## if CC1, delete door obstruction and add a hole for the door
            Delete_Line_Containing_String(f"'{scenario}_door", fn)           
            Draw_Door_Hole(cc_escape_door_coords[0], cc_escape_door_coords[1], cc_escape_door_coords[2], cc_escape_door_coords[3], cc_escape_door_coords[4]-0.01, cc_escape_door_coords[5], fn)

    #5 remove unecessary detectors
    if Proposed_Detection != CC_Detection:
        if "CC" in model:
            Delete_Line_Containing_String(f"Smoke detector LD{Proposed_Detection}", fn)       
    
    # TODOl change to array until the end
    file = open(fn, "a") # a for append
    for section in smoke_seal_fds_list:
            for row in section:
                file.write(f"{row}\n")
    ''' 
    find temp sensors, fire and door for slice placement
    z slices at 1.7m above FFL in relation to sensor -> may be different if over 2 levels and along connecting stair
    duplicates e.g. many at 1.7m z removed

    '''
    slice_points = []
    # fire co-ord
    fire_centre = find_centre_coords(firecoords)
    # change z to 1.7
    fire_centre_slice = fire_centre
    fire_centre_slice[-1] = 1.7 # changing from ground level
    slice_points.append(fire_centre_slice)
    # temp sensors
    temp_sensor_lines = [f for f in fds_lines if "ID='TEMP" in f]
    temp_sensor_coords = [extract_nums_from_string(f)[1:] for f in temp_sensor_lines]
    slice_points.extend(temp_sensor_coords)
    # door locations
    # add all in object; later have logic to just add the one's present in specific scenario
    door_slice_points = []
    ''' 
        doors should only have either x or y 
        not clear if code allows for multiple doors?
    '''
    if "CC" in model:
        # if z min = zero => 1.7 for z
        cc_escape_door_slice = find_centre_coords(cc_escape_door_coords) # change z
        cc_escape_door_slice[-1] = 1.7 # changing from mid door height
        slice_points.append(cc_escape_door_slice)

    front_door_slice = find_centre_coords(front_door_coords)
    front_door_slice[-1] = 1.7 # changing from mid door height
    slice_points.append(front_door_slice)


    pass
    slice_object = {"X":[], "Y":[], "Z":[]}
    for point in slice_points:
        x, y, z = point
        x = float(x)
        y = float(y)
        z = float(z)
        if x not in slice_object["X"]:
            slice_object["X"].append(x)
        if y not in slice_object["Y"]:
            slice_object["Y"].append(y)
        if z not in slice_object["Z"]:
            slice_object["Z"].append(z)

    # locate slices at slice_object locations
    # include lines for slices
    slice_types = ['TEMPERATURE', 'VISIBILITY', 'VELOCITY'] # check if any further types needed
    slice_lines = []
    for type in slice_types:
        for axis in list(slice_object.keys()):
            for axis_point in slice_object[axis]:
                line = f"&SLCF QUANTITY='{type}', ID='{axis} = {axis_point} m: Temperature', PB{axis}={axis_point}/"
                slice_lines.append(line)
                # &SLCF QUANTITY='TEMPERATURE', ID='X = 5.847309 m: Temperature', PBX=5.847309/
    for row in slice_lines:
        # for row in section:
        file.write(f"{row}\n")
    #6 resize inlet holes - to be added
    holecoords = search_string_in_file(f"'{scenario}_Inlet_Air'", fn) ## gets line of FDS code for temporary inlet obstruction
    holecoords = Get_Coords_from_FDS_Code(holecoords)  ## gets coordinates of temporary inlet obstruction from line of fds code, returns as a list of six floats 
    Delete_Line_Containing_String("_Inlet_Air", fn) 
    file = open(fn, "a") 
    file.write("\n")
    if model != "PD1":    
        file.write(f"&HOLE ID='Inlet Air', XB={holecoords[0]},{holecoords[1]},{holecoords[2]},{holecoords[3]},{holecoords[4]-0.01},{holecoords[5]} /\n")

    else:
    #    smaller fire requires 1x1 inlet
    #    wider of x and y should change to 1; z change to 1; other direction stays the same
        deltaX = abs(holecoords[0] - holecoords[1])
        deltaY = abs(holecoords[2] - holecoords[3])
        x1 = holecoords[0]
        y1 = holecoords[2]
        if deltaX > deltaY:
            x2 = x1 + 1
            y2 = holecoords[3]
        else:
            y2 = y1 + 1
            x2 = holecoords[1]
        file.write(f"&HOLE ID='Inlet Air', XB={x1},{x2},{y1},{y2},{holecoords[4]-0.01},{holecoords[4]+1} /\n") 
    
    file.close
    #7 remove uneccessary point measurements
    
    if model != "PD1":
        Delete_Line_Containing_String("DEVC_ID='WATER", fn)     
    

    #8 add tail
    file = open(fn, "a") 
    file.write("\n")    
    file.write("&TAIL /\n")
    print(f'{fn} saved')
    
#### 3. Get / Define Variables 
def draw_params_from_excel(
                            path_to_dir, 
                            root_dir,
                            peak_fs_non_sprinkler,
                            custom_fs_sprinkler,
                            custom_sprinkler_distance
                            ): 
    workbook = openpyxl.load_workbook(f"{path_to_dir}/{root_dir}/{root_dir} Variables.xlsx") # create spreadsheet and worksheet. This will be on the drive so other parts of the program can read it. 
    worksheet = workbook.active

    Project_Name = worksheet["B1"].value
    Number_Of_Bedrooms = worksheet["B2"].value
    Number_Of_Lounges = worksheet["B3"].value
    Number_Of_Kitchens = worksheet["B4"].value
    Lounge_Fires = worksheet["B5"].value
    Lounge_Fires_Own_Door = worksheet["B6"].value
    Bedroom_Fires = worksheet["B7"].value
    Bedroom_Fires_Own_Door = worksheet["B8"].value
    Kitchen_Fires = worksheet["B9"].value
    Kitchen_Fires_Own_Door = worksheet["B10"].value
    TD_From_Bedrooms = worksheet["B11"].value
    TD_From_Kitchens = worksheet["B12"].value
    TD_From_Lounges = worksheet["B13"].value
    Suppression_Type = worksheet["B14"].value
    No_Scenarios = worksheet["B15"].value
    Scenario_Names = string_to_list_and_clean(worksheet["B16"].value)
    No_Openable_Doors = worksheet["B17"].value
    Default_Door = worksheet["B18"].value
    Scenario_Doors = worksheet["B19"].value
    Proposed_Detection = (worksheet["B20"].value)
    CC_Detection = (worksheet["B21"].value)
    Floor_To_Ceiling = float(worksheet["B22"].value)

    names = ["peak_fs_non_sprinkler", "custom_fs_sprinkler", "custom_sprinkler_distance"]
    for idx, total in enumerate([peak_fs_non_sprinkler,
                            custom_fs_sprinkler,
                            custom_sprinkler_distance
                            ]):
        
        worksheet.write(25+idx,0,names[idx])
        worksheet.write(25+idx,1,total)
    # sprinklerRoomArea=30 # send in from stage 1!
    roomHeight=2.5
    rTI=90 # should be changeable??
    tActive=68 # should be changeable??

    return  [Project_Name, 
            # Number_Of_Bedrooms, 
            # Number_Of_Lounges, 
            # Number_Of_Kitchens,
            # Lounge_Fires,
            # Bedroom_Fires,
            # Kitchen_Fires,
            # TD_From_Bedrooms,
            # TD_From_Kitchens,
            # TD_From_Lounges, 
            # Suppression_Type,
            # No_Scenarios,
            Scenario_Names,
            Proposed_Detection,
            CC_Detection,
            Floor_To_Ceiling,
            rTI,
            # sprinklerRoomArea,
            tActive]

# TODO: slice placement generator
# TODO: needs to work for folder outside of current directory!
# a. get from excel sheet.
# prep for gui -> place in function and send in params

# TODO: have peak heat release rate as param,
# allow custom: calc or custom sprinklered peak hrr, 
# allow if calced distance can be calced or custom inputted
# get other info from file rather than sent in?
def run_stage_two(
        path_to_dir=None, 
        root_dir = 'Roneo Corner - Smallest Flat', 
        growthRate=growthRateObject["fast"], 
        peak_fs_non_sprinkler=1500,
        custom_fs_sprinkler=None,
        custom_sprinkler_distance=None
        ):


    # TODO: write inputs to excel and variables object

    # find path to txt file
    # TODO: extract file name
    file_name = os.path.basename(root_dir)
    if path_to_dir: 
        path_txt = f"{path_to_dir}/{root_dir}/{root_dir} Variables.txt"
    else:
        path_txt = f"{root_dir}/{file_name} Variables.txt"
        path_to_dir = os.path.dirname(root_dir)
        root_dir = os.path.basename(root_dir)
   
    param_list = [
        "Project_Name", 
        "Number_Of_Bedrooms", 
        "Number_Of_Lounges", 
        "Number_Of_Kitchens",
        "Lounge_Fires",
        "Bedroom_Fires",
        "Kitchen_Fires",
        "TD_From_Bedrooms",
        "TD_From_Kitchens",
        "TD_From_Lounges", 
        "Suppression_Type",
        "No_Scenarios",
        "Scenario_Names",
        "Proposed_Detection",
        "CC_Detection",
        "Floor_To_Ceiling",
        "rTI",
        "sprinklerRoomArea",
        "tActive"
        ]
    # TODO: throw error if txt file not present
    import ast
    import json
    if os.path.exists(path_txt):
        with open(path_txt, 'w') as f:
            lines = json.loads(f.readlines()[0])


    #         Project_Name = lines['Project_Name']
    #         # Number_Of_Bedrooms = lines['Number_Of_Bedrooms']
    #         # Number_Of_Lounges = lines['Number_Of_Lounges']
    #         # Number_Of_Kitchens = lines['Number_Of_Kitchens']
    #         # Lounge_Fires = lines['Lounge_Fires']
    #         # # Bedroom_Fires = lines['Bedroom_Fires']
    #         # Kitchen_Fires = lines['Kitchen_Fires']
    #         # TD_From_Bedrooms = lines['TD_From_Bedrooms']
    #         # TD_From_Kitchens = lines['TD_From_Kitchens']
    #         # TD_From_Lounges = lines['TD_From_Lounges']
    #         # Suppression_Type = lines['Suppression_Type']
    #         # No_Scenarios = lines['No_Scenarios']
    #         Scenario_Names = lines['Scenario_Names']
    #         Proposed_Detection = lines['Proposed_Detection']
    #         CC_Detection = lines['CC_Detection'] # not added apparently
    #         Floor_To_Ceiling = lines['Floor_To_Ceiling']
    #         rTI = lines['rti']
            sprinklered_room_area = lines['sprinklered_room_area']
            model_object = lines

            for item in [
                peak_fs_non_sprinkler,
                custom_fs_sprinkler,
                custom_sprinkler_distance
            ]:
                var_name = [ i for i, a in locals().items() if a == item][0]
                model_object[var_name] = item

            json.dump(model_object, f)
    else:
        sprinklered_room_area = 30
    #         tActive = lines['tActive']
    # else:
    [
    Project_Name, 
    # Number_Of_Bedrooms, 
    # Number_Of_Lounges, 
    # Number_Of_Kitchens,
    # Lounge_Fires,
    # Bedroom_Fires,
    # Kitchen_Fires,
    # TD_From_Bedrooms,
    # TD_From_Kitchens,
    # TD_From_Lounges, 
    # Suppression_Type,
    # No_Scenarios,
    Scenario_Names,
    Proposed_Detection,
    CC_Detection,
    Floor_To_Ceiling,
    rTI,
    # sprinklered_room_area,
    tActive
    ] = draw_params_from_excel(
                                path_to_dir, 
                                root_dir, 
                                peak_fs_non_sprinkler,
                                custom_fs_sprinkler,
                                custom_sprinkler_distance
                                )
   

    # b. new variables

    Model_List = ["CC1", "CC2", "PD1", "PD2"]
    cell_size = 0.1

    base_filename = Project_Name.replace(" ", "_")
    base_filename = base_filename + "_Base_Model.fds"

    #### 4. Generate all FDS Files
    n=0
    while n < len(Scenario_Names): # for each scenario in the list of the scenario names
        try: 
            os.mkdir(f"{path_to_dir}/{Project_Name}/{Scenario_Names[n]}") #try and make a directory for the scenario name, if it already exists dont bother
        except OSError as error: 
            print("")
        m=0
        while m < len(Model_List):  # for each model needed for each scenario - model list contains 4 models
            try: 
                os.mkdir(f"{path_to_dir}/{Project_Name}/{Scenario_Names[n]}/{Model_List[m]}") #try and make a directory for the model name in the scenario directory, if it already exists dont bother
            except OSError as error: 
                print("")
            dest_dir = f"{path_to_dir}/{Project_Name}/{Scenario_Names[n]}/{Model_List[m]}"  ### these lines copy the base model and paste it in the new model directory
            src_file = f"{path_to_dir}/{Project_Name}/{base_filename}"
            fds_file_name = f'{Model_List[m]}.fds'
            shutil.copy(src_file, dest_dir)
            # delete if already there
            if fds_file_name in os.listdir(dest_dir):
                os.remove(f'{dest_dir}/{fds_file_name}')
            # rename copy of base fds file
            os.rename(f"{dest_dir}/{base_filename}", f"{dest_dir}/{fds_file_name}")
            file_path = (f"{path_to_dir}/{Project_Name}/{Scenario_Names[n]}/{Model_List[m]}/{fds_file_name}") ## sets the copied file as the file to be edited
            Amend_FDS_File(
                scenario=Scenario_Names[n],
                model=Model_List[m], 
                fn=file_path, 
                Scenario_Names=Scenario_Names, 
                dest_dir=dest_dir, 
                fds_file_name=fds_file_name, 
                cell_size=cell_size, 
                Proposed_Detection=Proposed_Detection, 
                CC_Detection=CC_Detection, 
                sprinklerRoomArea=sprinklered_room_area, 
                roomHeight=Floor_To_Ceiling, 
                growthRate=growthRate, 
                rTI=rTI, 
                tActive=tActive,
                peak_fs_non_sprinkler=peak_fs_non_sprinkler,
                custom_fs_sprinkler=custom_fs_sprinkler,
                custom_sprinkler_distance=custom_sprinkler_distance
                )
            m=m+1
        n = n+1

if __name__ == '__main__':
    run_stage_two(
        root_dir = "test2", 
        growthRate=growthRateObject["medium"],
        peak_fs_non_sprinkler=1500,
        custom_fs_sprinkler=None,
        custom_sprinkler_distance=None
        ) 
    
    # should have 1500MW param








    
#write_sprinklered_fire(0.1, 1, 1, 0, "Kyyyy")


      




      


