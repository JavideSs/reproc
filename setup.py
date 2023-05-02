#Build>> python setup.py build_exe
from cx_Freeze import setup, Executable

import os
import sys
import shutil

#==================================================

PATHSTART = "." + os.sep

def exclude_files():
    print("running-> exclude_files()")

    for path, dirs, files in os.walk(PATHSTART):
        compiler_included_folders = (PATHSTART+"data", PATHSTART+"program", PATHSTART+"ui")
        if any(map(lambda folder: folder in path, compiler_included_folders)) and len(files):
            for file in files:
                if not file.endswith((".py", ".pyd", ".pyc")) and file not in ("IconExplorer.ico",):
                    home_path = path
                    temp_path = os.path.join(PATHSTART+"temp", home_path.replace(PATHSTART, ""))
                    file_home_path = os.path.join(home_path, file)
                    file_temp_path = os.path.join(temp_path, file)
                    os.makedirs(temp_path, exist_ok=True)
                    shutil.move(file_home_path, file_temp_path)


def return_excluded_files():
    print("running-> return_excluded_files()")

    shutil.copytree(PATHSTART+"temp", PATHSTART, dirs_exist_ok=True)
    shutil.rmtree(PATHSTART+"temp")


def include_data():
    print("running-> include_data()")

    def copy2ToBuildPath(path_build, pathto, file):
        build_pathto = os.path.join(path_build, *pathto)
        os.makedirs(build_pathto, exist_ok=True)
        shutil.copy2(os.path.join(*pathto, file), build_pathto)

    def copyTreeToBuildPath(path_build, pathto):
        shutil.copytree(os.path.join(*pathto), os.path.join(path_build, *pathto))

    path_build = sorted(os.scandir("build"), key=lambda x: x.stat().st_mtime)[-1].path

    pathto_data = ("data",)
    pathto_ui = ("ui",)
    pathto_docs = ("docs",)
    pathto_locale = (*pathto_data, "locale")
    pathto_themes = (*pathto_ui, "ttk_themes")
    pathto_images = (*pathto_ui, "images")
    pathto_images_b64 = (*pathto_images, "base64")
    pathto_images_file = (*pathto_images, "file")

    copyTreeToBuildPath(path_build, pathto_docs)
    copyTreeToBuildPath(path_build, pathto_locale)
    copyTreeToBuildPath(path_build, pathto_themes)
    copyTreeToBuildPath(path_build, pathto_images_file)

    copy2ToBuildPath(path_build, pathto_data, "user_config.json")
    copy2ToBuildPath(path_build, pathto_images_b64, "images.txt")

#==================================================

exclude_files()

setup(
    name="Reproc",
    version="1.0",
    description="Reproc - Local Music Player",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="reproc local music player multiplaylists",

    url="https://github.com/JavideSs/reproc",

    author="Javier Mellado Sánchez",
    author_email="javimelladoo@gmail.com",

    install_requires="requirements.txt",
    python_requires=">=3.6",

    executables = [Executable(
        script="reproc.py",
        target_name="Reproc",
        icon=os.path.join("ui", "images", "file", "icon", "IconExplorer.ico"),
        base="Win32GUI" if sys.platform == "win32" else None
    )],

    options = {"build_exe": {
        "optimize": 2,
        "include_msvcr": True
    }}
)

return_excluded_files()
include_data()