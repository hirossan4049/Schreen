import os
import sys

DEBUG = False

def resource_path(relative):
  if hasattr(sys, "_MEIPASS"):
      return os.path.join(sys._MEIPASS, relative)
  return os.path.join(relative)
