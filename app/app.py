import os
import kivy

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

from kivy.core.window import Window


from kivy.lang import Builder

Builder.load_file('uix/main.kv')
Builder.load_file('uix/settings.kv')
Builder.load_file('uix/createSSLKey.kv')

from uix.main import MainWindow
from uix.settings import SettingsWindow
from uix.createSSLKey import CreateSSLKeyWindow


isNoExit = False
class MainRoot(BoxLayout):
    window1 = None
    window2 = None

    def __init__(self, **kwargs):
        self.window1 = Factory.MainWindow()
        self.window2 = Factory.SettingsWindow()
        self.createsslWindow = Factory.CreateSSLKeyWindow()
        super(MainRoot, self).__init__(**kwargs)
        self.mainDisplay()  

    def mainDisplay(self):
        global isNoExit
        isNoExit = False
        self.clear_widgets()
        self.add_widget(self.window1)
        Window.size = 500, 300


    def settingsDisplay(self):
        global isNoExit
        isNoExit = True
        self.clear_widgets()
        self.add_widget(self.window2)
        Window.size = 1000,750

    def createSSLDisplay(self):
        global isNoExit
        isNoExit = True
        self.clear_widgets()
        self.add_widget(self.createsslWindow)




class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'Schreen'



def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}


if __name__ == "__main__":
    MainApp().run()
    while isNoExit:
        print("IS NO EXIT")
        reset()
        MainApp().run()
