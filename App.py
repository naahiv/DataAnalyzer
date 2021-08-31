from tkinter import *
from CriteriaSelector import *
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        crit_label = Label(self, text='Criteria Selection', font='none 12')
        crit_label.grid(row=0, column=0)
        crit_select = CriteriaSelector(self)
        crit_select.grid(row=1, column=0)

if __name__ == '__main__':
    root = Tk()
    root.title('Data Analyzer')
    root.geometry('1200x800')
    App(root).grid(row=0, column=0)
    root.mainloop()
