from config import *
import json

def get_route_data_from_route_id(route_id: int) -> str:
	for route_page in ROUTE_LOCAL_FILES:
		with open(route_page, 'r') as route_fp:
			route_data = json.load(route_fp)
			target_route = next((route for route in route_data['data'] if route['routeId'] == route_id), None)

			if target_route is None:
				# if the target route was not found in this page, go to the next one
				continue

			return target_route

	# if we went through all the route pages available then return None 
	# TODO: maybe raise exception?
	return None
