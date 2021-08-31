from tkinter import *
from MeasurementTypes import *
from Misc import VisualCriteria

class CriteriaSelector(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.crit_list = []

        self.button1 = Button(self, text="Add New Criteria", command=self.create_new_crit)
        self.button1.grid(row=0, column=0, sticky=W)

        self.button2 = Button(self, text="Print all", command=self.printAll)
        self.button2.grid(row=1, column=0, sticky=W)

    def switch_crit(self, meas, new_val):
        if new_val == 'Price':
            meas.switch(0)
        elif new_val == 'Input Value':
            meas.switch(1)

    def printAll(self):
        for critRow in self.crit_list:
            for e in critRow.get():
                print(e)
            print()

    def create_new_crit(self):
        self.button2.destroy()
        i = len(self.crit_list) + 1

        price_m = Measurement(self)

        optState = StringVar(self)
        optState.set('Price')
        optMenu = OptionMenu(self, optState, 'Price', 'Input Value', command=lambda new_val: self.switch_crit(price_m, new_val))

        m_label = Label(self, text=f'Measurement #{i}: ')

        m_label.grid(row=i, column=0)
        optMenu.grid(row=i, column=1, sticky=E)
        price_m.grid(row=i, column=2)

        self.crit_list.append(price_m)

        self.button2 = Button(self, text="Print all", command=self.printAll)
        self.button2.grid(row=i+1, column=0, sticky=W)
    
    def get():
        """
        Returns a list of VisualCriteria objects, one for each row in the criteria section of the app.
        """
        final_list = []
        for crit in crit_list:
            final_list.append(VisualCriteria(crit_list))
        return final_list


if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk(className='Criteria')
    root.geometry("900x600")
    CriteriaSelector(root).grid(row=0, column=0)
    root.mainloop() 
