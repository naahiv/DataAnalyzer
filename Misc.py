import json
import os.path as op
import os
import sys
import io
home = op.expanduser('~')
log_fp = op.join(home, 'da_output.log')
LOG_KB_LIMIT = 512
LOG_KB_PUSHBACK = 128

import pandas as pd

def line_filter(s, ec='\n'):
    if not s == ec:
        return '\n'.join(filter(''.__ne__, s.split(ec))).replace('#', '')
    else:
        return ''

class CustomIO(io.StringIO):
    def __init__(self):
        io.StringIO.__init__(self)
        self.check_for_clear()
        self.logfile = open(log_fp, 'a')

    def fix_changes(self):
        self.logfile.close()
        self.logfile = open(log_fp, 'a')

    def check_for_clear(self):
        if op.getsize(log_fp) >= 1000*LOG_KB_LIMIT:
            with open(log_fp, 'wb') as logfile:
                # TEMPORARY PATCH
                try:
                    logfile.write(logfile.read()[1000*LOG_KB_PUSHBACK:])
                except:
                    print('something weird...!')

    def write(self, s):
        io.StringIO.write(self, s)
        self.logfile.write(line_filter(self.getvalue(), '\x00'))
        self.truncate(0)
        self.fix_changes()

    def close(self):
        if not self.logfile.closed:
            self.logfile.close()
        io.StringIO.close(self)

iostream = CustomIO()

def begin_output_log():
    sys.stdout = iostream
    sys.stderr = iostream

def open_log_file():
    iostream.fix_changes()
    os.startfile(log_fp)

def revert_to_print_log():
    iostream.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

begin_output_log()
if sys.argv[0] == 'App.py':
    revert_to_print_log()

import pdb
import threading

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

class AnalysisSummary:
    """
    A class for organizing data for formatting it into an analysis summary csv file for the user. This is interacted with by clicking "Open Summary" or "Open Both" upon running completion.
    """
    def __init__(self, **kwargs):
        self.sum_block = kwargs['sum_block'] # i.e. ("eric's new profile", -0.37, 2.48)
        self.anal_block = kwargs['anal_block'] # i.e. [1, '9:31', 1, '9:39']
        self.crit_block = kwargs['crit_block'] # i.e. [visual_crit_1, visual_crit_2, ...]
        self.data_block = kwargs['data_block'] # i.e. [250, ('7/7/2021', 'decliners_jul_7.xslx), (...), ...]

        op = kwargs['out_path']
        self.out_path = os.path.join(os.path.dirname(op), 'summary_' + os.path.basename(op))

    def print_summary(self):
        df = self.setup_summary_array()
        df.to_csv(self.out_path, index=False)
        os.startfile(self.out_path)

    def setup_summary_array(self):
        block1 = [['Profile', 'Avg. Success Rate', 'Standard Deviation'],
                  self.sum_block]
        block2 = [['Analysis:'],
                  [f'Buy on Day {self.anal_block[0]}', f'at {self.anal_block[1]}', f'Sell on Day {self.anal_block[2]}', f'at {self.anal_block[3]}']]
        crit_arr = AnalysisSummary.arrayize(self.crit_block)
        block3 = [['Critera Selection']] + crit_arr

        block4 = [['Test Data', f'{self.data_block[0]} datapoints'],
                  ['Date', 'Filename']] + self.data_block[1:]
        emp = [[],[]]
        # pdb.set_trace()
        return pd.DataFrame(block1+emp+block2+emp+block3+emp+block4)

    def arrayize(crits):
        out = []
        for crit in crits:
            if crit.type == 0:
                out.append(['Price', f'on Day {crit.day1}', f'at {crit.time1}', crit.comp, f'on Day {crit.day2}', f'at {crit.time2}', f'by {crit.by_perc}'])
            elif crit.type == 1:
                out.append(['Input Value', f'{crit.input_field}', crit.comp, f'on Day {crit.value}'])
            else: # or clause...?
                out.append(['OR Clause'])
        return out
        


