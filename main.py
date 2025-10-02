import atexit
import os
import json
import pyvda

from profiles import DesktopProfile


profiles: dict[str:DesktopProfile] = {}


def save() -> None:
    profiles_json = {}
    for name, profile in profiles.items():
        profiles_json[name] = profile.__repr__()
    with open('saves.json', 'w') as file:
        json.dump(profiles_json, file)


def load() -> None:
    profiles_json: dict
    with open('saves.json', 'r') as file:
        profiles_json = json.load(file)
    
    for name, profile in profiles_json.items():
        profiles[name] = DesktopProfile(name)
        profiles[name].profile_bng(profile['bng_path'])
        profiles[name].profile_files_path(profile['files_path'])
        

def set_profile(profile: DesktopProfile | None = None) -> None:
    if not profile:
        prompt_name: str = 'What is the [Name] of the [Profile]:\n'
        name: str = input(prompt_name)
        while name in profiles_keys:
            print(f'[{name}] is already taken.')
            name = input(prompt_name)

        profiles[name] = DesktopProfile(name)
            
        path: str = input('What is the [Path] to the background image? Enter for none\n').replace('"', '')
        while not os.path.exists(path):
            if not path: break
            print('That is not a valid path')
            path: str = input('What is the [Path] to the background image? Enter for none\n').replace('"', '')

        files: list[str] = []
        files_bool: str = input('Would you like to add file paths to hide? Y/n\n').lower()
        if files_bool == 'y':
            file: str = ''
            while file != 'stop':
                file = input('What file path do you want to add? \'stop\' to stop adding files\n').replace('"','')
                if os.path.exists(file):
                    files.append(file)
                elif file != 'stop':
                    print('That file doesn\'t exist')

        
        methods: list = []

        auto_bng: str = input('Would you like to change background on activation? Y/n\n').lower()
        if auto_bng == 'y':
            methods.append(profiles[name].change_background)

        auto_hide: str = input('Would you like to hide files on activation? Y/n\n').lower()
        if auto_hide == 'y':
            methods.append(profiles[name].hide_files)
        else:
            methods.append(profiles[name].unhide_files)    

        profiles[name].profile_bng(path)
        profiles[name].profile_files_path(files)
        profiles[name].profile_quick_run_methods(methods)

        print()

        return
    
    choices = ['1', '2', '3', '4', '5']
    choice: str = ''
    while choice != 'stop':
        choice = input('What would you like to do:\n\t1. Rename Profile\n\t2. Change Background File\n\t3. Add File Paths to Hide\n\t4. Remove File Paths to Hide\n\t5. Change Defaults\n\tStop\n').lower()
        
        match choice:
            
            case '1':
                prompt_name: str = 'What is the [Name] of the [Profile]:\n'
                name: str = input(prompt_name)
                while name in profiles_keys:
                    print(f'[{name}] is already taken.')
                    name = input(prompt_name)
                
                profiles.pop(profile.Name)
                profile.profile_name(name)
                profiles[name] = profile

            case '2':
                path: str = input('What is the [Path] to the background image? Enter for none\n').replace('"', '')
                while not os.path.exists(path):
                    if not path: break
                    print('That is not a valid path')
                    path: str = input('What is the [Path] to the background image? Enter for none\n').replace('"', '')
                
                profile.profile_bng(path)

            case '3':
                files: list[str] = profile.get_files_path()
                file: str = ''
                while file != 'stop':
                    file = input('What file path do you want to add? \'stop\' to stop adding files\n').replace('"','').lower()
                    
                    if file == 'stop':
                        break

                    if os.path.exists(file):
                        files.append(file)
                    elif file != 'stop':
                        print('That file doesn\'t exist')
                                        
                profile.profile_files_path(files)

            case '4':
                file: str = ''
                while file != 'stop':
                    files: list[str] = profile.get_files_path()
                    prompt = 'What would you like to remove? \'Stop\' to stop\n'
                    for i, file in enumerate(files):
                        prompt += '\t' + str(i) + '. ' + file + '\n'
                    file = input(prompt).lower()

                    if file == 'stop':
                        break

                    if int(file) in range(len(files)):
                        files.pop(int(file))

            case '5':
                auto_bng: str = input('Would you like to change background on activation? Y/n\n').lower()
                if auto_bng == 'y':
                    methods.append(profiles[name].change_background)

                auto_hide: str = input('Would you like to hide files on activation? Y/n\n').lower()
                if auto_hide == 'y':
                    methods.append(profiles[name].hide_files)
                else:
                    methods.append(profiles[name].unhide_files)

                profiles[name].profile_quick_run_methods(methods)

            
        print()


def do_action(profile: DesktopProfile, action: str) -> None:
    match action:
        
        case '-1':
            profiles.pop(profile.Name)

        case '1':
            profile.quick_run()

        case '0':
            print()
            set_profile(profile)

        case '2':
            profile.change_background()

        case '3':
            profile.hide_files()

        case '4':
            profile.unhide_files()
    print()


if __name__ == '__main__':
    load()
    atexit.register(save)

    choices = ['-1','0', '1','2', '3', '4']

    while True:
        profiles_keys: list[str] = list(profiles.keys())


        select: str = ''
        while select not in profiles_keys and select != 'New':
            select = input('What profile would you like to choose? ' + ', '.join(profiles_keys) + ' | Type \'New\' for new profile.\n')

        print()

        if select == 'New':
            set_profile()

            continue


        profile: DesktopProfile = profiles[select]

        choice: str = ''
        if choice not in choices:
            choice = input('What would you like to do?\n\t1: All\n\t2: Set Background\n\t3: Hide Files\n\t4: Unhide Files\n\t0: Reconfigure\n\t-1: Delete Profile\n')

        do_action(profile, choice)