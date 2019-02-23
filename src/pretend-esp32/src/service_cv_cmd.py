from flask import Flask, request, render_template, jsonify
import requests

# see pretend_drive.py for description of key values
def generate_drive_xhr(direction):
    dictToSend = dict()
    if direction == 'stop':
        dictToSend['mode'] = 3
        dictToSend['AXIS_0'] = 0.0
        dictToSend['AXIS_1'] = 0.0
        dictToSend['AXIS_3'] = 0.0
        dictToSend['button_0'] = 1
    if direction == 'straight':
        dictToSend['mode'] = 3
        dictToSend['AXIS_0'] = 0.0
        dictToSend['AXIS_1'] = 1.0
        dictToSend['AXIS_3'] = 0.0
        dictToSend['button_0'] = 1
    elif direction == 'left':
        dictToSend['mode'] = 1
        dictToSend['AXIS_0'] = -1.0
        dictToSend['AXIS_1'] =  0.0
        dictToSend['AXIS_3'] =  0.0
        dictToSend['button_0'] = 1
    elif direction == 'right':
        dictToSend['mode'] = 1
        dictToSend['AXIS_0'] = 1.0
        dictToSend['AXIS_1'] = 0.0
        dictToSend['AXIS_3'] = 0.0
        dictToSend['button_0'] = 1
    return dictToSend

def count_valid_keys(dictToSend):
    count = 0
    for item in dictToSend.items():
        if item[1] != '':
            count = count + 1
    return count

def send_drive_xhr(dictToSend):
    post_str = 'http://' + drive_addr + ':' + drive_port \
            + '/' + drive_endpoint + '?'
    if count_valid_keys(dictToSend) == 1:
        for item in dictToSend.items():
            if item[1] != '':
                post_str = post_str + item[0] + '=' + item[1]
        res = requests.post(post_str)
    elif count_valid_keys(dictToSend) > 1:
        first_item = True
        for item in dictToSend.items():
            if item[1] != '':
                if first_item:
                    post_str = post_str + item[0] + '=' + item[1]
                    first_item = False
                else:
                    post_str = '&' \
                        + post_str + item[0] + '=' + item[1]
        res = requests.post(post_str)

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
    if 'stop' == dir_val:
        send_drive_xhr(generate_drive_xhr('stop'))
        ret_obj['dir'] = 'ACK stop'
    elif 'straight' == dir_val:
        send_drive_xhr(generate_drive_xhr('straight'))
        ret_obj['dir'] = 'ACK straight'
    elif 'left' == dir_val:
        send_drive_xhr(generate_drive_xhr('left'))
        ret_obj['dir'] = 'ACK left'
    elif 'right' == dir_val:
        send_drive_xhr(generate_drive_xhr('right'))
        ret_obj['dir'] = 'ACK right'
    else: # we must be freaking out if we attempted a bad request, so just e-stop
        send_drive_xhr(generate_drive_xhr('stop'))
        ret_obj['dir'] = 'NACK'
    return jsonify(ret_obj)

if __name__ == "__main__":
    app.run()

