#!/usr/bin/env python

import rospy
import requests
import time 

from std_msgs.mgs import String
#import numpy as np  

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + "Drive direction", data.data)

def drive_listener():
	rospy.init_node('drive_listener')
	rospy.Subscriber("drive_directions", String)
	rospy.spin()

	drive_data d_data
	d_data.mode = DM_DRIVE # set robot to standard drive mode. 

	# TODO: Check with mission control about joystick inputs 
	requests.post("http:// blah blah blah :80/ blah")

if __name == '__main__':
	drive_listener()

struct drive_data:
	mode
	AXIS_X 
	AXIS_Y
	THROTTLE
	button_0
	wheel_A
	wheel_B
	wheel_C
	mast_position