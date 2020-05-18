from kivymd.app import MDApp
from kivy.lang import Builder

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.label import MDLabel

from uix.main import MainWindow
from uix.settings import SettingsWindow
from uix.createSSLKey import CreateSSLKeyWindow
from kivy.lang import Builder
from kivy.factory import Factory

Builder.load_file('uix/main.kv')
Builder.load_file('uix/settings.kv')
Builder.load_file('uix/createSSLKey.kv')
 

kv_string = """
<ManagerWindow>:
    ScreenManager:
        id:screenmanager

<MainScreen>:
    BoxLayout:
        id:widget
<SettingsScreen>:
    SettingsWindow:
"""

Builder.load_string(kv_string)

class ManagerWindow(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.screenmanager.add_widget(MainScreen())

    def settingsDisplay(self):
        print("press settings display")

class MainScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.widget.add_widget(MainWindow())
class SettingsScreen(Screen):
    pass


class Main(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.boxLayout = BoxLayout()
        self.boxLayout.add_widget(MDLabel(text="hello wo®ld"))
        self.add_widget(self.boxLayout)

#sm = ScreenManager()
#mainWindow = Screen(name="hellO")
#sm.add_widget(SettingsWindow(name='settings'))
#sm.add_widget(CreateSSLKeyWindow(name='ssl')) 
#sm.switch_to(Main())

class TestApp(MDApp):
    def build(self):
        return Factory.ManagerWindow()

if __name__ == '__main__':
    TestApp().run()
