import concurrent.futures
import threading
import time
from kivy import Logger
Logger.info("CV2 LOAD NOW...")
import cv2
Logger.info("===CV2 LOAD OK!===")
import mss
import numpy
# import pyautogui

class Sct_loop:
    def __init__(self,quality=2):
        self.res = [0, b""]
        self._back_res = b""
        self.sct = mss.mss()
        self.quality = quality
        self.do_run = True
        # FIXME: 画面サイズを取得してやる。
        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1200}
        self.width = self.monitor["width"] * 2
        self.height = self.monitor["height"] * 2
        self._fps_cache = 0
        self._draw_num = 0
        self._draw_cache_num = 0
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 25]


    # TODO:マウスカーソルの描画
    def sct_func(self):
        t = time.time()
        self._fps_cache += 1
        sct_mss = self.sct.grab(self.monitor)
        img = numpy.array(sct_mss)
        # img = self._draw_mouse_cursor(img)
        # img = cv2.UMat(numpy.array(sct_mss))
        resized_img = cv2.resize(img, (self.width // self.quality, self.height // self.quality))

        _, jpeg = cv2.imencode('.jpg', resized_img, self.encode_param)
        ret_bytes = jpeg.tobytes()
        # self._draw_num += 1
        endtime = time.time() - t
        time.sleep(.7 - endtime)
        self.res = [self._draw_num, ret_bytes]
        # return ret_bytes

    def _draw_mouse_cursor(self, cvdata):
        pypos = pyautogui.position()
        pos = pypos.x * 2,pypos.y * 2
        cv2.circle(cvdata, pos, 10, (0,0,255), -1)
        return cvdata

    # def timeout_func(self):
    #     timeout_file = os.getcwd() + "/timeout_img.png"
    #     print(timeout_file)
    #     img = open(timeout_file,"r").read()
    #     print(img)
    #     _, jpeg = imencode('.jpg', img, self.encode_param)
    #     return jpeg.tobytes()

    def sct_mainloop(self):
        # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # FIXME:ここちゃんとできてねぇ
        with concurrent.futures.ThreadPoolExecutor() as excuter:
            while self.do_run:
                future = excuter.submit(self.sct_func)
                # self.res = future.result()
                # print("NOW LOADING")
                time.sleep(1/30)
                # time.sleep(1 / (self.quality * 30))
            print("DO RUN END")

    def fps_checker(self):
        self._fps_cache = 0
        time.sleep(1)
        Logger.info("FPS:" + str(self._fps_cache))

    def get_fps_realtime(self):
        while self.do_run:
            self.fps_checker()

    def set_quality(self, quality):
        self.quality = quality
        Logger.info("SET_QUALITY:{}".format(self.quality))

    def get_quality(self):
        return self.quality

    def get_value(self):
        res_num, res = self.res
        # debug用
        # print(res_num)
        # print(self._draw_cache_num)
        # if self._draw_cache_num > res_num:
        #     print(self._draw_cache_num - res_num)
        #     res = self._back_res
        # else:
        #     self._back_res = res
        #     self._draw_cache_num = res_num
        return res

    def exit(self):
        self.do_run = False
        self.main_thread.join()
        self.fpsThread.join()

    def start(self):
        self.do_run = True
        self.main_thread = threading.Thread(target=self.sct_mainloop)
        self.main_thread.start()
        # TODO:exit -> join
        self.fpsThread = threading.Thread(target=self.get_fps_realtime)
        self.fpsThread.start()
