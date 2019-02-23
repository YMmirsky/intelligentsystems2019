# pretend-esp32
## Purpose
Setting up XHR servers
## What's here
1. src/service\_cv\_cmd.py
    * Service cv_cmd requests
2. src/pretend\_drive.py
    * Service handle_update requests, simulating a drive ESP32
## Setup
1. Run run_me.sh
## Calling xhrs, from python
```
import requests
res = requests.post('http://' + ip_addr + ':' + port_no + '/' + endpoint + '?' + arg1 + '=' + arg1_val)
res.text
```
Example
```
import requests
res = requests.post('http://localhost:5000/cv_cmd?dir=stop')
res.text
res = requests.post('http://localhost:5000/cv_cmd?dir=straight')
res.text
res = requests.post('http://localhost:5000/cv_cmd?dir=left')
res.text
res = requests.post('http://localhost:5000/cv_cmd?dir=right')
res.text
```