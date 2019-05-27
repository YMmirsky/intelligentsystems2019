#define _GLIBCXX_USE_C99 1

#include "ros/ros.h"
#include "sensor_msgs/NavSatFix.h"
#include <iostream>
#include <sstream>
#include <string>
#include <stdio.h>
#include <stdint.h>

#include <curl/curl.h>
#include <curl/easy.h>
#include <memory>

struct MemoryStruct {
  char *memory;
  size_t size;
};
 
static size_t
WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
  size_t realsize = size * nmemb;
  struct MemoryStruct *mem = (struct MemoryStruct *)userp;
 
  char *ptr = (char*)realloc(mem->memory, mem->size + realsize + 1);
  if(!ptr) {
    /* out of memory! */ 
    printf("not enough memory (realloc returned NULL)\n");
    return 0;
  }
 
  mem->memory = ptr;
  memcpy(&(mem->memory[mem->size]), contents, realsize);
  mem->size += realsize;
  mem->memory[mem->size] = 0;
 
  return realsize;
}

int main(int argc, char** argv)
{
  ros::init(argc, argv, "accel");
  ros::NodeHandle node_handle;

  ros::Publisher pub = node_handle.advertise<sensor_msgs::NavSatFix>("NavSatFix", 1000);

  // publishing rate in hz
  ros::Rate loop_rate(10);
  int count = 0;

  CURL *curl = curl_easy_init();
  CURLcode res;
  std::string response_str;
  struct MemoryStruct chunk;

  sensor_msgs::NavSatFix GPS;

  const char *url = "http://192.168.4.1:80/update_name";
  while(ros::ok())
  {
    if (curl)
    {
      chunk.memory = (char*)malloc(1);  /* will be grown as needed by realloc above */ 
      chunk.size = 0;    /* no data at this point */

      /* First set the URL that is about to receive our POST. This URL can
       just as well be a https:// URL if that is what should receive the
       data. */ 
      curl_easy_setopt(curl, CURLOPT_FAILONERROR, 1);
      curl_easy_setopt(curl, CURLOPT_URL, url);
      /* Now specify the POST data */ 
      curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "name=grips");
   
      /* send all data to this function  */ 
      curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);

      /* we pass our 'chunk' struct to the callback function */ 
      curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

      /* some servers don't like requests that are made without a user-agent
       field, so we provide one */ 
      curl_easy_setopt(curl, CURLOPT_USERAGENT, "libcurl-agent/1.0");
      
      /* Perform the request, res will get the return code */ 
      res = curl_easy_perform(curl);

      /* Check for errors */ 
      if(res != CURLE_OK)
        fprintf(stderr, "curl_easy_perform() failed: %s\n",
                curl_easy_strerror(res));
      else
        printf("%s\n", chunk.memory);
      ROS_ERROR_STREAM("Node 'GPS' started. Talking to GPS ESP32 on IP address ");

      std::stringstream ss(chunk.memory);
      std::vector<float> coords;
      float i;
      while (ss >> i)
      {
        coords.push_back(i);
        if (ss.peek() == ',')
          ss.ignore();
      }
      GPS.latitude = coords[0];
      GPS.longitude = coords[1];
      GPS.altitude = 0;
      GPS.position_covariance = {0,0,0,0,0,0,0,0,0};
      pub.publish(GPS);
    }
    loop_rate.sleep();
  }
}