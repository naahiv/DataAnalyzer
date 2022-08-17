from tkinter import *
import time
from datetime import datetime
from pandas import DateOffset
from DataCollectorInterface import DataCollectorInterface
from RepeatedEntry import *
dci = DataCollectorInterface # alias
import os

def format_symbol_list(string_list):
    out = []
    arr = string_list.strip('\n').split('\n')
    for a in arr:
        out.append(a.strip(' '))
    return out

class OrderSenderWindow(Frame):
    def __init__(self, parent, init_symbols):
        Frame.__init__(self, parent)

        self.l1 = Label(self, text='BUY at: ')
        self.l1.grid(row=0, column=0, padx=10, pady=5, sticky=E)

        self.e1 = Entry(self, width=8)
        self.e1.grid(row=0, column=1, padx=5, pady=5)

        self.l2 = Label(self, text='SELL at: ')
        self.l2.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        self.e2 = Entry(self, width=8)
        self.e2.grid(row=0, column=3, padx=5, pady=5)

        self.l3 = Label(self, text='Price per stock (approx. $): ')
        self.l3.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        self.e3 = Entry(self, width=8)
        self.e3.grid(row=1, column=1, padx=5, pady=5)

        self.l4 = Label(self, text='Symbol List:')
        self.l4.grid(row=2, column=0, padx=5, pady=10)

        self.e4 = RepeatedEntry(self, init_symbols)
        self.e4.grid(row=3, column=0, columnspan=4, sticky=W, pady=10, padx=5)

        self.b1 = Button(self, text='Send to TD', command=self.send_button_clicked)
        self.b1.grid(row=4, column=0, padx=5, pady=10)

        self.l_timer = Label(self, font=('arial', 40))
        self.l_timer.grid(row=5, column=0, padx=5, pady=20)

        self.l6 = Label(self)
        self.l6.grid(row=6, column=0, padx=5, pady=10)

        self.l7 = Label(self)
        self.l7.grid(row=7, column=0, padx=5, pady=10)

        self.l8 = Label(self)
        self.l8.grid(row=8, column=0, padx=5, pady=10)


    def setup_event_labels(self, times_arr):
        for (i, l) in enumerate([self.l6, self.l7, self.l8]):
            l.config(text=f'PENDING #{i+1}: {times_arr[i]}')

    def stage_one(self):
        # in this step, we send market BUYs for each of the symbols
        self.l6.config(text='SUBMITTED')
        self.order_id_list = dci.create_batch_market_order(self.symbols, float(self.per_amt))

    def stage_two(self):
        # in this step, we cancel all unfilled orders
        self.l7.config(text='SUBMITTED')
        for order_id in self.order_id_list:
            if not dci.get_order_status(order_id) == 'FILLED':
                dci.cancel_order(order_id)

    def stage_three(self):
        # in this step, we close all remaining positions
        self.l8.config(text='SUBMITTED')
        dci.create_batch_closes(self.order_id_list)

    def start_timer(self, stop_time, callback):
        disp_time = time.strftime('%H:%M:%S')
        if disp_time == stop_time:
            callback()
            return
        self.l_timer.config(text=disp_time)
        self.l_timer.after(200, lambda: self.start_timer(stop_time, callback))

    def send_button_clicked(self):
        self.symbols = self.e4.get()
        self.per_amt = self.e3.get()
        start_time = self.e1.get()
        fmat = '%H:%M:%S'
        tt = datetime.strptime(start_time, fmat)
        tt = tt + DateOffset(minutes=1)
        cancel_time = tt.strftime(fmat)
        end_time = self.e2.get()
        self.setup_event_labels([start_time, cancel_time, end_time])

        def nested_callback():
            self.stage_one()
            def second_callback():
                self.stage_two()
                self.start_timer(end_time, self.stage_three)
            self.start_timer(cancel_time, second_callback)
        self.start_timer(start_time, nested_callback)

def create_order_sender_popup(root, lookouts):
    popup = Toplevel(root)
    popup.title('Order Sender')
    popup.geometry("900x1000")
    senderWindow = OrderSenderWindow(popup, lookouts)
    senderWindow.grid(row=0, column=0)
    return senderWindow

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.title('Order Sender')
    root.geometry("1800x1200")
    OrderSenderWindow(root).grid(row=0, column=0)
    root.mainloop() 
