from kivymd.app import App
from kivy.properties import StringProperty
# from kivy.graphics import *
from kivy.lang import Builder
from kivy.clock import mainthread

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior  
# from kivy.Factory

import threading
import time
import os

kv_str = """
<MainWindow>:
    size_hint:1,1
    StackLayout:
        id:stackLayout


<StackItem>:
    size_hint:None,None
    size:100,100
    Button:
        text:'^^'
    Image:
        source:root.source

"""
Builder.load_string(kv_str)

class StackItem(ButtonBehavior, BoxLayout):
    source = StringProperty()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_image()

    @mainthread
    def add_image(self):
        self.source = "testimage.png"



class MainWindow(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
#        self.ids.stackLayout.add_widget(Button(text="hello"))
        threading.Thread(target=self.add_stack).start()
        #self.add_stack()


    def add_stack(self):
        for _ in range(50):
            #btn = Button(text="oal",size_hint=(None,None),size=(100,100))
            btn = StackItem()
            self.ids.stackLayout.add_widget(btn)

class MainApp(App):
    def build(self):
        return MainWindow()

MainApp().run()
