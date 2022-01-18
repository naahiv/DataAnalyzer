import tkcap
import os
import os.path as op
from zipfile import ZipFile
import json
home = op.expanduser('~')
zip_fp = op.join(home, 'da_error_tmp.zip')
log_fp = op.join(home, 'da_output.log')
img_fp = op.join(home, 'window_capture.png')
json_fp = op.join(home, 'current_config.json')

class ErrorReport:
    def __init__(self, root, current_json_config, input_fp, output_fp):
        self.root = root
        self.input_fp = input_fp
        self.output_fp = output_fp
        json_file = open(json_fp, 'w')
        json.dump(current_json_config, json_file, indent=4)
        json_file.close()

    def gather_report(self):
        self.take_screenshot()
        zip_file = ZipFile(zip_fp, 'w')
        zip_file.write(img_fp, op.basename(img_fp))
        zip_file.write(log_fp, op.basename(log_fp))
        zip_file.write(json_fp, op.basename(json_fp))
        if self.input_fp:
            zip_file.write(self.input_fp, op.basename(self.input_fp))
        if self.output_fp:
            zip_file.write(self.output_fp, op.basename(self.output_fp))
        zip_file.close()

    def delete_tmp_files(self):
        # os.remove(zip_fp)
        os.remove(img_fp)
        os.remove(json_fp)
    
    def take_screenshot(self):
        cap = tkcap.CAP(self.root)
        cap.capture(img_fp)

    def send_report(self):
        self.gather_report()
        self.email_report()
        self.delete_tmp_files()
    
    def email_report(self):
        pass
