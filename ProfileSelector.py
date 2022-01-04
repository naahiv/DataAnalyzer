from tkinter import *
from tkinter import simpledialog
from Misc import *

class ProfileSelector(Frame):
    def __init__(self, parent, get_meas_info, switch_to_prof):
        Frame.__init__(self, parent)

        self.get_meas_info = get_meas_info
        self.switch_to_prof = switch_to_prof

        self.pf_list = ProfileList.get_profile_list()
        self.profile_names = [pf.name for pf in self.pf_list.prof_list]

        self.current_state = StringVar(self)
        self.current_state.set(self.profile_names[0])
        self.chooser = OptionMenu(self, self.current_state, *self.profile_names, command=self.switch_profile)
        self.chooser.grid(row=0, column=0, padx=10)

        self.save_btn = Button(self, text='Save', command=self.save_clicked)
        self.save_btn.grid(row=0, column=1, padx=10)

        self.save_as_btn = Button(self, text='Save As', command=self.save_as_clicked)
        self.save_as_btn.grid(row=0, column=2, padx=10)

        self.rename_btn = Button(self, text='Rename', command=self.rename_clicked)
        self.rename_btn.grid(row=0, column=3, padx=10)

        self.delete_btn = Button(self, text='Delete', command=self.delete_clicked)
        self.delete_btn.grid(row=0, column=4, padx=10)

        self.set_buttons_state(False)

    def switch_profile(self, prof_name):
        if not prof_name == self.profile_names[0]:
            self.set_buttons_state(True)
        else:
            self.set_buttons_state(False)
        prof = self.pf_list.prof_list[self.profile_names.index(prof_name)]
        self.switch_to_prof(prof)

    def save_clicked(self):
        prof_index = self.profile_names.index(self.current_state.get())
        new_profile = self.get_meas_info()
        new_profile.name = self.current_state.get()
        self.pf_list.prof_list[prof_index] = new_profile
        self.pf_list.export_profile_list()

    def save_as_clicked(self):
        name = simpledialog.askstring(title='Save As', prompt=f'Enter a name for this profile')
        if name == '' or name in self.profile_names or name == '(empty)':
            self.save_as_clicked()
        else:
            new_profile = self.get_meas_info()
            new_profile.name = name
            self.pf_list.prof_list.append(new_profile)
            self.pf_list.export_profile_list()
            self.switch_profile(name)

    def rename_clicked(self):
        prof_index = self.profile_names.index(self.current_state.get())
        new_name = simpledialog.askstring(title="Rename", prompt=f'Enter a new name for {self.current_state.get()}')
        if new_name == '' or new_name in self.profile_names or new_name == '(empty)':
            self.rename_clicked()
        else:
            self.pf_list.prof_list[prof_index].name = new_name
            self.pf_list.export_profile_list()
            self.current_state.set(new_name)
            self.update_chooser()
    
    def set_buttons_state(self, enable):
        if enable:
            self.save_btn['state'] = 'normal'
            self.rename_btn['state'] = 'normal'
            self.delete_btn['state'] = 'normal'
        else:
            self.save_btn['state'] = 'disabled'
            self.rename_btn['state'] = 'disabled'
            self.delete_btn['state'] = 'disabled'

    def delete_clicked(self):
        prof_name = self.current_state.get()
        prev_name = self.profile_names[self.profile_names.index(prof_name) - 1]
        self.current_state.set(prev_name)
        self.switch_profile(prev_name)
        self.pf_list.prof_list.pop(self.profile_names.index(prof_name))
        self.pf_list.export_profile_list()
        self.update_chooser()

    def update_chooser(self):
        self.profile_names = [pf.name for pf in self.pf_list.prof_list]
        self.chooser.destroy()
        self.chooser = OptionMenu(self, self.current_state, *self.profile_names, command=self.switch_profile)
        self.chooser.grid(row=0, column=0, padx=10)

if __name__ == '__main__':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.geometry("900x600")
    ProfileSelector(root).grid(row=0, column=0)
    root.mainloop() 
