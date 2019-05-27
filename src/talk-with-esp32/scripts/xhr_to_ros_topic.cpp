#define _GLIBCXX_USE_C99 1

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Int32.h"
#include "sensor_msgs/NavSatFix.h"
#include <iostream>
#include <sstream>
#include <string>

#include <curlpp/cURLpp.hpp>
#include <curlpp/Options.hpp>
#include <curlpp/Easy.hpp>
#include <curlpp/Exception.hpp>
//#include <resource_retriever/retriever.h>

// code from http://wiki.ros.org/resource_retriever/Tutorials/Retrieving%20Files
int main(int argc, char** argv)
{
  ros::init(argc, argv, "accel");
  ros::NodeHandle node_handle;

  //resource_retriever::Retriever r;
  //resource_retriever::MemoryResource resource;

  ros::Publisher pub = node_handle.advertise<std_msgs::String>("NavSatFix", 1);

  // publishing rate in hz
  ros::Rate loop_rate(10);

  std::ostringstream os;
  std::string accel_string;

  std::stringstream result;

  std::string url = "http://192.168.4.1:80/update_name";
  int count = 0;

  std_msgs::Int32 accel_dbl;

  sensor_msgs::NavSatFix gps;
  //std_msgs::String accel_string;

  while(ros::ok())
  {
    try 
    {
      curlpp::Cleanup cleaner;
      curlpp::Easy request;
      
      request.setOpt(new curlpp::options::Url(url)); 
      request.setOpt(new curlpp::options::Verbose(true)); 
      
      std::list<std::string> header; 
      header.push_back("Content-Type: application/octet-stream"); 
      
      request.setOpt(new curlpp::options::HttpHeader(header)); 
      
      //request.setOpt(new curlpp::options::PostFields("abcd"));
      //request.setOpt(new curlpp::options::PostFieldSize(5));
      request.setOpt(new curlpp::options::WriteStream(&result));
      request.perform(); 

      //const std::string tmp = result.str();
      //const char* cstr_result = result.c_str();
      //ROS_INFO(tmp);
    }
    catch ( curlpp::LogicError & e )
    {
      ROS_INFO(e.what());
    }
    catch ( curlpp::RuntimeError & e )
    {
      ROS_INFO(e.what());
    }

    /*try
    {
      // address taken from line 41 of Nelson's test.py
      resource = r.get("http://192.168.4.1:80/update_name"); 
    }
    catch (resource_retriever::Exception& e)
    {
      ROS_ERROR("Failed to retrieve file: %s", e.what());
      return 1;
    }

    unsigned char* accel = resource.data.get();
    */
    /*for (int i = 0; i < resource.size; i++)
    {
      os << i;
    }
    //std::string accel_string;
    os >> accel_string;

    accel_string = std::to_string(accel);
    */

    //union { void *pl int i; } converter;
    //converter.p = accel;


    //double accel_int = reinterpret_cast<double>(accel);
    //std::istringstream iss (accel_string);
    //iss >> accel_int;
    //double accel_int = *(double*)accel;


    //std::string accel_string(os.str());
    //accel_dbl.data = accel_int;
    //pub.publish(accel_dbl);

    loop_rate.sleep(); 
    
    //FILE* f = fopen("out.txt", "w");
    //fwrite(resource.data.get(), resource.size, 1, f);
    //fclose(f);
    //ROS_INFO("Wrote data from package://resource_retriever/test/test.txt to out.txt");
  }
  
}
