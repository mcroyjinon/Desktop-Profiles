import ctypes

class DesktopProfile:
    
    def __init__(self, name: str):
        self.Name: str = name
    
    def profile_bng(self, image_path: str):
        self.bng_path: str = image_path

    def set_bng(self):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, self.bng_path, 0)