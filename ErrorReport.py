import tkcap
from EmailSender import send_mail
import os
import os.path as op
from zipfile import ZipFile
import json
from tkinter import *
home = op.expanduser('~')
zip_fp = op.join(home, 'da_error_tmp.zip')
log_fp = op.join(home, 'da_output.log')
img_fp = op.join(home, 'window_capture.png')
json_fp = op.join(home, 'current_config.json')

class ErrorReport:
    def __init__(self, root, current_json_config, input_fp, output_fp, title, message):
        self.root = root
        self.input_fp = input_fp
        self.output_fp = output_fp
        self.error_title = title
        self.error_message = message
        self.delete_tmp_files()
        json_file = open(json_fp, 'w')
        json.dump(current_json_config, json_file, indent=4)
        json_file.close()

    def gather_report(self):
        self.take_screenshot()
        zip_file = ZipFile(zip_fp, 'w')
        self.att_fps = [img_fp, log_fp, json_fp]
        if self.input_fp:
            self.att_fps.append(self.input_fp)
        if self.output_fp:
            self.att_fps.append(self.output_fp)
        for fp in self.att_fps:
            zip_file.write(fp, op.basename(fp))
        zip_file.close()

    def delete_tmp_files(self):
        for fp in [img_fp, json_fp, zip_fp]:
            if op.exists(fp):
                os.remove(fp)
    
    def take_screenshot(self):
        cap = tkcap.CAP(self.root)
        cap.capture(img_fp)

    def send_report(self):
        self.gather_report()
        self.email_report()
        self.delete_tmp_files()
    
    def email_report(self):
        name = 'Data Analyzer'
        login = 'dataanalyzer7@gmail.com'
        pwd = 'naahivda7'

        paths = self.att_fps + [zip_fp]
        recip = 'vihaandheer@gmail.com' 
        cc_addrs = ['naahivrheed@gmail.com']
        # cc_addrs = ['eric@multichannelinsights.com']
        server = 'smtp.gmail.com'

        user_title = self.error_title
        user_message = self.error_message

        subject = f'New DA Error Report: {user_title}'
        message = f"""\
        <html>
            <head></head>
            <body>
                Hi Vihaan,<br>
                This is the latest error report titled {user_title}. The following message was added:<br>

                <blockquote>
                {user_message}
                </blockquote>

                All debug files are attached both individually and in the form of a zip file.<br>
                <br>
                Thanks,<br>
                Data Analyzer<br>
            </body>
        </html>
        """

        send_mail(name, [recip], subject, message, paths, 'smtp.gmail.com', 587, login, pwd, cc_addrs)
        print('email sent')

class ErrorReportBox(Frame):
    def __init__(self, parent, on_cancel, on_send):
        Frame.__init__(self, parent)

        self.l1 = Label(self, text='Error Report Title')
        self.l1.grid(row=0, column=0, sticky=W, pady=5)

        self.e1 = Entry(self, width=35)
        self.e1.grid(row=1, column=0, sticky=W, pady=10)

        self.l2 = Label(self, text='Error Report Message')
        self.l2.grid(row=2, column=0, sticky=W, pady=5)

        self.e2 = Text(self, height=5, width=45)
        self.e2.grid(row=3, column=0, columnspan=2, sticky=W, pady=10)

        self.b1 = Button(self, text='Cancel', command=on_cancel)
        self.b1.grid(row=4, column=0, sticky=E, pady=10, padx=5)

        self.b2 = Button(self, text='Send', command=lambda: on_send(self.get()))
        self.b2.grid(row=4, column=1, sticky=E, pady=10, padx=5)

    def get(self):
        return [self.e1.get(), self.e2.get("1.0", "end-1c")]


def create_error_report_popup(root, on_send):
    popup = Toplevel(root)
    popup.title('New Error Report')
    popup.geometry('800x400')
    def sender(otpt):
        popup.destroy()
        on_send(otpt)
    report_box = ErrorReportBox(popup, popup.destroy, sender)
    report_box.grid(row=0, column=0)
    popup.focus_set()
    return report_box

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.geometry("800x400")
    def fpass():
        pass
    ErrorReportBox(root, fpass, fpass).grid(row=0, column=0)
    root.mainloop() 
