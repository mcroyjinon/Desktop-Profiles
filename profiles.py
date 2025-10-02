import ctypes
import pyvda

class DesktopProfile:
    
    def __init__(self, name: str) -> None:
        self.Name: str = name
        self.bng_path: str = ''
        self.files_path: list[str] = []
        self.quick_run_methods: list[function] = [self.change_background]

    def __repr__(self) -> str:
        info: dict = {
            "Name": self.Name,
            "bng_path": self.bng_path,
            "files_path": self.files_path
        }
        return info
    
    # Getter Methods
    def get_files_path(self) -> list[str]:
        return self.files_path
    
    # Setter Methods
    def profile_bng(self, image_path: str) -> None:
        self.bng_path = image_path

    def profile_files_path(self, files_path: list[str]) -> None:
        self.files_path = files_path

    def profile_name(self, name: str) -> None:
        self.Name = name

    def profile_quick_run_methods(self, methods: list) -> None:
        self.quick_run_methods = methods

    # Functionality
    def quick_run(self):
        for func in self.quick_run_methods:
            func()

    def change_background(self) -> None:
        if self.bng_path:
            current_desktop: int = pyvda.VirtualDesktop.current().number

            for i in range(1,len(pyvda.get_virtual_desktops())+1):
                pyvda.VirtualDesktop(i).go()
                ctypes.windll.user32.SystemParametersInfoW(20, 0, self.bng_path, 0x01 | 0x02)
            
            pyvda.VirtualDesktop(current_desktop).go()

    def hide_files(self) -> None:
        for file_path in self.files_path:
            FILE_ATTRIBUTE_HIDDEN: any = 0x02
            ret: any = ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)
            if ret:
                print(f"{file_path} is now hidden.")
            else:
                print("Failed to hide the file.")
    
    def unhide_files(self) -> None:
        for file_path in self.files_path:

            FILE_ATTRIBUTE_HIDDEN = 0x02
            attrs: any = ctypes.windll.kernel32.GetFileAttributesW(file_path)
            if attrs == -1:
                print("Failed to get file attributes")
                return
            
            new_attrs = attrs & ~FILE_ATTRIBUTE_HIDDEN
            ctypes.windll.kernel32.SetFileAttributesW(file_path, new_attrs)
            print(f"File is now unhidden: {file_path}")