from Misc import *
import sys
from datetime import datetime
from pytz import timezone
now = datetime.now(tz=timezone('US/Eastern'))
s = f"""
---------------------------------------------------
Output for Data Analyzer run at {now.strftime("%H:%M:%S")} EST on {now.strftime("%Y-%m-%d")}:"""
print(s)

import time
from tkinter import *
from CriteriaSelector import *
from ProfileSelector import *
from FileInputPane import *
from DataCollectorInterface import *
from tkinter.ttk import Progressbar
from EntryExitTester import *
from MeasurementTypes import setText
from ErrorReport import *
from OrderSenderWindow import *
from CompletedMessage import *
import threading
from tkinter import messagebox

class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.file_input_label = Label(self, text='File Input', font='none 12')
        self.file_input_label.grid(row=0, column=0, padx=100, pady=15)

        self.file_input_pane = FileInputPane(self)
        self.file_input_pane.grid(row=1, column=0)

        self.profile_selector = ProfileSelector(self, self.get_meas_info, self.switch_to_profile)
        self.profile_selector.grid(row=0, column=1, padx=10, pady=20)

        self.crit_label = Label(self, text='Criteria Selection', font='none 12')
        self.crit_label.grid(row=1, column=1, pady=15)

        self.crit_select = CriteriaSelector(self)
        self.crit_select.grid(row=2, column=1, rowspan=10, columnspan=4)

        self.time_remaining = Label(self, text='00s')
        self.time_remaining.grid(row=3, column=0, pady=10)

        self.interr_button = Button(self, text='Halt', command=self.interrupt_run)
        self.interr_button.grid(row=4, column=0)

        self.entry_exit = EntryExitTester(self)
        self.entry_exit.grid(row=5, column=0, pady=20)

        self.file_input_pane.add_to_run(self.run_collection)

        self.progress = Progressbar(self, orient=HORIZONTAL, length=100,  mode='indeterminate')


        self.order_button = Button(self, text='Open Order Sender', command=self.open_order_window, state=DISABLED)
        self.order_button.grid(row=6, column=0, sticky=W, pady=15, padx=5)

        self.logfile_button = Button(self, text='Open Log File', command=open_log_file)
        self.logfile_button.grid(row=7, column=0, sticky=W, pady=15, padx=5)

        self.error_report_button = Button(self, text='Send Error Report', command=self.send_error_report)
        self.error_report_button.grid(row=8, column=0, sticky=W, pady=15, padx=5)

        self.recent_lookouts = []

        self.current_order_data = {'t1': '', 't2': '', 'amt': ''}

        self.check_for_auth_success()

    def send_error_report(self):
        def on_send(sel_arr):
            json_config = self.get_meas_info().export_to_dict()

            json_config.pop('name')
            input_fp, opts, output_fp = self.file_input_pane.get()
            json_config['day1_date'] = opts.dayOneDate
            report = ErrorReport(self, json_config, input_fp, output_fp, sel_arr[0], sel_arr[1])
            time.sleep(250.0 / 1000.0)
            report.send_report()

            messagebox.showinfo('Success!', f'The error was successfully reported to the developer, who will get back to you soon!')

        self.error_popup = create_error_report_popup(self, on_send)

    def get_meas_info(self):
        daysToPull = 0 # deprecated
        crit_list = self.crit_select.get()
        ee = self.entry_exit.get()
        ee_dict = None
        if DataCollectorInterface.validate_ee(ee):
            ee_dict = {'day1': ee[0], 'time1':ee[1], 'day2': ee[2], 'time2': ee[3]}
        prof = Profile(None, {'name': None, 'dtp': daysToPull,'crits': crit_list, 'ee': ee_dict})
        
        prof.order_data = self.get_current_order_data()
        return prof

    def get_current_order_data(self):
        try:
            return self.order_window.get()
        except:
            return self.current_order_data
    
    def update_order_data(self, order_data):
        if not order_data == None:
            self.current_order_data = order_data
        else:
            self.current_order_data = {'t1': '', 't2': '', 'amt': ''}
        try:
            self.order_window.update(self.current_order_data)
        except:
            pass

    def open_order_window(self):
        def on_closing(order_window):
            self.current_order_data = order_window.get()
        self.order_window = create_order_sender_popup(self, self.recent_lookouts, self.current_order_data, on_closing)

    def switch_to_profile(self, prof):
        self.crit_select.update_from_crit_list(prof.crits)
        if prof.ee_dict:
            self.entry_exit.set_manual(prof.ee_dict)
        else:
            self.entry_exit.set_manual({'day1': '', 'time1': '', 'day2': '', 'time2': ''})
        self.update_order_data(prof.order_data)

    def run_collection(self):
        criteria = self.crit_select.get()
        options = self.file_input_pane.get()
        entry_exit = self.entry_exit.get()

        class CustomThread(threading.Thread):
            def __init__(thr, *args, **kwargs):
                super(CustomThread, thr).__init__(*args, **kwargs)
                thr._stop_event = threading.Event()
            def stop(thr):
                thr._stop_event.set()
            def is_stopped(thr):
                return thr._stop_event.is_set()
            def run(thr):
                def time_callback(new_time):
                    self.time_remaining['text'] = f'{new_time}s'
                self.progress.grid(row=5, column=0)
                self.progress.start()
                out_val, perf_done, open_summary = DataCollectorInterface.run_analysis(options, criteria, entry_exit, prof_name=self.profile_selector.current_state.get(), time_callback=time_callback, thread=thr)
                if perf_done:
                    def mod_perf_done():
                        self.recent_lookouts = perf_done()
                    completed_popup = create_completed_popup(self, {
                        'success_rate': out_val,
                        'open_summary': open_summary,
                        'open_results': mod_perf_done,
                        'options': options
                    })
                else:
                    # add any completion action if halted
                    pass

        self.s_thread = CustomThread()
        self.s_thread.start()
        print(criteria, options)

    def interrupt_run(self):
        try:
            self.s_thread.stop()
            self.s_thread.join()
            self.progress.stop()
            self.progress.grid_forget()
        except Exception as e:
            print('stoppable_thread is not currently running')
            print(e)

    def check_for_auth_success(self):
        if not GLOBAL_ACCT_INFO == None:
            acct_name, trading_cash, liq_value = GLOBAL_ACCT_INFO
            l1 = Label(self, text=f'Welcome, {acct_name}.')
            l1.grid(row=8, column=0)

            l2 = Label(self, text=f'Trading Cash: {trading_cash}\tLiquid Value: {liq_value}')
            l2.grid(row=9, column=0)

            self.order_button.configure(state=NORMAL)


if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.title('Data Analyzer')
    root.geometry('2200x1400')
    App(root).grid(row=0, column=0)
    root.mainloop()
