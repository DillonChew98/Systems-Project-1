#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import cv2
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import matplotlib.pylab as plt
import numpy as np
import math

interested_region = [
    (0,435),
    (0,420),
    (580,420),
    (580,440)
]

angle_deg = 0
P = 0
I = 0
D = 0 
PIDvalue = 0
prev_error = 0
prev_I = 0

class ttt:
    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(10)
        
def shutdown(spd_z):
    sss = ttt()
    cmd = Twist()
    cmd.linear.x = 0.1
    cmd.angular.z = spd_z + PIDvalue
    print(cmd.angular.z)

    sss.pub.publish(cmd)

def calculate_angular_PID():
    Kp = 0.003
    Ki = 0
    Kd = 0.01

    if(angle_deg == 90):
        error = angle_deg
    else:
        error = angle_deg - 90

    global P, I, D, PIDvalue, prev_error
    P = error
    I = I + error
    D = error - prev_error
    PIDvalue = (Kp * P) + (Ki * I) + (Kd * D)
    prev_error = error
    

    
def read_image(image):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(image, desired_encoding="passthrough")
    cv_image_copy = cv_image.copy()

    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, (0,0,231), (180,18,255))
    white_res = cv2.bitwise_and(cv_image,cv_image,mask=white_mask)

    img = cv2.cvtColor(white_res, cv2.COLOR_BGR2GRAY)
    canny_img = cv2.Canny(img, 50, 150)

    mask = np.zeros_like(img)
    channel_count = cv_image.shape[2]
    match_mask_color = (255,) * channel_count
    vertices = np.array([interested_region], dtype=np.int32)
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_img = cv2.bitwise_and(img,mask)

    contours, hierarchy = cv2.findContours(masked_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

    # if len(contours) > 0:
    #     blackbox = cv2.minAreaRect(contours[0])
    #     (x_min, y_min), (w_min, h_min), ang = blackbox


    #     ang = int(ang)
    #     box = cv2.boxPoints(blackbox)
    #     box = np.int0(box)
    #     cv2.drawContours(cv_image, [box], 0, (0,0,255), 3)  
    #     cv2.putText(cv_image, str(ang), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    
    # midpt_box = ((box[0][0]+box[2][0])/2,(box[0][1]+box[2][1])/2)
    # cv_image = cv2.circle(cv_image, midpt_box, 5, (0,0,255), -1)
    cnt_x = 640/2
    cnt_y = 480

    cv2.line(cv_image, (cnt_x, cnt_y), (cnt_x,0), (0,0,255), 3)
    O = cx - cnt_x
    A = cy - cnt_y
    angle_rad = -math.atan2(A,O)
    global angle_deg
    angle_deg = (angle_rad/math.pi)*180

    if(angle_deg < 90):
        spd = -0.05
        calculate_angular_PID()
        shutdown(spd)
        
    if(angle_deg > 90):
        spd = 0.05
        calculate_angular_PID()
        shutdown(spd)
        

    cv2.line(cv_image, (cnt_x,cnt_y), (cx,cy), (0,0,255), 3)  
    cv2.putText(cv_image, str(angle_deg), (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.drawContours(cv_image, contours, 0, (0,0,255), 3)
    # plt.imshow(masked_img)
    # plt.show()
    cv2.imshow('LIMO_POV', cv_image)
    cv2.waitKey(3)
   
    

def main():
    rospy.init_node('path', anonymous=False)
    rospy.Subscriber('/camera/rgb/image_raw', Image, read_image)
    rospy.spin()


main()
