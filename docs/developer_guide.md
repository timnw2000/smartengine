# Developer Documentation
---
This Documentation serves as a guide on how to use this package and its including classes and methods.
# rApi Documentation
---
## class rApi(user: str, password: str, ipv4: str)
---
Initiate a rApi-Object.

```py
from smartengine.rapi import restful

api = restful.rApi(
    user="test", 
    password="test12345", 
    ipv4_adress="192.168.178.1"
)
```

This Object inherits its behavior from both the FixtureApi-Object and the LocationsApi-Object.
You can access the full functionality of both Base Classes. When you want your code to be clear regarding its functionality you can also still choose to implement the FixturesApi Class and the LocationsApi Class themself directly.
The functionalities of both Base Classes are listed below.

## class FixturesApi(user: str, password: str, ipv4: str)
---
Initiate a FixtureApi-Object.

```py
from smartengine.rapi import fixtures

engine = fixtures.FixtureApi(
    user="test", 
    password="test12345", 
    ipv4_adress="192.168.178.1"
)
```


### method get_all_fixtures(self) -> list[dict]
`Object.get_all_fixtures()`

---
Returns all Fixtures that are currently in a location,

```py
fixtures_list = Object.get_all_fixtures() 
```

Output: 



```py
{
    "serial_number": "CSJ00000000001J020143808848",
    "name": "Sensor45",
    "type": "LUMINAIRE"
},
```
   



### method get_beacons(self, sensor_type: list[str]=None) -> list[dict]
`Object.get_beacons()`

---
Returns all beacons that are currently in a location if `sensor_type` is not specified.
When `sensor_type` is specified only get beacons with the specified sensor_type.
Specified `sensor_type` needs to be a list. The default is sensor_types are `["LUMINAIRE", "WALL_SWITCH_5B", "SENSOR"]`.

```py
beacons_list = Object.get_beacons(sensor_type=["LUMINAIRE"])
```
Output: 

    

```py
{
    "serial_number": "000000000SVS1Z00977HS999000",
    "name": "Sensor2",
    "type": "LUMINAIRE",
    "beaconSupported": true
},
```

    



### method get_sensor_stats(self, *sensors: str, sensor_type: list[str]=None) -> list[dict]
`Object.get_sensor_stats()`

---
Returns all fixtures and their stats of fixtures that are currently in a location if `sensors` and `sensor_type` are not specified. `sensors` specifies the fixtures from which stats get returned. By default all fixtures will be taken into account. When `sensor_type` is specified only get fixtures and their stats with the specified sensor_type. Specified `sensor_type` needs to be a list. The default is sensor_types are `["LUMINAIRE", "WALL_SWITCH_5B", "SENSOR"]`.

```py
stats_list = Object.get_sensor_stats(
    "000000000SVS1Z00977HS999000", "000000000SVS1Z00977HS991111", 
    sensor_type=["LUMINAIRE"]
)
```

Output: 
    

```py
{
    "serial_number": "000000000SVS1Z00977HS999000",
    "stats": {
        "power": 0.53,
        "temperature": 17.75,
        "motion": 1701170920.0,
        "illuminance": 0.0,
        "brightness": 0.0
    }
},
{
    "serial_number": "000000000SVS1Z00977HS991111",
    "stats": {
        "power": 0.71,
        "temperature": 18.10,
        "motion": 1701140998.0,
        "illuminance": 0.0,
        "brightness": 0.0
    }
},
```
    



### method sort_fixtures(self, *fixtures: str, sort_by: str="power", order: str="ASC") -> list[dict]
`Object.sort_fixtures()`

---
Returns a sorted list of fixtures. The fixtures are sorted by their stats. You can specify the stat, the fixture should be sorted by through the `sort_by` parameter. The `sort_by` parameter takes 9 different parameters:  `"power"`, `"temperature"`, `"illuminance"`, `"brightness"`, `"humidity"`, `"voc"`, `"co2"`, `"airPressure"`, `"indoorAirQuality"`.
By default the fixtures will be sorted by `"power"`.
The `fixtures` parameter takes in serial numbers of fixtures. Only specified fixtures will be sorted according to the specified stat. By default all fixtures will be sorted according to the specified stat. The `order` parameter is by default set to `"ASC"`, which means the fixtures are sorted in ascending order. The `order` parameter can be set to `"DESC"` to sort the fixtures in descending order.

```py
sorted_list = Object.sort_fixtures(sort_by="temperature", order="DESC")
```

Output:

    
```py
{
    "serial_number": "000000000SVS1Z00977HS999000",
    "name": "Sensor7",
    "type": "LUMINAIRE",
    "temperature": 18.78
},
{
    "serial_number": "000000000SVS1Z00977HS991111",
    "name": "Sensor15",
    "type": "LUMINAIRE",
    "temperature": 16.76
},
```
    




