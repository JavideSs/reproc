#Build>> python setup.py build_exe
from cx_Freeze import setup, Executable

import os, sys, shutil, pkgutil

#==================================================

modules_basics = ("collections", "encodings", "importlib")
modules_imported = ("tkinter", "PIL", "tinytag", "pygame")
modules_required = ("logging", "urllib", "json", "ctypes")
modules_own = ("program", "data", "ui")

python_modules_included =  modules_basics + modules_imported + modules_required + modules_own
python_modules_excluded = {i.name for i in pkgutil.iter_modules() if i.ispkg} - set(python_modules_included)


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

    if sys.version_info < (3, 8):
        def copytree(src, dst, symlinks=False, ignore=None):
            if not os.path.exists(dst):
                os.makedirs(dst)

            # Copiamos los archivos
            for i in os.listdir(src):
                s = os.path.join(src, i)
                d = os.path.join(dst, i)
                if os.path.isdir(s):
                    copytree(s, d, symlinks, ignore)
                else:
                    if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                        shutil.copy2(s, d)

        copytree(PATHSTART+"temp", PATHSTART)

    else:
        shutil.copytree(PATHSTART+"temp", PATHSTART, dirs_exist_ok=True)
    shutil.rmtree(PATHSTART+"temp")


current_build_path = lambda: next((i.path for i in sorted(os.scandir("build"), key=lambda x: x.stat().st_mtime, reverse=True) if i.is_dir()), None)

def include_data():
    print("running-> include_data()")

    def copy2ToBuildPath(path_build, pathto, file):
        build_pathto = os.path.join(path_build, *pathto)
        os.makedirs(build_pathto, exist_ok=True)
        shutil.copy2(os.path.join(*pathto, file), build_pathto)

    def copyTreeToBuildPath(path_build, pathto):
        shutil.copytree(os.path.join(*pathto), os.path.join(path_build, *pathto))

    path_build = current_build_path()

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

def dirty_cleaning():
    print("running-> dirty_cleaning()")

    path_build = current_build_path()

    module_path_pygame = os.path.join(path_build, "lib", "pygame")
    for i in os.scandir(module_path_pygame):
        if i.is_dir():
            print(i)
            shutil.rmtree(i)


#==================================================

try:
    exclude_files()

    setup(
        name= "Reproc",
        version= "1.0",
        description= "Reproc - Local Music Player",
        keywords= "reproc local music player multiplaylists",
        author= "Javier Mellado Sánchez",
        author_email= "javimelladoo@gmail.com",
        long_description= open("README.md").read(),
        long_description_content_type= "text/markdown",
        url= "https://github.com/JavideSs/reproc",
        license= open("LICENSE").read(),

        python_requires= ">=3.6",
        install_requires= open("requirements.txt").readlines(),

        executables = [Executable(
            script="reproc.py",
            target_name="Reproc",
            icon=os.path.join("ui", "images", "file", "icon", "IconExplorer.ico"),
            base="Win32GUI" if sys.platform == "win32" else None
        )],

        options = {"build_exe": {
            "optimize": 2,
            "include_msvcr": True,
            "includes": python_modules_included,
            "excludes": python_modules_excluded
        }}
    )

    return_excluded_files()

    include_data()

    dirty_cleaning()

except Exception as e:
    print("=====!!!Error!!!=====\n", e)
    return_excluded_files()