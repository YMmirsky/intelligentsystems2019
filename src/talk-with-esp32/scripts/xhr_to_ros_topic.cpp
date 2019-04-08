#include <resource_retriever/retriever.h>
#include <ros/console.h>

// code from http://wiki.ros.org/resource_retriever/Tutorials/Retrieving%20Files
int main(int argc, char** argv)
{
  ros::init(argc, argv, "XHR_comm");
  ros::NodeHandle node_handle

  resource_retriever::Retriever r;
  resource_retriever::MemoryResource resource;

  ros::Publisher pub = node_handle.advertise<int>("accel", 100);

  // publishing rate in hz
  ros::Rate rate(10);

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

    int accel = resource.data.get();
    pub.publish(accel);

    rate.sleep();
    
    //FILE* f = fopen("out.txt", "w");
    //fwrite(resource.data.get(), resource.size, 1, f);
    //fclose(f);
    //ROS_INFO("Wrote data from package://resource_retriever/test/test.txt to out.txt");
  }
  
}
