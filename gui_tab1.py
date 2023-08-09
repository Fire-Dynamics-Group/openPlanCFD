import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk
import re

from suppression_db import suppression_object
from a_fds_basemodel_1 import create_fds_base_model
from suppression_db import suppression_object
BS_9251_Category_1 = [2, "&PROP ID='BS 9251',","      QUANTITY='SPRINKLER LINK TEMPERATURE',", "      PART_ID='Water',", "      FLOW_RATE=49.05,", "      PARTICLE_VELOCITY=5.0,", "      SPRAY_ANGLE=60.0,75.0/", "BS 9251"]
Smartscan = [2, "&PROP ID='Automist Smartscan',","      QUANTITY='SPRINKLER LINK TEMPERATURE',", "      PART_ID='Water',", "      FLOW_RATE=6.0,", "      PARTICLE_VELOCITY=15.0,", "      SPRAY_ANGLE=0.0,25.0/", "Automist Smartscan"]

class Tab1Content:
    def __init__(self, master, open_img):
      self.master = master
      self.label_width = 40
      self.entrybox_width = 50
      self.has_multiple_rooms = tk.StringVar()
      self.interface(open_img)

    ''' TODO: move validation to helper function script '''
    def int_validate(self, string):
        regex = re.compile(r"[0-9]*$") # regex for any string ending in an integer - does not work for floats!
        result = regex.match(string) # match checks last character entered
        return (string == ""
                or (string.count('+') <= 1
                    and string.count('-') <= 1
                    and result is not None
                    and result.group(0) != ""))

    def keybind_int_only(self, P):
        print(P)
        return self.int_validate(P)
    
    # def float_validate(self, string):
    #     regex = re.compile(r"[0-9]*\.?[0-9]*$") # regex allows positive floats
    #     result = regex.fullmatch(string)  # using fullmatch to ensure the entire string matches
    #     return (string == "" 
    #             or (string.count('.') <= 1
    #                 and result is not None))

    # def keybind_float_only(self, P):
    #     return self.float_validate(P)

    ''' TODO: list of floats should be same length as number of rooms '''
    def float_list_validate(self, string):
        regex = re.compile(r"([0-9]*\.?[0-9]*,)*[0-9]*\.?[0-9]*$") # regex allows comma separated positive floats
        result = regex.fullmatch(string) # using fullmatch to ensure the entire string matches
        return (string == "" 
                or (all(s.count('.') <= 1 for s in string.split(',')) 
                    and result is not None))

    def keybind_float_list_only(self, P):
        return self.float_list_validate(P)
    
    def interface(self, open_img):
        current_row = 0
        # step 1 -> page 1 Basemodel
        ''' Section 1 - folder path '''
        self.label_folder_path = tk.Label(self.master, text="CFD Folder Location: ", width=self.label_width, anchor="e")
        self.label_folder_path.grid(row=current_row, column=0)
        self.entry_folder_path = tk.Entry(self.master, width=75)
        self.entry_folder_path.grid(row=current_row, column=1)

        ''' Section 2 - Dwellings '''
        current_row += 1
        self.dwelling_details_frame = tk.LabelFrame(self.master, text="Dwelling Details")
        self.dwelling_details_frame.grid(row=current_row, column=0, columnspan=2)

        current_row += 1
        self.label_project_name = tk.Label(self.dwelling_details_frame, text="Project Name: ", width=self.label_width, anchor="e")
        self.label_project_name.grid(row=current_row, column=0)
        self.entry_project_name = tk.Entry(self.dwelling_details_frame, width=self.entrybox_width)
        self.entry_project_name.grid(row=current_row, column=1)

        # bedrooms
        current_row += 1
        self.label_num_bedrooms = tk.Label(self.dwelling_details_frame, text="Number of Bedrooms: ", width=self.label_width, anchor="e")
        self.label_num_bedrooms.grid(row=current_row, column=0)

        self.entry_num_bedrooms = tk.Entry(self.dwelling_details_frame, width=self.entrybox_width, validate='key')
        self.entry_num_bedrooms.grid(row=current_row, column=1)
        vcmd = (self.entry_num_bedrooms.register(self.keybind_int_only), '%P')
        self.entry_num_bedrooms.config(validatecommand=vcmd)

        current_row += 1
        self.label_td_bedroom = tk.Label(self.dwelling_details_frame, text="Travel Distances from Bedroom Door(s): ", width=self.label_width, anchor="e")
        self.label_td_bedroom.grid(row=current_row, column=0)
        self.entry_td_bedroom = tk.Entry(self.dwelling_details_frame, width=self.entrybox_width, validate='key')
        self.entry_td_bedroom.grid(row=current_row, column=1)
        vcmd = (self.entry_td_bedroom.register(self.keybind_float_list_only), '%P') # , validate='key'
        self.entry_td_bedroom.config(validatecommand=vcmd)

        # Lounges
        current_row += 1
        self.label_num_Lounges = tk.Label(self.dwelling_details_frame, text="Number of Lounges: ", width=self.label_width, anchor="e")
        self.label_num_Lounges.grid(row=current_row, column=0)
        self.entry_num_Lounges = tk.Entry(self.dwelling_details_frame, width=self.entrybox_width, validate='key')
        self.entry_num_Lounges.grid(row=current_row, column=1)
        vcmd = (self.entry_num_Lounges.register(self.keybind_int_only), '%P') # , validate='key'
        self.entry_num_Lounges.config(validatecommand=vcmd)

        current_row += 1
        self.label_td_Lounge = tk.Label(self.dwelling_details_frame, text="Travel Distances from Lounge Door(s): ", width=self.label_width, anchor="e")
        self.label_td_Lounge.grid(row=current_row, column=0)
        self.entry_td_Lounge = tk.Entry(self.dwelling_details_frame, width=self.entrybox_width)
        self.entry_td_Lounge.grid(row=current_row, column=1)
        # vcmd = (self.entry_td_Lounge.register(self.keybind_int_only), '%P') # , validate='key'
        # self.entry_td_Lounge.config(validatecommand=vcmd)

        # Kitchens
        current_row += 1
        self.label_num_Kitchens = tk.Label(self.dwelling_details_frame, text="Number of Kitchens: ", width=self.label_width, anchor="e")
        self.label_num_Kitchens.grid(row=current_row, column=0)
        self.entry_num_Kitchens = tk.Entry(self.dwelling_details_frame, width=self.entrybox_width, validate='key')
        self.entry_num_Kitchens.grid(row=current_row, column=1)
        vcmd = (self.entry_num_Kitchens.register(self.keybind_int_only), '%P') # , validate='key'
        self.entry_num_Kitchens.config(validatecommand=vcmd)

        current_row += 1
        self.label_td_Kitchen = tk.Label(self.dwelling_details_frame, text="Travel Distances from Kitchen Door(s): ", width=self.label_width, anchor="e")
        self.label_td_Kitchen.grid(row=current_row, column=0)
        self.entry_td_Kitchen = tk.Entry(self.dwelling_details_frame, width=self.entrybox_width)
        self.entry_td_Kitchen.grid(row=current_row, column=1)

        # fire floor floor to ceiling height
        current_row += 1
        self.label_ceiling_height = tk.Label(self.dwelling_details_frame, text="Floor to ceiling height on fire floor: ", width=self.label_width, anchor="e")
        self.label_ceiling_height.grid(row=current_row, column=0)
        self.entry_ceiling_height = tk.Entry(self.dwelling_details_frame, width=self.entrybox_width)
        self.entry_ceiling_height.grid(row=current_row, column=1)
        ''' TODO: should be float '''

        ''' Section 3 - Fires '''
        current_row += 1
        self.fire_details_frame = tk.LabelFrame(self.master, text="Fires to be Modelled")
        self.fire_details_frame.grid(row=current_row, column=0, columnspan=2)

        current_row += 1
        self.label_num_fires_kitchen = tk.Label(self.fire_details_frame, text="Number of Fires in Kitchen: ", width=self.label_width, anchor="e")
        self.label_num_fires_kitchen.grid(row=current_row, column=0)
        self.entry_num_fires_kitchen = tk.Entry(self.fire_details_frame, width=self.entrybox_width)
        self.entry_num_fires_kitchen.grid(row=current_row, column=1)

        current_row += 1
        self.label_num_fires_lounge = tk.Label(self.fire_details_frame, text="Number of Fires in Lounge: ", width=self.label_width, anchor="e")
        self.label_num_fires_lounge.grid(row=current_row, column=0)
        self.entry_num_fires_lounge = tk.Entry(self.fire_details_frame, width=self.entrybox_width)
        self.entry_num_fires_lounge.grid(row=current_row, column=1)

        current_row += 1

        self.label_multiple_rooms = tk.Label(self.fire_details_frame, text="If more than one fire, are they in different rooms? ", width=self.label_width, anchor="e")
        self.label_multiple_rooms.grid(row=current_row, column=0)
        # self.entry_multiple_rooms = tk.Entry(self.fire_details_frame, width=self.entrybox_width)
        self.has_multiple_rooms.set("False")
        self.multiple_rooms_selector1 = tk.Radiobutton(self.fire_details_frame, text="True",
                                                variable=self.has_multiple_rooms, value="True", font=("Poppins Light", 8))
        self.multiple_rooms_selector1.grid(row=current_row, column=1)
        self.multiple_rooms_selector2 = tk.Radiobutton(self.fire_details_frame, text="False",
                                                variable=self.has_multiple_rooms, value="False", font=("Poppins Light", 8))
        self.multiple_rooms_selector2.grid(row=current_row, column=2)

        ''' Section 3 - FIRE PROTECTION '''
        current_row += 2
        self.fire_protection_details_frame = tk.LabelFrame(self.master, text="Fire Protection Systems")
        self.fire_protection_details_frame.grid(row=current_row, column=0, columnspan=2)

        current_row += 1
        self.label_suppression_system = tk.Label(self.fire_protection_details_frame, text="Suppression System: ", width=self.label_width, anchor="e")
        self.label_suppression_system.grid(row=current_row, column=0)
        self.select_suppression_system = ttk.Combobox(
            self.fire_protection_details_frame, width=self.entrybox_width,
            state="readonly",
            values=list(suppression_object.keys())
        )
        self.select_suppression_system.set(list(suppression_object.keys())[0])
        self.select_suppression_system.grid(row=current_row, column=1)
        '''
        # LATER have facility to add additional
        '''

        # further sprinkler attributes
        # LATER this should affect model!
        current_row += 1
        self.label_rti = tk.Label(self.fire_protection_details_frame, text="Suppression RTI: ", width=self.label_width, anchor="e")
        self.label_rti.grid(row=current_row, column=0)
        # should have a default of 90
        self.entry_rti = tk.Entry(self.fire_protection_details_frame, width=self.entrybox_width)
        self.entry_rti.grid(row=current_row, column=1)
        self.entry_rti.insert(0, str(90))

        current_row += 1
        self.label_tActive = tk.Label(self.fire_protection_details_frame, text="Suppression T Active (°C): ", width=self.label_width, anchor="e")
        self.label_tActive.grid(row=current_row, column=0)
        # should have a default of 90
        self.entry_tActive = tk.Entry(self.fire_protection_details_frame, width=self.entrybox_width)
        self.entry_tActive.grid(row=current_row, column=1)
        self.entry_tActive.insert(0, str(68))

        current_row += 1
        self.label_room_area = tk.Label(self.fire_protection_details_frame, text="Suppression Room Area (m2): ", width=self.label_width, anchor="e")
        self.label_room_area.grid(row=current_row, column=0)
        # should have a default of 90
        self.entry_room_area = tk.Entry(self.fire_protection_details_frame, width=self.entrybox_width)
        self.entry_room_area.grid(row=current_row, column=1)

        current_row += 1
        detection_coverage_options = ["LD1", "LD2", "LD3"]

        # Proposed detection coverage
        self.label_proposed_detection_coverage = tk.Label(self.fire_protection_details_frame, text="Proposed Detection Coverage: ", width=self.label_width, anchor="e")
        self.label_proposed_detection_coverage.grid(row=current_row, column=0)
        self.select_proposed_detection_coverage = ttk.Combobox(
            self.fire_protection_details_frame, width=self.entrybox_width,
            state="readonly",
            values=detection_coverage_options
        )
        self.select_proposed_detection_coverage.set(detection_coverage_options[0])
        self.select_proposed_detection_coverage.grid(row=current_row, column=1)

        # Code Compliant detection coverage
        current_row += 1
        self.label_compliant_detection_coverage = tk.Label(self.fire_protection_details_frame, text="Code Compliant Detection Coverage: ", width=self.label_width, anchor="e")
        self.label_compliant_detection_coverage.grid(row=current_row, column=0)
        self.select_compliant_detection_coverage = ttk.Combobox(
            self.fire_protection_details_frame, width=self.entrybox_width,
            state="readonly",
            values=detection_coverage_options
        )
        self.select_compliant_detection_coverage.set(detection_coverage_options[0])
        self.select_compliant_detection_coverage.grid(row=current_row, column=1)

        current_row += 1
        ##### Output #####

        self.output_frame = tk.LabelFrame(self.master, text="Output")
        self.output_frame.grid(row=current_row, column=1, columnspan=2, sticky="w") # row 4
        self.output_frame.config(font=("Poppins Light", 10))

        # Output Log
        self.output_log = tk.Text(self.output_frame, width=69, height=5)
        self.output_log.grid(row=0, columnspan=6, pady=5, padx=(17,26), sticky="n") # row 0
        self.output_log.insert(tk.INSERT, "Click me to run!")
        self.output_log.configure(font=("Montserrat", 8), state="disabled")

        scrollb = tk.Scrollbar(self.output_frame, command=self.output_log.yview)
        scrollb.grid(row=0, column=0, pady=5, ipady=15, sticky='w') # row 0
        self.output_log['yscrollcommand'] = scrollb.set

        # Triangle
        canvas = tk.Canvas(self.output_frame, width=20, height=25, bd=0, highlightthickness=0)
        canvas.grid(row=0, column=5, pady=(20,0), padx=(0,10), sticky="ne")
        self.triangle = canvas.create_polygon(0, 0, 0, 30, 20, 0, fill="white")


        # current_row += 1
        self.img = ImageTk.PhotoImage(open_img)

        self.label_image = tk.Label(self.master, image=self.img)
        self.label_image.image = self.img
        self.label_image.grid(row=current_row, column=2, rowspan=2)
        self.label_image.bind('<Button-1>', func=self.generate_file)

        # TODO: run basemodel script using user inputs

    # Dummy function to handle the callback
    def generate_file(self, event):
        # TODO: prep for sending to other script
        # then typesafe at top of class
        folder_path = self.entry_folder_path.get()
        # some should be numbers etc
        project_name = self.entry_project_name.get()
        
        def return_float_list(string_list):
          if len(string_list) > 0:
            return [float(f) for f in string_list.split(",")]
          else:
             return []

        Number_Of_Bedrooms = int(self.entry_num_bedrooms.get())
        TD_From_Bedrooms = return_float_list(self.entry_td_bedroom.get())
        print(TD_From_Bedrooms)

        Number_Of_Lounges = int(self.entry_num_Lounges.get())
        TD_From_Lounges = self.entry_td_Lounge.get()


        Number_Of_Kitchens = int(self.entry_num_Kitchens.get())
        TD_From_Kitchens = self.entry_td_Kitchen.get()

        Floor_To_Ceiling = float(self.entry_ceiling_height.get()) # should be float
        print(Floor_To_Ceiling)

        Kitchen_Fires = self.entry_num_fires_kitchen.get()
        if len(Kitchen_Fires) == 0:
            Kitchen_Fires = 0
        else:
          Kitchen_Fires = int(Kitchen_Fires)
        print(Kitchen_Fires)

        Lounge_Fires = self.entry_num_fires_lounge.get()
        if len(Lounge_Fires) == 0:
            Lounge_Fires = 0
        else:
          Lounge_Fires = int(Lounge_Fires)
        print(Lounge_Fires)

        Bedroom_Fires = 0

        '''
            TODO: use multiple rooms
        has_multiple_rooms = self.has_multiple_rooms.get()
        '''
        Suppression_Type = self.select_suppression_system.get()
        if len(Suppression_Type) > 0:
          Suppression_Type = suppression_object[Suppression_Type]

        Proposed_Detection = self.select_proposed_detection_coverage.get()

        CC_Detection = self.select_compliant_detection_coverage.get()

        rti = float(self.entry_rti.get()) # change to float
        sprinklered_room_area = float(self.entry_room_area.get()) # change to float
        tActive = float(self.entry_tActive.get()) # change to float

        print(folder_path)
        # TODO: have stage a save to project folder? - check with sam this is required here
        create_fds_base_model(project_name, 
                          Number_Of_Bedrooms, # number
                          Number_Of_Lounges, # number
                          Number_Of_Kitchens, # number
                          Lounge_Fires, # number
                        #   Lounge_Fires_Own_Door, # boolean
                          Bedroom_Fires, # number
                        #   Bedroom_Fires_Own_Door, # boolean
                          Kitchen_Fires, # number
                        #   Kitchen_Fires_Own_Door, # boolean
                          TD_From_Bedrooms, # list numbers separated by commas
                          TD_From_Kitchens, # list numbers separated by commas
                          TD_From_Lounges, # list numbers separated by commas
                          Suppression_Type, # str
                          Proposed_Detection, # str
                          CC_Detection, #str
                          Floor_To_Ceiling, # float
                          rti, 
                          sprinklered_room_area,
                          tActive,
                          output_path=folder_path
                          )
