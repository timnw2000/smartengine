import requests
import json

class FixturesApi:

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


    