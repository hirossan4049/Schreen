from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import configparser

#FIXME:aaa


class SSLSetting(Screen):
    def __init__(self,**kwargs):
        super(SSLSetting,self).__init__(**kwargs)
        config_file = configparser.ConfigParser()
        config_file.read('settings/config.ini')

        self.ssl_enable  = eval(config_file.get("SSLSettings","enable"))
        self.openSSLPath = config_file.get("SSLSettings","OpenSSLPath")
        self.certPath    = config_file.get("SSLSettings","CertPath")
        self.keyPath     = config_file.get("SSLSettings","KeyPath")

        #config_file["SSLSettings"]["enable"] = "False"
        #config_file.set("SSLSettings","enable","False")
        #with open("settings/config.ini","w") as h:
        #    config_file.write(h)

        self.ids.enableSwitch.active = self.ssl_enable
        self.ids.opensslPathTextField.text = self.openSSLPath
        self.ids.certPathTextField.text = self.certPath
        self.ids.keyPathTextField.text = self.keyPath
        
class LangSetting(Screen):
    pass
class DarkmodeSetting(Screen):
    pass
class DeveloperSetting(Screen):
    pass


class SettingsWindow(BoxLayout):
    def __init__(self,**kwargs):
        super(SettingsWindow,self).__init__(**kwargs)
        self.ids.setting_screen_manager.add_widget(SSLSetting(name="ssl"))
        self.ids.setting_screen_manager.add_widget(LangSetting(name="lang"))
        self.ids.setting_screen_manager.add_widget(DarkmodeSetting(name="darkmode"))
        self.ids.setting_screen_manager.add_widget(DeveloperSetting(name="developer"))
        self.ids.setting_screen_manager.transition = NoTransition()
        #self.ids.setting_screen_manager.switch_to(SSLSetting())



    def gotoSSL(self):
        #self.ids.setting_screen_manager.switch_to(LangSetting())
        self.ids.setting_screen_manager.current = "ssl"

    def gotoLang(self):
        self.ids.setting_screen_manager.current = "lang"

    def gotoDarkmode(self):
        self.ids.setting_screen_manager.current = "darkmode"

    def gotoDeveloper(self):
        self.ids.setting_screen_manager.current = "developer"



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
