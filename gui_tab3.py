import tkinter as tk
from PIL import ImageTk

class Tab3Content:
    def __init__(self, master, open_img):
      self.master = master
      self.label_width = 40
      self.entrybox_width = 50
      self.has_custom_hrr_peak = tk.StringVar()
      self.has_custom_sprinkler_distance = tk.StringVar()
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