import os

from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField

    

class FileTextField(MDTextField):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.color_mode = "custom"
        #self.helper_text_mode = "on_focus"
        self.helper_text = ""
        self.helper_text_mode = "persistent"
        try:
            self.exts = kwargs.pop("exts")
            # folderかfileかの変数名って何がいいんだろ。
            #self.
        except:
            self.exts = ["all"]

    def on_focus(self,*args):
        foucus = args[1]
        if not foucus:
            self.check_path()
            #if self.text == "hello":
            #    self._found_path()
            #else:
            #    self._not_found_path()

    def check_path(self):
        # そもそもtextがファイルじゃなかったら。
        if not os.path.isfile(self.text):
            self._not_found_path()
            return
        # 拡張子を一つづつ
        for item in self.exts:
            if item == "all":
                self._found_path()
                return 
            # itemとtextの拡張子が一緒かどうか。
            _, ext = os.path.splitext(os.path.basename(self.text))
            if item == ext:
                self._found_path()
                return
        # 拡張子が一つもヒットしなかったら
        self._not_found_path()



    #def on_text(self, instance, text):
    #    print(text)
    #    if text == "hello":
    #        self._found_path()
    #    else:
    #        self._not_found_path()

    def _not_found_path(self):
        self.color_mode = "custom"
        self.line_color_focus = (1,0,0,1)
        self.helper_text = "not found path"

    def _found_path(self):
        self.color_mode = "primary"
        self.helper_text = ""



class MainApp(MDApp):
    def build(self):
        return FileTextField()

if __name__ == "__main__":
    MainApp().run()
