from flask import Flask , render_template, request

app = Flask(__name__)


@app.route('/')
def hello():
    name = "Hello World"
    return name

@app.route('/post_data', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        data = request.json['key']
        print(data)
    else:
        import time
        #return 'POST ONLY \n\n unixtime:' + str(time.time())
        return {'unix':str(time.time)}

## おまじない
if __name__ == "__main__":
    app.run(debug=True,port=2525)
