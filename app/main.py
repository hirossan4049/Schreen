import os
# from multiprocessing import Process
import threading
import time

importstart = time.time()
#import server.flaskserver as dashsev
from kivy import Logger
from kivy.core.text import LabelBase, DEFAULT_FONT
# from kivy.factory import Factory
from kivy.graphics.svg import Window
from kivy.properties import StringProperty
from kivy.resources import resource_add_path
# from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
# from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
# from kivy.uix.widget import Widget
# from kivy.utils import get_hex_from_color
from kivymd.app import MDApp
from kivy.lang import Builder

from DEBUG import DEBUG,resource_path

Logger.info("importTime:{}".format(time.time() - importstart))


if DEBUG:
    Logger.warning("""

    /////////////////////////////////////
    //      WARNING -> DEBUG TRUE      //
    /////////////////////////////////////
    
    """)
    resource_add_path("fonts/")
    LabelBase.register(DEFAULT_FONT, "fonts/SourceHanSans.otf")
    help_icon_path = "images/help_icon.png"
    schreen_icon_path = "images/icon.png"
else:
    resource_add_path(resource_path("app/fonts/"))
    LabelBase.register(DEFAULT_FONT, resource_path("app/fonts/SourceHanSans.otf"))
    # FIXME: PyinstallerでBuildすると、自動でmain.kvが読まれないが、
    #  DEBUG環境だと両方読まれて色々めんどくさいからデフォルト読まれるようにするのもありかも。
    Builder.load_file(resource_path("app/main.kv"))
    help_icon_path = resource_path("app/images/help_icon.png")
    schreen_icon_path = resource_path("app/images/icon.png")


# デフォルトのダイアログが超絶ダセェのでカスタムダイアログ。
class CustomDialog(ModalView):
    title = StringProperty()
    content = StringProperty()


class MainWindow(Screen):
    help_icon = StringProperty(help_icon_path)
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        # self.ids.stop_btn.disabled = True
        self._befor_port = ""
        self._befor_quality = 0

    # テスト用のクリックイベントです。
    def testClick(self):
        print("clicked!")

    def quality_help_dialog(self):
        popup = CustomDialog(
            size_hint=(.9, .9),
            title="品質",
            content="普通　: スライドなどにおすすめです。\n\n高品質: 細かいテキストなどにおすすめです。\n\n低品質: 動画などにおすすめです。")
        popup.open()

    def port_help_dialog(self):
        popup = CustomDialog(
            size_hint=(.9, .9),
            title="ポート",
            content="デフォルト 8050   数字のみ\n\n他のポートが重なっているときに変更できます。\n通常は4桁の数字から構成されます。")
        popup.open()

    def quality(self) -> int:
        item = self.ids.quality_dropdown.current_item
        res = 0
        if item == "普通":
            res = 2
        elif item == "高品質":
            res = 1
        elif item == "低品質":
            res = 4
        # 正直調停品質はいらねぇとおもった、
        # elif item == "超低品質":
        #     res = 8
        else:
            Logger.error("ERROR QUALITY FUNC LINE:57")
            self.error_dialog("内部エラー\nmain.py:60\n\nご不便をおかけして申し訳ございません。\n製作者にお問い合わせください。")
        return res

    def check_port(self):
        text = self.ids.port_text.text
        try:
            int(text)
            if not len(text) == 4:
                self.error_dialog("ポートが4桁ではありません。\n例:8050\n\n詳細: '{text}' is not four digits.".format(text=text))
                return False
        except ValueError as e:
            self.error_dialog("ポートが数字ではありません。\n例:8050\n\n詳細: {}".format(e))
            return False
        return True

    # FIXME:品質のみの再起動の場合は、品質のみ変えるように。
    def start(self):
        import server.flaskserver as flaskserver
        global server_thread
        quality = self.quality()
        if not self.ids.stop_btn.disabled:
            # 品質のみの再起動の場合は、品質のみ変えるように。
            if flaskserver.port == int(self.ids.port_text.text):
                if flaskserver.get_quality == quality:
                    Logger.info("stop_btn disabled shutdown server now")
                    # ユーザーが短気だった場合の保険(連打防止)  FIXME:実は意味無い説
                    self.ids.start_btn.disabled = True
                    flaskserver.shutdown_server()
                    time.sleep(.5)
                    Logger.info("=====SHUTDOWN MAYBE COMPLETE=====")
                else:
                    flaskserver.set_quality(quality)
                    return False

        if not self.check_port():
            self.ids.start_btn.disabled = False
            return False
        flaskserver.quality = quality
        flaskserver.port = int(self.ids.port_text.text)
        server_thread = threading.Thread(target=flaskserver.startServer)
        server_thread.start()
        self.ids.stop_btn.disabled = False
        self.ids.start_btn.disabled = False
        self.ids.start_btn.text = "再起動"



    def stop(self):
        try:
            flaskserver.shutdown_server()
        except ImportError:
            pass
        except:
            Logger.error("flaskserver:shutdown_server() func error.")

        self.ids.stop_btn.disabled = True
        self.ids.start_btn.text = "起動"
        print("EVENT CLEAR")

    def error_dialog(self,content):
        popup = CustomDialog(
            size_hint=(.9, .9),
            title="エラー",
            content=content)
        popup.open()


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'schreen'
        self.icon = schreen_icon_path
        Window.size = 500, 300

    def on_stop(self):
        global server_thread
        try:
            flaskserver.shutdown_server()
        except ImportError:
            pass
        except:
            Logger.error("flaskserver:MAINAPP ERROR.shutdown_server() func error.")

        try:
            Logger.info("server thread join now...")
            server_thread.join()
            Logger.info("Server join end!!")
        except:
            Logger.error("joinできません。")


    def build(self):
        return MainWindow()


if __name__ == "__main__":
    MainApp().run()
