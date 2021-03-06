from tkinter import *
import CriteriaSelector as CriSel

def setText(entry, text):
    entry.delete(0, 'end')
    entry.insert(0, text)

class Measurement(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.meas = PriceMeasurement(self)
        self.meas.grid(row=0, column=0)

    def switch(self, to):
        self.meas.destroy()
        if to == 0:
            self.meas = PriceMeasurement(self)
        elif to == 1:
            self.meas = InputMeasurement(self)
        elif to == 2:
            self.meas = OrMeasurement(self)
        self.meas.grid(row=0, column=0)

    def get(self):
        return self.meas.get()

    def destroy(self):
        self.meas.destroy()

    def data_setup(self, crit):
        # already switced
        if type(crit) == list:
            self.meas.current_state = crit
        else:
            if crit.type == 0:
                setText(self.meas.e1, crit.day1)
                setText(self.meas.e2, crit.time1)
                setText(self.meas.e3, crit.day2)
                setText(self.meas.e4, crit.time2)
                if crit.by_perc:
                    setText(self.meas.e5, crit.by_perc)
                self.meas.compState.set(' ' + crit.comp + ' ')
            elif crit.type == 1:
                setText(self.meas.e1, crit.input_field)
                setText(self.meas.e2, crit.value)
                self.meas.compState.set(' ' + crit.comp + ' ')

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

        self.l5 = Label(self, text=" by ")
        self.l5.grid(row=0, column=9, sticky=W, padx=10)

        self.e5 = Entry(self, width=4)
        self.e5.grid(row=0, column=10, padx=10)

        self.l6 = Label(self, text="%")
        self.l6.grid(row=0, column=11, sticky=W, padx=10)

    def get(self):
        # print(self.e1.get())
        return ['price', self.e1.get(), self.e2.get(), self.compState.get(), self.e3.get(), self.e4.get(), self.e5.get()]

    def destroy(self):
        self.l1.destroy()
        self.e1.destroy()
        self.e2.destroy()
        self.comp.destroy()
        self.l2.destroy()
        self.l3.destroy()
        self.e3.destroy()
        self.l4.destroy()
        self.e4.destroy()
        self.l5.destroy()
        self.e5.destroy()
        self.l6.destroy()

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

    def destroy(self):
        self.e1.destroy()
        self.comp.destroy()
        self.e2.destroy()

class OrMeasurement(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.b1 = Button(self, text='Open OR Clause', command=self.open_or_window)
        self.b1.grid(row=0, column=0)

        self.current_state = []

    def open_or_window(self):
        self.popup = Toplevel(self)
        self.popup.title("OR Clause")
        self.popup.geometry("1400x800")
        self.or_window = OrWindow(self.popup, self.on_saved)
        self.or_window.start_with_meas(self.current_state)
        self.or_window.grid(row=0, column=0)
        self.popup.focus_set()

    def on_saved(self):
        self.current_state = self.or_window.get()
        self.popup.destroy()

    def get(self):
        return self.current_state

    def destroy(self):
        self.b1.destroy()
        if hasattr(self, 'popup'):
            if self.popup.winfo_exists():
                self.popup.destroy() # emergency exit

class OrWindow(Frame):
    def __init__(self, parent, on_save):
        Frame.__init__(self, parent)

        self.crit_label = Label(self, text='Select OR Clause', font='none 12')
        self.crit_label.grid(row=0, column=0, pady=15)

        self.crit_selector = CriSel.CriteriaSelector(self, True)
        self.crit_selector.grid(row=1, column=0, rowspan=5)

        self.save_button = Button(self, text='Save OR Clause', command=on_save)
        self.save_button.grid(row=7, column=0, pady=15)

    def get(self):
        return self.crit_selector.get()

    def start_with_meas(self, crits):
        self.crit_selector.update_from_crit_list(crits)


if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.geometry("900x600")
    OrMeasurement(root).grid(row=0, column=0)
    root.mainloop() 
