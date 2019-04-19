#!/usr/bin/env python2
# Miguel Riem Oliveira, April 2019

import rospy
from actionlib.action_server import ActionServer
from my_action_server.msg import MyActionAction, MyActionGoal, MyActionFeedback, MyActionResult
import actionlib_msgs.msg
import threading
import collections

# Named tuple for storing the goal handle and the corresponding processing thread
GoalHandleThread = collections.namedtuple('GoalHandleThread', 'goal_handle thread')


class MyActionServer(ActionServer):
    """ Tutorial for how to write a ros action server in python.
        Works with multiple paralell goals, since it creates a processing thread for each newly received (and accepted) goal.
    """
    _threads = {}  # a dictionary containing a GoalHandleThread tuple for each goal processing thread

    def __init__(self, name):
        """ Initializes the actions sever

        :param name: name of the action server
        """
        self.server_name = name
        ActionServer.__init__(self, name, MyActionAction, self.goalCallback, self.cancelCallback,
                              False)  # initialize superclass
        rospy.loginfo("ActionServer " + name + " initialized.")

        self.start()  # start the action server
        rospy.loginfo("ActionServer " + name + " started.")

    def goalCallback(self, gh):
        """ Called whenever a new goal is received

        :param gh: a handle to the goal
        """
        # Analyse requested goal and decide whether to accept it or not
        goal = gh.get_goal()
        rospy.loginfo("Received request for goal " + str(goal.id))

        # Goal acceptance criteria: Accept only goals where id is even, and number of active goal processing threads
        # is < 3 (this is a dummy criteria)
        if goal.id % 2 == 0 and len(self._threads) < 3:
            gh.set_accepted()  # accept goal
            _current_goal = goal

            thread = threading.Thread(target=self.processGoal, args=(gh,))  # create a thread to process this goal
            self._threads[goal.id] = (GoalHandleThread(gh, thread))  # add to tasks dictionary
            thread.start()  # initiate thread
            rospy.logwarn("Accepted goal request. Launched a processing thread for goal id " + str(goal.id))

        else:  # goal rejection
            rospy.logwarn("Rejected goal request for goal id " + str(goal.id))
            gh.set_rejected(result=None, text="Goal id not even or number of active tasks > 3")

    def cancelCallback(self, gh):
        """ Called when a cancel request is received.

        :param gh: a handle to the goal
        """
        goal = gh.get_goal()  # get the goal
        rospy.logerr("Received cancel request for goal " + str(goal.id))
        result = MyActionResult()  # create an empty result class instance
        result.result = "Goal canceled"
        gh.set_canceled(result=result, text="Canceled.")  # cancel the goal

    def processGoal(self, gh):
        """ Processes the goal.
        Called in a separate thread(s), so that it does not interfere with the actionlib state machine

        :param gh: a handle to the goal
        :return:
        """
        # Get the goal handle and the thread using the id as dictionary key
        goal = gh.get_goal()
        _, thread = self._threads[goal.id]  # shows how to get the thread knowing the goal id

        r = rospy.Rate(1)  # 1hz
        tic = rospy.Time.now()
        while not rospy.is_shutdown():
            r.sleep()
            ellapsed_secs = rospy.Time.now() - tic  # get ellapsed time

            # Check if goal is active, if it is not active, interrupt processing
            if not gh.get_goal_status().status == actionlib_msgs.msg.GoalStatus.ACTIVE:
                rospy.logerr("Goal " + str(goal.id) + " canceled.")
                del self._threads[goal.id]  # remove from dictionary
                return  # the thread will terminate once the return is called

            # Check if goal processing is complete. If so, terminate goal
            if ellapsed_secs > goal.time_to_wait:
                rospy.logwarn(
                    "Completed goal " + str(goal.id) + " for " + '{:.1f}'.format(ellapsed_secs.to_sec()) + " secs.")

                result = MyActionResult()  # create an empty result class instance
                result.result = "Goal achieved successfuly."
                gh.set_succeeded(result=result, text="Reached time to wait.")
                del self._threads[goal.id]  # remove from dictionary
                return  # the thread will terminate once the return is called
            else:
                rospy.loginfo("Processing goal " + str(goal.id) + " for " + '{:.1f}'.format(
                    ellapsed_secs.to_sec()) + " out of " + '{:.1f}'.format(goal.time_to_wait.to_sec()) + " secs.")
                # put here code that continues to process the goal ...


if __name__ == "__main__":
    rospy.init_node("my_action_server")  # initialize node
    my_action_server = MyActionServer("my_action_server")  # create action server instance
    rospy.spin()  # spin away!
