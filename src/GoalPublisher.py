#!/usr/bin/env python2
# Miguel Riem Oliveira, April 2019
import random

import rospy

from actionlib.action_server import ActionServer
# from binpicking_action.msg import Robot_binpickingAction, Robot_binpickingFeedback, Robot_binpickingResult
from binpicking_action.msg import MyActionActionGoal
import threading

import collections

if __name__ == "__main__":

    rospy.init_node('goal_publisher', anonymous=True)
    pub = rospy.Publisher('/my_action_server/goal', MyActionActionGoal, queue_size=10)
    rospy.sleep(0.1)

    #Create the goal message to be published
    goal = MyActionActionGoal()

    goal.goal.id = random.randint(0, 1000)
    goal.header.stamp = rospy.Time.now()
    goal.goal.time_to_wait = rospy.Time.from_sec(random.randint(5, 20)) # wait between 5 and 20 secs
    pub.publish(goal)
    rospy.loginfo("Published goal id " + str(goal.goal.id) + ", time to wait is " + str(goal.goal.time_to_wait.to_sec()) )

