from tkinter import *
import time
from datetime import datetime
from pandas import DateOffset
from DataCollectorInterface import DataCollectorInterface
from RepeatedEntry import *
from tkinter import messagebox
dci = DataCollectorInterface # alias
import os

def format_symbol_list(string_list):
    out = []
    arr = string_list.strip('\n').split('\n')
    for a in arr:
        out.append(a.strip(' '))
    return out

class OrderSenderWindow(Frame):
    def __init__(self, parent, init_symbols=[]):
        Frame.__init__(self, parent)

        self.l1 = Label(self, text='BUY at: ')
        self.l1.grid(row=0, column=0, padx=10, pady=5, sticky=E)

        self.e1 = Entry(self, width=8)
        self.e1.grid(row=0, column=1, padx=5, pady=5)

        self.l2 = Label(self, text='SELL at: ')
        self.l2.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        self.e2 = Entry(self, width=8)
        self.e2.grid(row=0, column=3, padx=5, pady=5)

        self.l3 = Label(self, text='Amount per stock (approx. $): ')
        self.l3.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        self.e3 = Entry(self, width=8)
        self.e3.grid(row=1, column=1, padx=5, pady=5)

        self.tp_var = IntVar()
        self.tp_check = Checkbutton(self, text='Take Profit (%)', variable=self.tp_var, onvalue=1, offvalue=0, command=self.toggle_tp_e)
        self.tp_check.grid(row=2, column=0)

        self.tp_e = Entry(self, width=4)
        self.tp_e.grid(row=2, column=1, padx=5)
        self.tp_e.grid_remove() # maybe not

        self.sl_var = IntVar()
        self.sl_check = Checkbutton(self, text='Stop Loss (%)', variable=self.sl_var, onvalue=1, offvalue=0, command=self.toggle_sl_e)
        self.sl_check.grid(row=3, column=0)

        self.sl_e = Entry(self, width=4)
        self.sl_e.grid(row=3, column=1, padx=5)
        self.sl_e.grid_remove() # maybe not


        self.lf_var = IntVar()
        self.lf_check = Checkbutton(self, text='Limit Floor (%)', variable=self.lf_var, onvalue=1, offvalue=0, command=self.toggle_lf_e)
        self.lf_check.grid(row=4, column=0)

        self.lf_e = Entry(self, width=4)
        self.lf_e.grid(row=4, column=1, padx=5)
        self.lf_e.grid_remove() # maybe not

        self.lc_var = IntVar()
        self.lc_check = Checkbutton(self, text='Limit Ceiling (%)', variable=self.lc_var, onvalue=1, offvalue=0, command=self.toggle_lc_e)
        self.lc_check.grid(row=5, column=0)

        self.lc_e = Entry(self, width=4)
        self.lc_e.grid(row=5, column=1, padx=5)
        self.lc_e.grid_remove() # maybe not

        self.l4 = Label(self, text='Symbol List:')
        self.l4.grid(row=6, column=0, padx=5, pady=10)

        self.e4 = RepeatedEntry(self, init_symbols)
        self.e4.grid(row=7, column=0, columnspan=4, sticky=W, pady=10, padx=5)

        self.b1 = Button(self, text='Send to TD', command=self.send_button_clicked)
        self.b1.grid(row=8, column=0, padx=5, pady=10)

        self.l_timer = Label(self, font=('arial', 40))
        self.l_timer.grid(row=8, column=0, padx=5, pady=20)

        self.l6 = Label(self)
        self.l6.grid(row=10, column=0, padx=5, pady=10)

        self.l7 = Label(self)
        self.l7.grid(row=11, column=0, padx=5, pady=10)

        self.l8 = Label(self)
        self.l8.grid(row=12, column=0, padx=5, pady=10)

        self.ask_list = None

    def toggle_tp_e(self):
        if self.tp_var.get() == 0:
            self.tp_e.grid_remove()
        else:
            self.tp_e.grid()

    def toggle_sl_e(self):
        if self.sl_var.get() == 0:
            self.sl_e.grid_remove()
        else:
            self.sl_e.grid()

    def toggle_lf_e(self):
        if self.lf_var.get() == 0:
            self.lf_e.grid_remove()
        else:
            self.lf_e.grid()

    def toggle_lc_e(self):
        if self.lc_var.get() == 0:
            self.lc_e.grid_remove()
        else:
            self.lc_e.grid()


    def setup_event_labels(self, times_arr):
        for (i, l) in enumerate([self.l6, self.l7, self.l8]):
            l.config(text=f'PENDING #{i+1}: {times_arr[i]}')

    def stage_one(self):
        # in this step, we send market BUYs for each of the symbols
        limit_price, tp_perc, sl_perc, lc_perc = None, None, None, None
        if self.tp_var.get() == 1:
            tp_perc = float(self.tp_e.get())
        if self.sl_var.get() == 1:
            sl_perc = float(self.sl_e.get())
        if self.lc_var.get() == 1:
            lc_perc = float(self.lc_e.get())
        self.l6.config(text='SUBMITTED')
        # assume ask_list has been generated
        if lc_perc:
            self.order_id_list = dci.create_batch_limit_order(self.symbols, lc_perc, float(self.per_amt), tp_perc, sl_perc, self.ask_list)
        else:
            self.order_id_list = dci.create_batch_market_order(self.symbols, float(self.per_amt), tp_perc, sl_perc, self.ask_list)

    def stage_two(self):
        # in this step, we cancel all unfilled orders
        """
        In this edition of the software, i.e. anything version 3 or before, we will not 
        do the cancellation process. For some reason, the wrong orders apparently get
        canceled. In the next edition, we will implement a much more detailed TDOrder class,
        which will correctly obtain and separate orders and their legs.
        """
        pass
        # the following does not get executed
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
        error_message = self.validate_order_params()
        if error_message == None:
            self.initiate_order_sequence()
        else:
            messagebox.showerror('Order Configuration Error', error_message)

    def initiate_order_sequence(self):
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

    def validate_order_params(self):
        try:
            datetime.strptime(self.e1.get(), '%H:%M:%S')
            datetime.strptime(self.e1.get(), '%H:%M:%S')
            try:
                float(self.e3.get())
                try:
                    if self.tp_var.get() == 1:
                        float(self.tp_e.get())
                    if self.sl_var.get() == 1:
                        float(self.sl_e.get())

                    error_message, ask_list = dci.td_ask_validation(self.e4.get())
                    self.ask_list = ask_list
                    return error_message
                except:
                    return 'If Take Profit or Stop Loss boxes are checked, a valid percentage must be provided.'
            except:
                return 'A proper amount per stock must be provided.'

        except:
            return 'Times must be given in full format, e.g.: 09:35:22.'

    def get(self):
        d = {'t1': self.e1.get(), 't2': self.e2.get(), 'amt': self.e3.get()}
        if self.tp_var.get() == 1:
            d['tp'] = self.tp_e.get()
        if self.sl_var.get() == 1:
            d['sl'] = self.sl_e.get()
        return d

    def update(self, data):
        set_text(self.e1, data['t1'])
        set_text(self.e2, data['t2'])
        set_text(self.e3, data['amt'])
        if 'tp' in data:
            self.tp_var.set(1)
            self.toggle_tp_e()
            set_text(self.tp_e, data['tp'])
        else:
            self.tp_var.set(0)
            set_text(self.tp_e, 0)
            self.toggle_tp_e()

        if 'sl' in data:
            self.sl_var.set(1)
            self.toggle_sl_e()
            set_text(self.sl_e, data['sl'])
        else:
            self.sl_var.set(0)
            set_text(self.sl_e, 0)
            self.toggle_sl_e()

def create_order_sender_popup(root, lookouts, init_data, on_closing):
    popup = Toplevel(root)
    popup.title('Order Sender')
    popup.geometry("900x1000")
    senderWindow = OrderSenderWindow(popup, lookouts)
    senderWindow.grid(row=0, column=0)
    senderWindow.update(init_data)
    def closer(sen_win=senderWindow):
        on_closing(sen_win)
        popup.destroy()
    popup.protocol("WM_DELETE_WINDOW", closer)
    return senderWindow

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.title('Order Sender')
    root.geometry("1800x1200")
    OrderSenderWindow(root).grid(row=0, column=0)
    root.mainloop() 
