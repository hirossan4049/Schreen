from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout 
from kivymd.uix.dialog import MDDialog
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior  
from kivy.clock import Clock
from kivy.graphics import *
import time
import os

# FIXME:なんでデフォルトの（ｒｙhh
# [x] Kivy Filemanager -> ダサい
# [x] kivymd FIlemanager -> 動かん
# [x] tkinter filemanager -> なんか怒られた

# RecycleView使ってないけど許せ
# Windows not friendly :)

# TODO: [ ] PACKAGE CODING

Builder.load_string("""
<TestWindow>:
    MDRaisedButton:
        text:"popup"
        on_release:root.on_press()

<BeautifulFileManager>:
    background:"images/white.png"
    size_hint:1,1
    BoxLayout:
        orientation:"vertical"
        BoxLayout:
            size_hint:1,None
            MDIconButton:
                icon:"undo"
                on_release:root.undo()
                size_hint:None,None
            MDLabel:
                id:path_name
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

        MDSeparator:

        BoxLayout:
            size_hint:1,None
            padding: dp(10)
            MDRaisedButton:
                text:"createFolder"
                on_release:root.create_folder()
            MDTextField:
                id:path_textfield
                size_hint:.8,None
                pos_hint:{"center_y":.5}
                text:"ola!"
                #mode: "rectangle"

            MDTextButton:
                padding:30,30
                size_hint:None,None
                text:"閉じる"
                pos_hint: {"center_x": 0.9}
                on_release:root.dismiss()      
<IconListItem>:
    size_hint:None,None
    #size:250,250
    size:100,100
    orientation:"vertical"
    Image:
        source:root.source
        size_hint:1,1
        #size_hint:None,None
        #size:50,50
    MDLabel:
        size_hint:1,None
        size:10,100
        text_size:self.size
        halign:"center"
        text:root.filename

<CreateFolderDialog>:
    background:"images/white.png"
    size_hint:.3,.3
    BoxLayout:
        orientation:"vertical"
        MDLabel:
            size_hint:1,None
            padding:30,10
#            pos_hint: {"center_y": 0.9}
            text:root.title
            font_size:45
            color:0.32, 0.43, 0.47,1
            height: self.texture_size[1]

        MDSeparator:

        Widget:

        MDTextField:
            id:textField
            padding:30,30
            size_hint:.99,None
            pos_hint:{"center_x":.5}
            size:0,75
            #color:0.32, 0.43, 0.47,1

        BoxLayout:
            padding:40,10
            Widget:
            MDTextButton:
                padding:30,30
                size_hint:None,None
                text:"閉じる"
                pos_hint: {"center_x": 0.9}
                on_release:root.dismiss()

            MDRaisedButton:
                size_hint:None,None
                text:root.yes
                on_release:root.ok()
""" )

DIRIMAGE = "images/folder.png"
IMAGEIMAGE = "images/imageImage.png"

class CreateFolderDialog(ModalView):
    title = StringProperty()
    yes = StringProperty("ok")
    path = StringProperty()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.path = kwargs["path"]
        if not self.path[-1] == "/":
            self.path = self.path + "/"

    # ぐっちゃぐちゃだぁ
    def ok(self):
        createText = self.ids.textField.text
        if not createText:
            createText = "名称未設定"
        try:
            os.makedirs(self.path+createText)
            self.dismiss()
        except FileExistsError:
            for index in range(101):
                try:
                    os.makedirs(self.path+createText+str(index))
                    self.dismiss()
                    break
                except FileExistsError:
                    continue
                except:
                    print("ERROR file not create")
                    break
            if index == 100:
                print("FOLDER NOT CREATED")
        except:
            print("FOLDER NOT CREATED")
                

            
            


