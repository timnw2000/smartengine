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
        mapping = []
        if len(fixtures) > 0:
            for sensor in fixtures:
                for element in self.json_["location"]:
                    try:
                        if element["childFixture"]:
                            for serial in element["childFixture"]:
                                if sensor == serial[10:]:
                                    link = {}
                                    link["fixture"] = sensor
                                    link["room_id"] = element["id"]
                                    link["room_name"] = element["name"]
                                    link["room_fixtures"] = element["childFixture"]
                                    mapping.append(link)
                                    break
                    except KeyError:
                        continue
            return mapping
        
        else:
            raise ValueError("Argument - fixtures - is missing")
        




    def get_scenes(self, *locations: str) -> list[dict]:
        all_room_scenes = []
        if len(locations) > 0:
            for location in locations:
                for element in self.json_["location"]:
                    if element["id"] == location or element["name"] == location:
                        room = {}
                        room["id"] = element["id"]
                        room["name"] = element["name"]
                        room["scenes"] = []
                        try:
                            for scene in element["sceneControl"]["scene"]:
                                room["scenes"].append({scene["name"]: scene["order"]})
                                
                        except KeyError:
                            continue
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
                room["scenes"] = []
                try:
                    for scene in element["sceneControl"]["scene"]:
                        room["scenes"].append({scene["name"]: scene["order"]})
                        
                except KeyError:
                    continue
                else:
                    all_room_scenes.append(room)

            return all_room_scenes
        
        



    def get_location_stats(self, *locations: str) -> list[dict]:
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
                    pass
                else:
                    all_location_stats.append(room)
            
            return all_location_stats
        
