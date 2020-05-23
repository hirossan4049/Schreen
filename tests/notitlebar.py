from kivy.config import Config
Config.set('graphics', 'fullscreen', 'fake')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '300')
Config.set('graphics', 'left', '300')

from kivy.app import App
from kivy.uix.button import Button

class MyApp(App):
    def build(self):
        button = Button(text="Exit", size_hint=(None, None))
        button.bind(on_press=exit)
        return button

if __name__ == '__main__':
    MyApp().run()
