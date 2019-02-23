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
        ret_obj['mode'] = 'ACK spin'
    elif '2' == mode_val:
        ret_obj['mode'] = 'ACK crab'
    elif '3' == mode_val:
        ret_obj['mode'] = 'ACK drive'
    else:
        ret_obj['mode'] = 'NACK unrecognized'
    # get AXIS_0
    AXIS_0_val = str(request.args.get('AXIS_0'))
    print 'AXIS_0_val: ' + AXIS_0_val
    try:
        AXIS_0_val = float(AXIS_0_val)
        if float(AXIS_0_val) < 0.0:
            ret_obj['AXIS_0'] = 'ACK CCW'
        elif float(AXIS_0_val) == 0.0:
            ret_obj['AXIS_0'] = 'ACK straight'
        elif float(AXIS_0_val) > 0.0:
            ret_obj['AXIS_0'] = 'ACK CW'
        else:
            ret_obj['AXIS_0'] = 'NACK'
    except ValueError:
        ret_obj['AXIS_0'] = 'NACK not a float'
    # get AXIS_1
    AXIS_1_val = str(request.args.get('AXIS_1'))
    print 'AXIS_1_val: ' + AXIS_1_val
    try:
        AXIS_1_val = float(AXIS_1_val)
        if float(AXIS_1_val) < 0.0:
            ret_obj['AXIS_1'] = 'ACK forward'
        elif float(AXIS_1_val) == 0.0:
            ret_obj['AXIS_1'] = 'ACK stop'
        elif float(AXIS_1_val) > 0.0:
            ret_obj['AXIS_1'] = 'ACK reverse'
        else:
            ret_obj['AXIS_1'] = 'NACK'
    except ValueError:
        ret_obj['AXIS_1'] = 'NACK not a float'
    # get AXIS_3
    AXIS_3_val = str(request.args.get('AXIS_3'))
    print 'AXIS_3_val: ' + AXIS_3_val
    try:
        AXIS_3_val = float(AXIS_3_val)
        if float(AXIS_3_val) < 0.0:
            ret_obj['AXIS_3'] = 'ACK 51%-100%'
        elif float(AXIS_1_val) == 0.0:
            ret_obj['AXIS_3'] = 'ACK 50%'
        elif float(AXIS_1_val) > 0.0:
            ret_obj['AXIS_3'] = 'ACK 0%-49%'
        else:
            ret_obj['AXIS_3'] = 'NACK'
    except ValueError:
        ret_obj['AXIS_3'] = 'NACK not a float'
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

