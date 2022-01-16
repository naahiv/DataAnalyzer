from tkinter import *
from MeasurementTypes import *
from Misc import VisualCriteria

class CriteriaSelector(Frame):
    def __init__(self, parent, or_window=False):
        Frame.__init__(self, parent)
        self.or_window = or_window
        self.crit_list = []

        self.button1 = Button(self, text="Add New Criteria", command=self.create_new_crit)
        self.button1.grid(row=0, column=0, sticky=W)

        self.row_list = []
        self.option_states = []

        # self.button2 = Button(self, text="Print all", command=self.printAll)
        # self.button2.grid(row=1, column=0, sticky=W)

    def switch_crit(self, meas, new_val):
        if new_val == 'Price':
            meas.switch(0)
        elif new_val == 'Input Value':
            meas.switch(1)
        elif new_val == 'OR Clause':
            meas.switch(2)

    def printAll(self):
        print(len(self.crit_list))

    def delete_crit(self, r):
        for (i, row) in enumerate(self.row_list):
            if row[0].grid_info()["row"] == r:
                for obj in self.row_list[i]:
                    obj.destroy()
                self.row_list.pop(i)
                self.crit_list.pop(i)
                break

    def create_new_crit(self):
        # self.button2.destroy()

        l = len(self.row_list)
        try:
            i = self.row_list[l - 1][0].grid_info()["row"] + 1
        except IndexError:
            i = 1

        price_m = Measurement(self)

        optState = StringVar(self)
        optState.set('Price')
        opts_list = ['Price', 'Input Value']
        if not self.or_window:
            opts_list.append('OR Clause')
        optMenu = OptionMenu(self, optState, *opts_list, command=lambda new_val: self.switch_crit(price_m, new_val))

        m_label = Label(self, text=f'Measurement #{i}: ')

        del_button = Button(self, text="X",command=lambda r=i: self.delete_crit(r))

        m_label.grid(row=i, column=0)
        optMenu.grid(row=i, column=1, sticky=E)
        price_m.grid(row=i, column=2)
        del_button.grid(row=i, column=3)

        self.crit_list.append(price_m)

        self.row_list.append([m_label, optMenu, price_m, del_button])
        self.option_states.append(optState)

        # self.button2 = Button(self, text="Print all", command=self.printAll)
        # self.button2.grid(row=i+1, column=0, sticky=W)

    def update_from_crit_list(self, vis_crits):
        for i in range(len(self.row_list)):
            self.crit_list.pop(0)
            for obj in self.row_list.pop(0):
                obj.destroy()
        for crit in vis_crits:
            self.create_new_crit()
            row = self.row_list[-1]
            price_m = row[2]
            optState = self.option_states[-1]
            if type(crit) == list:
                optState.set('OR Clause')
                self.switch_crit(price_m, 'OR Clause')
            else:
                if crit.type == 1:
                    optState.set('Input Value')
                    self.switch_crit(price_m, 'Input Value')
            price_m.data_setup(crit)

    def get(self):
        """
        Returns a list of VisualCriteria objects (or a list for OR clauses), one for each row in the criteria section of the app.
        """
        final_list = []
        for crit in self.crit_list:
            outp = crit.get()
            if type(outp[0]) == str:
                final_list.append(VisualCriteria(outp))
            else:
                final_list.append(outp)
        return final_list


if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk(className='Criteria')
    root.geometry("900x600")
    CriteriaSelector(root).grid(row=0, column=0)
    root.mainloop() 
