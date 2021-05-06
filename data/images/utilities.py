from io import BytesIO
import base64

from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageColor, ImageEnhance
from PIL.Image import Image as PILImage

#==================================================

def b64ToPIL(img_b64:str) -> PILImage:
    return Image.open(BytesIO(base64.b64decode(img_b64)))


def b64ToTk(img_b64:str) -> PILImage:
    return PhotoImage(data=img_b64)


def PILToTk(img_pil:PILImage) -> PhotoImage:
    return ImageTk.PhotoImage(img_pil)


def TkSolid(size:int, color:str) -> PhotoImage:
    return ImageTk.PhotoImage(Image.new(mode="RGB", size=size, color=color))


def compositeImgs(img_src:PILImage, img_dst:PILImage) -> PILImage:
    img_dst.alpha_composite(img_src, dest=(0,0), source=(0,0))
    return img_dst


def brightensColorImg(img:PILImage, factor:float=0.5) -> PILImage:
    return ImageEnhance.Brightness(img).enhance(factor)


def changeColorImg(img:PILImage, color_old:str, color_new:str=None) -> PILImage:
    #Convert hex color and img to rgba
    color_new = ImageColor.getcolor(color_new, "RGBA")
    if color_old: color_old = ImageColor.getcolor(color_old, "RGBA")
    img = img.convert("RGBA")

    #Change rgb foreach pixel, keeping alpha
    pixel_data = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r,g,b,_ = color_new
            a = pixel_data[x,y][-1]
            pixel_data[x,y] = (r,g,b,a)

    return img


def imgTob64(img_path:str) -> str:
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


#==================================================


FILE_NAME_RESULT_COLOR = "_result_color.png"
FILE_NAME_RESULT_B64 = "_result_b64.txt"

if __name__ == "__main__":
    import sys, os

    try:
        if sys.argv[1] == "-changecolor":
            file_path = sys.argv[2]
            color_new = sys.argv[3]
            color_old = sys.argv[4] if len(sys.argv)==4 else None
            file_result_path = os.path.join(os.path.dirname(file_path), FILE_NAME_RESULT_COLOR)

            img = Image.open(file)
            img = changeColorImg(img, color_new, color_old)
            img.save(file_result_path)


        elif sys.argv[1] == "-tob64":
            folder_path = sys.argv[2]
            file_result_path = os.path.join(folder_path, FILE_NAME_RESULT_B64)

            with open(file_result_path, "w") as f:
                for path, dir, files in os.walk(folder_path):
                    for file in files:
                        if file.endswith((".png", ".gif")):
                            file_path = path + os.sep + file
                            f.write("---" + file + "\n" + imgTob64(file_path ) + "\n\n")

        else: raise Exception()

    except:
        print("Exception!")
        print("Usage: python utilities.py -changecolor file_name color_new color_old")
        print("Usage: python utilities.py -tob64 folder")