from tkinter import *

class CompletedPopup(Frame):
    def __init__(self, parent, data, cc):
        Frame.__init__(self, parent)

        def open_summary():
            data['open_summary']()
            cc()

        def open_results():
            data['open_results']()
            cc()

        def open_both():
            data['open_results']()
            data['open_summary']()
            cc()

        if data['success_rate']:
            self.l1 = Label(self, text=f"Your strategy had a success rate of {data['success_rate']}.", font='none 13')
            self.l1.grid(row=0, column=0, columnspan=4, sticky=W, pady=10)
        else:
            self.l1 = Label(self, text=f"Your strategy has finished running.", font='none 13')
            self.l1.grid(row=0, column=0, columnspan=4, sticky=W, pady=10)


        self.b1 = Button(self, text='Open Summary', command=open_summary)
        self.b1.grid(row=1, column=1, pady=30, padx=15)

        self.b2 = Button(self, text='Open Results', command=open_results)
        self.b2.grid(row=1, column=2, pady=10, padx=15)

        self.b3 = Button(self, text='Open Both', command=open_both)
        self.b3.grid(row=1, column=3, pady=10, padx=15)

        self.b4 = Button(self, text='Cancel', command=cc)
        self.b4.grid(row=1, column=4, pady=10, padx=15)

        
def create_completed_popup(root, data):
    popup = Toplevel(root)
    popup.title('Analysis Completed')
    popup.geometry('800x400')
    
    completed_popup = CompletedPopup(popup, data, lambda: popup.destroy())
    completed_popup.grid(row=0, column=0)
    popup.focus_set()
    return completed_popup

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.geometry('800x400')
    CompletedPopup(root, {'success_rate': '10%'}).grid(row=0, column=0)
    root.mainloop()

