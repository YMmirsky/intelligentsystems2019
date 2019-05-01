import rospy
import requests
import time
from sensor_msgs.msg import NavSatFix

# TODO: Find compass endpoint and how comms will be handled outbound from the ESP32. 
esp32_ipaddr = "192.168.4.1"

def get_compass():
	compass = requests.post("http://" + esp32_ipaddr + ":80/compass???")
	compass_list = compass.text.split(",")
	return compass_list

def compass_node():
	pub = rospy.Publisher('NavSatFix', NavSatFix)
	rospy.init_node('compass', anonymous = True)
	rate = rospy.Rate(10) # 10hz
	msg = NavSatFix

	while not rospy.is_shutdown():
		compass = get_compass()
		rospy.loginfo(msg)
		pub.publish(msg)
		rate.sleep()

if __name__ == '__main__':
	compass_node()