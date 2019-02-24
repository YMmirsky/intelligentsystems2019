import requests
import time

# drive_addr = '127.0.0.1'
# drive_port = '5001'
drive_addr = '192.168.4.1'
drive_port = '80'
drive_endpoint = 'handle_update'

post_str = 'http://'   \
    + drive_addr + ':' \
    + drive_port + '/' \
    + drive_endpoint + '?button_0=0'

while True:
    res = requests.post(post_str)
    print res.text
    time.sleep(0.1)
