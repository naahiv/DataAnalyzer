from tkinter import *
from MeasurementTypes import *
from Misc import VisualCriteria
from OptionsSelector import *
from tkinter.filedialog import askopenfile, asksaveasfile
import re
from datetime import datetime
import os

class FileInputPane(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.input_loc = None
        self.out_name = None

        self.file_button = Button(self, text='Choose File', command=self.open_file)
        self.file_button.grid(row=0, column=0, pady=10)
        
        self.filename_label = Label(self, text='')
        self.filename_label.grid(row=0, column=1, padx=20, pady=10)

        self.opt_sel = OptionsSelector(self)
        self.opt_sel.grid(row=1, column=0, pady=10)

        self.run_button = Button(self, text='Run Analysis', command=self.browse_for_save, state=DISABLED)
        self.run_button.grid(row=2, column=0)

        self.run_analysis = None


    def open_file(self): 
        filetypes = [
            ('Excel Spreadsheets', '*.xlsx'), 
            # ('Comma Separated Lists','*.csv'),
            ('All Files', '*')
        ]
        opened_file = askopenfile(mode ='r', filetypes=filetypes)
        if opened_file is not None: 
            self.input_loc = opened_file.name
            self.run_button.configure(state=NORMAL)
            self.filename_label.configure(text=os.path.basename(self.input_loc))
            pred_date = FileInputPane.predict_date(self.input_loc)
            self.opt_sel.set_date(*pred_date)

    def browse_for_save(self):
        f = asksaveasfile(mode='w', title='Save File', defaultextension='.csv')
        self.out_name = f.name
        f.close()
        self.run_analysis()

    def get(self):
        return [self.input_loc, self.opt_sel.get(), self.out_name]

    def add_to_run(self, run_collection):
        self.run_analysis = run_collection
    
    def predict_date(filename):
        try:
            d_string = re.findall(r"\w{3}-\d{2}-\d{4}", filename)[0]
            dt = datetime.strptime(d_string, '%b-%d-%Y')
            return (str(dt.month), str(dt.day), str(dt.year))
        except:
            return ("", "", "")

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.geometry("900x600")
    FileInputPane(root).grid(row=0, column=0)
    root.mainloop() 
