# my-action-server

Example of how to use actionlib for multiple parallel processing of goals. Canceling works too.

# How to use

Run the action server node

```bash
rosrun my_action_server my_action_server_node.py
```

## Create new goals with 

```bash
rosrun my_action_server goal_publisher.py
```

or by calling 

```bash
rostopic pub /my_action_server/goal my_action_server/MyActionActionGoal "header:
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: ''
goal_id:
  stamp:
    secs: 0
    nsecs: 0
  id: ''
goal:
  number: 50
  time_to_wait:
    secs: 30
    nsecs: 0" 

publishing and latching message. Press ctrl-C to terminate
```

## Cancel goals using

```bash
rostopic pub /my_action_server/cancel actionlib_msgs/GoalID "stamp:
  secs: 0
  nsecs: 0
id: ''" 
```

if you want to cancel all goals sent an empty id. But if you want to cancel only a specific goal add the id of that goal. Example: 

```bash
rostopic pub /my_action_server/cancel actionlib_msgs/GoalID "stamp:
  secs: 0
  nsecs: 0
id: '/my_action_server-3-1555752296.823899984'" 
```

The my_action_server_node.py is printting the running goal id.