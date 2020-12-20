#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty


#This code will cover just until the 'go_to_goal'
#For later development you can use the turtlesim_cleaner.py
def poseCallback(pose_message):
    global x
    global y, yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta

    #print "pose callback"
    #print ('x = {}'.format(pose_message.x)) #new in python 3
    #print ('y = %f' %pose_message.y) #used in python 2
    #print ('yaw = {}'.format(pose_message.theta)) #new in python 3

#Previously we've defined the libraries we are going to use
#Analize the arguments of the move method
#Move (The speed of the turtle, the distances traveled, the direction)
def move(speed, distance, is_forward):
        #declare a Twist message to send velocity commands
        velocity_message = Twist()
        #get current location 


        if (speed > 0.4):
            print 'speed must be lower than 0.4'
            return

        # This will ensure the direction of the robot
        if (is_forward):
            velocity_message.linear.x =abs(speed)

        else:
        	velocity_message.linear.x =-abs(speed)

        distance_moved = 0.0
        # we publish the velocity at 10 Hz (10 times a second) 
        loop_rate = rospy.Rate(10)    
        # cmd_vel_topic='/cmd_vel_mux/input/teleop'
        # This defines the topic in which the node is going to publish the velocity 
        cmd_vel_topic='/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        #Update the time
        t0 = rospy.Time.now().to_sec()

        while True :
                rospy.loginfo("Turtlesim moves forwards")
                velocity_publisher.publish(velocity_message)

                loop_rate.sleep()
                t1 =  rospy.Time.now().to_sec()
                #rospy.Duration(1.0)
                #Here you calculate de absolute distance traveled
                #d=sqrt((x-x0)**2+(y-y0)**2)
                #x,y is the current position ( always being updated)
                #x0,y0 is the initial position
                distance_moved = (t1-t0) * speed
                print  distance_moved  
                #     Check if we reached the goal        
                if  not (distance_moved<distance):
                    rospy.loginfo("reached")
                    break
        
        #finally, stop the robot when the distance is moved
        velocity_message.linear.x =0
        velocity_publisher.publish(velocity_message)

#Analize the arguments of the rotate method
#rotate (Angular velocity, the angle, the direction)    
#
def rotate (angular_speed_degree, relative_angle_degree, clockwise):
    
    #Here you are catching the values of Twists
    velocity_message = Twist()
    velocity_message.linear.x=0
    velocity_message.linear.y=0
    velocity_message.linear.z=0
    velocity_message.angular.x=0
    velocity_message.angular.y=0
    velocity_message.angular.z=0

    #You are changing the version to radians here.
    angular_speed=math.radians(abs(angular_speed_degree))


    if (clockwise):
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z =abs(angular_speed)

    angle_moved = 0.0
    # we publish the velocity at 10 Hz (10 times a second)
    # Change this can lead to errors, less time to update, the control is worse
    loop_rate = rospy.Rate(10)    
    # cmd_vel_topic='/cmd_vel_mux/input/teleop'
    #This defines the topic in which the node is going to publish the velocity 
    cmd_vel_topic='/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    #initial time
    t0 = rospy.Time.now().to_sec()

    while True :
        rospy.loginfo("Turtlesim rotates")
        velocity_publisher.publish(velocity_message)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        loop_rate.sleep()

        print 'current_angle_degree: ',current_angle_degree
                       
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break

    #finally, stop the robot when the distance is moved
    velocity_message.angular.z =0
    velocity_publisher.publish(velocity_message)


def go_to_goal(x_goal, y_goal):

    #Updated value
    global x
    global y, yaw

    velocity_message = Twist()
    cmd_vel_topic='/turtle1/cmd_vel'
     

    while (True):
        #The gain can increse the unstability of the controller
        K_linear = 0.8 
        # This is 
        distance = abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))
        #The speed is going to be proportional to the error
        linear_speed = distance * K_linear

        K_angular = 5.0
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        #The speed is going to be proportional to the error
        angular_speed = (desired_angle_goal-yaw)*K_angular

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed

        velocity_publisher.publish(velocity_message)
        print( 'x=', x, 'y=',y, ', distance to goal: ', distance)

        #0.01 es epsilon, it's the margin of error. It can not be 0.
        if (distance <0.01):
            break



if __name__ == '__main__':
    try:
        
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        #declare velocity publisher
        #This is the output of the plant
        cmd_vel_topic='/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        #declare pose subscriber
        #This is the sensor
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback) 
        time.sleep(2)

        #move (0.3, 4.0 , False)
        #time.sleep(1.0)
        #rotate (30, 180 , False)
        go_to_goal (7,5)
       
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")