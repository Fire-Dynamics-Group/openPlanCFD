import tkinter as tk
from PIL import ImageTk
from c_Behaviour_Model_3 import run_stage_three

'''
TODO: add the following inputs & connect to script
multistorey ticked -> protected stair
if flat exceeds 12 x 16
if residence is multi storey
'''
class Tab3Content:
    def __init__(self, master, open_img):
      self.master = master
      self.label_width = 40
      self.entrybox_width = 50
      self.has_multiple_storeys = tk.StringVar()
      self.has_greater_12x16 = tk.StringVar()
      self.has_kit_greater_8x4 = tk.StringVar()
      self.interface(open_img)

    def interface(self, open_img):
        # CFD folder location only 
        # then run button
        current_row = 0
        # step 3
        ''' Section 1 - folder path '''
        self.label_folder_path = tk.Label(self.master, text="CFD Folder Location: ", width=self.label_width, anchor="e")
        self.label_folder_path.grid(row=current_row, column=0)
        self.entry_folder_path = tk.Entry(self.master, width=75)
        self.entry_folder_path.grid(row=current_row, column=1)  
        ''' Section 2 - further inputs '''
        current_row += 1
        # multistorey ticked -> protected stair
        self.label_multiple_storeys = tk.Label(self.master, text="Is the apartment multi-storeyed? ", width=self.label_width, anchor="e")
        self.label_multiple_storeys.grid(row=current_row, column=0)
        self.has_multiple_storeys.set("False")
        self.multiple_storeys_selector1 = tk.Radiobutton(self.master, text="True",
                                                variable=self.has_multiple_storeys, value="True", font=("Poppins Light", 8))
        self.multiple_storeys_selector1.grid(row=current_row, column=1)
        self.multiple_storeys_selector2 = tk.Radiobutton(self.master, text="False",
                                                variable=self.has_multiple_storeys, value="False", font=("Poppins Light", 8))
        self.multiple_storeys_selector2.grid(row=current_row, column=2)
        current_row += 1
        # if flat exceeds 12 x 16
        self.label_greater_12x16 = tk.Label(self.master, text="Does the flat exceed 12m x 16m? ", width=self.label_width, anchor="e")
        self.label_greater_12x16.grid(row=current_row, column=0)
        self.has_greater_12x16.set("False")
        self.greater_12x16_selector1 = tk.Radiobutton(self.master, text="True",
                                                variable=self.has_greater_12x16, value="True", font=("Poppins Light", 8))
        self.greater_12x16_selector1.grid(row=current_row, column=1)
        self.greater_12x16_selector2 = tk.Radiobutton(self.master, text="False",
                                                variable=self.has_greater_12x16, value="False", font=("Poppins Light", 8))
        self.greater_12x16_selector2.grid(row=current_row, column=2)
        # if has open kitchen and exceeds 8 x 12
        current_row += 1
        self.label_kit_greater_8x4 = tk.Label(self.master, text="Open kitchen and the flat exceeds 8m x 4m? ", width=self.label_width, anchor="e")
        self.label_kit_greater_8x4.grid(row=current_row, column=0)
        self.has_kit_greater_8x4.set("False")
        self.kit_greater_8x4_selector1 = tk.Radiobutton(self.master, text="True",
                                                variable=self.has_kit_greater_8x4, value="True", font=("Poppins Light", 8))
        self.kit_greater_8x4_selector1.grid(row=current_row, column=1)
        self.kit_greater_8x4_selector2 = tk.Radiobutton(self.master, text="False",
                                                variable=self.has_kit_greater_8x4, value="False", font=("Poppins Light", 8))
        self.kit_greater_8x4_selector2.grid(row=current_row, column=2)
        # cc area
        current_row += 1
        self.label_cc_area = tk.Label(self.master, text="Code Compliant Fire Room Area(m): ", width=self.label_width, anchor="e")
        self.label_cc_area.grid(row=current_row, column=0)
        self.entry_cc_area = tk.Entry(self.master, width=75)
        self.entry_cc_area.grid(row=current_row, column=1)  
        # author name
        current_row += 1
        self.label_author = tk.Label(self.master, text="Author Name: ", width=self.label_width, anchor="e")
        self.label_author.grid(row=current_row, column=0)
        self.entry_author = tk.Entry(self.master, width=75)
        self.entry_author.grid(row=current_row, column=1)  
        # author email prefix
        current_row += 1
        self.label_email = tk.Label(self.master, text="Author email prefix: ", width=self.label_width, anchor="e")
        self.label_email.grid(row=current_row, column=0)
        self.entry_email = tk.Entry(self.master, width=75)
        self.entry_email.grid(row=current_row, column=1)  
        # client name
        current_row += 1
        self.label_client = tk.Label(self.master, text="Client Name: ", width=self.label_width, anchor="e")
        self.label_client.grid(row=current_row, column=0)
        self.entry_client = tk.Entry(self.master, width=75)
        self.entry_client.grid(row=current_row, column=1) 


        ##### Output #####
        current_row += 5

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

        self.img = ImageTk.PhotoImage(open_img)

        self.label_image = tk.Label(self.master, image=self.img)
        self.label_image.image = self.img
        self.label_image.grid(row=current_row, column=2, rowspan=2)
        self.label_image.bind('<Button-1>', func=self.generate_file)

    def generate_file(self, event):
        # TODO: prep for sending to other script
        # then typesafe at top of class
        folder_path = self.entry_folder_path.get()
        # TODO: add in other inputs
        has_multiple_storeys = self.has_multiple_storeys.get()
        has_greater_12x16 = self.has_greater_12x16.get()
        has_kitchen_above_8x4=self.has_kit_greater_8x4.get()
        cc_area = self.entry_cc_area.get()
        author = self.entry_author.get()
        email = self.entry_email.get()
        client = self.entry_client.get()
        # run_stage_three(folder_path)
        from report import prep_for_report_variables
        # first run below from here
        # later
        prep_for_report_variables(
                                cfd_output_path=folder_path, 
                                has_area_above_12x16=has_greater_12x16,
                                has_kitchen_above_8x4=has_kitchen_above_8x4,
                                is_multi_storey=has_multiple_storeys,
                                cc_area=cc_area,
                                author=author,
                                email=email
                            )
        # input_report_variables(
        #                     has_area_above_12x16=has_greater_12x16,
        #                     has_kitchen_above_8x4=True, # needs to be through user input in gui
        #                     is_multi_storey=has_multiple_storeys, 
        #                     num_kitchens=1, # has access through the excel sheet 
        #                     fire_locations=['Kitchen'],
        # )