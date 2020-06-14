import os.path
import sys

from kivy.resources import resource_add_path

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
        
class CrashApp(App):
    def __init__(self,text,**kwargs):
        super().__init__(**kwargs)
        self.text = str(text)

        self.text = 'Application Error:\n' + self.text
        for index in range(0,len(self.text),75):
            self.text = self.text[:index] + '\n' + self.text[index:]

    def build(self): 
        self.title = "Crash report"
        Window.size = (500,300)
        return Label(text=self.text)

def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}

try:
    from app import MainApp
except Exception as e:
    print("==============IMPORT  Error=================")
    print(e)
    print("==============IMPORT  Error=================")
    reset()
    CrashApp(text=e).run()


def get_fs_encoding():
    encoding = sys.getfilesystemencoding()
    if not encoding:
        encoding = sys.stdin.encoding
    if not encoding:
        encoding = sys.getdefaultencoding()
    return encoding


def main():
    data = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data')
    if isinstance(data, bytes):
        data = data.decode(get_fs_encoding())
    resource_add_path(data)

    try:
        MainApp().run()
    except Exception as e:
        print("==============MainApp Error=================")
        print(e)
        print("==============MainApp Error=================")
        reset()
        CrashApp(text=e).run()


if __name__ == '__main__':
    main()
