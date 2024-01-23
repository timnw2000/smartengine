# smartengine Package
---
This package simplifies the usage of smartengine's Restful-Api. More specifically it simplifies retrieving data from the Api. The data that can be retrieved includes sensor data such as serial_number, name and data sensors are continuesly collecting as well as location data such as location ids, location names and location sensors.



### Installation
---
This package can be installed via the `pip install` command.

    pip install smartengine



### Before Usage
---
Make sure the device that is running this code is connected to the master of the smartengine-system. It's either a smartengine or a smartdirector. The device should preferably be in the same network as the master of the smartengine-system. Physical direct Ethernet connection also works.



### Examples
---
1 - Import Package:

```py
from smartengine.r_api import fixtures, location, restful
from smartengine.u_api import subscribe, set, unified
```


2 - Initiate rAPI:

```py
smartengine1 = fixtures.FixturesApi(
    user="<some_user>", 
    password="<some_password>", 
    ipv4_adress="<master_ipv4_adress>"
)
```
OR

```py
smartengine2 = unified.uApi(
    user="<some_user>", 
    password="<some_password>", 
    ipv4_adress="<master_ipv4_adress>"
)
```


3 - Call desired method:

```py
all_fixtures = smartengine1.get_all_fixtures()
print(all_fixtures) 
>>> list of dictionaries
response = smartengine2.set_brightness(location=103, brightness=50)
print(response.status_code)
>>> 200
```


### Documentation
---
+ [Developer Guide](docs/developer_guide.md) - Documentation for Developers


## License
---
This Package is licensed under the [MIT License](LICENSE)
