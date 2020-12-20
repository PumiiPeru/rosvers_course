#!/usr/bin/env python

from rosvers_course.srv import ShortDist
from rosvers_course.srv import ShortDistRequest
from rosvers_course.srv import ShortDistResponse

import rospy
import math

def handle_pytha(req):
    print "Returning [((%s - %s)^2   +  (%s - %s)^2 )^1/2 =  %s ]"%(req.a,req.c,req.b,req.d, ((req.a - req.c)**2 + (req.b - req.d)**2)**0.5  )
    return ShortDistResponse(((req.a - req.c)**2 + (req.b - req.d)**2)**0.5 )

def pytha_server():
    rospy.init_node('pytha_server')
    s = rospy.Service('pytha', ShortDist, handle_pytha)
    print "Ready to calculate the shortest distance"
    rospy.spin()
    
if __name__ == "__main__":
    pytha_server()