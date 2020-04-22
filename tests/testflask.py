from flask import Flask, render_template, request, redirect, url_for, Response

#from OpenSSL import SSL
#context = SSL.Context(SSL.TLSv1_2_METHOD)
#context.use_certificate("server.crt")
#context.use_privatekey("server.key")

api = Flask(__name__)

@api.route("/")
def index():
    return "test\n"

if __name__ == '__main__':
    #api.run(host='192.168.0.103', port=334, ssl_context=('server.crt', 'server.key'), threaded=True, debug=False)
    api.run(host='192.168.0.103', port=334, ssl_context=('cert.pem', 'key.pem'), threaded=True, debug=False)
#    api.run(host='192.168.0.103', port=334, ssl_context=context, threaded=True, debug=False)
