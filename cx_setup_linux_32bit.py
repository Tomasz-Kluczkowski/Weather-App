import cx_Freeze
import sys
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None
# base = "Console" # use for testing in deployed version

if sys.platform == "win32":
    base = "Win32GUI"

include_files = ["Resources/", "app_icon48x48.ico", "README_Linux_32bit.txt"]
includes = []
excludes = ["PyQt5"]
packages = ["tkinter", "idna", "multiprocessing", "PIL"]
executables = [cx_Freeze.Executable("weather_gui.py", base=base,
                                    icon="app_icon96x96.ico",
                                    targetName="Weather_App_32bit")]

cx_Freeze.setup(
    name='Weather App 32bit',
    version='1.0',
    description='Weather report application',
    author='Tomasz Kluczkowski',
    author_email='tomaszk1@hotmail.co.uk',
    options={'build_exe': {'includes': includes,
                           'excludes': excludes,
                           'packages': packages,
                           'include_files': include_files}},
    executables=executables)
