import cx_Freeze
import sys
import os.path
from version_hunter.versioner import Versioner

# Collect version file
v = Versioner()
version = v.get_version()
print(version)


# This is needed for Cx_Freeze to find path to tcl and tk libraries.
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None
# base = "Console" # use for testing in deployed version

data = "../weather_app/Data/"

if sys.platform == "win32":
    base = "Win32GUI"

include_files = [data,
                 data + "Icons/app_icon/app_icon48x48.ico",
                 os.path.join("../weather_app/Data/DLLs/64bit", 'tk86t.dll'),
                 os.path.join("../weather_app/Data/DLLs/64bit", 'tcl86t.dll'),
                 ]
includes = []
excludes = ["PyQt5"]
packages = ["tkinter", "idna"]
executables = [
    cx_Freeze.Executable("../weather_app/weather_gui.py", base=base,
                         icon=data + "Icons/app_icon/app_icon96x96.ico",
                         targetName="Weather_App_64bit.exe")]

cx_Freeze.setup(
    name='Weather_App_64bit',
    version=version,
    description='Weather report application',
    author='Tomasz Kluczkowski',
    author_email='tomaszk1@hotmail.co.uk',
    options={'build_exe': {'includes': includes,
                           'excludes': excludes,
                           'packages': packages,
                           'include_files': include_files}},
    executables=executables)
