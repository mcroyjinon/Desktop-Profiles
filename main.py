import ctypes
import atexit

from profiles import DesktopProfile

profiles: dict[str:DesktopProfile] = {}

def save():
    print('exitting')

def load():
    pass

if __name__ == '__main__':
    atexit.register(save)

    while True:
        profiles_keys: list[str] = list(profiles.keys())
        select: str = ''
        while select not in profiles_keys and select != 'New':
            select = input('What profile would you like to choose? ' + ' '.join(profiles_keys) + ' | Type \'New\' for new profile.\n')
        
        if select == 'New':
            prompt_name: str = 'What is the [Name] of the [Profile]:\n'
            name: str = input(prompt_name)
            while name in profiles_keys:
                print(f'[{name}] is already taken.')
                name = input(prompt_name)
            
            path: str = input('What is the [Path] to the image?\n').replace('"', '')

            profiles[name] = DesktopProfile(name)
            profiles[name].profile_bng(path)

            continue

        profile: DesktopProfile = profiles[select]

        choice = ''
        choices = ['1']
        if choice not in choices:
            choice = input('What would you like to do?\n\t1: Set Background\n')
        
        match choice:
            case '1':
                profile.set_bng()
