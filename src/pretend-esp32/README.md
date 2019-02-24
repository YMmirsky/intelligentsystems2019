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

## How does drive work right now (2019-02-23)
### Switching modes
1. Send `button_0=0&...`
    * Set the brakes
2. Send `button_0=1&mode=DESIRED_MODE&...`
    * Initiate mode change, but this will activate the motors 
3. Send `button_0=0&mode=DESIRED_MODE&...`
    * Deactivate the motors 
4. Wait ten seconds
    * Mode changes takes up to ten seconds.
### Repeating XHRs
It is recommended to repeat XHRs at least twice to ensure the command is sent.

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