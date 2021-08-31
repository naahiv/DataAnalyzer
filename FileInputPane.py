from tkinter import *
from MeasurementTypes import *
from Misc import VisualCriteria
from OptionsSelector import *
from tkinter.filedialog import askopenfile, asksaveasfile
import os

class FileInputPane(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.input_file = None

        self.file_button = Button(self, text='Choose File', command=self.open_file)
        self.file_button.grid(row=0, column=0, pady=10)
        
        self.filename_label = Label(self, text='')
        self.filename_label.grid(row=0, column=1, padx=20, pady=10)

        self.opt_sel = OptionsSelector(self)
        self.opt_sel.grid(row=1, column=0, pady=10)

        self.run_button = Button(self, text='Run Analysis', command=self.run_anal, state=DISABLED)
        self.run_button.grid(row=2, column=0)


    def open_file(self): 
        filetypes = [
            ('Excel Spreadsheets', '*.xlsx'), 
            ('Comma Separated Lists','*.csv'),
            ('All Files', '*')
        ]
        opened_file = askopenfile(mode ='r', filetypes=filetypes)
        if opened_file is not None: 
            self.input_file = opened_file
            self.run_button.configure(state=NORMAL)
            self.filename_label.configure(text=os.path.basename(self.input_file.name))

    def run_anal(self):
        print('Program Running!')
        self.browse_for_save()

    def browse_for_save(self):
        f = asksaveasfile(mode='w', title='Save File', defaultextension='.csv')
        self.out_name = f.name
        f.close()

    def get(self):
        return [self.input_file, self.n_days, self.out_name]

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.geometry("900x600")
    FileInputPane(root).grid(row=0, column=0)
    root.mainloop() 
