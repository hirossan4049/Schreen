import concurrent.futures
import threading
import time
from kivy import Logger
Logger.info("CV2 LOAD NOW...")
# これで起動速くなるといいけど。
from cv2 import resize, imencode
Logger.info("===CV2 LOAD OK!===")
import mss
import numpy


class Sct_loop:
    def __init__(self,quality=2):
        self.res = b""
        self.sct = mss.mss()
        self.quality = quality
        self.do_run = True
        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1200}


    def sct_func(self):
        sct_mss = self.sct.grab(self.monitor)
        img = numpy.array(sct_mss)
        # success, img = video.read()
        height = img.shape[0]
        width = img.shape[1]
        resized_img = resize(img, (width // self.quality, height // self.quality))
        _, jpeg = imencode('.jpg', resized_img)
        return jpeg.tobytes()

    def timeout_func(self):
        timeout_file = os.getcwd() + "/timeout_img.png"
        print(timeout_file)
        img = open(timeout_file,"r").read()
        print(img)
        _, jpeg = imencode('.jpg', img)
        return jpeg.tobytes()

    def sct_mainloop(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            while self.do_run:
                future = executor.submit(self.sct_func)
                self.res = future.result()
                time.sleep(1 / 60)

    def set_quality(self, quality):
        self.quality = quality

    def exit(self):
        self.do_run = False
        self.main_thread.join()

    def start(self):
        self.do_run = True
        self.main_thread = threading.Thread(target=self.sct_mainloop)
        self.main_thread.start()
