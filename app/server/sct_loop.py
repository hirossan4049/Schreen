import concurrent.futures
import threading
import time
from kivy import Logger
Logger.info("CV2 LOAD NOW...")
import cv2
Logger.info("===CV2 LOAD OK!===")
import mss
import numpy


class Sct_loop:
    def __init__(self,quality=2):
        self.res = b""
        self.sct = mss.mss()
        self.quality = quality
        self.do_run = True
        # FIXME: 画面サイズを取得してやる。
        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1200}
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 25]

    def sct_func(self):
        sct_mss = self.sct.grab(self.monitor)
        img = numpy.array(sct_mss)
        # success, img = video.read()
        height = img.shape[0]
        width = img.shape[1]
        resized_img = cv2.resize(img, (width // self.quality, height // self.quality))
        _, jpeg = cv2.imencode('.jpg', resized_img,self.encode_param)
        ret_bytes = jpeg.tobytes()
        # print(len(ret_bytes))
        return ret_bytes

    def timeout_func(self):
        timeout_file = os.getcwd() + "/timeout_img.png"
        print(timeout_file)
        img = open(timeout_file,"r").read()
        print(img)
        _, jpeg = imencode('.jpg', img, self.encode_param)
        return jpeg.tobytes()

    def sct_mainloop(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            while self.do_run:
                future = executor.submit(self.sct_func)
                self.res = future.result()
                # time.sleep(1 / (self.quality * 40))
                time.sleep(1 / 120)

    def set_quality(self, quality):
        self.quality = quality
        print("SET_QUALITY",self.quality)

    def get_quality(self):
        return self.quality

    def exit(self):
        self.do_run = False
        self.main_thread.join()

    def start(self):
        self.do_run = True
        self.main_thread = threading.Thread(target=self.sct_mainloop)
        self.main_thread.start()
