import tkinter as tk
from PIL import ImageTk

from b_Create_FDS_Files_2 import run_stage_two
from constants import growthRateObject



class Tab2Content:
    def __init__(self, master, open_img):
      self.master = master
      self.label_width = 40
      self.entrybox_width = 50
      self.has_custom_hrr_peak = tk.StringVar()
      self.has_custom_sprinkler_distance = tk.StringVar()
      self.interface(open_img)

    def interface(self, open_img):
        current_row = 0
        # step 2 -> page 1 Basemodel
        ''' Section 1 - folder path '''
        self.label_folder_path = tk.Label(self.master, text="CFD Folder Location: ", width=self.label_width, anchor="e")
        self.label_folder_path.grid(row=current_row, column=0)
        self.entry_folder_path = tk.Entry(self.master, width=75)
        self.entry_folder_path.grid(row=current_row, column=1)       

        ''' Section 2 - Advanced Options '''
        current_row += 1
        self.options_frame = tk.LabelFrame(self.master, text="Advanced Options - Feel Free to Leave as default")
        self.options_frame.grid(row=current_row, column=0, columnspan=2)        



        current_row += 1
        self.label_non_sprinkler_hrr_peak = tk.Label(self.options_frame, text="Non Sprinklered Peak Heat Release Rate (kW): ", width=self.label_width, anchor="e")
        self.label_non_sprinkler_hrr_peak.grid(row=current_row, column=0)
        self.entry_non_sprinkler_hrr_peak = tk.Entry(self.options_frame, width=self.entrybox_width)
        self.entry_non_sprinkler_hrr_peak.grid(row=current_row, column=1)
        self.entry_non_sprinkler_hrr_peak.insert(0, str(1500))        

        current_row += 1
        self.label_has_custom_hrr_peak = tk.Label(self.options_frame, text="Sprinklered Peak Heat Release Rate: ", width=self.label_width, anchor="e")
        self.label_has_custom_hrr_peak.grid(row=current_row, column=0)
        # self.entry_custom_hrr_peak = tk.Entry(self.options_frame, width=self.entrybox_width)
        self.has_custom_hrr_peak.set("False")
        self.custom_hrr_peak_selector1 = tk.Radiobutton(self.options_frame, text="Calculate",
                                                variable=self.has_custom_hrr_peak, value="False", font=("Poppins Light", 8))
        self.custom_hrr_peak_selector1.grid(row=current_row, column=1)
        self.custom_hrr_peak_selector2 = tk.Radiobutton(self.options_frame, text="Input Custom Value",
                                                variable=self.has_custom_hrr_peak, value="True", font=("Poppins Light", 8))
        self.custom_hrr_peak_selector2.grid(row=current_row, column=2)
        # only allow entry if has_custom == True
        current_row += 1
        self.label_custom_hrr_peak = tk.Label(self.options_frame, text="If Custom, input here: ", width=self.label_width, anchor="e")
        self.label_custom_hrr_peak.grid(row=current_row, column=0)
        self.entry_custom_hrr_peak = tk.Entry(self.options_frame, width=self.entrybox_width)
        self.entry_custom_hrr_peak.grid(row=current_row, column=1) 
        # sprinkler head distance
        current_row += 1
        self.label_sprinkler_distance = tk.Label(self.options_frame, text="If calculated, distance to sprinkler head: ", width=self.label_width, anchor="e")
        self.label_sprinkler_distance.grid(row=current_row, column=0)
        # self.entry_custom_hrr_peak = tk.Entry(self.options_frame, width=self.entrybox_width)
        self.has_custom_sprinkler_distance.set("False")
        self.custom_sprinkler_distance_selector1 = tk.Radiobutton(self.options_frame, text="Calculate",
                                                variable=self.has_custom_sprinkler_distance, value="False", font=("Poppins Light", 8))
        self.custom_sprinkler_distance_selector1.grid(row=current_row, column=1)
        self.custom_sprinkler_distance_selector2 = tk.Radiobutton(self.options_frame, text="Input Custom Value",
                                                variable=self.has_custom_sprinkler_distance, value="True", font=("Poppins Light", 8))
        self.custom_sprinkler_distance_selector2.grid(row=current_row, column=2)
        # only allow entry if has_custom == True
        current_row += 1
        self.label_custom_sprinkler_distance = tk.Label(self.options_frame, text="If Custom, input here: ", width=self.label_width, anchor="e")
        self.label_custom_sprinkler_distance.grid(row=current_row, column=0)
        self.entry_custom_sprinkler_distance = tk.Entry(self.options_frame, width=self.entrybox_width)
        self.entry_custom_sprinkler_distance.grid(row=current_row, column=1)           

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
        peak_fs_non_sprinkler = float(self.entry_non_sprinkler_hrr_peak.get())
        growthRate = growthRateObject["fast"] # TODO: have dropdown

        if self.has_custom_hrr_peak.get() == "True":
          custom_fs_sprinkler = float(self.entry_custom_hrr_peak.get())
        else:
           custom_fs_sprinkler = None

        
        if self.has_custom_sprinkler_distance.get() == "True":
          custom_sprinkler_distance = float(self.entry_custom_sprinkler_distance.get())
        else:
          custom_sprinkler_distance = None
           

        run_stage_two(
                      root_dir=folder_path, 
                      growthRate=growthRate, # unclear if this would just be fast for kitchen? or be customisable?
                      peak_fs_non_sprinkler=peak_fs_non_sprinkler,
                      custom_fs_sprinkler=custom_fs_sprinkler,
                      custom_sprinkler_distance=custom_sprinkler_distance
                      )
