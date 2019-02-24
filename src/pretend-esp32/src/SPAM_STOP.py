import requests
import time

# drive_addr = '127.0.0.1'
# drive_port = '5001'
drive_addr = '192.168.4.1'
drive_port = '80'
drive_endpoint = 'handle_update'

MODE_DRIVE = '3'
MODE_SPIN = '2'
MODE_CRAB = '1'
MODE_DEBUG = '0'
CURRENT_MODE = MODE_DEBUG

DRIVE_ENABLED = True

# see pretend_drive.py for description of key values
def generate_drive_xhr(direction):
    dictToSend = dict()
    if direction == 'stop':
        dictToSend['mode'] = CURRENT_MODE
        dictToSend['AXIS_X'] = '0.0'
        dictToSend['AXIS_Y'] = '0.0'
        dictToSend['THROTTLE'] = '0.0'
        dictToSend['button_0'] = '0'
        dictToSend['wheel_A'] = '0'
        dictToSend['wheel_B'] = '0'
        dictToSend['wheel_C'] = '1'
        dictToSend['mast_position'] = '0'
    elif direction == 'set_mode_no_throttle':
        dictToSend['mode'] = CURRENT_MODE
        dictToSend['AXIS_X'] = '0.0'
        dictToSend['AXIS_Y'] = '0.0'
        dictToSend['THROTTLE'] = '0.0'
        dictToSend['button_0'] = '1'
        dictToSend['wheel_A'] = '0'
        dictToSend['wheel_B'] = '0'
        dictToSend['wheel_C'] = '1'
        dictToSend['mast_position'] = '0'
    elif direction == 'straight':
        dictToSend['mode'] = CURRENT_MODE
        dictToSend['AXIS_X'] = '0.0'
        dictToSend['AXIS_Y'] = '1.0'
        dictToSend['THROTTLE'] = '0.0'
        dictToSend['button_0'] = '1'
        dictToSend['wheel_A'] = '0'
        dictToSend['wheel_B'] = '0'
        dictToSend['wheel_C'] = '0'
        dictToSend['mast_position'] = '0'
    elif direction == 'left':
        dictToSend['mode'] = CURRENT_MODE
        dictToSend['AXIS_X'] = '-1.0'
        dictToSend['AXIS_Y'] =  '0.0'
        dictToSend['THROTTLE'] =  '0.5'
        dictToSend['button_0'] = '1'
        dictToSend['wheel_A'] = '0'
        dictToSend['wheel_B'] = '0'
        dictToSend['wheel_C'] = '1'
        dictToSend['mast_position'] = '0'
    elif direction == 'right':
        dictToSend['mode'] = CURRENT_MODE
        dictToSend['AXIS_X'] = '1.0'
        dictToSend['AXIS_Y'] = '0.0'
        dictToSend['THROTTLE'] = '0.5'
        dictToSend['button_0'] = '1'
        dictToSend['wheel_A'] = '0'
        dictToSend['wheel_B'] = '0'
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

while True:
    send_drive_xhr(generate_drive_xhr('set_mode_no_throttle'))
    time.sleep(0.1)
    send_drive_xhr(generate_drive_xhr('stop'))
