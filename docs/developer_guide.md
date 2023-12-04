# Developer Documentation
---
This Documentation serves as a guide on how to use this package and its including classes and methods.




## class FixturesApi(user: str, password: str, ipv4: str)
---
Initiate an FixtureApi-Object.

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
Returns all beacons that are currently in a location if `sensor_type` in not specified
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
Takes a one or more locations as an input and returns all scenes that are available for the specified location. The `location` parameter takes in either the `id` as and `int`  or the `name` as a `string` of the location. It is recommended to use an `id` rather than a `name`, because an `id` is a unique identifier.

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
