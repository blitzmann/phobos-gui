import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "reverence"],
    "includes": ["ConfigParser"],
    "excludes": ["tkinter"],
    "include_files": "Phobos.zip"
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Phobos-GUI",
        version = "0.2",
        description = "GUI frontend for Phobos",
        options = {"build_exe": build_exe_options},
        executables = [Executable("phb_gui.py", base=base)])
