from tkinter import *
from CriteriaSelector import *
from ProfileSelector import *
from FileInputPane import *
from DataCollectorInterface import *
from tkinter.ttk import Progressbar
from EntryExitTester import *
from Misc import *
from MeasurementTypes import setText

import threading
from tkinter import messagebox

class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.file_input_label = Label(self, text='File Input', font='none 12')
        self.file_input_label.grid(row=0, column=0, padx=100, pady=15)

        self.file_input_pane = FileInputPane(self)
        self.file_input_pane.grid(row=1, column=0)

        self.profile_selector = ProfileSelector(self, self.get_meas_info, self.switch_to_profile)
        self.profile_selector.grid(row=0, column=1, padx=10, pady=20)

        self.crit_label = Label(self, text='Criteria Selection', font='none 12')
        self.crit_label.grid(row=1, column=1, pady=15)

        self.crit_select = CriteriaSelector(self)
        self.crit_select.grid(row=2, column=1, rowspan=10, columnspan=4)

        self.entry_exit = EntryExitTester(self)
        self.entry_exit.grid(row=2, column=0, pady=20)

        self.file_input_pane.add_to_run(self.run_collection)

        self.progress = Progressbar(self, orient=HORIZONTAL, length=100,  mode='indeterminate')

    def get_meas_info(self):
        daysToPull = self.file_input_pane.opt_sel.e1.get()
        crit_list = self.crit_select.get()
        ee = self.entry_exit.get()
        ee_dict = None
        if DataCollectorInterface.validate_ee(ee):
            ee_dict = {'day1': ee[0], 'time1':ee[1], 'day2': ee[2], 'time2': ee[3]}
        return Profile(None, {'name': None, 'dtp': daysToPull,'crits': crit_list, 'ee': ee_dict})

    def switch_to_profile(self, prof):
        if prof.daysToPull:
            setText(self.file_input_pane.opt_sel.e1, prof.daysToPull)
        else:
            setText(self.file_input_pane.opt_sel.e1, "")
        self.crit_select.update_from_crit_list(prof.crits)
        if prof.ee_dict:
            self.entry_exit.set_manual(prof.ee_dict)
        else:
            self.entry_exit.set_manual({'day1': '', 'time1': '', 'day2': '', 'time2': ''})

    def run_collection(self):
        criteria = self.crit_select.get()
        options = self.file_input_pane.get()
        entry_exit = self.entry_exit.get()

        def run_threaded_process():
            self.progress.grid(row=2, column=0)
            self.progress.start()
            out_val = DataCollectorInterface.run_analysis(options, criteria, entry_exit)
            self.progress.stop()
            self.progress.grid_forget()
            if not out_val == None:
                messagebox.showinfo("Success Rate", f'The overall sucess rate of this strategy was {out_val}%')

        threading.Thread(target=run_threaded_process).start()
        print(criteria, options)

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.title('Data Analyzer')
    root.geometry('2200x1400')
    App(root).grid(row=0, column=0)
    root.mainloop()
