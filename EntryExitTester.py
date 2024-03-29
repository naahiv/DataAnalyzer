from tkinter import *
import os
from MeasurementTypes import setText

class EntryExitTester(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.l1 = Label(self, text="Buy on Day ")
        self.l1.grid(row=0, column=0, sticky=W, padx=10)

        self.e1 = Entry(self, width=2)
        self.e1.grid(row=0, column=1, padx=10)

        self.l2 = Label(self, text=" at ")
        self.l2.grid(row=0, column=2, sticky=W, padx=10)

        self.e2 = Entry(self, width=5)
        self.e2.grid(row=0, column=3, padx=10)

        self.l3 = Label(self, text="Sell on Day ")
        self.l3.grid(row=0, column=5, sticky=W, padx=10)

        self.e3 = Entry(self, width=2)
        self.e3.grid(row=0, column=6, padx=10)

        self.l4 = Label(self, text=" at ")
        self.l4.grid(row=0, column=7, sticky=W, padx=10)

        self.e4 = Entry(self, width=5)
        self.e4.grid(row=0, column=8, padx=10)

        # take profit / stop loss stuff
        self.tpl = Label(self, text='Take Profit (%): ')
        self.tpl.grid(row=1, column=0, pady=10)
        
        self.tpe = Entry(self, width=4)
        self.tpe.grid(row=1, column=1)

        self.sll = Label(self, text='Stop Loss (%): ')
        self.sll.grid(row=2, column=0, pady=10)

        self.sle = Entry(self, width=4)
        self.sle.grid(row=2, column=1)
    
    def set_manual(self, ee_dict):
        setText(self.e1, ee_dict['day1'])
        setText(self.e2, ee_dict['time1'])
        setText(self.e3, ee_dict['day2'])
        setText(self.e4, ee_dict['time2'])

    def get(self):
        return [self.e1.get(), self.e2.get(), self.e3.get(), self.e4.get(), self.tpe.get(), self.sle.get()]

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.geometry("900x600")
    EntryExitTester(root).grid(row=0, column=0)
    root.mainloop() 
