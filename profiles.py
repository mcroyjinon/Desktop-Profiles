import ctypes

class DesktopProfile:
    
    def __init__(self, name: str) -> None:
        self.Name: str = name
        self.bng_path: str = ''
        self.files_path: list[str] = []

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

    # Functionality
    def change_background(self) -> None:
        if self.bng_path:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, self.bng_path, 0)

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