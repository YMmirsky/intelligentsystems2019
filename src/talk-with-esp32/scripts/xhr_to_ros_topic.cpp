#define _GLIBCXX_USE_C99 1

#include "ros/ros.h"
#include "std_msgs/String.h"
#include <iostream>
#include <sstream>
#include <string>
#include <resource_retriever/retriever.h>

// code from http://wiki.ros.org/resource_retriever/Tutorials/Retrieving%20Files
int main(int argc, char** argv)
{
  ros::init(argc, argv, "accel");
  ros::NodeHandle node_handle;

  resource_retriever::Retriever r;
  resource_retriever::MemoryResource resource;

  ros::Publisher pub = node_handle.advertise<double>("imu/raw", 1);

  // publishing rate in hz
  ros::Rate rate(100);

  std::ostringstream os;

  while(ros::ok())
  {
    try
    {
      // address taken from line 41 of Nelson's test.py
      resource = r.get("http://192.168.0.192:80/accel"); 
    }
    catch (resource_retriever::Exception& e)
    {
      ROS_ERROR("Failed to retrieve file: %s", e.what());
      return 1;
    }

    unsigned char* accel = resource.data.get();
    
    for (int i = 0; i < resource.size; i++)
    {
      os << i;
    }
    
    //double accel_dbl;
    //os >> accel_dbl;

    //std::string accel_string = std::string str(accel, resource.size);
    std::string accel_string(os.str());
    double accel_dbl = std::stod(accel_string);
    pub.publish(accel_dbl);

    rate.sleep();
    
    //FILE* f = fopen("out.txt", "w");
    //fwrite(resource.data.get(), resource.size, 1, f);
    //fclose(f);
    //ROS_INFO("Wrote data from package://resource_retriever/test/test.txt to out.txt");
  }
  
}
