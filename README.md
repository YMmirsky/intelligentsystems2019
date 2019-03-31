# SJSU Robotics 2018 - Cerberus Intelligence System Stack

## 1. Getting started
### 1. Pre-reqs
1. Linux environment
2. ROS-kinetic
3. [Intel RealSense SDK 2.0](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md#installing-the-packages)

### 2. ROS packages in this workspace
* pretend-esp32
* talk-with-esp32
* realsense2\_camera
  * from [this repo](https://github.com/intel-ros/realsense)
  * Using commit hash 855cf51

### 3. Download this project
```
git clone --recursive <the_git_repo>
cd <repo_local_directory>/src/realsense
git checkout 855cf51
cd -
```
### 4. Set it up
`catkin_make`

### 5. ROS tips
#### rosbag
* Replaying recordings
  * `$ rosbag play path/to/file.bag`
* Recording messages
  * `$ rosbag record <list of topics>`
* Topics to record
  * /camera/color/camera\_info
  * /camera/color/image\_raw
  * /camera/depth/camera\_info
  * /camera/depth/image\_rect\_raw
  * /tf\_static

## 96. RealSense
### Visualize with Intel's viewer
`$ realsense-viewer`

### Bring-up
`$ roslaunch realsense2_camera rs_camera.launch filters:=spatial,temporal,pointcloud`

### Visualize in ROS rviz
`$ roslaunch realsense2_camera view_d435_model.launch`
You'll need to add the following to the visualizer:
* DepthCloud
  * /camera/depth/image\_rect\_raw as the Depth Map Topic
  * /camera/color/image\_raw as the Color Image Topic
* Image
  * /camera/color/image\_raw as the Image Topic

### Attributes to keep in mind
* Point cloud is relatively noisy
* Minimum distance: 20 cm
* Tolerance: +/- 5 cm

### Calibration
[See this link](https://github.com/IntelRealSense/librealsense/issues/2329)

## 97. E-Stop
```
$ python src/pretend-esp32/src/SPAM_STOP.py
```

## 98. Notes
### 1. Handling XHR requests
    * We use [Flask](http://flask.pocoo.org/)

### 2. Issuing XHR requests
    * We use [Python Requests](http://docs.python-requests.org/en/master/)
    * To test, we can also use bash `curl`, i.e.
        * `curl --request POST 'http://192.168.43.137/calculator' --data 'operation=\"add\"&a=1&b=2'`

To ROS-ify XHRs is to translate XHRs into topics, service calls, and actions

### 3. Network setup during development
This is in regards to RPi <> CV <> Autonomy
    * RPi eth0 to Autonomy enx00e07cc8718a
    * Autonomy wlp4s0 to Hotspot
    * CV wifi to Hotspot

Use of `iptables` to expose RPi to CV, routing performed by Autonomy. In the following example, 10.42.0.166 is RPi's IPv4 address, and 80 is the port. We wish to forward all requests to Autonomy at port 50000 to the RPi.
```
sudo iptables -t nat -A PREROUTING -p tcp -i wlp4s0 --dport 50000 -j DNAT --to-destination 10.42.0.166:80
 sudo iptables -A FORWARD -p tcp -d 10.42.0.166 --dport 80 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
 sudo iptables -t nat -A PREROUTING -p udp -i wlp4s0 --dport 50000 -j DNAT --to-destination 10.42.0.166:80
 sudo iptables -A FORWARD -p udp -d 10.42.0.166 --dport 80 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
sudo iptables -S FORWARD
```
The last command returned the following:
```
-P FORWARD ACCEPT
-A FORWARD -d 10.42.0.0/24 -o enx00e07cc8718a -m state --state RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -s 10.42.0.0/24 -i enx00e07cc8718a -j ACCEPT
-A FORWARD -i enx00e07cc8718a -o enx00e07cc8718a -j ACCEPT
-A FORWARD -o enx00e07cc8718a -j REJECT --reject-with icmp-port-unreachable
-A FORWARD -i enx00e07cc8718a -j REJECT --reject-with icmp-port-unreachable
-A FORWARD -d 10.42.0.166/32 -p tcp -m tcp --dport 80 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -d 10.42.0.166/32 -p udp -m udp --dport 80 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT
```
We wish to remove all listings that reject our port forwarding, which are appended at lines 4 and 5, so:
```
sudo iptables -D FORWARD 5
sudo iptables -D FORWARD 4
```

## 99. Versioning
* 0.0.1 (ETA 2018-11-30)
    * Demonstration of XHRs between ESP32s via ROS environment as an intermediary
        * Accelerometer ROS node `accel_node` interfacing an ESP32, via rospy + requests library; ESP32 continuously writes (streams) acceleration telemetry to this node
        * Servomotor ROS node `servo_node` interfacing an ESP32, via rospy + flask library; ESP32 polling for PWM commands from this node
