import json
import requests
import time

from config import *
from helper import get_route_data_from_route_id

# User defined targets (buses and stations)
# TODO: a lot of work to personalize these
ROUTE_IDS = [1, 2, 3, 4, 5]
STATION_IDS = [1, 2, 3, 4, 5]

# Session Init
s = requests.Session()
s.headers.update({
    # Much obfuscated, very secure
    'azza': '.'.join('eyJhbGciOiJIUzI1NiJ9', 'Ykk2MTdQQU51b2lVWWhFTzgzMkJNdmVodUFrbk9MaWY', 'IX1_yu8Al_OUcWivOBQRnX46Cd2Bh_ybzZqqo_eueYA']),
    'user-agent': 'okhttp/4.7.2'    
})

# ACTUAL CODE
while True:
    try:
        data_res = s.get(REALTIME_ENDPOINT)
        if data_res.status_code != 200 or data_res.text is None:
            # Should probably log this and not just continue
            continue

        live_routes = json.loads(data_res.text)
        if 'data' not in live_routes.keys():
            # Should probably log this and not just continue
            continue

        # We only want the routes that interest us, not the entire data
        relevant_routes = [route for route in live_routes['data'] if route['routeId'] in ROUTE_IDS]

        # And from those relevant routes, we only want those that are yet to reach our target stations
        targets = []
        for bus in relevant_routes:
            arrival_info = [arrival_data for arrival_data in bus['liveTime'] if arrival_data['stationId'] in STATION_IDS]
            
            if len(arrival_info) > 0:
                bus['liveTime'] = arrival_info # only keep the Time-To-Arrive information for target stations
                route_data = get_route_data_from_route_id(bus['routeId'])

                # Get additional relevant information for display purposes
                bus['routeName'] = route_data['routeName']
                bus['busLineNumber'] = route_data['routeShortname']
                bus['routeColor'] = route_data['routeColor'] # ????

                # and finally add it to the list
                targets.append(bus)

        for target in targets:
            print(f'{target["routeName"]} - {target["busLineNumber"]}')
            print(f'LAT={target["lat"]}; LONG={target["lng"]}')
            for liveTime in target['liveTime']:
                print(f'\tTimeToArrive={liveTime["timeToArrive"]}; Station={liveTime["stationId"]}')
            print()

        print('*' * 20)
        time.sleep(10)
    except Exception as err:
        print(err)
