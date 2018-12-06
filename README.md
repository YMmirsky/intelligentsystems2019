# SJSU Robotics 2018 - Cerberus Intelligence System Stack

## 98. Notes
1. Handling XHR requests
    * We use [Flask](http://flask.pocoo.org/)

2. Issuing XHR requests
    * We use [Python Requests](http://docs.python-requests.org/en/master/)
    * To test, we can also use bash `curl`, i.e.
        * `curl --request POST 'http://192.168.43.137/calculator' --data 'operation=\"add\"&a=1&b=2'`

To ROS-ify XHRs is to translate XHRs into topics, service calls, and actions


## 99. Versioning
* 0.0.1 (ETA 2018-11-30)
    * Demonstration of XHRs between ESP32s via ROS environment as an intermediary
        * Accelerometer ROS node `accel_node` interfacing an ESP32, via rospy + requests library; ESP32 continuously writes (streams) acceleration telemetry to this node
        * Servomotor ROS node `servo_node` interfacing an ESP32, via rospy + flask library; ESP32 polling for PWM commands from this node
