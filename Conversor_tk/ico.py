import os, sys

def url():
    if hasattr(sys, "_MEIPASS"):
        url_ico = os.path.join(sys._MEIPASS, "src", "ico.ico")
        return url_ico
    else:
        url_ico = os.path.join(os.getcwd(), "src", "ico.ico")
        return url_ico
