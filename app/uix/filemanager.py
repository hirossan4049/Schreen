from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty

# FIXME:なんでデフォルトの（ｒｙhh
# [x] Kivy Filemanager -> ダサい
# [x] kivymd FIlemanager -> 動かん
# [x] tkinter filemanager -> なんか怒られた

# RecycleView使ってないけど許せ

# TODO: [ ] PACKAGE CODING

Builder.load_string("""
<TestWindow>:
    MDRaisedButton:
        text:"popup"
        on_release:root.on_press()

<BeautifulFileManager>:
    background:"images/white.png"
    size_hint:None,None
    BoxLayout:
        orientation:"vertical"
        MDLabel:
            size_hint:1,None
            padding:30,10
#            pos_hint: {"center_y": 0.9}
            text:"hello"
            font_size:45
            color:0.32, 0.43, 0.47,1
            height: self.texture_size[1]

        MDSeparator:

        ScrollView:
            size_hint:1,1
            StackLayout:  
                height: self.minimum_height
                id:stackLayout
                padding:30,30
                size_hint:1,None
                pos_hint:{"center_x",.5}
                #text_size:50,50
                #color:0.32, 0.43, 0.47,1


        MDTextButton:
            padding:30,30
            size_hint:None,None
            text:"閉じる"
            pos_hint: {"center_x": 0.9}
            on_release:root.dismiss()      
<IconListItem>:
    size_hint:None,None
    size:300,300
    orientation:"vertical"
    Image:
        #text:root.source
        source:"images/folder.png"
        size_hint:1,None
    MDLabel:
        text_size:self.size
        halign:"center"
        text:root.filename
        size_hint:1,None
""" )

class IconListItem(BoxLayout):
    source = StringProperty()
    filename = StringProperty()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

class BeautifulFileManager(ModalView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
       
        for i in range(10):
            self.ids.stackLayout.add_widget(IconListItem(source="hello",filename="filename"+str(i)))
        
        
    pass

class TestWindow(FloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def on_press(self):
        popup = BeautifulFileManager(
                size_hint=(1, 1),)
        popup.open()     


class MainApp(MDApp):
    def build(self):
        return TestWindow()

if __name__ == "__main__":
    MainApp().run()                 
