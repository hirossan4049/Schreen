from flask import Flask, Response, request, send_from_directory, render_template, url_for,jsonify
from Crypto import Random
import crypter
import random
import cv2


def random_string(num):
    abcs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    res = [random.choice(abcs) for i in range(num)]
    return ''.join(res)


app = Flask(__name__, template_folder="templates", static_folder="static")

# USER PASSWORD 16, 32, 64文字,
USER_PASSWORD = b'admin12345678987'
AES_PASSWORD  = random_string(16)
DECRYPT_AES_PASSWORD = crypter.decrypt(crypter.encrypt(AES_PASSWORD, USER_PASSWORD),USER_PASSWORD)


print('USER_PASSWORD:',USER_PASSWORD)
print('AES_PASSWORD :',AES_PASSWORD)
print('DECRY_AES_PAS :',DECRYPT_AES_PASSWORD)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt_message')
def encrypt_message():
    data = crypter.encrypt(AES_PASSWORD, USER_PASSWORD)
    print('encrypt_data :',data)
    return jsonify({'data':data.decode()})


@app.route('/passwd_correct',methods=['GET','POST'])
def passwd_correct():
    print(request.args)
    print(request.get_json())
    try:
        if request.method == 'POST':
            json_data = request.get_json()['data']
            print(json_data)
            #decry = crypter.decrypt('G255kra8WaVTOXPiIwd7oEV/T4juG3ej7NmvsJR+nPE=',USER_PASSWORD)
            decry = crypter.decrypt(json_data,USER_PASSWORD)
            print(decry)
            if decry == DECRYPT_AES_PASSWORD:
                return {'result':'OK'}
            else:
                return {'result':'NG'}
        elif request.method == 'GET':
            return 'POST ONLY'
    except Exception as e:
        return {'result':'ERROR'}


@app.route('/video_feed')
def video_feed():
    img = cv2.imread('./nazo.jpg')
    _, jpeg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 25])

    encrypt_data = repr(jpeg.tobytes())
    print(encrypt_data[:30])

    jpeg_crypto = crypter.encrypt(encrypt_data,AES_PASSWORD)

    print(len(jpeg_crypto))
    header = (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + jpeg_crypto + b'\r\n\r\n') 
    return Response(header, mimetype='multipart/x-mixed-replace; boundary=frame')
    



app.run(debug=False, port=2342, threaded=True)
