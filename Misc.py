import json
import os.path as op

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
        if direct_init:
            self.name = direct_init['name']
            self.crits = direct_init['crits']
            self.ee_dict = direct_init['ee']
            self.daysToPull = direct_init['dtp']
        else:
            self.name = prof_dict['name']
            self.daysToPull = prof_dict['daysToPull']
            self.crits = [VisualCriteria(None, crit_dict) for crit_dict in prof_dict['criteria']]
            self.ee_dict = None
            if 'entry_exit' in prof_dict:
                self.ee_dict = prof_dict['entry_exit']

    def export_to_dict(self):
        prof_dict = {}
        prof_dict['name'] = self.name
        prof_dict['daysToPull'] = self.daysToPull
        if self.ee_dict:
            prof_dict['entry_exit'] = self.ee_dict
        prof_dict["criteria"] = [crit.export_to_dict() for crit in self.crits]
        return prof_dict

home = op.expanduser('~')
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
