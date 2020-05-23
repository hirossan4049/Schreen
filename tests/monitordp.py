import time
import threading

from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.app import App


label = Label()

def updatelabel(*args):
    global label
    for i in range(100):
        label.text = "10dp is {}.\nnow index is {}.".format(str(dp(10)),str(i))
        time.sleep(1)

threading.Thread(target=updatelabel).start()



class MainApp(App):
    def build(self):
        return label
        
MainApp().run()
