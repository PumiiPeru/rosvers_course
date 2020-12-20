#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def position_callback(message):
    #get_caller_id(): Get fully resolved name of local node
    rospy.loginfo(rospy.get_caller_id() + " Information from the rover '  %s ' - Reported", message.data)
    
def station():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'station' node so that multiple stations can
    # run simultaneously.
    rospy.init_node('station', anonymous=True)

    rospy.Subscriber("position", String, position_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    station()
