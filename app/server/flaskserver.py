from flask import Flask, Response, request, send_from_directory, render_template, url_for
import time
import threading
import socket
import uuid
import sys
import os
from server.sct_loop import Sct_loop
from kivy import Logger

from pathlib import Path
path = Path(__file__).parent   # test.pyのあるディレクトリ
path /= '../'     # ディレクトリ移動
# print(path.resolve())          # 絶対パスを表示 (デバッグ用)

from DEBUG import DEBUG,resource_path

# どういう書き方がいちばんいいのかいまいちわからん。
# if __name__ == '__main__':
#     from sct_loop import Sct_loop
# else:
#     from server.sct_loop import Sct_loop
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localIP = s.getsockname()[0]
    s.close()
except:
    Logger.error("INTERNET ERROR")
# FIXME:Flaskってどうやったらきれいにかけるんや？

do_run = True
quality = 0
port = 2525
isSsl = False
cert = "/Users/unkonow/Documents/pg/python/nowProject/schreen/Schreen/app/ssl/server.crt"
key  = "/Users/unkonow/Documents/pg/python/nowProject/schreen/Schreen/app/ssl/secret.key"

SHUTDOWN_UUID = uuid.uuid4()

sct_cls = Sct_loop(quality)


def client_loop():
    global do_run
    while do_run:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + sct_cls.get_value() + b'\r\n\r\n')
        time.sleep(1/30)
    return "Server exited!"


if DEBUG:
    Logger.warning("!!!!!DEBUG TRUE!!!!!!!")
    app = Flask(__name__, template_folder="templates", static_folder="static")
else:
    app = Flask(__name__, template_folder=resource_path("app/server/templates/"))



# === DEBUG時、Cache使われるとDEBUGしにくいので。 ===
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# =================================================


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(client_loop(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/shutdown/{}".format(SHUTDOWN_UUID))
def shutdown_acs():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "SERVER EXITED!"

# ====================================================

def set_quality(quality):
    sct_cls.set_quality(quality)

def get_quality():
    return sct_cls.get_quality()

def openBrowser():
    import webbrowser
    time.sleep(.5)
    if isSsl:
        webbrowser.open("https://{ip}:{port}".format(ip=localIP, port=port))
    else:
        webbrowser.open("http://{ip}:{port}".format(ip=localIP, port=port))


def startServer():
    global do_run
    do_run = True
    sct_cls.start()
    sct_cls.set_quality(quality)
    th = threading.Thread(target=openBrowser)
    th.start()
    # app.run_server(debug=False, host=localIP, port=port)
    if isSsl:
        try:
            app.run(debug=False, host=localIP, port=port, ssl_context=(cert, key),  threaded=True)
        except FileNotFoundError:
            logger.error("FILE NOT FOUND ERROR")
    else:
        app.run(debug=False, host=localIP, port=port, threaded=True)

    th.join()


def shutdown_server():
    global do_run
    import requests
    do_run = False
    try:
        if isSsl:
            requests.get("https://{ip}:{port}/shutdown/{uuid}".format(ip=localIP, port=port, uuid=SHUTDOWN_UUID))
        else:
            requests.get("http://{ip}:{port}/shutdown/{uuid}".format(ip=localIP, port=port, uuid=SHUTDOWN_UUID))
        sct_cls.exit()
    except requests.exceptions.ConnectionError:
        Logger.info("すでにEXITしてます")


if __name__ == '__main__':
    startServer()
