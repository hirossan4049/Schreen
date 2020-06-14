import threading
import time

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout



class MainWindow(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.start_time = time.time()
        self.label = Label(text="hello world")
        self.add_widget(self.label)
        threading.Thread(target=self.loop_ctrl).start()

    def loop(self):
        self.label.text = str(time.time() - self.start_time)

    def loop_ctrl(self):
        while True:
            threading.Thread(target=self.loop).start()
            time.sleep(1)
    


class MainApp(App):
    def build(self):
        return MainWindow()


MainApp().run()

