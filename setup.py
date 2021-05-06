#Build .exe -> cmd>> python setup.py build_exe
import os, sys, shutil
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

    executables=[Executable(
        script="reproc.py",
        icon=os.path.join("data", "images", "images_files", "icon.ico"),
        base="Win32GUI" if sys.platform == "win32" else None)],

    options = {"build_exe": {
        "packages": ["pygame", "PIL", "tinytag"],
        "includes": ["tkinter", "pygame", "PIL", "tinytag"],
        'include_msvcr': True
    }},
)

path = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
build_path = os.path.join(path, 'build', 'exe.win32-3.7')
shutil.copy(r'C:\Users\javim\AppData\Local\Programs\Python\Python37-32\DLLs\tcl86t.dll', build_path)
shutil.copy(r'C:\Users\javim\AppData\Local\Programs\Python\Python37-32\DLLs\tk86t.dll', build_path)