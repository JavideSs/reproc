from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageColor, ImageEnhance

from io import BytesIO
import base64

if __name__ != "__main__":
    from data.data_types import *
else:
    from tkinter import PhotoImage as TkImage
    from PIL.Image import Image as PILImage

#==================================================

def fileTob64(img_path:str) -> str:
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def fileToPIL(img_file:str) -> PILImage:
    return Image.open(img_file)


def b64ToPIL(img_b64:str) -> PILImage:
    return Image.open(BytesIO(base64.b64decode(img_b64)))


def fileToTk(img_file:str) -> TkImage:
    return PhotoImage(file=img_file)


def b64ToTk(img_b64:str) -> TkImage:
    return PhotoImage(data=img_b64)


def PILToTk(img_pil:PILImage) -> ImageTk.PhotoImage:
    return ImageTk.PhotoImage(img_pil)


def TkSolid(size:Tuple[int,int], color:str) -> ImageTk.PhotoImage:
    return ImageTk.PhotoImage(Image.new(mode="RGB", size=size, color=color))


def compositeImgs(img_src:PILImage, img_dst:PILImage) -> PILImage:
    img_dst.alpha_composite(img_src, dest=(0,0), source=(0,0))
    return img_dst


def lightenImg(img:PILImage, factor:float=0.5) -> PILImage:
    return ImageEnhance.Brightness(img).enhance(factor)


def changeColorImg(img:PILImage, color_old, color_new="") -> PILImage:
    #Convert hex color and img to rgba
    color_new = ImageColor.getcolor(color_new, "RGBA")
    if color_old: color_old = ImageColor.getcolor(color_old, "RGBA")
    img = img.convert("RGBA")

    #Change rgb foreach pixel, keeping alpha
    pixel_data = img.getdata()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r,g,b,_ = list(color_new)
            a = pixel_data[x,y][-1]
            pixel_data[x,y] = (r,g,b,a)

    return img

#==================================================

if __name__ == "__main__":
    import sys, os

    FNAME_RESULT_COLOR = "_result_color.png"
    FNAME_RESULT_B64 = "_result_b64.txt"

    try:
        if sys.argv[1] == "--changecolor":
            file_path = sys.argv[2]
            color_new = sys.argv[3]
            color_old = sys.argv[4] if len(sys.argv)==4 else ""
            file_result_path = os.path.join(os.path.dirname(file_path), FNAME_RESULT_COLOR)

            img = Image.open(file)
            img = changeColorImg(img, color_new, color_old)
            img.save(file_result_path)

        elif sys.argv[1] == "--tob64":
            folder_path = sys.argv[2]
            file_result_path = os.path.join(folder_path, FNAME_RESULT_B64)

            with open(file_result_path, "w") as f:
                for path, dir, files in os.walk(folder_path):
                    for file in files:
                        if file.endswith((".png", ".gif")):
                            file_path = path + os.sep + file
                            f.write("---" + file + "\n" + fileTob64(file_path) + "\n\n")

        else: raise Exception()

    except:
        print("Exception!")
        print("Usage: python utilities.py --changecolor file_name hexcolor_new hexcolor_old")
        print("Usage: python utilities.py --tob64 folder")