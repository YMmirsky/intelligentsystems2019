from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
app.debug = True

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        name = request.form["name"]
        return name + " Hello"
    return render_template("index.html")

@app.route("/cv_cmd", methods=['GET', 'POST'])
def index2():
    ret_obj = dict()
    dir_val = str(request.args.get('dir'))
    print type(dir_val)
    print 'data from client: ' + dir_val
    if 'straight' == dir_val:
        ret_obj['dir'] = 'ACK straight'
    elif 'left' == dir_val:
        ret_obj['dir'] = 'ACK left'
    elif 'right' == dir_val:
        ret_obj['dir'] = 'ACK right'
    else:
        ret_obj['dir'] = 'NACK'
    return jsonify(ret_obj)

if __name__ == "__main__":
    app.run()

