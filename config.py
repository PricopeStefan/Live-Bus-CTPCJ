
# Endpoint definitions
BACKEND_URL = 'https://m-go.wink.ro'
STATION_ENDPOINT = f'{BACKEND_URL}/api/station/all'
ROUTE_ENDPOINTS = [f'{BACKEND_URL}/api/route/all/{page}' for page in range(0, 13)]
REALTIME_ENDPOINT = f'{BACKEND_URL}/api/realTime/all'

# In case online lookup fails, fall back to cached local files
STATION_LOCAL_FILE = 'json_data/statii.json'
ROUTE_LOCAL_FILES = [f'json_data/route_{page}.json' for page in range(0, 13)]
REALTIME_LOCAL_FILE = 'json_data/realTime_1.json' # kinda ironic having this one, good for complete failure?

