from profiles import DesktopProfile
import customtkinter as CTk
from tkinter import filedialog
import atexit
import os
import json


class RemoveDir(CTk.CTk):

    def remove_dir(self, index: int):
        self.app.information['Directory'].pop(index)
        self.app.stores['Directory'].configure(state='normal')
        self.app.stores['Directory'].delete('0.0','end')
        self.app.stores['Directory'].insert('0.0', ', '.join(self.app.information['Directory']))
        self.app.stores['Directory'].configure(state='disabled')
        self.create_removal()

    def create_removal(self):
        for widget in self.winfo_children():
            widget.destroy()

        for i, dir in enumerate(self.app.information['Directory']):
            label_name: CTk.CTkLabel = CTk.CTkLabel(
                master=self,
                text=dir
            )
            label_name.grid(row=i, column=0)

            button_remove: CTk.CTkButton = CTk.CTkButton(
                master=self,
                text='Remove',
                command=lambda: self.remove_dir(i)
            )
            button_remove.grid(row=i, column=1)

    def __init__(self, app: CTk.CTk):
        super().__init__()

        self.geometry('300x300')
        self.resizable(False, False)
        self.title('Remove Directory')

        self.grid_columnconfigure((0),weight=3)
        self.grid_columnconfigure((1),weight=1)

        self.protocol('WM_DELETE_WINDOW', lambda: self.withdraw())

        self.app: CTk.CTk = app

        self.create_removal()

        self.mainloop()

class NewProfileApp(CTk.CTk):

    def create_profile(self):
        profile: DesktopProfile = DesktopProfile(name=self.var_name.get())

        file_paths = self.information.get('Files') + self.information.get('Directory')

        profile.profile_bng(self.information.get('Wallpaper'))
        profile.profile_files_path(file_paths)

        profile.profile_quick_run_methods([profile.change_background, profile.hide_files])

        self.app.add_profile(profile)

        self.withdraw()

    def file_selector(self, selector: str, info_store: str):
        files: tuple[str] | str
        if selector == 'file':
            files = filedialog.askopenfilename(
                title='Select File(s)',
                filetypes=(("All files", "*.*"),("All files", "*.*"))
            )
            self.information[info_store] = files
        elif selector == 'files':
            files = filedialog.askopenfilenames(
                title='Select File',
                filetypes=(("All files", "*.*"),("All files", "*.*"))
            )
            self.information[info_store] = list(files)
        elif selector == 'directories':
            files = filedialog.askdirectory(
                title='Select Directory(s)',
                mustexist=True
            )
            self.information[info_store].append(files)
            files = ', '.join(self.information[info_store])
        
        self.stores[info_store].configure(state='normal')
        self.stores[info_store].delete('0.0','end')
        self.stores[info_store].insert('0.0',files)
        self.stores[info_store].configure(state='disabled')
        self.focus_force()

    def __init__(self, app: CTk.CTk) -> None:
        super().__init__()

        self.geometry('500x350')
        self.resizable(True, False)
        self.title('New Profile')
        self.grid_columnconfigure((0),weight=1)
        self.grid_columnconfigure((1,2,3),weight=2)
        self.grid_rowconfigure((10),weight=5)

        self.protocol('WM_DELETE_WINDOW',lambda: self.withdraw())

        self.information: dict[str: str] = {}
        self.stores: dict[str: any] = {}
        self.app = app

        #Name Entry
        label_name: CTk.CTkLabel = CTk.CTkLabel(
            master=self,
            text='Name'
        )
        label_name.grid(row=0, column=0, pady=5, padx=5, sticky='e')

        self.var_name: CTk.StringVar = CTk.StringVar(self)
        entry: CTk.CTkEntry = CTk.CTkEntry(
            master=self,
            placeholder_text='Enter Name Here',
            textvariable=self.var_name
        )
        entry.grid(row=0, column=1, pady=2, padx=5, sticky='ew', columnspan=3)

        #Wallpaper Entry
        label_wallpaper: CTk.CTkLabel = CTk.CTkLabel(
            master=self,
            text='Wallpaper'
        )
        label_wallpaper.grid(row=1, column=0, pady=5, padx=5, sticky='e')

        self.information['Wallpaper'] = ''
        button_wallpaper: CTk.CTkButton = CTk.CTkButton(
            master=self,
            text='Choose File',
            command=lambda: self.file_selector('file', 'Wallpaper')
        )
        button_wallpaper.grid(row=1, column=1, pady=2, padx=5, sticky='ew')

        self.stores['Wallpaper'] = CTk.CTkTextbox(
            master=self,
            font=('CTkFont', 10),
            height=40,
            state='disabled'
        )
        self.stores['Wallpaper'].grid(row=1, column=2, pady=2, columnspan=2, sticky='ew')

        #Hidden Files Entry
        label_files: CTk.CTkLabel = CTk.CTkLabel(
            master=self,
            text='Hidden Files'
        )
        label_files.grid(row=2, column=0, pady=5, padx=5, sticky='e')

        self.information['Files'] = []
        button_files: CTk.CTkButton = CTk.CTkButton(
            master=self,
            text='Choose File(s)',
            command=lambda: self.file_selector('files', 'Files')
        )
        button_files.grid(row=2, column=1, pady=2, padx=5, sticky='ew')

        self.stores['Files'] = CTk.CTkTextbox(
            master=self,
            font=('CTkFont', 10),
            height=75,
            state='disabled'
        )
        self.stores['Files'].grid(row=2, column=2, pady=2, columnspan=2, sticky='ew')

        #Hidden Directories Entry
        label_directories: CTk.CTkLabel = CTk.CTkLabel(
            master=self,
            text='Hidden Dir(s)'
        )
        label_directories.grid(row=3, column=0, pady=5, padx=5, sticky='e')

        self.information['Directory'] = []
        button_directories: CTk.CTkButton = CTk.CTkButton(
            master=self,
            text='Add Dir',
            command=lambda: self.file_selector('directories', 'Directory')
        )
        button_directories.grid(row=3, column=1, pady=2, padx=5, sticky='ew')

        button_directories_remove: CTk.CTkButton = CTk.CTkButton(
            master=self,
            text='Remove Dir(s)',
            command=lambda: RemoveDir(self)
        )
        button_directories_remove.grid(row=3, column=2, sticky='ew', padx=2)

        self.stores['Directory'] = CTk.CTkTextbox(
            master=self,
            font=('CTkFont', 10),
            height=75,
            state='disabled'
        )
        self.stores['Directory'].grid(row=3, column=3, pady=2, padx=2, sticky='ew')

        #Create Profile Button
        self.button_create: CTk.CTkButton = CTk.CTkButton(
            master=self,
            text='Create Profile',
            command=self.create_profile
        )
        self.button_create.grid(row=10, column=0, sticky='ew', columnspan=4, padx=20)


