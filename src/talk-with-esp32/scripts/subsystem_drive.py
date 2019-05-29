#!/usr/bin/env python

import rospy, math, requests, time
import numpy as np
import tf.transformations
from std_msgs.msg import String
from geometry_msgs.msg import Twist

esp32_ipaddr = "192.168.4.1"
topic_to_listen = "cmd_vel"
wheelbase = 0.88537 # distance in meters from the midpoint of the front wheels to the back wheel
					# used for converting linear.x and angular.z commands to steering angles

class drive_data:
	def __init__(self):	
		"""
		List of drive mode enums:
		DM_DEBUG = 0
		DM_CRAB = 1
		DM_SPIN = 2
		DM_DRIVE = 3
		"""
		# code taken from https://github.com/SJSURobotics2019/missioncontrol2019/blob/drive/src/modules/Drive/joystick_new.js
		self.mode = 0
		self.T_MAX = 20
		self.AXIS_X = 0.0
		self.AXIS_Y = 0.0
		self.YAW = 0
		self.THROTTLE = 0.0
		self.BRAKES = 0
		# on the physical joystick the button acts as a dead man's switch
		self.MAST_POSITION = 0
		self.TRIGGER = 0
		self.REVERSE = 0
		# in drive mode, this determines which wheel is the rear wheel
		# this may be changed depending on the position of the RealSense camera on the rover
		self.wheel_A = 0
		self.wheel_B = 0
		self.wheel_C = 1

# code taken from http://wiki.ros.org/teb_local_planner/Tutorials/Planning%20for%20car-like%20robots
def convert_trans_rot_vel_to_steering_angle(v, omega):
	if omega == 0 or v == 0:
		return 0
	radius = v / omega
	return math.atan(wheelbase / radius)

# converts the steering angle calculated in the above function to an x-axis joystick value.
# 45 degrees to the left = -1, 45 degrees to the right = 1. I think...
def normalize_steering(steering_angle):
	min_steer = -1
	max_steer = 1
	return ((steering_angle - min_steer) / (max_steer - min_steer))

# msg is the twist message. Look at the loginfo statements for info on whats inside msg
def callback(msg):
	# each element in the message is a float64
	#now = rospy.get_rostime()
	#rospy.loginfo("Recieved twist message at %i %i", now.secs, now,nsecs)
	rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
	rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))
	d_data = drive_data()
	# info about drive modes from mission control: https://github.com/SJSURobotics2019/missioncontrol2019/blob/master/src/modules/Drive/model.js
	d_data.mode = 3 # set robot to standard drive mode. 
	# pin the throttle to maximum, let position of joystick y-axis set the speed
	# Throttle ranges from 0 (max reverse) or 1 (max forward)
	d_data.THROTTLE = 0

	# TODO: Ask Nelson on how speed will be received. Will I need to convert it to joystick throttle inputs?
	# According to Colin: The joystick goes from 1 (zero speed) to -1 (full speed)
	# Forward motion is regulated by the joystick y-axis, side motion is the joystick x-axis. 
	# TODO: Figure out the range of msg.linear.x so it can be remapped

	# I assume(?) that the max linear.x speed is 5 so I'm just going with that don't @ me
	# The joystick axis are inverted so we need to invert this YEAH LETS DO THAT
	# note that axis_y is front and back axis, axis_x is side to side
	d_data.AXIS_Y = -msg.linear.x / 5
	steering_angle = convert_trans_rot_vel_to_steering_angle(msg.linear.x, msg.angular.z)
	d_data.AXIS_X = normalize_steering(steering_angle)
	rospy.loginfo("Steering angle: %f, steering angle scaled to joystick: %f"%(steering_angle, d_data.AXIS_X))

	# change mode to spin in place
	if msg.linear.x == 0 and msg.linear.y == 0 and msg.angular.z != 0:
		d_data.mode = 2
	# no movement commands mean to brake immediately
	if msg.linear.x == 0 and msg.linear.y == 0 and msg.angular.z == 0:
		d_data.BRAKES = 0

	d_data_str = "mode=%i&T_MAX=%i&AXIS_X=%f&AXIS_Y=%f&YAW=%f&THROTTLE=%f&BRAKES=%r&MAST_POSITION=%f&TRIGGER=%r&REVERSE=%r&wheel_A=%i&wheel_B=%i&wheel_C=%i" % (
		d_data.mode, d_data.T_MAX, d_data.AXIS_X, d_data.AXIS_Y, d_data.YAW, d_data.THROTTLE, d_data.BRAKES, 
		d_data.MAST_POSITION, d_data.TRIGGER, d_data.REVERSE, d_data.wheel_A, d_data.wheel_B, d_data.wheel_C)

	# ip address taken from https://github.com/SJSURobotics2019/missioncontrol2019/blob/master/src/modules/Drive/DriveModule.jsx#L31
	# endpoint taken from https://github.com/SJSURobotics2019/missioncontrol2019/blob/master/src/modules/Drive/joystick.js#L139
	requests.post("http://" + esp32_ipaddr + ":80/handle_update?" + d_data_str)
	rospy.loginfo("http://" + esp32_ipaddr + ":80/handle_update?" + d_data_str)

def drive_listener():
	rospy.init_node('drive_listener')
	rospy.Subscriber(topic_to_listen, Twist, callback)
	rospy.loginfo("Node 'drive_listener' started.\nListening to '%s'. talking to Drive ESP32 on IP address %s", topic_to_listen, esp32_ipaddr)
	rospy.spin()

if __name__ == '__main__':
	drive_listener()
