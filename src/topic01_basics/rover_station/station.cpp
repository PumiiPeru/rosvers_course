/*
 * Author: Anis Koubaa for Gaitech EDU
 * Year: 2016
 *
 */

#include "ros/ros.h"
#include "std_msgs/String.h"

// Topic messages callback
void positionCallback(const std_msgs::String::ConstPtr& msg)
{
    ROS_INFO("[station] I heard: [%s]\n", msg->data.c_str());
}

int main(int argc, char **argv)
{
    // Initiate a new ROS node named "station"
	ros::init(argc, argv, "station_node");
	//create a node handle: it is reference assigned to a new node
	ros::NodeHandle node;


    // Subscribe to a given topic, in this case "position".
	//positionCallback: is the name of the callback function that will be executed each time a message is received.
    ros::Subscriber sub = node.subscribe("position", 1000, positionCallback);

    // Enter a loop, pumping callbacks
    ros::spin();

    return 0;
}