class EditProfileApp(NewProfileApp):

    def __init__(self, app):
        super().__init__(app)

        self.title('Reconfigure Profile: '+app.current_profile.Name)

        self.app = app

        self.var_name.set(app.current_profile.Name)
        self.information['Wallpaper'] = app.current_profile.get_bng_path()
        
        for file_path in app.current_profile.get_files_path():
            if os.path.isfile(file_path):
                self.information['Files'].append(file_path)
            elif os.path.isdir(file_path):
                self.information['Directory'].append(file_path)
        
        self.stores['Wallpaper'].configure(state='normal')
        self.stores['Wallpaper'].delete('0.0','end')
        self.stores['Wallpaper'].insert('0.0',self.information['Wallpaper'])
        self.stores['Wallpaper'].configure(state='disabled')

        self.stores['Files'].configure(state='normal')
        self.stores['Files'].delete('0.0','end')
        self.stores['Files'].insert('0.0',self.information['Files'])
        self.stores['Files'].configure(state='disabled')

        self.stores['Directory'].configure(state='normal')
        self.stores['Directory'].delete('0.0','end')
        self.stores['Directory'].insert('0.0',self.information['Directory'])
        self.stores['Directory'].configure(state='disabled')

        self.button_create.configure(command=self.update_profile, text='Update Profile: '+app.current_profile.Name)

        self.mainloop()

    
    def update_profile(self):
        file_paths = self.information.get('Files') + self.information.get('Directory')

        self.app.current_profile.profile_bng(self.information.get('Wallpaper'))
        self.app.current_profile.profile_files_path(file_paths)

        self.withdraw()


