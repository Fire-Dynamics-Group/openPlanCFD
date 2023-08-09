''' Part of Stage 2 '''
# fix -> second leakage vents have 1 cell gap from door rather than snug to door side
from helper_function import convert_print_to_string, find_centre_coords, find_dist, Get_Coords_from_FDS_Code

def return_door_object_and_cc_escape_door(firecoords, fds_lines):
    door_types = ['Internal_Flat_Door_Single', 'Internal_Flat_Door_Double', 'Flat_Entrance_Door'] # flat_entrance to be actioned for all
    # TODO: test if door type not in fds e.g. no double doors
    # create object with co-ords of each
    doors_object = {}
    
    fire_centre = find_centre_coords(firecoords)
    min_dist = None
    closest_door = None
    for type in door_types:
        lines_with_type = [Get_Coords_from_FDS_Code(line) for line in fds_lines if type in line]
        doors_object[type] = lines_with_type
        # find closest door to fire
        # find door centre
        if "Entrance" not in type:
            for index, current_door in enumerate(lines_with_type):
                current_centre = find_centre_coords(current_door)
                current_dist = find_dist(current_centre, fire_centre)
                if min_dist == None or current_dist < min_dist:
                    closest_door = {"type": type, "index": index}
                    min_dist = current_dist
            # should add leakages for CC only
            # add leakages for front door for all models
    # could ask user to confirm -> if not cycle through doors
    cc_escape_door = closest_door

    return doors_object, cc_escape_door


# # variables required door height, door width, smoke sealed or not, cell size, along x or y axis


# cell_size = float(input("Enter the grid size (m): "))
# door_height = float(input("Enter the door height (m): "))
# door_width = float(input("Enter the door width (m): "))
# smoke_sealed = input("Are the doors smoke sealed (yes or no): ")
# #while smoke_sealed != "yes" or "no":
# #    smoke_sealed = input("enter 'yes' or 'no', it's case sensitive: ")
# number_of_doors = int(input("Enter number of doors: "))

