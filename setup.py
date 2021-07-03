#Build>> python setup.py build_exe
import os, sys, shutil
from cx_Freeze import setup, Executable

with open("README.md", "r") as readme_f:
    readme = readme_f.read()

icon_path = os.path.join("data", "images", "images_files", "CD", "IconExplorer.ico")

setup(
    name="Reproc",
    version="1.0.0",
    description="Reproc - Local Music Player",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="reproc local music player multiplaylists python tkinter tcl pygame.mixer tinytag",

    url="https://github.com/JavideSs/reproc",

    author="Javier Mellado Sánchez",
    author_email="javimelladoo@gmail.com",

    install_requires="requirements.txt",
    python_requires='>=3.7.4',

    executables = [Executable (
        script="reproc.py",
        target_name="Reproc",
        icon=icon_path,
        base="Win32GUI" if sys.platform == "win32" else None
    )],

    options = {"build_exe": {
        "optimize": 1,
        "include_msvcr": True,
        #"packages": [],
        #"includes": [],
        #"excludes" : [],
    }}
)

#Copy data and themes
with os.scandir("build") as it:
    for build in it:
        path_themes = os.path.join(build.path, "customTk", "ttk_themes")
        path_data = os.path.join(build.path, "data")
        path_locale = os.path.join(path_data, "locale")

        shutil.copytree(os.path.join("customTk", "ttk_themes"), path_themes)
        shutil.copytree(os.path.join("data", "locale"), path_locale)
        shutil.copy2(os.path.join("data", "user_config.json"), path_data)