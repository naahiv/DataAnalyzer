from tkinter import *
from MeasurementTypes import *
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

root = Tk(className='Criteria')
root.geometry("900x600")

entry_list = []

def printAll():
    for elist in entry_list:
        for e in elist.get():
            print(e)
        print()

def switch_crit(meas, new_val):
    if new_val == 'Price':
        meas.switch(0)
    elif new_val == 'Input Value':
        meas.switch(1)

i = 0
def createNewCrit():
    global button2
    button2.destroy()

    global i
    i += 1

    price_m = Measurement(root)

    optState = StringVar(root)
    optState.set('Price')
    optMenu = OptionMenu(root, optState, 'Price', 'Input Value', command=lambda new_val: switch_crit(price_m, new_val))

    optMenu.grid(row=i, column=0, sticky=E)
    price_m.grid(row=i, column=1)

    entry_list.append(price_m)

    button2 = Button(root, text="Print all", command=printAll)
    button2.grid(row=i+1, column=0, sticky=W)

button1 = Button(root, text="Add New Criteria", command=createNewCrit)
button1.grid(row=0, column=0, sticky=W)

button2 = Button(root, text="Print all", command=printAll)
button2.grid(row=1, column=0, sticky=W)

root.mainloop() 
