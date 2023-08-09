import math
# TODO: if fire size met using alpha*t^2 before sprinkler activation -> max fire from that time 
def return_sprinklered_fire_fds(x_org, y_org, z_org, Scenario_Name, fdsfile, cell_size, sprinkler_activation, custom_hrr=None):
    array = []
    all_ring_list = []
    time_step = 1
    fire_height = 0.1
    if "Kitchen" in Scenario_Name:
        fgr = 0.0469
        # peak_time = 73 
    else:
        fgr = 0.0117
    
    HRRPUA = 445

    peak_time = sprinkler_activation # or using alpha t^2
    # 
    peak_hrr = fgr * (peak_time **2) # prev value: 250 
    total_fire_area = peak_hrr / HRRPUA # prev value: 0.5617977528 

    no_rings = math.ceil(math.sqrt(total_fire_area) / (2*cell_size))  
 
    t = 0
    # current_ring = 1
    
    # ring_peak_hrr = (ring*cell_size*2)**2*HRRPUA 
    peak_hrr_of_all_prev_rings = 0
    current_fire_area = 0


    array.append("\n")
    array.append("\n")

    for current_ring in range(1, no_rings + 1):
        # TODO: remove reliance on file write here
        array.append(f"&OBST ID='Fire Ring {current_ring}', XB={x_org - (current_ring*cell_size)}, {x_org + (current_ring * cell_size)}, {y_org - (current_ring * cell_size)}, {y_org - (current_ring * cell_size)+ cell_size}, {z_org}, {z_org + fire_height},SURF_IDS='Ring {current_ring}','Gypsum','Gypsum'/\n")
        array.append(f"&OBST ID='Fire Ring {current_ring}', XB={x_org - (current_ring*cell_size)}, {x_org + (current_ring * cell_size)}, {y_org + (current_ring * cell_size) - cell_size}, {y_org + (current_ring * cell_size)}, {z_org}, {z_org + fire_height},SURF_IDS='Ring {current_ring}','Gypsum','Gypsum'/\n")
        array.append(f"&OBST ID='Fire Ring {current_ring}', XB={x_org - (current_ring*cell_size)}, {x_org - (current_ring * cell_size) + cell_size}, {y_org - (current_ring * cell_size) + cell_size}, {y_org + (current_ring * cell_size)- cell_size}, {z_org}, {z_org + fire_height},SURF_IDS='Ring {current_ring}','Gypsum','Gypsum'/\n")
        array.append(f"&OBST ID='Fire Ring {current_ring}', XB={x_org + (current_ring*cell_size) - cell_size}, {x_org + (current_ring * cell_size)}, {y_org - (current_ring * cell_size) + cell_size}, {y_org + (current_ring * cell_size)- cell_size}, {z_org}, {z_org + fire_height},SURF_IDS='Ring {current_ring}','Gypsum','Gypsum'/\n")
        array.append(f"&SURF ID='Ring {current_ring}',\n")
        array.append("    COLOR='RED',\n")
        array.append(f"    HRRPUA={HRRPUA},\n")
        array.append(f"    RAMP_Q='RAMP_{current_ring}',\n")
        array.append("    TMP_FRONT=300.0/\n")

        if t > 0:
            array.append(f"&RAMP ID='RAMP_{current_ring}', T={t}, F=0,/\n")
            t += 0.0001
    # pre amble code for ring

    # get ring area
        ring_area = ((current_ring*cell_size*2)**2) - current_fire_area
    # get ring peak 
        ring_peak_hrr = (ring_area * HRRPUA)

        current_ring_hrr = 0
            
        
    # t and F i.e. % of ring peak
        # loop through while ring_hrr < target_hrr
        #  
        current_ring_list = []
        if current_ring == 4:
            pass
        # add t; and F
        while peak_hrr_of_all_prev_rings + current_ring_hrr < peak_hrr and current_ring_hrr < ring_peak_hrr * 0.999:
            current_ring_hrr = min((t*t*fgr) - peak_hrr_of_all_prev_rings, peak_hrr - peak_hrr_of_all_prev_rings)
            hrr_ramp = round(current_ring_hrr / ring_peak_hrr, 7) # add to array
            if hrr_ramp > 0.99:
                hrr_ramp = 1.0
            current_ring_list.append({"F": hrr_ramp, "t": t})
            array.append(f"&RAMP ID='RAMP_{current_ring}', T={t}, F={hrr_ramp},/\n")
            t = min(t + time_step, math.sqrt((ring_peak_hrr + peak_hrr_of_all_prev_rings) / fgr), peak_time)
    # after loop
        if t != peak_time :
            array.append(f"&RAMP ID='RAMP_{current_ring}', T={peak_time}, F={hrr_ramp},/\n")
        array.append(f"&RAMP ID='RAMP_{current_ring}', T={peak_time+120}, F=0,/\n")
        current_ring_list.append({"F": hrr_ramp, "t": peak_time})
        current_ring_list.append({"F": hrr_ramp, "t": peak_time + 120})
        all_ring_list.append(current_ring_list) 

        peak_hrr_of_all_prev_rings = ring_peak_hrr +peak_hrr_of_all_prev_rings
        current_fire_area = (current_ring*cell_size*2)**2

    file = open(fdsfile, "a")
    for line in array:
        file.write(line)
    file.close
    return array

if __name__ == '__main__':
    from helper_function import computeActivationTime
    sprinklerRoomArea=92
    sprinkler_activation = computeActivationTime(2, sprinklerRoomArea, 2.3, growthRate=0.0117)
    fdsfile = r'C:\Users\IanShaw\Dropbox\R&D\Open Plan Robot\Test Run for Ian\Other Code\test2.fds'
    return_sprinklered_fire_fds(1.9, 9.1, 0.1, "Lounge Fire 1", fdsfile, 0.1, sprinkler_activation)

    # run_stage_two(
    #     root_dir = "NHBC 12x16", 
    #     sprinklerRoomArea=92, 
    #     roomHeight=2.3, 
    #     growthRate=growthRateObject["medium"], 
    #     rTI=90, 
    #     tActive=68
    #     ) 