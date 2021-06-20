# Reversing Bus CTPCluj Live data

### Endpoints and misc:
* Stolen from Bus Cluj-Napoca
  - Harcoded JWT used for `azza` header (authorization for every API request): eyJhbGciOiJIUzI1NiJ9.Ykk2MTdQQU51b2lVWWhFTzgzMkJNdmVodUFrbk9MaWY.IX1_yu8Al_OUcWivOBQRnX46Cd2Bh_ybzZqqo_eueY
    - Add a `A` to the end of the token (I have no clue if this prevents any automated tools looking for exposed JWT secrets or not, worth a shot).
  - `m-go.wink.ro` - base domain for API requests.
  - `GET /api/station/all` - return all information about stations/bus stops (name, id, lat&long, comments).
  - `GET /api/route/all/<index>` - `index` ranges from 0 to 12, returns all information possible about all routes (all stops, accurate long&lat for map pins, names etc.).
  - `GET /api/realTime/all` - return real time location of all transports with information regarding time left to reach next stops.

* Stolen from Tranzy (supposedly official application from Wink)
  - `tranzy.wink.ro` - base domain 1
    - `POST /api/info?city=2&lang=1` - `city=1` is Iasi, `city=2` is Cluj Napoca. `lang=1` is Romanian, `lang=2` is English, `lang=3` for stack trace error :). `GET` also works, but for some reason the application uses `POST`.
    - `/uploads` - access to all uploads, directory access not restricted.
  - `roclj.tranzy.wink.ro` - base domain 2
    - `/stations` - return all information about stations/bus stops (similar to the `m-go.wink.ro/api/station/all` endpoint, but also includes basic information about all routes that pass through the station).
    - `/stations/<station id>` - returns information only about the station with the specified id. Also returns live arrival data (how many minutes left until the bus arrives).
    - `/stations/next-on-routes/<station id>/<latitude>/<longitude>` - returns only live arrival data for the specified station id. Also requires a latitude and longitude for an unknown reason, can be set to any positive float value.
    - `/route/<route id>?startStationId=<station id>&nextVehicleIdOnRoute=` - needs further analysis
    - `/api/autocomplete/<station name>` - not hard
    - `/routesnearme/<latitude>/<longitude>/<max results>` - not hard
  - `osm.tranzy.wink.ro` - base domain 3, used for OpenStreetMaps integration. Running [Open Source Routing Machine](https://github.com/Project-OSRM/osrm-backend) as the backend. API endpoints used from this framework:
    - `/reverse?format=jsonv2&lat=<latitude>&lon=<longitude>` - reverse map a pair of lat, long coordinates (give lat, long coordinates, returns street address and other general information)
    - `/route/v1/foot/<longitudeStart>,<latitudeStart>;<longitudeEnd>,<latitudeEnd>` - returns a route between the given start and end coordinates, the length of the route in feet, estimated duration (unknown time unit, doesn't seem like seconds).


### Analyzed using `HTTP Toolkit`
Useful query for filtering out uninteresting requests:
```
hostname!=clients4.google.com hostname!=app-measurement.com hostname!=chromefeedcontentsuggestions-pa.googleapis.com hostname!=googleads.g.doubleclick.net hostname!=clientservices.googleapis.com hostname!=safebrowsing.googleapis.com hostname!=graph.facebook.com hostname!=a.tile.openstreetmap.org hostname!=b.tile.openstreetmap.org hostname!=c.tile.openstreetmap.org hostname!=www.googleapis.com 
```