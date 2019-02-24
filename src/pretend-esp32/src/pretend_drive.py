from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
app.debug = True

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        name = request.form["name"]
        return name + " Hello"
    return render_template("index.html")

@app.route("/handle_update", methods=['GET', 'POST'])
def index2():
    ret_obj = dict()
    # get mode
    mode_val = str(request.args.get('mode'))
    print 'mode_val: ' + mode_val
    if '0' == mode_val:
        ret_obj['mode'] = 'ACK debug'
    elif '1' == mode_val:
        ret_obj['mode'] = 'ACK crab'
    elif '2' == mode_val:
        ret_obj['mode'] = 'ACK spin'
    elif '3' == mode_val:
        ret_obj['mode'] = 'ACK drive'
    else:
        ret_obj['mode'] = 'NACK unrecognized'
    # get AXIS_X
    AXIS_X_val = str(request.args.get('AXIS_X'))
    print 'AXIS_X_val: ' + AXIS_X_val
    try:
        AXIS_X_val = float(AXIS_X_val)
        if float(AXIS_X_val) < 0.0:
            ret_obj['AXIS_X'] = 'ACK CCW'
        elif float(AXIS_X_val) == 0.0:
            ret_obj['AXIS_X'] = 'ACK straight'
        elif float(AXIS_X_val) > 0.0:
            ret_obj['AXIS_X'] = 'ACK CW'
        else:
            ret_obj['AXIS_X'] = 'NACK'
    except ValueError:
        ret_obj['AXIS_X'] = 'NACK not a float'
    # get AXIS_Y
    AXIS_Y_val = str(request.args.get('AXIS_Y'))
    print 'AXIS_Y_val: ' + AXIS_Y_val
    try:
        AXIS_Y_val = float(AXIS_Y_val)
        if float(AXIS_Y_val) < 0.0:
            ret_obj['AXIS_Y'] = 'ACK forward'
        elif float(AXIS_Y_val) == 0.0:
            ret_obj['AXIS_Y'] = 'ACK stop'
        elif float(AXIS_Y_val) > 0.0:
            ret_obj['AXIS_Y'] = 'ACK reverse'
        else:
            ret_obj['AXIS_Y'] = 'NACK'
    except ValueError:
        ret_obj['AXIS_Y'] = 'NACK not a float'
    # get THROTTLE
    THROTTLE_val = str(request.args.get('THROTTLE'))
    print 'THROTTLE_val: ' + THROTTLE_val
    try:
        THROTTLE_val = float(THROTTLE_val)
        if float(THROTTLE_val) < 0.0:
            ret_obj['THROTTLE'] = 'ACK 51%-100%'
        elif float(AXIS_Y_val) == 0.0:
            ret_obj['THROTTLE'] = 'ACK 50%'
        elif float(AXIS_Y_val) > 0.0:
            ret_obj['THROTTLE'] = 'ACK 0%-49%'
        else:
            ret_obj['THROTTLE'] = 'NACK'
    except ValueError:
        ret_obj['THROTTLE'] = 'NACK not a float'
    # get button_0
    button_0_val = str(request.args.get('button_0'))
    print 'button_0_val: ' + button_0_val
    try:
        button_0_val = int(button_0_val)
        if float(button_0_val) == 0:
            ret_obj['button_0'] = 'ACK drive disabled'
        elif float(button_0_val) == 1:
            ret_obj['button_0'] = 'ACK drive enabled'
        else:
            ret_obj['button_0'] = 'NACK bad value'
    except ValueError:
        ret_obj['button_0'] = 'NACK not an int'
    # return acks/nacks
    return jsonify(ret_obj)

if __name__ == "__main__":
    app.run()

