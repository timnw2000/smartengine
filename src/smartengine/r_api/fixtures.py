import requests
import json

class FixturesApi:
    """
    A class for interacting with a smartdirector's rAPI to retrieve and process fixture data.

    This class establishes a connection to a ssmartdirector using IP address, username, and password 
    credentials. It fetches and stores JSON data from the smartdirector, focusing on fixture-related information. 
    The class provides various methods to parse, manipulate, and retrieve specific data related to fixtures.

    Attributes:
        ip (str): IP address of the network system, default set to '192.168.1.1'.
        user (str): Username for authentication to access the network system.
        password (str): Password for authentication.
        system_name (str): Name of the smartengine-system extracted from the JSON data.

    Methods:
        __repr__: Returns a formal string representation of the FixturesApi instance.
        __str__: Returns a string representation of fixture information in JSON format.
        get_all_fixtures: Retrieves detailed information about all fixtures.
        get_beacons: Fetches beacon information for fixtures based on specified sensor types.
        get_sensor_stats: Retrieves sensor statistics for specific sensors and sensor types.
        sort_fixtures: Sorts a list of fixtures based on a specified attribute and order.

    The class uses HTTP requests to communicate smartdirector and is capable of handling various fixture-related 
    queries and operations, such as retrieving all fixture data, filtering beacons, fetching sensor statistics, and 
    sorting fixtures based on specific criteria.

    Example:
        api = FixturesApi(user='admin', password='password123')
        fixture_data = api.get_all_fixtures()
        print(fixture_data)
    """
    def __init__(self, user: str, password: str, ipv4_adress: str="192.168.1.1"):
        self.ip = ipv4_adress
        self.user = user
        self.password = password
        self.json_ = requests.get(f"https://{self.ip}/rApi", auth=(self.user, self.password), verify=False).json()
        self.system_name = self.json_["name"]
        

    def __repr__(self):
        return f"{__class__.__name__}({self.user}, {self.password}, ip_adress={self.ip})"


    def __str__(self):
        return json.dumps(self.json_["fixture"], indent=4)


    def get_all_fixtures(self) -> list[dict]:
        """
        Retrieves all fixture information from the stored JSON data.

        This method parses the 'fixture' key in the 'self.json_' object to collect data about each fixture. For each 
        fixture, it captures essential details such as serial number, name (if available), and type. If a fixture does 
        not have a name specified, the name is set to None.

        Returns:
        - list[dict]: A list of dictionaries, where each dictionary contains details of a fixture. This includes the 
        fixture's serial number, name, and type.

        Each dictionary in the returned list has the following format:
            {
                "serial_number": <fixture_serial_number>,
                "name": <fixture_name> or None if not specified,
                "type": <fixture_type>
            }

        Notes:
        - The method handles cases where the 'name' key might be missing for some fixtures. In such cases, it sets 
        the 'name' field to None, ensuring consistent data structure across all fixture entries.
        """


        all_fixtures = []
        for element in self.json_["fixture"]:
            fixture = {}
            fixture["serial_number"] = element["serialNum"]
            try:
                fixture["name"] = element["name"]
            except KeyError:
                fixture["name"] = None

            fixture["type"] = element["type"]
            all_fixtures.append(fixture)

        return all_fixtures


    


    def get_beacons(self, sensor_type: list[str]=None) -> list[dict]:
        """
        Retrieves a list of beacons from the stored JSON data based on specified sensor types.

        This method filters and returns beacon information for fixtures that support beacon functionality. The 
        filtering is based on a list of sensor types. If no sensor type is specified, it defaults to include 
        "LUMINAIRE", "WALL_SWITCH_5B", and "SENSOR".

        Parameters:
        - sensor_type (list[str], optional): A list of sensor types to filter the beacons. Defaults to 
        ["LUMINAIRE", "WALL_SWITCH_5B", "SENSOR"] if None.

        Returns:
        - list[dict]: A list of dictionaries, each representing a beacon. The dictionaries include the beacon's 
        serial number, name (if available), type, and a boolean indicating beacon support.

        Each dictionary in the returned list has the following structure:
            {
                "serial_number": <beacon_serial_number>,
                "name": <beacon_name> or None if not specified,
                "type": <beacon_type>,
                "beaconSupported": True
            }

        Notes:
        - The method only includes fixtures in the returned list if the 'beaconSupported' field is True and the 
        fixture type matches one of the specified sensor types.
        - In cases where the 'name' key is missing for a beacon, the 'name' field in the dictionary is set to None.
        - The method handles 'KeyError' if either 'beaconSupported' or 'type' keys are missing in any fixture 
        entries, skipping those fixtures.
        """


        if sensor_type is None:
            sensor_type = ["LUMINAIRE", "WALL_SWITCH_5B", "SENSOR"]

        all_beacons = []
        for element in self.json_["fixture"]:
            try:
                if element["beaconSupported"] == True and element["type"] in sensor_type:
                    beacon = {}
                    beacon["serial_number"] = element["serialNum"]
                    try:
                        beacon["name"] = element["name"]
                    except KeyError:
                        beacon[element["serialNum"]]["name"] = None

                    beacon["type"] = element["type"]
                    beacon["beaconSupported"] = True
                    all_beacons.append(beacon)
            except KeyError:
                pass
            
        return all_beacons





    def get_sensor_stats(self, *sensors: str, sensor_type: list[str]=None) -> list[dict]:
        """
        Retrieves sensor statistics for specified sensors and sensor types from stored JSON data.

        This method filters and returns statistics for sensors based on the provided sensor serial numbers and 
        sensor types. If no specific sensors are provided, it returns stats for all sensors of the specified types. 
        The default sensor types are "LUMINAIRE", "WALL_SWITCH_5B", and "SENSOR".

        Parameters:
        - sensors (str): Variable number of arguments, each a string representing a sensor serial number.
        - sensor_type (list[str], optional): A list of sensor types to filter the sensors. Defaults to 
        ["LUMINAIRE", "WALL_SWITCH_5B", "SENSOR"] if None.

        Returns:
        - list[dict]: A list of dictionaries, each representing the statistics of a sensor. The dictionaries 
        include the sensor's serial number and a nested dictionary of its stats.

        Each dictionary in the returned list has the following structure:
            {
                "serial_number": <sensor_serial_number>,
                "stats": {
                    <stat_key>: <stat_value> or None if not available,
                    ...
                }
            }

        Notes:
        - If specific sensors are provided, only those matching the serial numbers and types in 'sensor_type' are 
        included.
        - The method converts the 'instant' values of sensor stats to floats. If the 'instant' key is missing, 
        the corresponding stat value is set to None.
        - The method handles 'KeyError' if 'sensorStats' is missing in any fixture entries, skipping those fixtures.
        """


        if sensor_type is None:
            sensor_type = ["LUMINAIRE", "WALL_SWITCH_5B", "SENSOR"]

        all_sensor_stats = []
        if len(sensors) > 0:
            for sensor in sensors:
                for element in self.json_["fixture"]:
                    if element["serialNum"] == sensor and element["type"] in sensor_type:
                        stats = {}
                        stats["serial_number"] = element["serialNum"]
                        stats["stats"] = {}
                        try:
                            for key in element["sensorStats"]:
                                try:
                                    stats["stats"][key] = float(element["sensorStats"][key]["instant"])
                                except KeyError:
                                    stats["stats"][key] = None
                        except KeyError:
                            pass

                        all_sensor_stats.append(stats)
            
            return all_sensor_stats
        else:
            for element in self.json_["fixture"]:
                if element["type"] in sensor_type:
                    stats = {}
                    stats["serial_number"] = element["serialNum"]
                    stats["stats"] = {}
                    try:
                        for key in element["sensorStats"]:
                            try:
                                stats["stats"][key] = float(element["sensorStats"][key]["instant"])
                            except KeyError:
                                stats["stats"][key] = None
                    except KeyError:
                        pass

                    all_sensor_stats.append(stats)
                
            return all_sensor_stats


        


    def sort_fixtures(self, *fixtures: str, sort_by: str="power", order: str="ASC") -> list[dict]:
        """
        Sorts a list of fixtures based on a specified attribute and order.

        This method sorts fixtures by a specified attribute such as power, temperature, illuminance, etc., 
        in either ascending (ASC) or descending (DESC) order. If no fixtures are specified, it sorts all fixtures 
        in 'self.json_["fixture"]'. The method defaults to sorting by 'power' in ascending order if 'sort_by' or 
        'order' parameters are not provided or are invalid.

        Parameters:
        - fixtures (str): Variable number of arguments, each a string representing a fixture's serial number.
        - sort_by (str, optional): The attribute to sort the fixtures by. Defaults to "power".
        - order (str, optional): The order of sorting, either "ASC" for ascending or "DESC" for descending. 
        Defaults to "ASC".

        Returns:
        - list[dict]: A sorted list of dictionaries, each representing a fixture. Each dictionary includes 
        the fixture's serial number, name (if available), type, and the specified sorting attribute.

        Each dictionary in the returned list has the following structure:
            {
                "serial_number": <fixture_serial_number>,
                "name": <fixture_name> or None if not specified,
                "type": <fixture_type>,
                <sort_by>: <value_of_sort_by_attribute>
            }

        Notes:
        - The method ensures the 'sort_by' attribute is one of the predefined sensor attributes. If not, it defaults 
        to "power".
        - The method converts the sorting attribute value to a float for numerical sorting. In cases where the 
        attribute value is missing, it is set to infinity (float("inf")).
        - Sorting is applied based on the provided 'order' parameter (ascending or descending).
        """


        if sort_by in ["power", "temperature", "illuminance", "brightness", "humidity", "voc", "co2", "airPressure", "indoorAirQuality"]:
            pass
        else:
            sort_by = "power"

        if order in ["ASC", "DESC"]:
            pass
        else:
            order = "ASC"

        sorted_fixtures = []

        if len(fixtures) > 0:
            for serialnumber in fixtures:
                for element in self.json_["fixture"]:
                    if element["serialNum"] == serialnumber:
                        fixture = {}
                        fixture["serial_number"] = element["serialNum"]
                        try:
                            fixture["name"] = element["name"]
                        except KeyError:
                             fixture["name"] = None

                        fixture["type"] = element["type"]
                        
                        try:
                            fixture[sort_by] = float(element["sensorStats"][sort_by]["instant"])
                        except KeyError:
                            fixture[sort_by] = float("inf")

                        sorted_fixtures.append(fixture)

        else:
            for element in self.json_["fixture"]:
                fixture = {}
                fixture["serial_number"] = element["serialNum"]
                try:
                    fixture["name"] = element["name"]
                except KeyError:
                    fixture["name"] = None
                fixture["type"] = element["type"]
                
                try:
                    fixture[sort_by] = float(element["sensorStats"][sort_by]["instant"])
                except KeyError:
                    fixture[sort_by] = float("inf")
                sorted_fixtures.append(fixture)

        if order == "ASC":
            sorted_fixtures.sort(key=lambda element: element[sort_by])
            return sorted_fixtures
        else:
            sorted_fixtures.sort(key=lambda element: element[sort_by], reverse=True)
            return sorted_fixtures
