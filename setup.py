#Build .exe -> cmd>> python setup.py build_exe
#Build .exe with installer -> cmd>> python setup.py bdist_msi(win)/bdist_dmg(mac)
import os, sys
from cx_Freeze import setup, Executable

os.environ["TCL_LIBRARY"] = os.path.join(sys.exec_prefix, "tcl", "tcl8.6")
os.environ["TK_LIBRARY"] = os.path.join(sys.exec_prefix, "tcl", "tk8.6")

setup(
    name="Reproc",
    version="1.0.0",
    description="Reproc",
    long_description="Reproc",
    long_description_content_type="text/markdown",

    url="https://github.com/JavideSs/Reproc",

    author="Javier Mellado Sánchez",
    author_email="javimelladoo@gmail.com",

    install_requires="requirements.txt",
    python_requires='>=3.7.4',

    executables = [Executable (
        script="reproc.py",
        target_name="Reproc",
        #icon=os.path.join("data", "images", "images_files", "CD" "IconExplorer.ico"),
        base="Win32GUI" if sys.platform == "win32" else None
    )],

    options = {"build_exe": {
        "optimize": 1,
        "include_msvcr": True,
        "packages": ["pygame", "PIL", "tinytag"],
        "includes": ["tkinter", "pygame", "PIL", "tinytag"],
        "excludes" : [],
        #"include_files": [
        #    os.path.join(sys.path[2], "tcl86t.dll"),
        #    os.path.join(sys.path[2], "tk86t.dll")
        #]
    }}
)