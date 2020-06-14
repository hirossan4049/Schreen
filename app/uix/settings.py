import os

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from uix.filetextfield import FileTextField
import configparser
from pprint import pprint

from DEBUG import resource_path



class SSLSetting(Screen):
    def __init__(self,**kwargs):
        super(SSLSetting,self).__init__(**kwargs)

        config_file = configparser.ConfigParser()
        config_file.read(resource_path('app/settings/config.ini'))

        self.ssl_enable  = eval(config_file.get("SSLSettings","enable"))
        self.openSSLPath = config_file.get("SSLSettings","OpenSSLPath")
        self.certPath    = config_file.get("SSLSettings","CertPath")
        self.keyPath     = config_file.get("SSLSettings","KeyPath")

        self.ids.enableSwitch.active = self.ssl_enable
        self.ids.opensslPathTextField.text = self.openSSLPath
        self.ids.certPathTextField.text = self.certPath
        self.ids.keyPathTextField.text = self.keyPath
                 

    def press_ok(self):
        noExit = self.settings_save()
        if noExit:
            return
        MDApp.get_running_app().stop()
    def press_cancel(self):
        MDApp.get_running_app().stop()

    def press_apply(self):
        print("PRESS APPLY")
        self.settings_save()

    def settings_save(self):
        for settings,content,arg,isChanged in self.check_changeSettings():
            if isChanged:
                print("is changed!",content,arg)
                self.save_config(settings,content,arg)
                print("save done!")

        isFoundEvenOne = False
        if self.getSSLSwitch():
            for name,isFound in self.search_files():
                if not isFound:
                    toast(f"{name}のファイルが見つかりませんでした。")
                    isFoundEvenOne = True
        return isFoundEvenOne
                    

    def getSSLSwitch(self):
        return self.ids.enableSwitch.active


    def check_changeSettings(self):
        """設定に変更があるか確認"""
        # SSL Settings
        ssl = "SSLSettings"
        arg = self.getSSLSwitch()
        yield ssl, "enable", arg, not self.ssl_enable == arg

        arg = self.ids.opensslPathTextField.text 
        yield ssl, "OpenSSLPath", arg, not self.openSSLPath == arg

        arg = self.ids.certPathTextField.text 
        yield ssl, "CertPath", arg, not self.certPath == arg 

        arg = self.ids.keyPathTextField.text 
        yield ssl, "KeyPath", arg, not self.keyPath == arg


    def search_files(self):
        #file = self.ids.opensslPathTextField.check_path()
        #print("SEARCH FILES SSL PATH",file)
        #yield "openSSLPath",file

        file = self.ids.certPathTextField.check_path()
        yield "certPath", file

        file = self.ids.keyPathTextField.check_path()
        yield "keyPath", file





    def save_config(self, settings, content, arg):
        config = configparser.ConfigParser()
        config.read(resource_path("app/settings/config.ini"))
        config.set(settings,content,str(arg))
        with open(resource_path("app/settings/config.ini"),"w") as h:
            config.write(h)

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
        self.selected_color_draw("sslSettings")
        #self.ids.setting_screen_manager.switch_to(SSLSetting())
        # いけるんかーーーーい
        #print(self.ids.setting_screen_manager.get_screen("ssl").ids)

    def gotoSSL(self):
        #self.ids.setting_screen_manager.switch_to(SSLSetting())
        self.ids.setting_screen_manager.current = "ssl"
        self.selected_color_draw("sslSettings")
    def gotoLang(self):
        #self.ids.setting_screen_manager.switch_to(LangSetting())
        self.ids.setting_screen_manager.current = "lang"
        self.selected_color_draw("langSettings")
    def gotoDarkmode(self):
        self.ids.setting_screen_manager.current = "darkmode"
        self.selected_color_draw("darkmodeSettings")
    def gotoDeveloper(self):
        self.ids.setting_screen_manager.current = "developer"
        self.selected_color_draw("developerSettings")
    def gotoHelp(self):
        #TODO:help window create
        self.selected_color_draw("helpSettings")


    def selected_color_draw(self,selected_window):
        idlist = ["sslSettings","langSettings","darkmodeSettings","developerSettings","helpSettings"]
        for item in idlist:
            self.ids[item].md_bg_color = (0,0,0,0)
        #self.ids[selected_window].md_bg_color = (.3,.3,.3,.2)
        self.ids[selected_window].md_bg_color = (.3,.3,.3,.15)
        
    
    def press_ok(self):
        pass
    def press_cancel(self):
        pass
    def press_apply(self):
        self.settings_save()

    def settings_save(self):
        for settings,content,arg,isChanged in self.check_changeSettings():
            if isChanged:
                print("is changed!",content,arg)


    # FIXME;汚ったねぇｗｗ
    def check_changeSettings(self):
        """設定に変更があるか確認"""
        # SSL Settings
        ssl = "SSLSettings"
        arg = self.ids.enableSwitch.active
        yield ssl, "enable", arg, self.ssl_enable == arg

        arg = self.ids.opensslPathTextField.text 
        yield ssl, "OpenSSLPath", arg, self.openSSLPath == arg

        arg = self.ids.certPathTextField.text 
        yield ssl, "CertPath", arg, self.certPath == arg 

        arg = self.ids.keyPathTextFielf.text 
        yield ssl, "KeyPath", arg, self.keyPath == arg
        # Lang Settings

    def save_config(self, settings, content, arg):
        config = configparser.ConfigParser()
        config.read(resource_path("app/settings/config.ini"))
        config.set(settings,content,arg)
        with open(resource_path("app/settings/config.ini")) as h:
            config.write(h)



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
