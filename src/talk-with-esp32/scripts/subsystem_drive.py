#!/usr/bin/env python

import rospy
import requests
import time 
import numpy as np
import tf.transformations
from std_msgs.msg import String
from geometry_msgs.msg import Twist

"""
DM_DEBUG = 0
DM_CRAB = 1
DM_SPIN = 2
DM_DRIVE = 3
"""
esp32_ipaddr = "192.168.4.1"

class drive_data:
	def __init__(self):	
		self.mode = 0
		self.AXIS_X = 0.0
		self.AXIS_Y = 0.0
		self.THROTTLE = 0.0
		self.button_0 = 1
		# in drive mode, this determines which wheel 
		self.wheel_A = 0
		self.wheel_B = 0
		self.wheel_C = 1
		self.mast_position = 0

def callback(msg):
	# each element in the message is a float64
	rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
	rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))
	d_data = drive_data()
	# info about drive modes from mission control: https://github.com/SJSURobotics2019/missioncontrol2019/blob/master/src/modules/Drive/model.js
	d_data.mode = 3 # set robot to standard drive mode. 

	# TODO: Ask Nelson on how speed will be received. Will I need to convert it to joystick throttle inputs?
	# According to Colin: The joystick goes from 1 (zero speed) to -1 (full speed)
	# Forward motion is regulated by the joystick y-axis, side motion is from the x-axis. 
	# TODO: Figure out the range of msg.linear.x so it can be remapped
	""" 
	geometry_msgs/Twist contains:
	Vector3 linear - represents linear part of velocity [m/s]
	Vector3 angular - represents angular part of velocity [rad/s]
	"""
	# I assume(?) that the max linear.x speed is 5 so I'm just going with that don't @ me
	# The joystick axis are inverted so we need to invert this YEAH LETS DO THAT
	d_data.AXIS_Y = -msg.linear.x / 5

	# set throttle to maximum, let position of joystick y-axis set the speed
	# Throttle ranges from 0 (max reverse) or 1 (max forward)
	d_data.THROTTLE = 0
	# edge case if the rover is meaning to spin in place, similar to a differential drive turtlebot. Might not need?
	if msg.linear.x == 0 and msg.linear.y == 0 and msg.linear.z == 0 and msg.angular.x != 0:
		d_data.mode = 2
	# no movement commands mean to brake immediately
	if msg.linear.x == 0 and msg.linear.y == 0 and msg.linear.z == 0 and msg.angular.x == 0:
		d_data.button_0 = 0
	
	rospy.loginfo(d_data.AXIS_Y)

	d_data_str = 'mode=%i&AXIS_X=%f&AXIS_Y=%f&THROTTLE=%f&button_0=%r&wheel_A=%i&wheel_B=%i&wheel_C=%i&mast_position=%d' % (d_data.mode, d_data.AXIS_X, d_data.AXIS_Y, d_data.THROTTLE, d_data.button_0, d_data.wheel_A, d_data.wheel_B, d_data.wheel_C, d_data.mast_position)

	# ip address taken from https://github.com/SJSURobotics2019/missioncontrol2019/blob/master/src/modules/Drive/DriveModule.jsx#L31
	# endpoint taken from https://github.com/SJSURobotics2019/missioncontrol2019/blob/master/src/modules/Drive/joystick.js#L139
	requests.post("http://" + esp32_ipaddr + ":80/handle_update?" + d_data_str)
	rospy.loginfo("http://" + esp32_ipaddr + ":80/handle_update?" + d_data_str)

def drive_listener():
	
	rospy.init_node('drive_listener')
	rospy.Subscriber("drive_directions", Twist, callback)
	rospy.loginfo("Node 'drive_listener' started. \n listening to 'drive_directions'. talking to ESP32 on ip address %s", esp32_ipaddr)
	rospy.spin()

if __name__ == '__main__':
	drive_listener()

