#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

##################
# Initialization #
##################

x=0
y=0
yaw=0

#########
# Input #
#########
def poseCallback(pose_message):
    global x
    global y, yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta

################################################################
# def move(speed of the robot, disired displacement, direction)#
################################################################
def move(speed, distance, is_forward):

        #Define a Twist message to send velocity commands
        velocity_message = Twist()
        #Get the current location (input)
        global x, y
        x0=x
        y0=y

        #Determine the direction
        if (is_forward):
            velocity_message.linear.x =abs(speed)
        else:
        	velocity_message.linear.x =-abs(speed)


        distance_moved = 0.0
        loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
        cmd_vel_topic='/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        while True :
                rospy.loginfo("Turtlesim moves forwards")
                #Publishing in a loop until you reach the objetive
                velocity_publisher.publish(velocity_message)
                loop_rate.sleep()
                
                #rospy.Duration(1.0)
                
                distance_moved = abs(math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
                print  distance_moved 
                #If the distance is shorter that the desired displacement, the loop breaks              
                if  not (distance_moved<distance):
                    rospy.loginfo("Reached location")
                    break
        
        #finally, stop the robot when the distance is moved
        velocity_message.linear.x =0
        velocity_publisher.publish(velocity_message)
    
##################################################################################
# def rotate(angular speed of the robot, disired angular displacement, direction)#
##################################################################################   
def rotate (angular_speed_degree, relative_angle_degree, clockwise):
    
    global yaw
    velocity_message = Twist()
    velocity_message.linear.x=0
    velocity_message.linear.y=0
    velocity_message.linear.z=0
    velocity_message.angular.x=0
    velocity_message.angular.y=0
    velocity_message.angular.z=0

    #get current location 
    theta0=yaw
    angular_speed=math.radians(abs(angular_speed_degree))

    if (clockwise):
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z =abs(angular_speed)

    angle_moved = 0.0
    loop_rate = rospy.Rate(20) # we publish the velocity at 10 Hz (10 times a second)    
    cmd_vel_topic='/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    t0 = rospy.Time.now().to_sec()

    while True :
        rospy.loginfo("Turtlesim rotates")
        velocity_publisher.publish(velocity_message)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        loop_rate.sleep()


                       
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break

    #finally, stop the robot when the distance is moved
    velocity_message.angular.z =0
    velocity_publisher.publish(velocity_message)

########################################################
# def go_to_goal(desired x position,desired y position)#
########################################################
def go_to_goal(x_goal, y_goal):
    global x
    global y, yaw

    velocity_message = Twist()
    cmd_vel_topic='/turtle1/cmd_vel'

    while (True):

        #proporcional Gain
        K_linear = 0.5 
        distance = abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))

        linear_speed = distance * K_linear

        #proporcional Gain
        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        angular_speed = (desired_angle_goal-yaw)*K_angular


        #Asign the computed velocities
        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed

        #Publish and print the values
        velocity_publisher.publish(velocity_message)
        print 'x=', x,'cm/s, y=',y,'cm/s'

        #Error tolerance, if the position is lower, the loop breaks and he motion stops
        if (distance <0.01):
            break

###############################################################################
# def setDesiredOrientation(desired angle in radiants in absolute coordinates)#
###############################################################################
def setDesiredOrientation(desired_angle_radians):
    relative_angle_radians = desired_angle_radians - yaw
    if relative_angle_radians < 0:
        clockwise = 1
    else:
        clockwise = 0
    print relative_angle_radians
    print desired_angle_radians
    rotate(30 ,math.degrees(abs(relative_angle_radians)), clockwise)

###############################################
# def spiralClean(set speed,set angular speed)#
###############################################
def spiralClean(rk,wk):
    #Defining a velocity message
    vel_msg = Twist()
    loop_rate = rospy.Rate(10)

    #Upper limit in position, belyond that limit the algorithm stops
    while((x<7.5) and (y<8)):
        rk=rk+0.05
        vel_msg.linear.x =rk
        vel_msg.linear.y =0
        vel_msg.linear.z =0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z =wk
        velocity_publisher.publish(vel_msg)
        loop_rate.sleep()
 
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

##############
# Main method#
##############
def gridClean():
 
    desired_pose = Pose()
    desired_pose.x = 1
    desired_pose.y = 1
    desired_pose.theta = 0


    go_to_goal(desired_pose.x,desired_pose.y)
    setDesiredOrientation(math.radians(desired_pose.theta))
    move(2.0, 9.0, True)
    rotate(20, 90, False)
    move(2.0, 9.0, True)
    rotate(20, 90, False)
    move(2.0, 9.0, True)
    rotate(20, 90, False)
    move(2.0, 9.0, True)
    rotate(30, 90, False)
    move(2.0, 9.0, True)
    rotate(30, 90, False)
    move(2.0, 9.0, True)
    rotate(30, 90, False)
    go_to_goal(5.3,5.3)
    spiralClean(1,2)
    pass

###############
# Main routine#
###############
if __name__ == '__main__':
    try:
        
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        #declare velocity publisher, it's always listening the velocity topic
        cmd_vel_topic='/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        #declare position publisher, it's always listening the position topic
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback) 
        time.sleep(2)

        #You can check all the method one by one, main routine.
        gridClean()
       
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")