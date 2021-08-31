from tkinter import *
from CriteriaSelector import *
from FileInputPane import *
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        file_input_label = Label(self, text='File Input', font='none 12')
        file_input_label.grid(row=0, column=0, padx=100, pady=15)

        file_input_pane = FileInputPane(self)
        file_input_pane.grid(row=1, column=0)

        crit_label = Label(self, text='Criteria Selection', font='none 12')
        crit_label.grid(row=0, column=1, pady=15)

        crit_select = CriteriaSelector(self)
        crit_select.grid(row=1, column=1, rowspan=10, columnspan=4)

if __name__ == '__main__':
    root = Tk()
    root.title('Data Analyzer')
    root.geometry('1600x1000')
    App(root).grid(row=0, column=0)
    root.mainloop()
