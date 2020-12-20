#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan

def callback(message):
    #get_caller_id(): Get fully resolved name of local node
    rospy.loginfo(rospy.get_caller_id() + "I heard scan")
    
def station():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'station' node so that multiple stations can
    # run simultaneously.
    rospy.init_node('station_scanner', anonymous=True)
    print('scanner')
    rospy.Subscriber("scan", LaserScan, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    station()
