from tkinter import *
from MeasurementTypes import *
from Misc import VisualCriteria, revert_to_print_log
from OptionsSelector import *
from tkinter.filedialog import askopenfilenames, asksaveasfilename
import re
from datetime import datetime
import os

class FileInputPane(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.input_locs = None
        self.out_name = None

        self.file_button = Button(self, text='Choose File(s)', command=self.open_file)
        self.file_button.grid(row=0, column=0, pady=10)
        
        self.opts_wrapper = None

        self.run_button = Button(self, text='Run Analysis', command=self.browse_for_save, state=DISABLED)
        self.run_button.grid(row=2, column=0)

        self.run_analysis = None


    def open_file(self): 
        filetypes = [
            ('Excel Spreadsheets', '*.xlsx'), 
            # ('Comma Separated Lists','*.csv'),
            ('All Files', '*')
        ]
        filenames = askopenfilenames(filetypes=filetypes, title='Choose Lists', multiple=True)
        if not filenames == '':
            self.input_locs = list(filenames)
            if not self.opts_wrapper == None:
                self.opts_wrapper.destroy()
            self.opts_wrapper = OptionsWrapper(self, self.input_locs)
            self.opts_wrapper.grid(row=1, column=0, columnspan=2, padx=5)
            self.run_button.configure(state=NORMAL)

    def browse_for_save(self):
        self.out_name = asksaveasfilename(title='Save Results', defaultextension='.csv', filetypes=[('Comma Separated Lists', '*.csv')])
        if not self.out_name == None and not self.out_name == '':
            self.run_analysis()

    def get(self):
        return [self.input_locs, self.opts_wrapper.get(), self.out_name]

    def add_to_run(self, run_collection):
        self.run_analysis = run_collection
    

class OptionsWrapper(Frame):
    def __init__(self, parent, filenames):
        Frame.__init__(self, parent)

        self.opts_list = []

        for (r, filename) in enumerate(filenames):
            fn = os.path.basename(filename)
            opt = OptionsSelector(self)
            opt.grid(row=r, column=0, pady=10, padx=5)
            opt.set_date(*OptionsWrapper.predict_date(fn))
            self.opts_list.append(opt)
            Label(self, text=fn).grid(row=r, column=1, pady=10, padx=5)

    def get(self):
        return [opt.get() for opt in self.opts_list]

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
