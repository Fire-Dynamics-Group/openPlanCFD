import tkinter as tk
from tkinter import ttk
from PIL import Image

from gui_tab1 import Tab1Content
from gui_tab2 import Tab2Content
from gui_tab3 import Tab3Content


class Application(tk.Frame):
    #     # Default Value
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.master = master
        self.master.title("Fire Dynamics Open Plan Robot")

        interfaceheight = str(750)
        interfacewidth = str(943)

        self.master.geometry(interfacewidth+"x"+interfaceheight+"+25+0")  # width x height

        self.grid()

        self.interface()

    def interface(self):
        '''
        TODO: tabs for each step at top
        '''
        # later have constants for widths etc and styles
        label_width = 20
        entrybox_width = 50

        # Fire Dynamics AI
        path = "FDAI_grey.jpg"
        open_image = Image.open(path).resize((60, 90), Image.Resampling.LANCZOS) # Image.ANTIALIAS deprecated to LANCZOS

        # Create the tab control
        tabControl = ttk.Notebook(self.master)
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        # tab1 = create_tab1(tab1, label_width, entrybox_width, self.img)
        tab1_content = Tab1Content(tab1, open_image)
        tab2_content = Tab2Content(tab2, open_image)
        tab3_content = Tab3Content(tab3, open_image)
        tabControl.add(tab1, text='Tab 1')
        tabControl.add(tab2, text='Tab 2')
        tabControl.add(tab3, text='Tab 3')
        tabControl.grid(sticky="nsew")

 

# TODO: scope tabs
# TODO: how to have placeholder text??

root = tk.Tk()
root.resizable(False, False)
app = Application(master=root)
app.mainloop()