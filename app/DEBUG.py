import os
import sys

DEBUG = True

def resource_path(relative):
    if DEBUG:
        return relative
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
