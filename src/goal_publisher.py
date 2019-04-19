#!/usr/bin/env python2
# Miguel Riem Oliveira, April 2019
import random

import rospy

from actionlib.action_server import ActionServer
# from binpicking_action.msg import Robot_binpickingAction, Robot_binpickingFeedback, Robot_binpickingResult
from my_action_server.msg import MyActionActionGoal
import threading

import collections

if __name__ == "__main__":

    rospy.init_node('goal_publisher', anonymous=True)
    pub = rospy.Publisher('/my_action_server/goal', MyActionActionGoal, queue_size=1)
    rospy.sleep(0.2)

    #Create the goal message to be published
    goal = MyActionActionGoal()

    goal.goal.number = random.randint(0, 1000)
    goal.header.stamp = rospy.Time.now()
    goal.goal.time_to_wait = rospy.Time.from_sec(random.randint(50, 200)) # wait between 5 and 20 secs
    pub.publish(goal)
    rospy.loginfo("Published goal with number " + str(goal.goal.number) + ", time to wait is " + str(goal.goal.time_to_wait.to_sec()) )

    rospy.sleep(0.2)
