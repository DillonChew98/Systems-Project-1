#!/usr/bin/env python

import rospy
import actionlib

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from tf.transformations import quaternion_from_euler, euler_from_quaternion



def call_server():
    clients = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    clients.wait_for_server()

    x = [-4.05,-5.01,-1.90,-2.04,-2.12,-2.33,-2.06,-2.04,-2.08,-2.22,-3.98,-5.06,-5.43,-5.93,-5.86,-5.83,-6.12]
    y = [-2.91,-2.51,-2.51,-3.95,-4.98,-5.99,-5.84,-4.35,-2.50,-2.49,-4.18,-4.35,-4.12,-4.08,-5.06,-5.77,-6.58]

    ori_z = [0.94,0.01,-0.67,-0.73,-0.67,-0.04,0.67,0.73,0.99,-0.62,0.99,0.92,0.99,-0.74,-0.66,-0.86,-0.67]
    ori_w = [0.33,0.99,0.73,0.67,0.74,0.99,0.73,0.67,0.05,0.78,-0.04,0.37,0.07,0.66,0.74,0.50,0.74]

    sz = len(x)

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()

    i = 0
    while i < sz:
        goal.target_pose.pose.position.x = x[i]
        goal.target_pose.pose.position.y = y[i]
        goal.target_pose.pose.position.z = 0.0
        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = ori_z[i]
        goal.target_pose.pose.orientation.w = ori_w[i]
        clients.send_goal(goal)
        clients.wait_for_result()
        res = clients.get_state()

        rospy.loginfo(goal)

        if(res == actionlib.GoalStatus.SUCCEEDED):
            i = i+1
            print('passed')
        else:
            print('failed')
            break


if __name__ == '__main__':
    try:
        rospy.init_node('limo_nagivator_node')
        call_server()
    except rospy.ROSInitException as e:
        print('Something went wrong: ', e)

