from tkinter import *

class Measurement(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.meas = PriceMeasurement(self)
        self.meas.grid(row=0, column=0)

    def switch(self, to):
        self.meas.destroy()
        if to == 0:
            self.meas = PriceMeasurement(self)
            self.meas.grid(row=0, column=0)
        elif to == 1:
            self.meas = InputMeasurement(self)
            self.meas.grid(row=0, column=0)

    def get(self):
        return self.meas.get()

class PriceMeasurement(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.l1 = Label(self, text="on Day ")
        self.l1.grid(row=0, column=0, sticky=W, padx=10)

        self.e1 = Entry(self, width=2)
        self.e1.grid(row=0, column=1, padx=10)

        self.l2 = Label(self, text=" at ")
        self.l2.grid(row=0, column=2, sticky=W, padx=10)

        self.e2 = Entry(self, width=5)
        self.e2.grid(row=0, column=3, padx=10)

        self.compState = StringVar(self)
        self.compState.set(' > ')
        self.comp = OptionMenu(self, self.compState, ' > ', ' < ', ' = ')
        self.comp.grid(row=0, column=4, sticky=W, padx=10)

        self.l3 = Label(self, text="Day ")
        self.l3.grid(row=0, column=5, sticky=W, padx=10)

        self.e3 = Entry(self, width=2)
        self.e3.grid(row=0, column=6, padx=10)

        self.l4 = Label(self, text=" at ")
        self.l4.grid(row=0, column=7, sticky=W, padx=10)

        self.e4 = Entry(self, width=5)
        self.e4.grid(row=0, column=8, padx=10)

    def get(self):
        return ['price', self.e1.get(), self.e2.get(), self.compState.get(), self.e3.get(), self.e4.get()]


class InputMeasurement(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.e1 = Entry(self, width=11)
        self.e1.grid(row=0, column=0, padx=12)

        self.compState = StringVar(self)
        self.compState.set(' > ')
        self.comp = OptionMenu(self, self.compState, ' > ', ' < ', ' = ')
        self.comp.grid(row=0, column=1, sticky=W, padx=12)

        self.e2 = Entry(self, width=12)
        self.e2.grid(row=0, column=2, padx=12)

    def get(self):
        return ['input', self.e1.get(), self.compState.get(), self.e2.get()]