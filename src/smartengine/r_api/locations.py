import requests
import json

class LocationsApi:

    def __init__(self, user: str, password: str, ipv4_adress: str="192.168.1.1"):
        self.ip = ipv4_adress
        self.user = user
        self.password = password
        self.json_ = requests.get(f"https://{self.ip}/rApi", auth=(self.user, self.password), verify=False).json()
        self.system_name = self.json_["name"]


    def __repr__(self):
        return f"{__class__.__name__}({self.user}, {self.password}, ip_adress={self.ip})"
    
    
    def __str__(self):
        return json.dumps(self.json_["location"], indent=4)
    

    def get_all_locations(self) -> list[dict]:
        """
        Retrieves all location information from the stored JSON data.

        This method iterates through the 'location' key in the 'self.json_' object and constructs a list of dictionaries, 
        each representing a location. For each location, it captures the location ID and name. It also checks for the 
        presence of any child locations and indicates this in the dictionary.

        Returns:
        - list[dict]: A list of dictionaries, each containing details of a location. The details include the location's 
        ID, name, and a boolean indicating whether the location has child locations.

        Each dictionary in the returned list has the following structure:
            {
                "id": <location_id>,
                "name": <location_name>,
                "child_location": <boolean> # True if child locations exist, False otherwise
            }

        Notes:
        - The method safely handles 'KeyError' if the 'childLocation' key is missing in any of the location entries 
        in 'self.json_', defaulting the 'child_location' value to False in such cases.
        """
        all_locations = []
        for element in self.json_["location"]:
            location = {}
            location["id"] = element["id"]
            location["name"] = element["name"]

            try:
                if element["childLocation"]:
                    location["child_location"] = True
            except KeyError:
                location["child_location"] = False

            all_locations.append(location)

        return all_locations
    



    
    def fixture_in_location(self, *fixtures: str) -> list[dict]:
        """
        Maps given fixture serial numbers to their corresponding room details.

        This method takes one or more fixture serial numbers and searches for their corresponding room information 
        within a JSON object stored in 'self.json_'. For each fixture, it finds the room it is located in and 
        compiles a list of all fixtures in that room. If no fixtures are provided as arguments, a ValueError is raised.

        Parameters:
        - fixtures (str): Variable number of arguments, each a string representing a fixture serial number.

        Returns:
        - list[dict]: A list of dictionaries, each representing a mapping of a fixture to its room. Each dictionary 
        contains the fixture serial number, the room ID, the room name, and a list of all fixtures in the room.

        Each dictionary in the returned list has the following structure:
            {
                "fixture": <fixture_serial_number>,
                "room_id": <room_id>,
                "room_name": <room_name>,
                "room_fixtures": [<list_of_fixture_serial_numbers_in_room>]
            }

        Raises:
        - ValueError: If no fixture serial numbers are provided as arguments.

        Notes:
        - The method only adds fixtures to the mapping if they are found in the 'childFixture' field of a room in 
        'self.json_'.
        - The method handles 'KeyError' if the 'childFixture' key is missing in the JSON object and continues 
        processing other fixtures.
        """
        mapping = []
        if len(fixtures) > 0:
            for sensor in fixtures:
                for element in self.json_["location"]:
                    try:
                        if element["childFixture"]:
                            for serial in element["childFixture"]:
                                if sensor == serial[9:]:
                                    link = {}
                                    link["fixture"] = sensor
                                    link["room_id"] = element["id"]
                                    link["room_name"] = element["name"]
                                    link["room_fixtures"] = []

                                    for childFixture in element["childFixture"]:
                                        childFixture = childFixture[9:]
                                        link["room_fixtures"].append(childFixture)
                                    mapping.append(link)
                                    break
                    except KeyError:
                        continue
            return mapping
        
        else:
            raise ValueError("Argument - fixtures - is missing")
        




    def get_scenes(self, *locations: str) -> list[dict]:
        """
        Gathers scene control data for specified rooms based on location identifiers.

        This method processes a list of location identifiers (either IDs or names) and extracts scene control 
        information for each room from a JSON object in 'self.json_'. If 'locations' is empty, scene control data 
        for all rooms in 'self.json_' are collected. The scene control data includes the room's ID, name, and a 
        dictionary of scenes with their corresponding order.

        Parameters:
        - locations (list): A list of location identifiers (IDs or names). If empty, scene control data for all 
        rooms in 'self.json_' will be returned.

        Returns:
        - list: A list of dictionaries, each representing a room. Each dictionary contains the room's ID, name, 
        and a nested dictionary of scenes with their orders. If a room in 'locations' is not found in 
        'self.json_', it is skipped.

        Each dictionary in the returned list has the following structure:
            {
                "id": <room_id>,
                "name": <room_name>,
                "scenes": {
                    <scene_name>: <scene_order>,
                    ...
                }
            }

        Notes:
        - The method handles 'KeyError' if the 'sceneControl' or 'scene' keys are missing in the JSON object, 
        and continues processing other rooms.
        - If a location identifier in the 'locations' list does not match any room in 'self.json_', it is 
        ignored and processing continues with the next identifier.
        """
        all_room_scenes = []
        if len(locations) > 0:
            for location in locations:
                for element in self.json_["location"]:
                    if element["id"] == location or element["name"] == location:
                        room = {}
                        room["id"] = element["id"]
                        room["name"] = element["name"]
                        room["scenes"] = {}
                        try:
                            for scene in element["sceneControl"]["scene"]:
                                room["scenes"][scene["name"]] = scene["order"]
                                
                        except KeyError:
                            all_room_scenes.append(room)
                            pass
                        else:
                            all_room_scenes.append(room)

                    else:
                        pass
            
            return all_room_scenes

        else:
            for element in self.json_["location"]:
                room = {}
                room["id"] = element["id"]
                room["name"] = element["name"]
                room["scenes"] = {}
                try:
                    for scene in element["sceneControl"]["scene"]:
                        room["scenes"][scene["name"]] = scene["order"]
                        
                except KeyError:
                    all_room_scenes.append(room)
                    pass
                else:
                    all_room_scenes.append(room)

            return all_room_scenes
        
        



    def get_location_stats(self, *locations: str) -> list[dict]:
        """
        Collects and returns statistics for specified locations.

        This method processes a list of location identifiers (either IDs or names) and retrieves their corresponding 
        statistics from a JSON object stored in 'self.json_'. If the 'locations' list is empty, it collects statistics 
        for all locations present in 'self.json_'. The statistics for each location include its ID, name, and sensor 
        stats.

        Parameters:
        - locations (list): A list of location identifiers (IDs or names). If empty, statistics for all locations 
        in 'self.json_' will be returned.

        Returns:
        - list: A list of dictionaries, each containing the ID, name, and sensor stats of a location. If a location 
        in the 'locations' list is not found in 'self.json_', it is skipped.

        Each dictionary in the returned list has the following structure:
            {
                "id": <location_id>,
                "name": <location_name>,
                "room_stats": {
                    <sensor_stat_key>: <sensor_stat_value>,
                    ...
                }
            }

        Notes:
        - The method handles 'KeyError' for missing 'sensorStats' in the JSON object and continues processing 
        other locations.
        - If a location identifier in the 'locations' list does not match any location in 'self.json_', it is 
        ignored and processing continues with the next identifier.
        """
        all_location_stats = []
        if len(locations) > 0:
            for location in locations:
                for element in self.json_["location"]:
                    if element["id"] == location or element["name"] == location:
                        room = {}
                        room["id"] = element["id"]
                        room["name"] = element["name"]
                        room["room_stats"] = {}
                        try:
                            for key in element["sensorStats"]:
                                room["room_stats"][key] = element["sensorStats"][key]["instant"]
                        except KeyError:
                            all_location_stats.append(room)
                            pass
                        else:
                            all_location_stats.append(room)

                    else:
                        pass
            
            return all_location_stats
        
        else:
            for element in self.json_["location"]:
                room = {}
                room["id"] = element["id"]
                room["name"] = element["name"]
                room["room_stats"] = {}
                try:
                    for key in element["sensorStats"]:
                        room["room_stats"][key] = element["sensorStats"][key]["instant"]
                except KeyError:
                    all_location_stats.append(room)
                    pass
                else:
                    all_location_stats.append(room)
            
            return all_location_stats
        
