#!/usr/bin/env python2
# Tiago Almeida Tavares , DEM-UA  77001 , 17 April 2019
import rospy
import time  # sleep
import sys
import copy

from actionlib.action_server import ActionServer
from binpicking_action.msg import Robot_binpickingAction, Robot_binpickingFeedback, Robot_binpickingResult


class RefServer (ActionServer):

    def __init__(self, name):
        self.server_name = name
        action_spec = Robot_binpickingAction
        ActionServer.__init__(
            self, name, action_spec, self.goalCallback, self.cancelCallback, False)
        self.start()  # como metemos o ultimo parametro a False, damos o start aqui
        rospy.loginfo("Creating ActionServer [%s]\n", name)

        self.saved_goals = []
        self._feedback = Robot_binpickingFeedback()
        self._result = Robot_binpickingResult()

    # G======================GOALCALLBACK================================
    def goalCallback(self, gh):

        success = True
        goal = gh.get_goal()

        self._feedback.sequence = []

        rospy.loginfo("Got goal %d", int(goal.mode))

        # if self.is_preempt_requested():
        #     rospy.loginfo('%s: Preempted' % self.name)
        #     self.set_preempted()
        #     success = False

        if goal.mode == 1:
            gh.set_accepted()

            count=0
            while count < 11:
                count+=1
                # self._result.sequence = self._feedback.sequence
                self._feedback.sequence.append(count)
                gh.publish_feedback(self._feedback)

                time.sleep(1)

                if count>=10 :
                    break
        else:
            success = False
            gh.set_aborted(None, "The ref server has aborted")

        if success:
            
            self._result.result = True
            rospy.loginfo('%s: Succeeded', self)



    def cancelCallback(self, gh):
        rospy.loginfo("XXX action canceled XXX")
        # if self._as.is_preempt_requested():
        #     self._as.set_preempted()
            # pass


if __name__ == "__main__":
    rospy.init_node("BinPickingAction")
    ref_server=RefServer("BinPickingAction")

    rospy.spin()
