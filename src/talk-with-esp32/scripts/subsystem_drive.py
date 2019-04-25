#!/usr/bin/env python

import rospy
import requests
import time 
import numpy as np
import tf.transformations
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def callback(msg):
	rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
	rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))
	d_data = drive_data()
	# info about drive modes from mission control: https://github.com/SJSURobotics2019/missioncontrol2019/blob/master/src/modules/Drive/model.js
	d_data.mode = DM_DRIVE # set robot to standard drive mode. 

	# TODO: Ask Nelson on how speed will be received. Will I need to convert it to joystick throttle inputs?
	# According to Colin: The joystick goes from 1 (zero speed) to -1 (full speed)
	# Forward motion is regulated by the joystick y-axis, side motion is from the x-axis. 
	# TODO: Figure out the range of msg.linear.x so it can be remapped
	if abs(msg.linear.x) > 1.0:
		rospy.loginfo("throttle is out of range: " + msg.linear.x)

	# set throttle to maximum, let position of joystick y-axis set the speed
	d_data.THROTTLE = -1

	# edge case if the rover is meaning to spin in place, similar to a differential drive turtlebot. Might not need?
	if msg.linear.x == 0 && msg.linear.y == 0 && msg.linear.z == 0 && msg.angular.x != 0:
		d_data.mode = DM_CRAB

	""" 
	geometry_msgs/Twist contains:
	Vector3 linear - represents linear part of velocity [m/s]
	Vector3 angular - represents angular part of velocity [rad/s]
	"""

	# ip address taken from https://github.com/SJSURobotics2019/missioncontrol2019/blob/master/src/modules/Drive/DriveModule.jsx#L31
	# endpoint taken from https://github.com/SJSURobotics2019/missioncontrol2019/blob/master/src/modules/Drive/joystick.js#L139
	requests.post("http://" + esp32_ipaddr + ":80/handle_update?" + d_data)


def drive_listener():
	esp32_ipaddr = "192.168.4.1"
	rospy.init_node('drive_listener')
	rospy.Subscriber("drive_directions", Twist, callback)
	rospy.loginfo("Node 'drive_listener' started. \n listening to 'drive_directions'. talking to ESP32 on ip address %s", esp32_ipaddr)
	rospy.spin()

if __name__ == '__main__':
	
class drive_data:
	def __init__(self):	
		mode = 0
		AXIS_X = 0
		AXIS_Y = 0
		THROTTLE = 0
		button_0 = 0
		wheel_A = 0
		wheel_B = 0
		wheel_C = 0
		mast_position = 0