class VisualCriteria:
    """
    An interim class for holding & organizing information before being passed to 
    a 'logical criteria' object (that is part of the td_data_collector package)
    """
    def __init__(self, list_crit, sd=None):
        if sd == None:
            self.type = 0
            if list_crit[0] == 'input':
                self.type = 1
            if self.type == 0:
                self.day1 = list_crit[1]
                self.time1 = list_crit[2]
                self.comp = list_crit[3][1]
                self.day2 = list_crit[4]
                self.time2 = list_crit[5]
                self.by_perc = None
                if not list_crit[6] == "":
                    self.by_perc = float(list_crit[6])
            elif self.type == 1:
                self.input_field = list_crit[1]
                self.comp = list_crit[2][1]
                self.value = list_crit[3]
        else:
            if sd['type'] == 0:
                self.type = 0
                self.day1 = sd['day1']
                self.time1 = sd['time1']
                self.comp = sd['comp']
                self.day2 = sd['day2']
                self.time2 = sd['time2']
                self.by_perc = None
                if 'by_perc' in sd:
                    self.by_perc = float(sd['by_perc'])
            else:
                self.type = 1
                self.input_field = sd['input_field']
                self.comp = sd['comp']
                self.value = sd['value']

    def export_to_dict(self):
        dct = {}
        if self.type == 0:
            dct['type'] = 0
            dct['day1'] = self.day1
            dct['time1'] = self.time1
            dct['comp'] = self.comp
            dct['day2'] = self.day2
            dct['time2'] = self.time2
            if self.by_perc:
                dct['by_perc'] = self.by_perc

        else:
            dct['type'] = 1
            dct['comp'] = self.comp
            dct['input_field'] = self.input_field
            dct['value'] = self.value
        return dct

class VisualOptions:
    """
    An interim class for storing the options selected before td_data_collector use
    """
    def __init__(self, infoList):
        self.daysToPull = infoList[0]
        self.dayOneDate = f'{infoList[1]}/{infoList[2]}/{infoList[3]}'

class Profile:
    def __init__(self, prof_dict, direct_init=None):
        self.order_data = None
        if direct_init:
            self.name = direct_init['name']
            self.crits = direct_init['crits']
            self.ee_dict = direct_init['ee']
            self.daysToPull = direct_init['dtp']
        else:
            self.crits = []
            self.name = prof_dict['name']
            self.daysToPull = prof_dict['daysToPull']
            for crit_dict in prof_dict['criteria']:
                if type(crit_dict) == list:
                    self.crits.append([VisualCriteria(None, inner_crit_dict) for inner_crit_dict in crit_dict])
                else:
                    self.crits.append(VisualCriteria(None, crit_dict))
            self.ee_dict = None
            if 'entry_exit' in prof_dict:
                self.ee_dict = prof_dict['entry_exit']
            if 'order_data' in prof_dict:
                self.order_data = prof_dict['order_data']

    def export_to_dict(self):
        prof_dict = {}
        prof_dict['name'] = self.name
        prof_dict['daysToPull'] = self.daysToPull
        if self.ee_dict:
            prof_dict['entry_exit'] = self.ee_dict
        prof_dict['criteria'] = []
        for crit in self.crits:
            if type(crit) == list: # or clause
                prof_dict['criteria'].append([inner_crit.export_to_dict() for inner_crit in crit])
            else:
                prof_dict['criteria'].append(crit.export_to_dict())
        if not self.order_data == None:
            prof_dict['order_data'] = self.order_data
        return prof_dict

fp = op.join(home, 'profiles.json')

class ProfileList:
    def __init__(self, json_arr):
        self.prof_list = [Profile(prof_dict) for prof_dict in json_arr]

    def get_profile_list():
        try:
            json_file = open(fp, 'r')
            json_arr = json.load(json_file)
            return ProfileList(json_arr)
        except FileNotFoundError:
            print('creating local profiles.json file')
            src = open('profiles.json', 'r')
            dest = open(fp, 'w')
            dest.write(src.read())
            src.close()
            dest.close()
            return ProfileList.get_profile_list()

    def export_profile_list(self):
        dArray = [prof.export_to_dict() for prof in self.prof_list]
        json_file = open(fp, 'w')
        json.dump(dArray, json_file, indent = 4)

if __name__ == '__main__':
    revert_to_print_log()
