#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix

""" documentatnion of sensor_msgs/NavSatFix:
http://docs.ros.org/api/sensor_msgs/html/msg/NavSatFix.html """

def get_coords():
	gps = requests.post("http://blahblahblah:80/GPS???")
	gps_list = res.text.split(",")
	return gps_list

def GPS_node():
	pub = rospy.Publisher('NavSatFix', NavSatFix)
	rospy.init_node('GPS', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	msg = NavSatFix

	while not rospy.is_shutdown():
		gps_list = get_coords()
		# websocket stuff goes here
		# don't know how the GPS data will be transmitted from the ESP32 but who cares HEYOOOOO
		# lets just say that the robot is already on Mars, yeah?
		msg.latitude = 0.0
		msg.longitude = 0.0
		msg.altidude = 0.0
		msg.position_covariance = []
		msg.position_covariance_type = 0
		rospy.loginfo(msg)
		pub.publish(msg)
		rate.sleep()

if __name__ == '__main__':
	GPS_node()