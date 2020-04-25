import multiprocessing
import threading
import subprocess

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.core.window import Window


#from twokivys2 import ChildApp
# 色々考えた結果,1つの画面で頑張って切り替えるようにした。

kvfile = """
<MainWindow>:
    Button:
        text:"MainWindow"
        on_press:app.pressed()
<SettingWindow>:
    Label:
        text:"Setting Window"
"""
Builder.load_string(kvfile)

class MainWindow(BoxLayout):
    def __init__(self,**kwargs):
        super(MainWindow,self).__init__(**kwargs)


class SettingWindow(BoxLayout):
    def __init__(self,**kwargs):
        super(SettingWindow,self).__init__(**kwargs)
        self.add_widget(Label(text="SettingWindow"))


# 画面増えたらどうしよｗint型？hmmm.....
isSetting = False
class MainApp(App):
    def build(self):
        global isSetting
        isSetting = False
        Window.size = (600,450)
        #return(Button(text="MainApp",on_press=self.pressed))
        #self.root = MainWindow()
        #return self.root
        return Factory.MainWindow()

    def pressed(self,*args):
        global isSetting
        print("pressed")
        if isSetting:
            Window.size = (600,450)
        else:
            Window.size = (1000,700)

        isSetting = not isSetting
        #startSecondApp()

        #app = ChildApp()
        #p = multiprocessing.Process(target=app.run)
        #p.start()
        #subprocess.Popen("python3 twokivys2.py".split())

    def on_stop(self):
        print("ON STOP")

class SecondApp(App):
    def build(self):
        return(Label(text="SecondApp"))



def mainAppStart():
    MainApp().run()

def secondAppStart():
    SecondApp().run()

def startSecondApp(*args):
    app = ChildApp()
    b = multiprocessing.Process(tarqet=app.run)
    b.start()

def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}


if __name__ == '__main__':
    mainAppStart()
    while isSetting:
        print("IS SETTING")
        isSetting = not isSetting
        reset()
        mainAppStart()
    
    #a = multiprocessing.Process(target=mainAppStart)
    #b = multiprocessing.Process(target=secondAppStart)
    #b.start()
    #a.start()
