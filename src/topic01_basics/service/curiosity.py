#!/usr/bin/env python

import sys
import rospy
from rosvers_course.srv import ShortDist
from rosvers_course.srv import ShortDistRequest
from rosvers_course.srv import ShortDistResponse
import math

def pytha_client(x, y, m, n):
    rospy.wait_for_service('pytha')
    try:
        pytha = rospy.ServiceProxy('pytha', ShortDist)
        resp1 = pytha(x, y, m, n)
        return resp1.dist
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return

if __name__ == "__main__":
    if len(sys.argv) == 5:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        m = int(sys.argv[3])
        n = int(sys.argv[4])
    else:
        print usage()
        sys.exit(1)
    print "Requesting [((%s - %s)^2   +  (%s - %s)^2 )^1/2"%(x, m, y, n)
    s = pytha_client(x, y, m, n)
    print "The shortest distance to travel for the rover is [((%s - %s)^2   +  (%s - %s)^2 )^1/2 = %s]"%(x, m, y, n, s)