#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class ttt:
    def __init__(self):
        rospy.init_node('trial', anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(10)

def shutdown():
    sss = ttt()
    cmd = Twist()
    cmd.linear.x = 1
    cmd.angular.z = 0.0

    while not rospy.is_shutdown():
        sss.pub.publish(cmd)
        sss.rate.sleep()







if __name__ == '__main__':
    shutdown()
    rospy.spin()