## class LocationsApi(user: str, password: str, ipv4: str)
---
Initiate an LocationsApi-Object.

```py
from smartengine.rapi import locations

engine = locations.LocationsApi(
    user="test", 
    password="test12345", 
    ipv4_adress="192.168.178.1"
)
```


### method get_all_locations(self) -> list[dict]
`Object.get_all_locations()`

---
Gets all locations that are currently available.

```py
locations_list = Object.get_all_locations() 
```

Output: 

   
```py
{
    "id": 222,
    "name": "Office",
    "child_location": false
},
```
    



### method fixture_in_location(self, *fixtures: str) -> list[dict]
`Object.fixture_in_location()`

---
Takes one or more fixtures as an input and returns the location the specified fixture or fixtures are located in. The `fixtures` parameter needs to be one or more serial numbers.

```py
locations_list = Object.fixture_in_location(
    "000000000SVS1Z00977HS999000", "000000000SVS1Z00977HS991111"
)
```
Output:

```py
[
    {
        "fixture": "000000000SVS1Z00977HS999000",
        "room_id": 222,
        "room_name": "Corridor",
        "room_fixtures": [
            "000000000SVS1U0101195006666",
            "CSJ00000000000C020133907777",
            "CSJ00000000000C020133908888",
            "CSJ00000000000C020133909999",
            "000000000SVS1Z00977HS999000",
            "CSJ00000000000C020133901234",
            "CSJ00000000000C020133904321"
        ]
    },
    {
        "fixture": "000000000SVS1Z00977HS991111",
        "room_id": 223,
        "room_name": "Office",
        "room_fixtures": [
            "00300000000001J030151102222",
            "00200000000001J020140203333",
            "00100000000001J020143804444",
            "000000000SVS1Z00977HS991111"
        ]
    }
]
```


### method get_scenes(self, *locations: str) -> list[dict]
`Object.get_scenes()`

---
Takes one or more locations as an input and returns all scenes that are available for the specified location. The `location` parameter takes in either the `id` as and `int`  or the `name` as a `string` of the location. It is recommended to use an `id` rather than a `name`, because an `id` is a unique identifier.

```py
locations_scene_list = Object.get_scenes(
    114, 348
)
```

Output:

```py
[
    {
        "id": 114,
        "name": "Corridor",
        "scenes": {
            "0%": 4,
            "100%": 1,
            "30%": 3,
            "60%": 2,
            "SOS_0": 5,
            "SOS_1": 6,
            "SOS_2": 7,
            "SOS_3": 8,
            "SOS_4": 9,
            "SOS_5": 10,
            "SOS_6": 11
        }
    },
    {
        "id": 348,
        "name": "Office Area",
        "scenes": {}
    }
]
```


### method get_location_stats(self, *locations: str) -> list[dict]
`Object.get_location_stats()`

---
Takes a one or more locations as an input and returns all stats that are available for the specified location. The `location` parameter takes in either the `id` as and `int`  or the `name` as a `string` of the location. It is recommended to use an `id` rather than a `name`, because an `id` is a unique identifier. The stats of a location can include `power`, `ceilingTemperature`, `roomTemperature`, `illuminance`, `brightness`, `motion`, `humidity`, `pressure`, `indoorAirQuality`, `co2` and `voc` depending on the sensors that are installed in the specified location. By default all locations and their stats will be returned.

```py
location_stats_list = Object.get_location_stats(
    114, 348
)
```

Output:

```py
[
    {
        "id": 114,
        "name": "Corridor",
        "room_stats": {
            "power": 18.1,
            "ceilingTemperature": 18.45,
            "roomTemperature": 20.5,
            "illuminance": 51.0,
            "brightness": 0.0,
            "motion": 1701602973,
            "humidity": 31.5,
            "pressure": 100477.0,
            "indoorAirQuality": 69.48,
            "co2": 777.58,
            "voc": 3.01
        }
    },
    {
        "id": 348,
        "name": "Office Area",
        "room_stats": {
            "power": 4.6,
            "ceilingTemperature": 20.51,
            "roomTemperature": 24.05,
            "illuminance": 105.0,
            "brightness": 0.0,
            "motion": 1701450200
        }
    }
]
```
# uApi Documentation
---
## class ApiSetting(user: str, password: str, ipv4_adress: str)
---
Initiate an ApiSetting object to interact with the smardirector's uAPI.

```py
Copy code
from smartengine.uapi import set

api = set.ApiSetting(
    user="admin", 
    password="admin12345", 
    ipv4_adress="192.168.1.1"
)
```

The ApiSetting object allows you to set scenes and the brighness within a location through its methods. It manages uAPI interactions by constructing requests with the necessary credentials and endpoint information.

