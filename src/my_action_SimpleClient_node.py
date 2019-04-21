#!/usr/bin/env python2
# Miguel Riem Oliveira, Tiago Tavares, April 2019
import genpy
import rospy
import actionlib
from my_action_server.msg import MyActionAction, MyActionGoal, MyActionFeedback, MyActionResult

import time

def MyActionClient(cancel):

    client = actionlib.SimpleActionClient('my_action_server', MyActionAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = MyActionGoal(number=10, time_to_wait=genpy.Duration(10) )

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    if cancel != 1 :
        client.wait_for_result()
        # Prints out the result of executing the action
        return client.get_result()  # Result
    else:
        time.sleep(5)
        client.cancel_goal()
        #client.cancel_all_goals()
        result= MyActionResult()
        result.result= "Action Canceled"
        return result

    

if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('my_action_client_py')
        cancel=0 # 1 to cancel goal with 5 delay secs
        result = MyActionClient(cancel)
        print ("Result:" + str(result.result) )
    except rospy.ROSInterruptException:
        print "program interrupted before completion"
