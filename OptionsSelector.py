from tkinter import *
from MeasurementTypes import *
from Misc import VisualCriteria

class OptionsSelector(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.l1 = Label(self, text='Days to Pull:')
        self.l1.grid(row=0, column=0, sticky=W, padx=10)
        self.e1 = Entry(self, width=2)
        self.e1.grid(row=0, column=1, padx=5)

    def get():
        return [self.e1.get()]

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.geometry("900x600")
    OptionsSelector(root).grid(row=0, column=0)
    root.mainloop() 
