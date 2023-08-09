import pandas as pd
import random
import math

def get_FDS_data(series, tcs, maxmin, df):
    temp_list = []
    for i in tcs:
        string = str(i)
        temp_list.append(series+string)
    tempdf = df[temp_list]  ## creates a data frame of vis values only

    if maxmin == "min":    
        tempdf = tempdf.min(axis=1)   # creates a column of minimum values
        output = tempdf.tolist()   # converts the minimum values to a list    

    else:
        tempdf = tempdf.max(axis=1)   # creates a column of maximum values
        output = tempdf.tolist()   # converts the maximum values to a list
    return output

def get_list_of_headers(df, string):
    list1 = list(df.columns)
    list2 = []
    for i in list1:
        if string in i:
            list2.append(i)
    return list2

def get_detection_time(df, detection_activation_value):
    det = df[get_list_of_headers(df, "Smoke detector")]
    det = det.max(axis=1)   # creates a column of maximum values
    det_list = det.tolist()   # converts the minimum values to a list    
    n = 0
    i = 0
    while i < detection_activation_value:
        i = det_list[n]
        n=n+1
    return n

# TODO: generate different sheets in workbook for appendix i.e. 100 runs, 1k runs etc
# later use excel sheets for charts
def generate_data(
        name, 
        devc, 
        HRR, 
        sn,
        results_dir, 
        Project_Name,
        No_Runs,
        FED_Toxc_Tenability_Limit,
        DensityCM,
        DCO,
        FED_Heat_Tenability_Limit_NS,
        Radiation_Tenability_Limit_S,
        Temp_Tenability_Limit_S,
        workbook,
        TC_From_Bedrooms,
        Pre_dict,
        TD_From_Bedrooms,
        Probability_Occupant_in_Bedroom,
        Probability_Occupant_in_Lounge,
        TD_From_Lounges,
        TC_From_Lounges,
        Probability_Occupant_in_Kitchen,
        TD_From_Kitchens,
        TC_From_Kitchens,
        Probability_Of_3m_Tenability_Limit,
        High_Visibility_Tenability_Limit,
        Low_Visibility_Tenability_Limit,
        detection_activation_value,
        DensityCD,
        FED_RAD_tol,
        VE
        ): 

    fds_data = pd.read_csv(devc, skiprows=[0])  ##  gets FDS device data
    fire_data = pd.read_csv(HRR, skiprows=[0])
    HRR = fire_data['HRR'].tolist()
    HRR_Time = fire_data['Time'].tolist()
    plot_time = fds_data['Time'].tolist()
    
    end = HRR_Time[-1]
    hrr_end = HRR[-1]

    if name == "PD1":
        Simulation_Time = 1800
    else:
        Simulation_Time = 1200

    
    while end < Simulation_Time:
        HRR_Time.append(end+1)
        HRR.append(hrr_end)
        end = end+1
 
    ### a. Visibility Tenability Data list
    
    n=0    # Counter for loop
    vis_ten_list = []    # Blank list for adding values to
    while n < No_Runs * Probability_Of_3m_Tenability_Limit: # adds number of occupants with 3m tenability limit for visibility
        vis_ten_list.append(High_Visibility_Tenability_Limit) 
        n=n+1
    while n < No_Runs: # adds the rest of the occupants as having a 2m tenability limit
        vis_ten_list.append(Low_Visibility_Tenability_Limit)
        n=n+1
    random.shuffle(vis_ten_list) # shuffles list
    
    
    # b. Occupant Travel Distance
    
    n = 0  ## first counter for loop
    x = 1 ## second counter for loop - this one is for naming the room
    TD_List = [] ## to be a list of lists, so room name and travel distance are associated when drawn randomly
    
    No_Per_Kitchen = Probability_Occupant_in_Kitchen / len(TD_From_Kitchens) * No_Runs  ## calculates the probability of an occupant being in a kitchen based on the number of kitchens
    for i in TD_From_Kitchens:  ## for each kitchen
        while n < No_Per_Kitchen:   ## adds a list to the list with the name of the room and the maximum TD from that room
            TD_List.append([f"Kitchen {x}",i])
            n = n+1
        n = 0
        x = x+1   ## counter to account for multiple rooms
    
    x = 1
    No_Per_Lounge = Probability_Occupant_in_Lounge / len(TD_From_Lounges) * No_Runs ## same as above for living spaces
    for i in TD_From_Lounges:
        while n < No_Per_Lounge:
            TD_List.append([f"Living Space {x}",i])
            n = n+1
        n = 0
        x = x+1
        
    x = 1
    No_Per_Bedroom = Probability_Occupant_in_Bedroom / len(TD_From_Bedrooms) * No_Runs ### same as above for bedrooms
    for i in TD_From_Bedrooms:
        while n < No_Per_Bedroom:
            TD_List.append([f"Bedroom {x}",i])
            n = n+1
        n = 0
        x = x+1
        
    random.shuffle(TD_List)
    
    
    # c. Pre-movement time
    
    # need to add a function which returns the premovement time distribution as a dictionary of integers based on the number of runs 
    
    Pre_List = []  ## list to be populated
    Detection_Time = get_detection_time(fds_data, detection_activation_value)
    # TODO: repeat process x times for num_total_runs / 10k
    for count in range(max(1, int(No_Runs / 10000))):
        for a,b in Pre_dict.items():  
            n = 0  ## counter resets after the number of entries corresponding to the dictionary value every key is "added"
            while n < b:
                Pre_List.append(a+Detection_Time) # adds the starting escape time (det + pre) b times with b being the dictionary value
                n=n+1
    random.shuffle(Pre_List)
    
    bedroom_vis = get_FDS_data("VIS", TC_From_Bedrooms, "min", fds_data) ### based on Thermocouples, gets data for each room type
    bedroom_temp = get_FDS_data("TEMP", TC_From_Bedrooms, "max", fds_data)
    bedroom_rad = get_FDS_data("RAD", TC_From_Bedrooms, "max", fds_data)
    bedroom_water = get_FDS_data("WATER", TC_From_Bedrooms, "max", fds_data)
    bedroom_CD = get_FDS_data("CD", TC_From_Bedrooms, "max", fds_data)
    bedroom_CM = get_FDS_data("CM", TC_From_Bedrooms, "max", fds_data)
    bedroom_HCN = get_FDS_data("HCN", TC_From_Bedrooms, "max", fds_data)
    
    kitchen_vis = get_FDS_data("VIS", TC_From_Kitchens, "min", fds_data)
    kitchen_temp = get_FDS_data("TEMP", TC_From_Kitchens, "max", fds_data)
    kitchen_rad = get_FDS_data("RAD", TC_From_Kitchens, "max", fds_data)
    kitchen_water = get_FDS_data("WATER", TC_From_Kitchens, "max", fds_data)
    kitchen_CD = get_FDS_data("CD", TC_From_Kitchens, "max", fds_data)
    kitchen_CM = get_FDS_data("CM", TC_From_Kitchens, "max", fds_data)
    kitchen_HCN = get_FDS_data("HCN", TC_From_Kitchens, "max", fds_data)
    
    lounge_vis = get_FDS_data("VIS", TC_From_Lounges, "min", fds_data)
    lounge_temp = get_FDS_data("TEMP", TC_From_Lounges, "max", fds_data)
    lounge_rad = get_FDS_data("RAD", TC_From_Lounges, "max", fds_data)
    lounge_water = get_FDS_data("WATER", TC_From_Lounges, "max", fds_data)
    lounge_CD = get_FDS_data("CD", TC_From_Lounges, "max", fds_data)
    lounge_CM = get_FDS_data("CM", TC_From_Lounges, "max", fds_data)
    lounge_HCN = get_FDS_data("HCN", TC_From_Lounges, "max", fds_data)
    
    
 
    
    
    
    ## 4. Crunch Results
    
    # a. create worksheet
    
    
    worksheet = workbook[name]
     
    n = 0
    number_harmed = 0
    number_trapped = 0
    escape_times = []
    pre_times = []
    max_heat_FED = []
    max_toxc_FED = []
    room_list = []
    
    while n < No_Runs:   ## main loop for model
        worksheet[f"A{n+2}"]=n+1  ## writes run number
        # perhaps restart pre_list if n>len(pre_list)??
        pre = Pre_List.pop()  ## picks a random starting escape time time
        worksheet[f"B{n+2}"]=pre  ## writes pre movement time plus detection time
        VisTen = vis_ten_list.pop()  ## picks a random visibility tenability limit
        worksheet[f"E{n+2}"]=VisTen  ## writes the random visibility tenability limit
        loc_dat = TD_List.pop()  ## picks a random starting location and TD
        location = loc_dat[0]   ## writes to spreadsheet
        
        if "Bedroom" in location:   ### sets lists for the calc below based on data retrieved
            vis_list = bedroom_vis
            Temp_list = bedroom_temp
            RAD_list = bedroom_rad
            CM_List = bedroom_CM
            CD_List = bedroom_CD
            HCN_List = bedroom_HCN
            Water_list = bedroom_water
        elif "Living Space" in location:
            vis_list = lounge_vis
            Temp_list = lounge_temp
            RAD_list = lounge_rad
            CM_List = lounge_CM
            CD_List = lounge_CD
            HCN_List = lounge_HCN
            Water_list = lounge_water        
        elif "Kitchen" in location:
            vis_list = kitchen_vis
            Temp_list = kitchen_temp
            RAD_list = kitchen_rad
            CM_List = kitchen_CM
            CD_List = kitchen_CD
            HCN_List = kitchen_HCN
            Water_list = kitchen_water          
        else:
            print("error error error")
            break
              
        
        
        worksheet[f"C{n+2}"]=location  
        TD = float(loc_dat[1])   ## same for TD
        worksheet[f"D{n+2}"]=TD
        time = pre    ## sets run start time to the start of escape
        min_vis = 30    ## starting values for max / min exposure
        max_temp = 20
        FED_toxc = 0.0
        max_rad = 0
        FED_heat = 0.0
        distance = TD
        Harmed = "no"
        Escaped = "no"
        water_temp_measurement = "no"
        while time<Simulation_Time and Escaped == "no" and Harmed == "no": 
            try:    ##tries to get vis value for timestep, if not just uses last value - this is incase a model hasnt fully run.
                vis = vis_list[time-1]
            except IndexError:
                vis = vis_list[-1]

            if vis >= 5:  ## checks visibility and moves occupant accordingly.
                distance = distance - 1.2
            elif vis >= VisTen:
                distance = distance - 0.3
                
            if vis < min_vis:  ## updates minimum visibility reading if required.
                min_vis = vis
        
                
            if name == "PD1": # if PD1, works out correct temperature tenability limit based on moisture in air 
                try:    ##tries to get water value for timestep, if not just uses last value - this is incase a model hasnt fully run.
                    Water = Water_list[time-1]
                except IndexError:
                    Water = Water_list[-1] 
                if Water >= 0.1:
                    water_temp_measurement = "yes"

            if water_temp_measurement == "yes":
                try:    ##tries to get temp value for timestep, if not just uses last value - this is incase a model hasnt fully run.
                    temp = Temp_list[time-1]
                except IndexError:
                    temp = Temp_list[-1]
    
                if temp >= Temp_Tenability_Limit_S:
                    Harmed = "yes"
                if temp > max_temp:
                    max_temp = temp 
    
                try:    ##tries to get rad value for timestep, if not just uses last value - this is incase a model hasnt fully run.
                    RAD = RAD_list[time-1]
                except IndexError:
                    RAD = RAD_list[-1]
    
                if RAD >= Radiation_Tenability_Limit_S:
                    Harmed = "yes"
                if RAD > max_rad:
                    max_rad = RAD                

            else:
                try:    ##tries to get temp value for timestep, if not just uses last value - this is incase a model hasnt fully run.
                    temp = Temp_list[time-1]
                except IndexError:
                    temp = Temp_list[-1]               
                try:    ##tries to get rad value for timestep, if not just uses last value - this is incase a model hasnt fully run.
                    RAD = RAD_list[time-1]
                except IndexError:
                    RAD = RAD_list[-1]
                if temp > max_temp:
                    max_temp = temp 
                if RAD > max_rad:
                    max_rad = RAD  
                tol_temp = 2 * 10**31*temp**-16.963+4+10**8*temp**-3.7561    ### as per PD7974:6
                temp_FED = 1/tol_temp/60
                
                tol_RAD = FED_RAD_tol/RAD**1.33
                if type(tol_RAD) == complex:
                    tol_RAD = float(abs(tol_RAD))
                RAD_FED = 1/tol_RAD/60
                
                FED_heat = FED_heat + temp_FED + RAD_FED
                if float(FED_heat) >= FED_Heat_Tenability_Limit_NS:
                    Harmed = "yes"
                    
            try:    ##tries to get CM value for timestep, if not just uses last value - this is incase a model hasnt fully run.
                CM = CM_List[time-1]
            except IndexError:
                CM = CM_List[-1]    
            FICO = 3.317*10**-5*(CM/DensityCM*1000000)**1.036/DCO
            
            try:    ##tries to get CM value for timestep, if not just uses last value - this is incase a model hasnt fully run.
                CD = CD_List[time-1]
            except IndexError:
                CD = CD_List[-1]             
            VCO2 = math.exp(CD/DensityCD*100/5)
            
            FIN = FICO*VE*VCO2*1/60
            FED_toxc = FED_toxc +FIN
            
            if FED_toxc >= FED_Toxc_Tenability_Limit:
                Harmed = "yes"
                                      
                
            if distance <= 0:
                Escaped = "yes"
                
            time = time+1
            
        if Harmed == "yes":
            number_harmed = number_harmed + 1
            worksheet[f"I{n+2}"]="yes"
        else:
            worksheet[f"I{n+2}"]="no"        
        if Escaped == "no":
            number_trapped = number_trapped + 1
            worksheet[f"H{n+2}"]="yes"

            worksheet[f"F{n+2}"]="N/A"
            worksheet[f"G{n+2}"]="N/A"
        else:
            worksheet[f"H{n+2}"]="no"   
            worksheet[f"F{n+2}"]=time-1
            worksheet[f"G{n+2}"]=time-1-pre
            escape_times.append(time-1)
        pre_times.append(pre)
        max_heat_FED.append(FED_heat)
        max_toxc_FED.append(FED_toxc)
        room_list.append(location)
        worksheet[f"J{n+2}"]=min_vis
        worksheet[f"K{n+2}"]=max_temp
        worksheet[f"M{n+2}"]=FED_toxc
        worksheet[f"L{n+2}"]=max_rad
        worksheet[f"N{n+2}"]=FED_heat        
            
        
        
        n = n + 1
    
    vis_list2 = get_FDS_data("VIS", ["1","2","3","4","5","6","7","8","9","10"], "min", fds_data) ### based on Thermocouples, gets data for each room type
    Temp_list = get_FDS_data("TEMP", ["1","2","3","4","5","6","7","8","9","10"], "max", fds_data)
    RAD_list= get_FDS_data("RAD", ["1","2","3","4","5","6","7","8","9","10"], "max", fds_data)
    Water_list = get_FDS_data("WATER", ["1","2","3","4","5","6","7","8","9","10"], "max", fds_data)
    CD_list = get_FDS_data("CD", ["1","2","3","4","5","6","7","8","9","10"], "max", fds_data)
    CM_list = get_FDS_data("CM", ["1","2","3","4","5","6","7","8","9","10"], "max", fds_data)



    
    n = 0
    while n <= Simulation_Time:
        worksheet[f"P{n+2}"]=n
        worksheet[f"Q{n+2}"]=f"""=(COUNTIF(F$2:F${No_Runs+1}, "<="&P{n+2}))/{No_Runs}*100"""
        worksheet[f"R{n+2}"]=f"""=(COUNTIF(G$2:G${No_Runs+1}, "<="&P{n+2}))/{No_Runs}*100"""
 
        try:    
            worksheet[f"S{n+2}"]=vis_list2[-1]
        except IndexError:
            worksheet[f"S{n+2}"]=vis_list2[-1]      
 
        try:    
            worksheet[f"T{n+2}"]=Temp_list[n]
        except IndexError:
            worksheet[f"T{n+2}"]=Temp_list[-1]      
 
        try:    
            worksheet[f"U{n+2}"]=RAD_list[n]
        except IndexError:
            worksheet[f"U{n+2}"]=RAD_list[-1]

        try:    
            worksheet[f"V{n+2}"]=CD_list[n]
        except IndexError:
            worksheet[f"V{n+2}"]=CD_list[-1] 

        try:    
            worksheet[f"W{n+2}"]=CM_list[n]
        except IndexError:
            worksheet[f"W{n+2}"]=CM_list[-1]     
 
       
        try:    
            worksheet[f"X{n+2}"]=Water_list[n]
            wl = Water_list[n]
        except IndexError:
            worksheet[f"X{n+2}"]=Water_list[-1]
            wl = Water_list[-1]
        else:
            wl = 0
    

        n=n+1
   

    if number_trapped == 0:
        worksheet["AD1"]=0  
    else:
        worksheet["AD1"]=number_trapped/No_Runs      
  
    if number_harmed == 0:
        worksheet["AD2"]=0  
    else:
        worksheet["AD2"]=number_harmed/No_Runs 
        
    if No_Runs-number_trapped == 0:
        worksheet["AD3"]=0
    else:
        worksheet["AD3"]=(No_Runs-number_trapped)/No_Runs 

    worksheet["AD4"]=Detection_Time     
    
    n = 0
    

    while n < len(HRR):
        worksheet[f"AF{n+2}"]=HRR_Time[n]       
        worksheet[f"AG{n+2}"]=HRR[n]     
        n=n+1
    

    prog_HRR = []
    prog_time = []
    t = 0    
    if name == "PD1":
        ylim = 300
        if "Kitchen" in sn:
            fgr = 0.0469
            peak_time = 73
        else:
            fgr = 0.0117
            peak_time = 147
        peak_HRR = 250
        while t <= peak_time:
            prog_HRR.append(min(t**2*fgr, peak_HRR))
            prog_time.append(t)
            t = t+1
        while t <= Simulation_Time:
            prog_HRR.append(max(peak_HRR + (t - peak_time)*(0-peak_HRR)/120, 0))
            prog_time.append(t)
            t = t+1
    else:
        ylim = 2000    
        peak_HRR = 1500
        if "Kitchen" in sn:
            fgr = 0.0469
        else:
            fgr = 0.0117
        while t <= Simulation_Time:
            prog_HRR.append(min(t**2*fgr, peak_HRR))
            prog_time.append(t)
            t = t+1    

    # run_charts(
    #     name,
    #     No_Runs, 
    #     HRR_Time, 
    #     HRR, 
    #     prog_time, 
    #     prog_HRR, 
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
    #     )    
  


    print(f"{sn} - {name}: done")

