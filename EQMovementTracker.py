import math
import os
import datetime
import time
import EQ_waypoints

###DONE###
#open log scan for new entries
#determine location, speed, heading and current zone
#scan for most recently modified log and dynamically switch
#Read from waypoints list to display relevant (close or directionally identified) waypoints
#For relevant waypoints display accuracy, distance and time to destination

toon = ''
log_path = 'C:/Everquest/Logs/'
zone_name = 'Unknown - Do a /who or zone to update.'
previous_coords = [0.0, 0.0, 0.0]
previous_time = datetime.datetime.now()
speed = 0.0
waypoints = EQ_waypoints.return_waypoints(zone_name)

def get_active_toon():
    toon_logs = []
    os.chdir(log_path)
    files_list = os.listdir()
    for file in files_list:
        if file[:6] == 'eqlog_': #find files that start with eqlog_
            toon_logs.append([file, os.stat(file).st_mtime])
    toon_logs = sorted(toon_logs,key=lambda l:l[1], reverse=True)
    toon = toon_logs[0][0]
    return toon

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def tail(filepath):
    with open(filepath, "rb") as f:
        first = f.readline()      # Read the first line.
        f.seek(-2, 2)             # Jump to the second last byte.
        while f.read(1) != b"\n": # Until EOL is found...
            try:
                f.seek(-2, 1)     # ...jump back the read byte plus one more.
            except IOError:
                f.seek(-1, 1)
                if f.tell() == 0:
                    break
        last = f.readline()       # Read last line.
    return last   

def direction_lookup(destination_x, origin_x, destination_y, origin_y):
    deltaX = destination_x - origin_x
    deltaY = destination_y - origin_y
    degrees_temp = math.atan2(deltaX, deltaY)/math.pi*180
    if degrees_temp < 0:
        degrees_final = 360 + degrees_temp
    else:
        degrees_final = degrees_temp
    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    compass_lookup = round(degrees_final / 45)
    return compass_brackets[compass_lookup], degrees_final

while True:
    time.sleep(0.05)
    toon = get_active_toon() #Probably a waste since this function is updating the global 'toon', running it w/o having it return would be the same?
    last_log = tail(log_path + toon)
    last_log = last_log.strip()
    last_log = last_log.decode()
    #Not used for now, fidelity is only to the second which is not good enough for speed calcs
    log_time =  last_log[1:25]

    #Message content of the most recent log entry
    log_message = last_log[27:]

    #Look for zone name
    if last_log[27:43] == "You have entered":
        zone_name = last_log[44:-1]
        waypoints = EQ_waypoints.return_waypoints(zone_name)
    if last_log[27:33] == "There ":
        zone_name = ''
        words = log_message.split()
        words[-1] = words[-1].replace('.','')
        for word in words[5:]:
            zone_name += word + " "
        zone_name = zone_name.rstrip()
        waypoints = EQ_waypoints.return_waypoints(zone_name)
    
    #Look for a new location entry
    if last_log[27:43] == "Your Location is":
        #Split entry into coordinates and remove the prefix from first coordinate
        log_coords = log_message.split(", ")
        log_coords[0] = log_coords[0].replace('Your Location is ','')
        
        #shift log coords into a new list with floats
        coordinates = [float(x) for x in log_coords]

        #Location has been detected, check to see if it's different from previous
        if previous_coords[1] != coordinates[1] or previous_coords[0] != coordinates[0]:
            #New coord detected, update coordinates and time and calculate distance, headings, and speed
            y2, x2, z2 = coordinates
            y1, x1, z1 = previous_coords
            distance = math.sqrt(((x2-x1) ** 2) +  ((y2-y1) ** 2))
            compass_heading, degrees_heading = direction_lookup(x1, x2, y2, y1) #x coords reversed to fix EQ's inverse x scale
            current_time = datetime.datetime.now()
            timedelta = current_time - previous_time
            if timedelta.total_seconds() != 0:
                speed = round(distance / timedelta.total_seconds(), 2)
            cls()
            waypoint_message = ''
            
            if isinstance(waypoints,list):
                for waypoint in waypoints:
                    wp_x = float(waypoint['x'])
                    wp_y = float(waypoint['y'])
                    wp_dist = math.sqrt(((wp_x-x1) ** 2) +  ((wp_y-y1) ** 2))
                    wp_time = wp_dist // speed
                    wp_comp, wp_degs = direction_lookup(x2, wp_x, wp_y, y2)
                    wp_offset = round((wp_degs - degrees_heading), 1)
                    if wp_dist < 500 or abs(wp_offset) < 20:
                        waypoint_message += f"\n{waypoint['waypoint']} = Accuracy: {-wp_offset} Distance: {round(wp_dist)} Time: {wp_time}"
            else:
                waypoint_message = '\n' + waypoints
            
            print(f'''
Toon: {toon[6:-16]} Zone: {zone_name} Loc: {x2}, {y2}
Compass: {compass_heading} / {round(degrees_heading, 1)}° Speed: {speed}
Waypoints: {waypoint_message}
            ''')
            
            #if zone in zone_landmarks.dat and waypoint
            previous_coords = coordinates
            previous_time = current_time