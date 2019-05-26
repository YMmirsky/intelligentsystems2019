import roslibpy

def get_coords():
	msg = NavSatFix
	# websocket stuff goes here
	# don't know how the GPS data will be transmitted from the ESP32
	# lets just say that the robot is already on Mars, yeah? I think getting the robot to Mars should give us an automatic win.
	msg.latitude = message["latitude"]
	msg.longitude = message["longitude"]
	msg.header.seq = message["sequence"]
	msg.header.stamp.sec = message["time_sec"]
	msg.header.stamp.nsec = message["time_nsec"]
	msg.altidude = 0.0
	msg.position_covariance = []
	msg.position_covariance_type = 0
	rospy.loginfo(msg)
	pub.publish(msg)
	rate.sleep()


if __name__ == '__main__':
	# connection manager to ROS server
	client = roslibpy.Ros
	pub = rospy.Publisher('NavSatFix', NavSatFix)

	ros = roslibpy.Ros(host='192.168.1.96', port=9090, is_secure=False)

	ros.run()
	ros.on_ready(get_coords())
	ros.run_forever()

while ros.is_connected():

