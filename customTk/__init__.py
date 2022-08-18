from .buttonImg import TkButtonImgHoverNone, TkButtonImgHoverImg, TkButtonImgHoverBg
from .buttonText import TkButtonTextHoverFg, TkButtonTextHoverBg
from .canvasGif import TkCanvasGif
from .frameInfo import TkFrameInfo
from .popup import TkPopup
#from .win7Features import Win7Features

#If there is not text or all the text there is are spaces
#len(self.entry_search.get()) - self.entry_search.get().count(" ") == 0
#[And if old text is not the same as the new text]
def validEntryText(text:str, text_original:str=None) -> bool:
    return text!=text_original and any(filter(lambda i: i!=" ", text))