def return_doors_seals_fds(cell_size, smoke_sealed, number_of_doors, door_coords, Door_Number, single_door = True):
    array = []
    x1, x2, y1, y2, z1, z2 = door_coords

    x_delta = abs(x2 - x1)
    y_delta = abs(y2 - y1)

    door_width = round(max(x_delta, y_delta), 5)
    door_height = round(abs(z2 - z1), 5)

    if x_delta > y_delta:
        # top and bottom vents
        top_x1_i = x1
        top_x2_i = x2
        top_x1_ii = x1
        top_x2_ii = x2
        top_y1_i = y1
        top_y2_i = y1
        # top_y1_ii = y2 + cell_size
        # top_y2_ii = y2 + cell_size
        top_y1_ii = y2
        top_y2_ii = y2
        # lhs vents - lower in x
        lhs_x1_i = x1
        lhs_x2_i = round((x1 + cell_size),5)
        lhs_y1_i = y1 
        lhs_y2_i = y1
        lhs_x1_ii = x1
        lhs_x2_ii = round((x1 + cell_size),5)
        # lhs_y1_ii = y2 + cell_size       
        # lhs_y2_ii = y2 + cell_size 
        lhs_y1_ii = y2       
        lhs_y2_ii = y2 
        # rhs vents - higher in x
        rhs_x1_i = round((x2 - cell_size),5)
        rhs_x2_i = x2
        rhs_y1_i = y1 
        rhs_y2_i = y1
        rhs_x1_ii = round((x2 - cell_size),5)
        rhs_x2_ii = x2
        # rhs_y1_ii = y2 + cell_size       
        # rhs_y2_ii = y2 + cell_size 
        rhs_y1_ii = y2       
        rhs_y2_ii = y2 
    else:
        # top and bottom vents
        top_x1_i = x1
        top_x2_i = x1
        # top_x1_ii = x2 + cell_size
        # top_x2_ii = x2 + cell_size
        top_x1_ii = x2
        top_x2_ii = x2
        top_y1_i = y1
        top_y2_i = y2
        top_y1_ii = y1
        top_y2_ii = y2 
        # lhs vents - lower in y
        lhs_x1_i = x1
        lhs_x2_i = x1
        lhs_y1_i = y1 
        lhs_y2_i = round((y1 + cell_size),5)
        # lhs_x1_ii = x2 + cell_size
        # lhs_x2_ii = x2 + cell_size
        lhs_x1_ii = x2
        lhs_x2_ii = x2
        lhs_y1_ii = y1       
        lhs_y2_ii = round((y1 + cell_size),5) 
        # rhs vents - higher in y
        rhs_x1_i = x1
        rhs_x2_i = x1
        rhs_y1_i = round((y2 - cell_size),5)
        rhs_y2_i = y2
        # rhs_x1_ii = x2 + cell_size
        # rhs_x2_ii = x2 + cell_size
        rhs_x1_ii = x2
        rhs_x2_ii = x2
        rhs_y1_ii = round((y2 - cell_size),5)       
        rhs_y2_ii = y2  

    '''
        always have one apartment door with smoke seals and one normal door
        bring into excel sheet
    '''

    if smoke_sealed == True or smoke_sealed == "yes":
        # only one door
        bottom_gap = 0.003
        other_gaps = 0.00035
        door_prefix = "smoke_sealed_"
    else:
        bottom_gap = 0.01
        other_gaps = 0.004
        door_prefix = "nonsmoke_sealed_"

    if single_door:
        door_prefix += "single_"
    else: #is double
        door_prefix += "double_"
    # generate vents
    file = open("fdsdoors.txt", "w")
    
    counter = 0

    while counter < number_of_doors:
        ''' 
            have smoke_sealed_door1
            non_smoke_sealed_door1
            Internal_Flat_Door_Single_smoke_sealed

            needs to be located to door
        '''
        door_name = f'_{door_prefix}{Door_Number}'

        line_list = [
            (f"&VENT ID='Door{door_name}top vent 1', SURF_ID='INERT', XB={top_x1_i},{top_x2_i},{top_y1_i},{top_y2_i},{round((door_height - cell_size),5)},{door_height}, RGB=200,200,200 / Door{door_name}, Top Vent 1"),            
            (f"&VENT ID='Door{door_name}top vent 2', SURF_ID='INERT', XB={top_x1_ii},{top_x2_ii},{top_y1_ii},{top_y2_ii},{round((door_height - cell_size),5)},{door_height}, RGB=200,200,200 / Door{door_name}, Top Vent 2"),
            (" "),
            (f"&HVAC ID='Door{door_name}top leak', TYPE_ID='LEAK', VENT_ID='Door{door_name}top vent 1', VENT2_ID='Door{door_name}top vent 2', AREA={door_width * other_gaps}, LEAK_ENTHALPY=.TRUE. / Door{door_name}top leak"),
            (f"&VENT ID='Door{door_name}left vent 1', SURF_ID='INERT', XB={lhs_x1_i},{lhs_x2_i},{lhs_y1_i},{lhs_y2_i},{cell_size},{round((door_height - cell_size),5)}, RGB=200,200,200 / Door{door_name}, Left Vent 1"),            
            (f"&VENT ID='Door{door_name}left vent 2', SURF_ID='INERT', XB={lhs_x1_ii},{lhs_x2_ii},{lhs_y1_ii},{lhs_y2_ii},{cell_size},{round((door_height - cell_size),5)}, RGB=200,200,200 / Door{door_name}, Left Vent 2"),
            (" "),
            (f"&HVAC ID='Door{door_name}left leak', TYPE_ID='LEAK', VENT_ID='Door{door_name}left vent 1', VENT2_ID='Door{door_name}left vent 2', AREA={door_height * other_gaps}, LEAK_ENTHALPY=.TRUE. / Door{door_name}left leak"),
            (" "),
            (f"&VENT ID='Door{door_name}right vent 1', SURF_ID='INERT', XB={rhs_x1_i},{rhs_x2_i},{rhs_y1_i},{rhs_y2_i},{cell_size},{round((door_height - cell_size),5)}, RGB=200,200,200 / Door{door_name}, Right Vent 1"),
            (f"&VENT ID='Door{door_name}right vent 2', SURF_ID='INERT', XB={rhs_x1_ii},{rhs_x2_ii},{rhs_y1_ii},{rhs_y2_ii},{cell_size},{round((door_height - cell_size),5)}, RGB=200,200,200 / Door{door_name}, Right Vent 2"),
            (""),
            (f"&HVAC ID='Door{door_name}right leak', TYPE_ID='LEAK', VENT_ID='Door{door_name}right vent 1', VENT2_ID='Door{door_name}right vent 2', AREA={door_height * other_gaps}, LEAK_ENTHALPY=.TRUE. / Door{door_name}right leak"),
            (""),
            (f"&VENT ID='Door{door_name}bottom vent 1', SURF_ID='INERT', XB={top_x1_i},{top_x2_i},{top_y1_i},{top_y2_i},0.0,{cell_size}, RGB=200,200,200 / Door{door_name}, Bottom Vent 1"),
            (f"&VENT ID='Door{door_name}bottom vent 2', SURF_ID='INERT', XB={top_x1_ii},{top_x2_ii},{top_y1_ii},{top_y2_ii},0.0,{cell_size}, RGB=200,200,200 / Door{door_name}, Bottom Vent 2"),
            (""),
            (f"&HVAC ID='Door{door_name}bottom leak', TYPE_ID='LEAK', VENT_ID='Door{door_name}bottom vent 1', VENT2_ID='Door{door_name}bottom vent 2', AREA={door_height * bottom_gap}, LEAK_ENTHALPY=.TRUE. / Door{door_name}bottom leak"),
            (""),            
        ]
        for current_line in line_list:
            # smoke_sealed i.e. external door only needs one set of vents to the external
            # non smoke sealed i.e. internal door, needs all vents
            if  not smoke_sealed or "Vent 2" not in current_line: 
                array.append(convert_print_to_string(current_line))
        counter += 1
        Door_Number += 1
        return array