### Attributes:
---
- ip (str): The IPv4 address of the smart home system's API endpoint.
- user (str): The username for API authentication.
- url (str): The full URL to the API endpoint.
- NotFoundInApiError (int): Error code for not found entities in the API.
- SensorStatsNotAvailableError (int): Error code for unavailable sensor stats.
- MissingArgumentError (int): Error code for missing required arguments.
- sensor_stats (list): A list of possible sensor statistics to retrieve.

### Special Methods:
__repr__:
Returns a formal string representation of the ApiSetting instance.


### method set_scene(self, location: str=None, scene_name: str=None) -> requests.Response
---
Set scenes of a specified location and returns a requests.Response Object
```py
Object.set_scene(location=104, scene_name="PresentaionMode")
```
Activates a specified scene at a given location. This method only works when the specified scene is available for the specified location.

Parameters:
---
- location (int, required): The ID of the location where the scene should be set.
- scene_name (str, required): The name of the scene to activate.

#### Returns:
---
requests.Response: The HTTP response from the API endpoint.

#### Raises:
---
- ValueError: If location is not provided.
- ValueError: If scene_name is not provided.


Output:

```py
{
    response = Object.set_scene(location=104, scene_name="PresentaionMode")
    response.status_code
    >>> 200
}
```

### method set_brightness(self, location: int=None, brightness: int=None) -> requests.Response
```py
Object.set_brightness(location=104, brightness=66)
```

Parameters:
---
- location (int, required): The ID of the location where the brightness should be set.
- brightness (int, required): The desired brightness level, where acceptable values range from 0 (off) to 100 (maximum brightness).

#### Returns:
---
requests.Response: The HTTP response from the uAPI endpoint.

#### Raises:
---

ValueError: If location is not provided.
ValueError: If brightness is not provided.

Output:

```py
{
    response = Object.set_scene(location=104, scene_name="PresentaionMode")
    response.status_code
    >>> 200
}
```



The `ApiSubscription` class is designed for managing API subscriptions to stream real-time location and fixture data from a smartdirector's API.

## Class ApiSubscription(user: str, password: str, ipv4_adress: str)
---
Initiate an ApiSetting object to interact with the smardirector's uAPI.
The methods of this class are generator objects, which are only yielding the specified data, when the server sends data. The Server only sends data, when there is a change in the specified data.
(e.g. temperature: 22° C -> temperature 22,3° C => Server sends 22,3° C)

```py
from smartengine.u_api import subscribe
api = subscribe.ApiSubscription(
    user="admin", 
    password="admin12345", 
    ipv4_adress="192.168.1.1"
)
```
This ApiSubscription Object establishes a connection with a smartdirector's API using provided user credentials and an IP address. It supports streaming data for specific locations or fixtures by subscribing to the server's updates, ensuring continuous data flow as changes occur.

### Attributes
---
- ip (str): IP address of the network system, default set to '192.168.1.1'.
- user (str): Username for authentication with the network system.
- url (str): Formatted URL string for making API requests.
- NotFoundInApiError (int): Custom error code for not found errors in API.
- SensorStatsNotAvailableError (int): Custom error code for unavailable sensor statistics.
- MissingArgumentError (int): Custom error code for missing arguments in method calls.
- sensor_stats (list[str]): List of available sensor statistics that can be streamed.

### Special Methods
__repr__:
Returns a formal string representation of the ApiSubscription instance.


### method stream_location_data(self, location: int=None, sensor_stat: str=None) -> dict
---
Generates a stream of data for a specified location and its datapoints.

Parameters:
---
- location (str, optional): ID of the location.
- sensor_stat (str, required): Specific room data to subscribe to.

#### Yields:
---
dict: A dictionary containing the streamed data for the specified location and its sensor data.

#### Raises:
---
- ValueError: If the provided 'sensor_stat' is not available.

#### Example Usage:
---

```py
api = ApiSubscription(user='admin', password='password123', ipv4_adress="192.168.178.1")
generator_object = api.stream_location_data(location=101, sensor_stat="roomTemperature")
for data in generator_object:
    print(data)
```


### method stream_fixture_data(self, fixture: str=None, sensor_stat: str=None) -> dict
---
Generates a stream of data for a specified fixture and its sensor data.

Parameters:
---
- fixture (str, required): Serial number of the fixture.
- sensor_stat (str, optional): Specific sensor status to subscribe to.

#### Yields:
---
dict: A dictionary containing the streamed data for the specified fixture.

#### Raises:

- ValueError: If 'fixture' is not provided or if the provided 'sensor_stat' is not available.

#### Example Usage
---

```py
api = ApiSubscription(user='admin', password='password123')
for data in api.stream_fixture_data(location=101, sensor_stat="humidity"):
    print(data)
```
Note: This class utilizes streaming HTTP requests, and the yielded dictionaries depend on the response structure from the server. It is designed to continuously yield data as long as the server provides it.