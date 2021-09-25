from tkinter import *
from CriteriaSelector import *
from FileInputPane import *
from DataCollectorInterface import *
from tkinter.ttk import Progressbar
import threading

class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.file_input_label = Label(self, text='File Input', font='none 12')
        self.file_input_label.grid(row=0, column=0, padx=100, pady=15)

        self.file_input_pane = FileInputPane(self)
        self.file_input_pane.grid(row=1, column=0)

        self.crit_label = Label(self, text='Criteria Selection', font='none 12')
        self.crit_label.grid(row=0, column=1, pady=15)

        self.crit_select = CriteriaSelector(self)
        self.crit_select.grid(row=1, column=1, rowspan=10, columnspan=4)

        self.file_input_pane.add_to_run(self.run_collection)

        self.progress = Progressbar(self, orient=HORIZONTAL,length=100,  mode='indeterminate')

    def run_collection(self):
        criteria = self.crit_select.get()
        options = self.file_input_pane.get()

        def run_threaded_process():
            self.progress.grid(row=2, column=0)
            self.progress.start()
            DataCollectorInterface.run_analysis(options, criteria)
            self.progress.stop()
            self.progress.grid_forget()

        threading.Thread(target=run_threaded_process).start()
        print(criteria, options)

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.title('Data Analyzer')
    root.geometry('1600x1000')
    App(root).grid(row=0, column=0)
    root.mainloop()