if __name__ == '__main__': 
    def kick_to_fds_file(array, file_name):
        temp = "\n".join(array)
        with open(f"{file_name}.fds", 'w') as f:
            f.write(temp)
        return f"{file_name}.fds"     
    # test for leakage vents
    # use basemodel unchanged as fds_lines 
    dest_dir = 'C:\\Users\\IanShaw\\Dropbox\\R&D\\Open Plan Robot\\Test Run for Ian\\1. Input Variables/Roneo Corner - Smallest Flat/Kitchen_Fire_1/CC1'
    fds_file_name = 'CC1.fds'
    fire_coords = [3.0, 5.4, -2.4, 0.0, 0.0, 0.1]
    door_coords = [9.0, 9.8, 0.0, 0.0, 0.0, 2.1]
    fds_lines = open(f"{dest_dir}/{fds_file_name}", "r").readlines()

    smoke_seal_fds_list = []
    cell_size = 0.1
    doors_object, cc_escape_door = return_door_object_and_cc_escape_door(fire_coords, fds_lines)
    cc_escape_door_coords = doors_object[cc_escape_door["type"]][cc_escape_door["index"]] 
    door_types = list(doors_object.keys())
    # add flat entrance door seals for all
    front_door_coords = doors_object['Flat_Entrance_Door'][0] 
    smoke_seal_fds_list.append(return_doors_seals_fds(cell_size, smoke_sealed=True, number_of_doors=1, door_coords=front_door_coords, Door_Number=0)) 
        # add all door seals here as test
    for door_type in door_types:
        if '_Entrance' not in door_type:
            is_single_door = "Double" not in door_type
            for index, current_door_coords in enumerate(doors_object[door_type]):
                # if current_door_coords != cc_escape_door_coords: # added for CC2 below
                smoke_seal_fds_list.append(return_doors_seals_fds(cell_size, smoke_sealed=False, number_of_doors=1, door_coords=current_door_coords, Door_Number=index, single_door=is_single_door))    
    # cell_size, smoke_sealed, number_of_doors, door_coords, Door_Number, single_door = True
    # array = return_doors_seals_fds(cell_size=0.1, smoke_sealed=True, number_of_doors=1, door_coords=door_coords, Door_Number=0)
    # for row in smoke_seal_fds_list:
    from itertools import chain
    unpacked = list(chain.from_iterable(smoke_seal_fds_list))
    name = kick_to_fds_file(unpacked, file_name="test2")

