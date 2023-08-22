import tkinter as tk
from PIL import ImageTk
from c_Behaviour_Model_3 import run_stage_three

class Tab3Content:
    def __init__(self, master, open_img):
      self.master = master
      self.label_width = 40
      self.entrybox_width = 50
    #   self.has_custom_hrr_peak = tk.StringVar()
    #   self.has_custom_sprinkler_distance = tk.StringVar()
      self.interface(open_img)

    def interface(self, open_img):
        current_row = 0
        # CFD folder location only 
        # then run button
        current_row = 0
        # step 3
        ''' Section 1 - folder path '''
        self.label_folder_path = tk.Label(self.master, text="CFD Folder Location: ", width=self.label_width, anchor="e")
        self.label_folder_path.grid(row=current_row, column=0)
        self.entry_folder_path = tk.Entry(self.master, width=75)
        self.entry_folder_path.grid(row=current_row, column=1)  

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
        run_stage_three(folder_path)