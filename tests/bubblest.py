# https://cheeseshop.hatenadiary.org/entry/20131208/1386465681
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.bubble import Bubble
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from functools import partial

from kivy.lang import Builder
Builder.load_string('''
<Bubbles>:
    canvas.before:
        Color:
            rgb: 0.0, 0.2, 0.2, 1
        Rectangle:
            pos: self.pos
            size: self.size
<Result>:
    label: _label
    arrow_pos: 'bottom_left'
    size_hint: (None, None)
    size: (200, 50)
    Label:
        color:1,1,1,1
        id: _label
        text:root.text
''')

class Result(Bubble):
    text = StringProperty()
    def __init__(self, **kwargs):
        super(Result, self).__init__(**kwargs)
        #self.label.text = kwargs['text']
        #self.text = ""
        #self.label.text = self.text

class Bubbles(FloatLayout):
    #def __init__(self,**kwargs):
    #    super(Bubbles,self).__init__(**kwargs)

    def on_touch_up(self, touch):
        print("ON TOUCH UP")  
        text = str(int(touch.pos[0]))+","+str(int(touch.pos[1]))
        result = Result(text=str(text),pos=touch.pos)
        self.add_widget(result)
        Clock.schedule_once(partial(self.remove_bubbles,result),.5)

    def remove_bubbles(self,result,*args):
        self.remove_widget(result)

class BubblesApp(App):

    def build(self):
        return Bubbles()

if __name__ == '__main__':
    BubblesApp().run()