# Ontouchdown doble click? No.
class IconListItem(ButtonBehavior,BoxLayout):
    source = StringProperty()
    filename = StringProperty()
    now_dir = StringProperty()

    def __init__(self,on_press,**kwargs):
        super().__init__(**kwargs)
        #print(kwargs)
        self.filepath = kwargs["now_dir"] + "/" + kwargs["filename"]
        self.on_press = on_press
        self.isdir = False
        self.filecheck()

    
    def filecheck(self):
        if os.path.isdir(self.filepath):
            self.isdir = True
            self.source = "images/folder.png"
        elif os.path.isfile(self.filepath):
            self.source = "images/imageImage.png"
            self.imget()
        if len(self.filename) >= 13:
            path,ext = os.path.splitext(os.path.basename(self.filename))
            path = path[:10]
            self.filename = path + ".." + ext


    def imget(self):
        path, ext = os.path.splitext(os.path.basename(self.filepath))
        if ext == ".app":
            pass
        elif ext == ".png":
            image = self.filepath
        elif ext == ".pdf":
            image = "images/pdfImage.png"
        elif ext == ".py":
            image = "images/pythonImage.png"
        else:
            image = "images/nazoImage.png"
        self.source = image
        
        pass
    def setIcon(self,imagepath):
        pass
    def on_release(self,*args):
        self.on_press(self.filename,self.isdir,self.filepath)
        #with self.canvas:
        #    Color(.1, .6, .3,.3)
        #    Rectangle(pos=self.pos, size=self.size)




class BeautifulFileManager(ModalView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #print(kwargs)
        #self._return_func = kwargs["return_func"]
        self.baclick = ""   
        #self.backfilepath = ""
        self.now_dir = ""
        self.backtime = 0
        self.hidden_file_look = False
        self.undo_path = []
        self.add_stack()  
        Clock.schedule_interval(self.check_dir_loop,2)

        #homedir = os.path.expanduser("~")
        #files = os.listdir(homedir)
       
        #for fileitem in files:
        #    self.ids.stackLayout.add_widget(IconListItem(
        #                                        on_press=self.filepressed,
        #                                        #source="hello",
        #                                        filename=fileitem,
        #                                        now_dir=homedir))

    def filepressed(self,*args):
        if not args:
            return
        filepath,isdir,filepath = args
        if self.baclick == filepath:
            if time.time() - self.backtime <= .3:
                print("dble Clicked")
                if isdir:
                    self.add_stack(dir=filepath)
                    return
        self.baclick = filepath
        self.backtime = time.time()

    def stack_clear(self):
        self.ids.stackLayout.clear_widgets()
            
    def add_stack(self,dir="~"):
        self.stack_clear()
        homedir = os.path.expanduser(dir)
        self.undo_path.append(homedir)
        self.ids.path_name.text = homedir
        self.ids.path_textfield.text = homedir
        self.now_dir = homedir
        files = os.listdir(homedir)
        self.now_listdir = files
        for fileitem in files:
            if fileitem[0] == ".":
                if not self.hidden_file_look:
                    continue
            self.ids.stackLayout.add_widget(IconListItem(
                                                on_press=self.filepressed,
                                                #source="hello",
                                                filename=fileitem,
                                                now_dir=homedir))
    def create_folder(self):
        dialog = CreateFolderDialog(title="ファイル名を入力",path=self.now_dir)
        dialog.open()

    def check_dir_loop(self,*args):
        try:
            now_listdir = os.listdir(self.now_dir)
            if not self.now_listdir == os.listdir(self.now_dir):
                self.add_stack(dir=self.now_dir)
        except FileNotFoundError:
            self.undo()
        
    def undo(self):
        undo_path = ""
        try:
            undo_path = self.undo_path.pop(-2)
            del self.undo_path[-1]
        except IndexError:
            from kivymd.toast import toast
            toast("これ以上戻れません")
            return
        self.add_stack(undo_path)

        
    

class TestWindow(FloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def on_press(self):
        popup = BeautifulFileManager(
                size_hint=(1, 1),
                )
        popup.open()     
    
    def return_func(self,path):
        print("PATH:",path)


class MainApp(MDApp):
    def build(self):
        return TestWindow()

if __name__ == "__main__":
    MainApp().run()                 
