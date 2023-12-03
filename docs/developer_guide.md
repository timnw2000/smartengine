# Developer Documentation
---
This Documentation serves as a guide on how to use this package and its including classes and methods.


### class FixtureApi(user: str, password: str, ipv4: str)
`smartengine.rapi.fixtures`

---
Initiate an FixtureApi-Object.

    from smartengine.rapi import fixtures

    engine = fixtures.FixtureApi(
        user="test", 
        password="test12345", 
        ipv4_adress="192.168.178.1"
    )

#### method get_all_fixtures(self) -> list[dict]
`Object.get_all_fixtures()`

---
Gets all Fixtures that are currently in a location

    fixtures_list = Object.get_all_fixtures() 

Output: 
    
    list of dictionaries containing data about each fixture

#### method get_beacons(self, sensor_type: list[str]=None) -> list[dict]
`Object.get_beacons()`

---
Gets all beacons that are currently in a location if `sensor_type` in not specified
When `sensor_type` is specified only get beacons with the specified sensor_type.
Specified `sensor_type` needs to be a list. The default is sensor_types are `["LUMINAIRE", "WALL_SWITCH_5B"]`

    beacons_list = Object.get_beacons(sensor_type=["LUMINAIRE"])

Output: 
    
    list of dictionaries containing data about each fixture

#### method get_sensor_stats(self, *sensors: str, sensor_type: list[str]=None) -> list[dict]
`Object.get_sensor_stats()`

---
Gets all fixtures and their stats of fixtures that are currently in a location if `sensors` and `sensor_type` are not specified. `sensors` specifies the fixtures from which stats get returned. By default all fixtures will be taken into account. When `sensor_type` is specified only get fixtures and their stats with the specified sensor_type. Specified `sensor_type` needs to be a list. The default is sensor_types are `["LUMINAIRE", "WALL_SWITCH_5B"]`

    stats_list = Object.get_sensor_stats(["test_serialnumber1", "test_serialnumber2"]sensor_type=["LUMINAIRE"])

Output: 
    
    list of dictionaries containing data about each fixture


#### method (self, *fixtures: str, sort_by: str="power", order: str="ASC") -> list[dict]
`Object.sort_fixtures()`

---