class DesktopApp(CTk.CTk):

    def add_profile(self, profile: DesktopProfile):
        self.desktop_profiles[profile.Name] = profile
        self.options_profiles.configure(values=list(self.desktop_profiles.keys()) + ['New'])
    
    def __init__(self) -> None:
        super().__init__()

        self.geometry('325x325')
        self.resizable(False,False)
        self.title('Desktop Profiles')
        self.protocol('WM_DELETE_WINDOW',exit)


        #Object Variables
        self.desktop_profiles: dict[str: DesktopProfile] = {'None': None}
        self.current_profile: DesktopProfile | None = None

        #Load Saves
        profiles_json: dict
        with open('saves.json', 'r') as file:
            profiles_json = json.load(file)
    
        for name, profile in profiles_json.items():
            self.desktop_profiles[name] = DesktopProfile(name)
            self.desktop_profiles[name].profile_bng(profile['bng_path'])
            self.desktop_profiles[name].profile_files_path(profile['files_path'])

        #Save Function
        def save() -> None:
            profiles_json = {}
            for name, profile in self.desktop_profiles.items():
                if name == 'None': continue
                profiles_json[name] = profile.__repr__()
            with open('saves.json', 'w') as file:
                json.dump(profiles_json, file)
        atexit.register(save) 

        #Profile Selector
        self.frame_profiles: CTk.CTkFrame = CTk.CTkFrame(
            master=self,
            bg_color='transparent'
        )
        self.frame_profiles.pack(side='top', fill='x')

        self.options_profiles: CTk.CTkOptionMenu = CTk.CTkOptionMenu(
            master=self.frame_profiles,
            bg_color='transparent',
            fg_color='gray77',
            corner_radius=0,
            text_color='black',
            button_color='gray60',
            button_hover_color='gray30',
            command=self.options_chosen,
            values=list(self.desktop_profiles.keys()) + ['New']
        )
        self.options_profiles.pack(fill='x')

        #Buttons
        self.frame_app: CTk.CTkFrame = CTk.CTkFrame(
            master=self,
            bg_color='transparent',
            fg_color='gray92'
        )
        self.frame_app.grid_columnconfigure((0,1),weight=1)
        self.frame_app.grid_rowconfigure((0), weight=2)
        self.frame_app.grid_rowconfigure((1), weight=1)
        self.frame_app.pack(fill='both', expand=True)

        self.button_background: CTk.CTkButton = CTk.CTkButton(
            self.frame_app,
            text='Set Background',
            command=lambda: self.current_profile.change_background() if self.current_profile else print()
        )
        self.button_background.grid(row=0, column=0, sticky='ns', pady=10)

        self.button_quick: CTk.CTkButton = CTk.CTkButton(
            self.frame_app,
            text='Quick Activate',
            command=lambda: self.current_profile.quick_run() if self.current_profile else print()
        )
        self.button_quick.grid(row=0, column=1, sticky='ns', pady=10)

        self.frame_hide: CTk.CTkFrame = CTk.CTkFrame(
            master=self.frame_app,
            bg_color='transparent',
            fg_color='gray92',
            height=0,
            width=0
        )
        self.frame_hide.grid_columnconfigure((0,1),weight=1)
        self.frame_hide.grid_rowconfigure((0,1),weight=1)
        self.frame_hide.grid(row=1, column=0, sticky='ns', pady=10)

        self.button_hide: CTk.CTkButton = CTk.CTkButton(
            self.frame_hide,
            text='Hide Files',
            command=lambda: self.current_profile.hide_files() if self.current_profile else print()
        )
        self.button_hide.grid(row=0, column=0, sticky='ns', pady=5)

        self.button_unhide: CTk.CTkButton = CTk.CTkButton(
            self.frame_hide,
            text='Unhide Files',
            command=lambda: self.current_profile.unhide_files() if self.current_profile else print()
        )
        self.button_unhide.grid(row=1, column=0, sticky='ns', pady=5)
        

        self.button_reconfigure: CTk.CTkButton = CTk.CTkButton(
            self.frame_app,
            text='Reconfigure',
            command=lambda: EditProfileApp(self) if self.current_profile else print()
        )
        self.button_reconfigure.grid(row=1, column=1, sticky='ns', pady=10)


        self.mainloop()
    
    def options_chosen(self, option: str):
        if option == 'New':
            self.options_profiles.set('None')

            NewProfileApp(self).mainloop()
        else:
            self.current_profile = self.desktop_profiles[option]
            print(self.current_profile.__repr__())


if __name__ == '__main__':
    
    DesktopApp()