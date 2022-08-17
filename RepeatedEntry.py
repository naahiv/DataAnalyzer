from tkinter import *

def set_text(e, text):
    e.delete(0, END)
    e.insert(0, text)

def capitalize(e):
    set_text(e, e.get().upper())

class RepeatedEntry(Frame):
    def __init__(self, parent, init_list=[]):
        Frame.__init__(self, parent)
        self.entry_list = []
        self.force_list(init_list)

        self.add_button = Button(self, text='+', command=self.add_entry)
        self.add_button.grid(row=0, column=0, pady=5)

        if len(self.entry_list) == 0:
            self.add_entry()

    def force_list(self, lst):
        for s in lst:
            self.add_entry()
            set_text(self.entry_list[-1][0], s)

    def add_entry(self):
        
        var = StringVar()

        entry = Entry(self, width=8, textvariable=var)
        entry.grid(row=len(self.entry_list) + 1, column=0, pady=8)

        var.trace("w", lambda name, index, mode, var=var, e=entry: capitalize(e))

        delete_button = Button(self, text='X')
        delete_button.configure(command=lambda btn=delete_button, e=entry: self.remove_entry(btn, e))
        delete_button.grid(row=len(self.entry_list) + 1, column=1, padx=3)

        self.entry_list.append((entry, delete_button))

    def remove_entry(self, btn, e):
        btn.destroy()
        e.destroy()

    def get(self):
        return [entry.get() for (entry, delete_button) in self.entry_list]

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.geometry("1000x800")
    RepeatedEntry(root).grid(row=0, column=0)
    root.mainloop()