if __name__ == '__main__':
    import openpyxl

    Pre_dict = {14: 1, 15: 2, 16: 3, 17: 4, 18: 5, 19: 6, 20: 7, 21: 8, 22: 9, 23: 10, 24: 11, 25: 12, 26: 13, 27: 14, 28: 15, 29: 16, 30: 18, 31: 19, 32: 20, 33: 21, 34: 22, 35: 23, 36: 24, 37: 25, 38: 26, 39: 27, 40: 28, 41: 29, 42: 30, 43: 31, 44: 32, 45: 33, 46: 34, 47: 34, 48: 35, 49: 36, 50: 36, 51: 37, 52: 38, 53: 38, 54: 39, 55: 40, 56: 41, 57: 41, 58: 42, 59: 42, 60: 42, 61: 42, 62: 42, 63: 42, 64: 42, 65: 42, 66: 42, 67: 42, 68: 42, 69: 42, 70: 42, 71: 42, 72: 42, 73: 42, 74: 42, 75: 42, 76: 42, 77: 42, 78: 42, 79: 42, 80: 42, 81: 42, 82: 42, 83: 42, 84: 42, 85: 42, 86: 42, 87: 42, 88: 41, 89: 41, 90: 41, 91: 41, 92: 41, 93: 40, 94: 40, 95: 40, 96: 40, 97: 39, 98: 39, 99: 39, 100: 39, 101: 39, 102: 38, 103: 38, 104: 38, 105: 38, 106: 38, 107: 37, 108: 37, 109: 37, 110: 37, 111: 37, 112: 36, 113: 36, 114: 36, 115: 36, 116: 36, 117: 35, 118: 35, 119: 35, 120: 35, 121: 35, 122: 34, 123: 34, 124: 34, 125: 34, 126: 34, 127: 33, 128: 33, 129: 33, 130: 33, 131: 33, 132: 32, 133: 32, 134: 32, 135: 32, 136: 32, 137: 31, 138: 31, 139: 31, 140: 31, 141: 31, 142: 30, 143: 30, 144: 30, 145: 30, 146: 29, 147: 29, 148: 29, 149: 29, 150: 29, 151: 28, 152: 28, 153: 28, 154: 28, 155: 28, 156: 27, 157: 27, 158: 27, 159: 27, 160: 27, 161: 26, 162: 26, 163: 26, 164: 26, 165: 26, 166: 25, 167: 25, 168: 25, 169: 25, 170: 25, 171: 24, 172: 24, 173: 24, 174: 24, 175: 24, 176: 23, 177: 23, 178: 23, 179: 23, 180: 23, 181: 22, 182: 22, 183: 22, 184: 22, 185: 22, 186: 21, 187: 21, 188: 21, 189: 21, 190: 21, 191: 20, 192: 20, 193: 20, 194: 20, 195: 19, 196: 19, 197: 19, 198: 19, 199: 19, 200: 18, 201: 18, 202: 18, 203: 18, 204: 18, 205: 17, 206: 17, 207: 17, 208: 17, 209: 17, 210: 16, 211: 16, 212: 16, 213: 16, 214: 16, 215: 15, 216: 15, 217: 15, 218: 15, 219: 15, 220: 14, 221: 14, 222: 14, 223: 14, 224: 14, 225: 14, 226: 14, 227: 14, 228: 14, 229: 14, 230: 14, 231: 14, 232: 14, 233: 14, 234: 14, 235: 14, 236: 14, 237: 14, 238: 14, 239: 14, 240: 13, 241: 13, 242: 13, 243: 13, 244: 13, 245: 13, 246: 13, 247: 13, 248: 13, 249: 13, 250: 13, 251: 13, 252: 13, 253: 13, 254: 13, 255: 13, 256: 13, 257: 13, 258: 13, 259: 13, 260: 13, 261: 13, 262: 13, 263: 13, 264: 13, 265: 13, 266: 13, 267: 13, 268: 13, 269: 13, 270: 13, 271: 13, 272: 13, 273: 13, 274: 13, 275: 12, 276: 12, 277: 12, 278: 12, 279: 12, 280: 12, 281: 12, 282: 12, 283: 12, 284: 12, 285: 12, 286: 12, 287: 12, 288: 12, 289: 12, 290: 12, 291: 12, 292: 12, 293: 12, 294: 12, 295: 12, 296: 12, 297: 12, 298: 12, 299: 12, 300: 12, 301: 12, 302: 12, 303: 12, 304: 12, 305: 12, 306: 12, 307: 12, 308: 12, 309: 12, 310: 12, 311: 11, 312: 11, 313: 11, 314: 11, 315: 11, 316: 11, 317: 11, 318: 11, 319: 11, 320: 11, 321: 11, 322: 11, 323: 11, 324: 11, 325: 11, 326: 11, 327: 11, 328: 11, 329: 11, 330: 11, 331: 11, 332: 11, 333: 11, 334: 11, 335: 11, 336: 11, 337: 11, 338: 11, 339: 11, 340: 11, 341: 11, 342: 11, 343: 11, 344: 11, 345: 11, 346: 10, 347: 10, 348: 10, 349: 10, 350: 10, 351: 10, 352: 10, 353: 10, 354: 10, 355: 10, 356: 10, 357: 10, 358: 10, 359: 10, 360: 10, 361: 10, 362: 10, 363: 10, 364: 10, 365: 10, 366: 10, 367: 10, 368: 10, 369: 10, 370: 10, 371: 10, 372: 10, 373: 10, 374: 10, 375: 10, 376: 10, 377: 10, 378: 10, 379: 10, 380: 10, 381: 10, 382: 9, 383: 9, 384: 9, 385: 9, 386: 9, 387: 9, 388: 9, 389: 9, 390: 9, 391: 9, 392: 9, 393: 9, 394: 9, 395: 9, 396: 9, 397: 9, 398: 9, 399: 9, 400: 9, 401: 9, 402: 9, 403: 9, 404: 9, 405: 9, 406: 9, 407: 9, 408: 9, 409: 9, 410: 9, 411: 9, 412: 9, 413: 9, 414: 9, 415: 9, 416: 9, 417: 9, 418: 8, 419: 8, 420: 8, 421: 8, 422: 8, 423: 8, 424: 8, 425: 8, 426: 8, 427: 8, 428: 8, 429: 8, 430: 8, 431: 8, 432: 8, 433: 8, 434: 8, 435: 8, 436: 8, 437: 8, 438: 8, 439: 8, 440: 8, 441: 8, 442: 8, 443: 8, 444: 8, 445: 8, 446: 8, 447: 8, 448: 8, 449: 8, 450: 8, 451: 8, 452: 8, 453: 7, 454: 7, 455: 7, 456: 7, 457: 7, 458: 7, 459: 7, 460: 7, 461: 7, 462: 7, 463: 7, 464: 7, 465: 7, 466: 7, 467: 7, 468: 7, 469: 7, 470: 7, 471: 7, 472: 7, 473: 7, 474: 7, 475: 7, 476: 7, 477: 7, 478: 7, 479: 7, 480: 7, 481: 7, 482: 7, 483: 7, 484: 7, 485: 7, 486: 7, 487: 7, 488: 7, 489: 6, 490: 6, 491: 6, 492: 6, 493: 6, 494: 6, 495: 6, 496: 6, 497: 6, 498: 6, 499: 6, 500: 6, 501: 6, 502: 6, 503: 6, 504: 6, 505: 6, 506: 6, 507: 6, 508: 6, 509: 6, 510: 6, 511: 6, 512: 6, 513: 6, 514: 6, 515: 6, 516: 6, 517: 6, 518: 6, 519: 6, 520: 6, 521: 6, 522: 6, 523: 6, 524: 6, 525: 5, 526: 5, 527: 5, 528: 5, 529: 5, 530: 5, 531: 5, 532: 5, 533: 5, 534: 5, 535: 5, 536: 5, 537: 5, 538: 5, 539: 5, 540: 5, 541: 5, 542: 5, 543: 5, 544: 5, 545: 5, 546: 5, 547: 5, 548: 5, 549: 5, 550: 5, 551: 5, 552: 5, 553: 5, 554: 5, 555: 5, 556: 5, 557: 5, 558: 5, 559: 5, 560: 4, 561: 4, 562: 4, 563: 4, 564: 4, 565: 4, 566: 4, 567: 4, 568: 4, 569: 4, 570: 4, 571: 4, 572: 4, 573: 4, 574: 4, 575: 4, 576: 4, 577: 4, 578: 4, 579: 4, 580: 4, 581: 4, 582: 4, 583: 4, 584: 4, 585: 4, 586: 4, 587: 4, 588: 4, 589: 4, 590: 4, 591: 4, 592: 4, 593: 4, 594: 4, 595: 4, 596: 4, 597: 4, 598: 4, 599: 4, 600: 4, 601: 4, 602: 4, 603: 4, 604: 4, 605: 4, 606: 4, 607: 4, 608: 4, 609: 4, 610: 4, 611: 4, 612: 4, 613: 4, 614: 4, 615: 4, 616: 4, 617: 4, 618: 4, 619: 4, 620: 4, 621: 4, 622: 4, 623: 4, 624: 4, 625: 4, 626: 4, 627: 4, 628: 4, 629: 4, 630: 4, 631: 4, 632: 4, 633: 4, 634: 4, 635: 4, 636: 4, 637: 4, 638: 4, 639: 4, 640: 4, 641: 4, 642: 4, 643: 4, 644: 4, 645: 4, 646: 4, 647: 4, 648: 4, 649: 4, 650: 4, 651: 4, 652: 4, 653: 4, 654: 4, 655: 4, 656: 4, 657: 4, 658: 4, 659: 4, 660: 4, 661: 4, 662: 4, 663: 4, 664: 3, 665: 3, 666: 3, 667: 3, 668: 3, 669: 3, 670: 3, 671: 3, 672: 3, 673: 3, 674: 3, 675: 3, 676: 3, 677: 3, 678: 3, 679: 3, 680: 3, 681: 3, 682: 3, 683: 3, 684: 3, 685: 3, 686: 3, 687: 3, 688: 3, 689: 3, 690: 3, 691: 3, 692: 3, 693: 3, 694: 3, 695: 3, 696: 3, 697: 3, 698: 3, 699: 3, 700: 3, 701: 3, 702: 3, 703: 3, 704: 3, 705: 3, 706: 3, 707: 3, 708: 3, 709: 3, 710: 3, 711: 3, 712: 3, 713: 3, 714: 3, 715: 3, 716: 3, 717: 3, 718: 3, 719: 3, 720: 3, 721: 3, 722: 3, 723: 3, 724: 3, 725: 3, 726: 3, 727: 3, 728: 3, 729: 3, 730: 3, 731: 3, 732: 3, 733: 3, 734: 3, 735: 3, 736: 3, 737: 3, 738: 3, 739: 3, 740: 3, 741: 3, 742: 3, 743: 3, 744: 3, 745: 3, 746: 3, 747: 3, 748: 3, 749: 3, 750: 3, 751: 3, 752: 3, 753: 3, 754: 3, 755: 3, 756: 3, 757: 3, 758: 3, 759: 3, 760: 3, 761: 3, 762: 3, 763: 3, 764: 3, 765: 3, 766: 3, 767: 3, 768: 3, 769: 3, 770: 3, 771: 3, 772: 3, 773: 3, 774: 3, 775: 2, 776: 2, 777: 2, 778: 2, 779: 2, 780: 2, 781: 2, 782: 2, 783: 2, 784: 2, 785: 2, 786: 2, 787: 2, 788: 2, 789: 2, 790: 2, 791: 2, 792: 2, 793: 2, 794: 2, 795: 2, 796: 2, 797: 2, 798: 2, 799: 2, 800: 2, 801: 2, 802: 2, 803: 2, 804: 2, 805: 2, 806: 2, 807: 2, 808: 2, 809: 2, 810: 2, 811: 2, 812: 2, 813: 2, 814: 2, 815: 2, 816: 2, 817: 2, 818: 2, 819: 2, 820: 2, 821: 2, 822: 2, 823: 2, 824: 2, 825: 1, 826: 1, 827: 1, 828: 1, 829: 1, 830: 1, 831: 1, 832: 1, 833: 1, 834: 1, 835: 1, 836: 1, 837: 1, 838: 1, 839: 1, 840: 1, 841: 1, 842: 1, 843: 1, 844: 1, 845: 1, 846: 1, 847: 1, 848: 1, 849: 1, 850: 1, 851: 1, 852: 1, 853: 1, 854: 1, 855: 1, 856: 1, 857: 1, 858: 1, 859: 1, 860: 1, 861: 1, 862: 1, 863: 1, 864: 1, 865: 1, 866: 1, 867: 1, 868: 1, 869: 1, 870: 1, 871: 1, 872: 1, 873: 1}
    generate_data(
        name='CC1', 
        devc=r'C:\\Users\\IanShaw\\localProgramming\\fd\\open plan\\Appendix Output/NHBC 8x10/Lounge_Fire_1/CC1/CC1_devc.csv', 
        HRR=r'C:\\Users\\IanShaw\\localProgramming\\fd\\open plan\\Appendix Output/NHBC 8x10/Lounge_Fire_1/CC1/CC1_hrr.csv',
        sn='Lounge_Fire_1',
        results_dir=r'C:\\Users\\IanShaw\\localProgramming\\fd\\open plan\\Appendix Output/NHBC 8x10/Lounge_Fire_1', 
        Project_Name='NHBC 8x10',
        No_Runs=100000,
        FED_Toxc_Tenability_Limit=1.0,
        DensityCM=1.14,
        DCO=30,
        FED_Heat_Tenability_Limit_NS=1.0,
        Radiation_Tenability_Limit_S=2.5,
        Temp_Tenability_Limit_S=60,
        workbook=openpyxl.load_workbook(r"C:\\Users\\IanShaw\\localProgramming\\fd\\open plan\\Appendix Output/NHBC 8x10/Lounge_Fire_1/Lounge_Fire_1_100000_Results.xlsx") ,
        # workbook="<openpyxl.workbook.workbook.Workbook object at 0x00000207433A6E90>",
        TC_From_Bedrooms=['1', '2', '3', '4', '5', '6', '7', '8', '9'],
        Pre_dict=Pre_dict,
        TD_From_Bedrooms=['3', '4.7'],
        Probability_Occupant_in_Bedroom=0.51,
        Probability_Occupant_in_Lounge=0.46,
        TD_From_Lounges=['3.8'],
        TC_From_Lounges=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        Probability_Occupant_in_Kitchen=0.03,
        TD_From_Kitchens=['1.4'],
        TC_From_Kitchens=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        Probability_Of_3m_Tenability_Limit=0.3,
        High_Visibility_Tenability_Limit=3,
        Low_Visibility_Tenability_Limit=2,
        detection_activation_value=2,
        DensityCD=1.87,
        FED_RAD_tol=1.33,
        VE=25
        )