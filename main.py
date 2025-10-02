import atexit
import os

from profiles import DesktopProfile


profiles: dict[str:DesktopProfile] = {}


def save() -> None:
    print('exitting')


def load() -> None:
    pass


def set_profile(profile: DesktopProfile | None=None) -> None:
    if not profile:
        prompt_name: str = 'What is the [Name] of the [Profile]:\n'
        name: str = input(prompt_name)
        while name in profiles_keys:
            print(f'[{name}] is already taken.')
            name = input(prompt_name)
            
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
                    print('That file doesn\'nt exist')


        profiles[name] = DesktopProfile(name)
        profiles[name].profile_bng(path)
        profiles[name].profile_files(files)

        print

        return
    
    pass


def do_action(profile: DesktopProfile, action: str) -> None:
    match action:
        
        case '0':
            pass

        case '2':
            profile.set_bng()

        case '3':
            profile.hide_files()

        case '4':
            profile.unhide_files()
    print()


if __name__ == '__main__':
    atexit.register(save)


    all: list[str] = ['2', '3']
    choices = ['0', '1','2', '3', '4']


    while True:
        profiles_keys: list[str] = list(profiles.keys())


        select: str = ''
        while select not in profiles_keys and select != 'New':
            select = input('What profile would you like to choose? ' + ' '.join(profiles_keys) + ' | Type \'New\' for new profile.\n')

        print()

        if select == 'New':
            set_profile()

            continue


        profile: DesktopProfile = profiles[select]

        choice: str = ''
        if choice not in choices:
            choice = input('What would you like to do?\n\t1: All\n\t2: Set Background\n\t3: Hide Files\n\t4: Unhide Files\n\t0: Reconfigure\n')

        if choice == '1':
            for action in all:
                do_action(profile, action)
        else:
            do_action(profile, choice)