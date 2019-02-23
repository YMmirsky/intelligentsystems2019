from flask import Flask, request, render_template, jsonify
import requests

# drive_addr = '127.0.0.1'
# drive_port = '5001'
drive_addr = '192.168.4.1'
drive_port = '80'
drive_endpoint = 'handle_update'

# see pretend_drive.py for description of key values
def generate_drive_xhr(direction):
    dictToSend = dict()
    if direction == 'stop':
        dictToSend['mode'] = '3'
        dictToSend['AXIS_X'] = '0.0'
        dictToSend['AXIS_Y'] = '0.0'
        dictToSend['THROTTLE'] = '0.0'
        dictToSend['button_0'] = '0'
        dictToSend['wheel_A'] = '0'
        dictToSend['wheel_B'] = '0'
        dictToSend['wheel_C'] = '1'
        dictToSend['mast_position'] = '0'
    if direction == 'straight':
        dictToSend['mode'] = '3'
        dictToSend['AXIS_X'] = '0.0'
        dictToSend['AXIS_Y'] = '1.0'
        dictToSend['THROTTLE'] = '0.0'
        dictToSend['button_0'] = '1'
        dictToSend['wheel_A'] = '0'
        dictToSend['wheel_B'] = '0'
        dictToSend['wheel_C'] = '0'
        dictToSend['mast_position'] = '0'
    elif direction == 'left':
        dictToSend['mode'] = '1'
        dictToSend['AXIS_X'] = '-1.0'
        dictToSend['AXIS_Y'] =  '0.0'
        dictToSend['THROTTLE'] =  '0.0'
        dictToSend['button_0'] = '1'
        dictToSend['wheel_A'] = '1'
        dictToSend['wheel_B'] = '1'
        dictToSend['wheel_C'] = '1'
        dictToSend['mast_position'] = '0'
    elif direction == 'right':
        dictToSend['mode'] = '1'
        dictToSend['AXIS_X'] = '1.0'
        dictToSend['AXIS_Y'] = '0.0'
        dictToSend['THROTTLE'] = '0.0'
        dictToSend['button_0'] = '1'
        dictToSend['wheel_A'] = '0'
        dictToSend['wheel_B'] = '1'
        dictToSend['wheel_C'] = '1'
        dictToSend['mast_position'] = '0'
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
    elif count_valid_keys(dictToSend) > 1:
        first_item = True
        for item in dictToSend.items():
            if item[1] != '':
                if first_item:
                    post_str = post_str + item[0] + '=' + item[1]
                    first_item = False
                else:
                    post_str = post_str \
                        +  '&'  + item[0] + '=' + item[1]
    else:
        post_str = post_str + 'button_0=0'
    res = requests.post(post_str)
    print res.text

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

