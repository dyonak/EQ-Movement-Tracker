# EQ-Movement-Tracker
Detects location (/loc) commands within Everquest using the log file. From this the script with determine direction, speed, etc. and load waypoints for the given zone to help guide you to them.

## Features
- Dynamically switch between characters based on modified time of character log files
- Update current zone with a /who command
- Calculate and display toon, zone, location, heading, compass direction, and speed
- Dynamically include waypoint data if available waypoint is either inline (w/in 20deg +/-) with current heading or w/in 500 units
- Waypoints calculate accuracy (0.0 indicates perfect path), distance, and time to destination

## Setup
Change log_path to reflect your current Everquest Logs directory **with the trailing slash** (e.g. 'C:/EQ/Logs/'). No other changes should be needed!

If you have waypoints that are not currently included you can add them to the [waypoints file](EQWaypoints.py).

## Output:

![image](https://user-images.githubusercontent.com/6036049/162824372-99c8bc00-3d1c-4383-a6d5-4590095849e6.png)
