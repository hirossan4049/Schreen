import threading
import sys
import pathlib

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.filemanager import MDFileManager
from kivy.clock import Clock
from timeout_decorator import TimeoutError

from uix.filemanager import BeautifulFileManager

current_dir = pathlib.Path(__file__).resolve().parent
#print(current_dir)
sys.path.append( str(current_dir) + '/../settings/' )
from ssl_setting import CreateSSLKey,OpenSSLNotFoundError


class FirstScreen(Screen):
    pass
class SecondScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        # geoip使ったろおもたけど流石にキモいからやめた
        self.ids.countryTextField.text = "JP"
        self.ids.provinceTextField.text = "Osaka"
        self.ids.localityTextField.text = "Sakai"
        self.ids.emailTextField.text = ""


    def file_manager_open(self):                      
        popup = BeautifulFileManager(on_selected=self.select_path)
        popup.open()     

    def select_path(self,path):
        self.ids.keyPathTextField.text = path

class ThirdScreen(Screen):
    pass
class DoneScreen(Screen):
    pass

class CreateSSLKeyWindow(BoxLayout):  
    def __init__(self,**kwargs):
        super(CreateSSLKeyWindow,self).__init__(**kwargs)
        self.ids.wizard_ScreenManager.add_widget(FirstScreen(name="first"))
        self.ids.wizard_ScreenManager.add_widget(SecondScreen(name="second"))
        self.ids.wizard_ScreenManager.add_widget(ThirdScreen(name="third"))
        self.ids.wizard_ScreenManager.add_widget(DoneScreen(name="done"))






    def press_next(self):
        nowscreen = self.ids.wizard_ScreenManager.current
        nextscreen = ""
        if nowscreen == "first":
            nextscreen = "second"

        elif nowscreen == "second":
            if self.isAllburied():
                nextscreen = "third"
                self.ids.nextButton.disabled = True
                #Clock.schedule_once(self.createStartSSLKey)
                threading.Thread(target=self.createStartSSLKey).start()
            else:
                toast("未入力の項目があります。")
                return False
                
        # thirdにはこないはず
        elif nowscreen == "third":
            nextscreen = "done" 
            self.ids.nextButton.text = "Exit"
        elif nowscreen == "done":
            #TODO:EXIT
            #self.app.settingsDisplay()
            from kivymd.app import MDApp
            MDApp.get_running_app().stop()
            return
        self.ids.wizard_ScreenManager.current = nextscreen

    def press_cancel(self):
        pass


    def exit_manager(self,*args):
        pass
    def select_path(self,path):
        print(path)


    def isAllburied(self):
        secondScreen = self.ids.wizard_ScreenManager.get_screen("second")
        if not secondScreen.ids.keyPathTextField.text:
            return False
        if not secondScreen.ids.countryTextField.text:
            return False
        if not secondScreen.ids.provinceTextField.text:
            return False
        if not secondScreen.ids.localityTextField.text:
            return False
        if not secondScreen.ids.emailTextField.text:
            return False
        return True

    def createStartSSLKey(self,*args):
        secondScreen = self.ids.wizard_ScreenManager.get_screen("second")

        ip = "192.168.0.100"

        path     = secondScreen.ids.keyPathTextField.text
        country  = secondScreen.ids.countryTextField.text
        province = secondScreen.ids.provinceTextField.text
        locality = secondScreen.ids.localityTextField.text
        email    = secondScreen.ids.emailTextField.text

        createssl = CreateSSLKey(path=path,
                    ip=ip,
                    country=country,
                    province=province,
                    locality=locality,
                    email=email)

        try:
            createssl.start()
        except OpenSSLNotFoundError:
            print("OPEN SSL NOT FOUND ERROR!!!")
        except TimeoutError:
            print("TIME OUT ERROR")
            toast("ERROR!")
        except:
            print("UMM ERROR!")
            toast("ERRORRRRR!!!")
        else:
            toast("Done!")
        self.ids.nextButton.disabled = False
        self.save_settings(path)

    def save_settings(self,path):
        self.save_config("SSLSettings","CertPath",path+"/server.crt")
        self.save_config("SSLSettings","KeyPath",path+"/secret.key")

    def save_config(self, settings, content, arg):
        import configparser
        config = configparser.ConfigParser()
        config.read("settings/config.ini")
        config.set(settings,content,str(arg))
        with open("settings/config.ini","w") as h:
            config.write(h)
        

    #def __init__(self,path,ip,country="JP",province="Osaka",locality="Sakai",email="unko@unko.com"):

        
        


class MainApp(MDApp):
    def build(self):
        return CreateSSLKeyWindow()

if __name__ == "__main__":
    Builder.load_file("createSSLKey.kv")
    MainApp().run()
