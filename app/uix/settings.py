from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
#Builder.load_string("""
#<SettingsWindow>:
#    MDFlatButton:
#        text:"setting window!"
#""")

class SSLSetting(Screen):
    pass
class LangSetting(Screen):
    pass


class SettingsWindow(BoxLayout):
    def __init__(self,**kwargs):
        super(SettingsWindow,self).__init__(**kwargs)
        self.ids.setting_screen_manager.add_widget(SSLSetting(name="ssl"))
        self.ids.setting_screen_manager.add_widget(LangSetting(name="lang"))
        self.ids.setting_screen_manager.transition = NoTransition()
        #self.ids.setting_screen_manager.switch_to(SSLSetting())



    def clicked(self):
        print("Clicked!!!")
        #self.ids.setting_screen_manager.switch_to(LangSetting())
        self.ids.setting_screen_manager.current = "lang"



class MainApp(MDApp):
    def build(self):
        return SettingsWindow()

    def on_start(self):
        pass
        #self.fps_monitor_start()
        #self.theme_cls.theme_style = "Dark"


if __name__ == "__main__":
    Builder.load_file("settings.kv")
    MainApp().run()
