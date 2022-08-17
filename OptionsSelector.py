from tkinter import *
from MeasurementTypes import *
from Misc import *

def set_text(e, text):
    e.delete(0, END)
    e.insert(0, text)

class OptionsSelector(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.l1 = Label(self, text='Days to Pull:')
        self.l1.grid(row=0, column=0, sticky=W, padx=10)
        self.e1 = Entry(self, width=2)
        self.e1.insert(0, '1')
        self.e1.grid(row=0, column=1, padx=5)

        self.l2 = Label(self, text='Date:')
        self.l2.grid(row=1, column=0, sticky=W, padx=10)

        self.e_month = Entry(self, width=2)
        self.lS1 = Label(self, text='/')
        self.e_day = Entry(self, width=2)
        self.lS2 = Label(self, text='/')
        self.e_year = Entry(self, width=4)

        self.e_month.grid(row=1, column=1)
        self.lS1.grid(row=1, column=2)
        self.e_day.grid(row=1, column=3)
        self.lS2.grid(row=1, column=4)
        self.e_year.grid(row=1, column=5)

    def get(self):
        # TODO: get rid of the zero from 'Days to Pull'
        infoList = [0, self.e_month.get(), self.e_day.get(), self.e_year.get()]
        return VisualOptions(infoList)

    def set_date(self, mo, d, yr):
        set_text(self.e_month, mo)
        set_text(self.e_day, d)
        set_text(self.e_year, yr)

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.geometry("900x600")
    OptionsSelector(root).grid(row=0, column=0)
    root.mainloop() 
