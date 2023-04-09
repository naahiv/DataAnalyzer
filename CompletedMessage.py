from tkinter import *

class CompletedPopup(Frame):
    def __init__(self, parent, data):
        Frame.__init__(self, parent)
        
        self.l1 = Label(self, text=f"Your strategy had a success rate of {data['success_rate']}.")
        self.l1.grid(row=0, column=0, columnspan=4, sticky=W, pady=5)

        self.b1 = Button(self, text='Open Summary')
        self.b1.grid(row=1, column=0, pady=10, padx=5)

        self.b2 = Button(self, text='Open Results')
        self.b2.grid(row=1, column=1, pady=10, padx=5)

        self.b3 = Button(self, text='Open Both')
        self.b3.grid(row=1, column=2, pady=10, padx=5)

        self.b4 = Button(self, text='Cancel')
        self.b4.grid(row=1, column=3, pady=10, padx=5)

        
def create_completed_popup(root):
    popup = TopLevel(root)
    popup.title('Analysis Completed')
    popup.geometry('800x400')
    
    completed_popup = CompletedPopup(popup,)
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

