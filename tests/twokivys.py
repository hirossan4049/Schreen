import multiprocessing

from kivy.app import App
from kivy.uix.label import Label


class MainApp(App):
    def build(self):
        return(Label(text="MainApp"))

class SecondApp(App):
    def build(self):
        return(Label(text="SecondApp"))



def mainAppStart():
    MainApp().run()

def secondAppStart():
    SecondApp().run()

if __name__ == '__main__':
    a = multiprocessing.Process(target=mainAppStart)
    b = multiprocessing.Process(target=secondAppStart)
    a.start()
    b.start()
