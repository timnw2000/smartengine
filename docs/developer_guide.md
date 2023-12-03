# Developer Documentation
---
This Documentation serves as a guide on how to use this package and its including classes and methods.


## class FixtureApi(user: str, password: str, ipv4: str)
---
Initiate an FixtureApi-Object.

    from smartengine.rapi import fixtures

    engine = fixtures.FixtureApi(
        user="test", 
        password="test12345", 
        ipv4_adress="192.168.178.1"
    )

### method get_all_fixtures(self) -> list[dict]
`Object.get_all_fixtures()`

---
Gets all Fixtures that are currently in a location

    fixtures_list = Object.get_all_fixtures() 

Output: 

    ...

    {
        "serial_number": "CSJ00000000001J020143808848",
        "name": "Sensor45",
        "type": "LUMINAIRE"
    },

    ...

### method get_beacons(self, sensor_type: list[str]=None) -> list[dict]
`Object.get_beacons()`

---
Gets all beacons that are currently in a location if `sensor_type` in not specified
When `sensor_type` is specified only get beacons with the specified sensor_type.
Specified `sensor_type` needs to be a list. The default is sensor_types are `["LUMINAIRE", "WALL_SWITCH_5B", "SENSOR"]`

    beacons_list = Object.get_beacons(sensor_type=["LUMINAIRE"])

Output: 

    ...

    {
        "serial_number": "000000000SVS1Z00977HS999000",
        "name": "Sensor2",
        "type": "LUMINAIRE",
        "beaconSupported": true
    },

    ...

### method get_sensor_stats(self, *sensors: str, sensor_type: list[str]=None) -> list[dict]
`Object.get_sensor_stats()`

---
Gets all fixtures and their stats of fixtures that are currently in a location if `sensors` and `sensor_type` are not specified. `sensors` specifies the fixtures from which stats get returned. By default all fixtures will be taken into account. When `sensor_type` is specified only get fixtures and their stats with the specified sensor_type. Specified `sensor_type` needs to be a list. The default is sensor_types are `["LUMINAIRE", "WALL_SWITCH_5B", "SENSOR"]`

    stats_list = Object.get_sensor_stats(
        *["000000000SVS1Z00977HS999000", "000000000SVS1Z00977HS991111"], 
        sensor_type=["LUMINAIRE"]
    )

Output: 
    
    ...

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
    
    ...


### method sort_fixtures(self, *fixtures: str, sort_by: str="power", order: str="ASC") -> list[dict]
`Object.sort_fixtures()`

---
Gets a sorted list of fixtures. The fixtures are sorted by their stats. You can specify the stat, the fixture should be sorted by through the `sort_by` parameter. The `sort_by` parameter takes 9 different parameters:  `"power", "temperature", "illuminance", "brightness", "humidity", "voc", "co2", "airPressure", "indoorAirQuality"`.
By default the fixtures will be sorted by `"power"`.
The `fixtures` parameter takes in serial numbers of fixtures. Only specified fixtures will be sorted according to the specified stat. By default all fixtures will be sorted according to the specified stat. The `order` parameter is by default set to `"ASC"`, which means the fixtures are sorted in ascending order. The `order` parameter can be set to `"DESC"` to sort the fixtures in descending order.

    sorted_list = Object.sort_fixtures(sort_by="temperature", order="DESC")


Output:

    ...

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

    ...

