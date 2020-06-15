import threading

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.label import MDLabel

try:
    from app.uix.main import MainWindow
    from app.uix.settings import SettingsWindow
    from app.uix.createSSLKey import CreateSSLKeyWindow
except ImportError:
    from uix.main import MainWindow
    from uix.settings import SettingsWindow
    from uix.createSSLKey import CreateSSLKeyWindow
    from DEBUG import resource_path

from kivy.lang import Builder
from kivy.factory import Factory


try:
    Builder.load_file('app/uix/main.kv')
    Builder.load_file('app/uix/settings.kv')
    Builder.load_file('app/uix/createSSLKey.kv')
except:
    Builder.load_file(resource_path('app/uix/main.kv'))
    Builder.load_file(resource_path('app/uix/settings.kv'))
    Builder.load_file(resource_path('app/uix/createSSLKey.kv'))
 

import os
import shutil
import configparser
def check_settings_file():
    home = os.path.expanduser('~')
    path = home + '/Schreenconf.ini'
    if not os.path.isfile(path):
        shutil.copy(resource_path('app/settings/config.ini'),path)

    try:
        config_file = configparser.ConfigParser()
        config_file.read(home + '/Schreenconf.ini')
        config_file.get("SSLSettings","enable")
        config_file.get("SSLSettings","OpenSSLPath")
        config_file.get("SSLSettings","CertPath")
        config_file.get("SSLSettings","KeyPath")
    except:
        shutil.copy(resource_path('app/settings/config.ini'),path)



kv_string = """
<ManagerWindow>:
    ScreenManager:
        id:screenmanager

<MainScreen>:
    BoxLayout:
        id:widget
<SettingsScreen>:
    BoxLayout:
        id:widget
<CreateSSLKeyScreen>:
    BoxLayout:
        id:widget
"""

Builder.load_string(kv_string)

isDontExitMe = False
undofunc = None
class ManagerWindow(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.screenmanager.transition = NoTransition()
        check_settings_file()
        global undofunc
        try:
            print("undo func",undofunc.__name__)
        except:
            pass
        if not undofunc:
            self.mainDisplay()
        else:
            commando = "self.{}()".format(undofunc.__name__)
            eval(commando)
        #elif undofunc.__name__ == self.settingsDisplay.__name__:
        #    self.settingsDisplay()
        #elif undofunc.__name__ == self.mainDisplay.__name__:
        #    self.mainDisplay()

    
    def mainDisplay(self):
        global isDontExitMe
        isDontExitMe = False
        self.ids.screenmanager.switch_to(MainScreen())
        Window.size = 500, 300


    def settingsDisplay(self):
        global isDontExitMe
        global undofunc
        isDontExitMe = True
        undofunc = self.mainDisplay
        self.ids.screenmanager.switch_to(SettingsScreen())
        Window.size = 700,550

    def createSSLDisplay(self):
        global isDontExitMe
        global undofunc
        isDontExitMe = True
        undofunc = self.settingsDisplay
        self.ids.screenmanager.switch_to(CreateSSLKeyScreen())
        Window.size = 700,500

class MainScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.widget.add_widget(MainWindow())

class SettingsScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.widget.add_widget(SettingsWindow())

class CreateSSLKeyScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.widget.add_widget(CreateSSLKeyWindow())


#sm = ScreenManager()
#mainWindow = Screen(name="hellO")
#sm.add_widget(SettingsWindow(name='settings'))
#sm.add_widget(CreateSSLKeyWindow(name='ssl')) 
#sm.switch_to(Main())

class MainApp(MDApp):
    def build(self):
        return Factory.ManagerWindow()
    def on_stop(self):
        reset()

def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}

def main():
    MainApp().run()
    while isDontExitMe:
        print("IS NO EXIT")
        reset()
        MainApp().run()

if __name__ == '__main__':
    main()
