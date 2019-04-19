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
rostopic pub /my_action_server/goal my_action_server/MyActnActionGoal "header:
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
  id: 0
  time_to_wait:
    secs: 10
    nsecs: 0" 
publishing and latching message. Press ctrl-C to terminate
```

## Cancel goals using

```bash
rostopic pub /my_action_server/cancel actionlib_msgsoalID "stamp:
  secs: 0
  nsecs: 0
id: ''" 
```

if you want to cancel only a specific goal add the id of that goal (This is not working, opened issue #2 for this).

