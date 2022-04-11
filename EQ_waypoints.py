waypoints = {
    'Western Wastes':[
        {
        'waypoint': 'Temple of Veeshan Zoneline',
        'y':1450.0,
        'x':700.0
        },
        {
        'waypoint': 'Dragon Necropolis Zoneline',
        'y':-2800.0,
        'x':380.0
        }
    ],
    'The Emerald Jungle':[
        {
        'waypoint': 'Trakanon\'s Teeth Zoneline',
        'y':-3425.0,
        'x':1570.0
        },
        {
        'waypoint': 'City of Mist Zoneline',
        'y':299.0,
        'x':-1972.0
        },
        {
        'waypoint': 'Severilous',
        'y':2500.0,
        'x':3480.0
        }
    ]
}

def return_waypoints(zone):
    if zone in waypoints:
        return waypoints[zone]
    else:
        return "No waypoints found."

#example usage of output
#waypoints = return_waypoints('Western Wastes')
#if isinstance(waypoints,list):
#    for waypoint in waypoints:
#        print(waypoint['waypoint'], waypoint['x'], waypoint['y'])

