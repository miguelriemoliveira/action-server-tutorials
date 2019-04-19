# my-action-server

Example of how to use actionlib for multiple parallel processing of goals. Canceling works too.

# How to use

Run the action server node

```bash
rosrun binpicking_action my_action_server.py
```

Create new goals with 

```bash
rostopic pub /my_action_server/goal binpicking_action/MyActnActionGoal "header:
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

or by calling 

```bash
rosrun binpicking_action goal_publisher.py
```
