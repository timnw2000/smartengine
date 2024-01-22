import requests
import json
import threading
import re

class ApiSetting:
    """
    A class for managing and setting scenes and policies.

    This class provides functionality to interact with a smartdirector's uAPI for the purpose of setting or updating 
    various configurations such as scenes and policies. It is designed to send structured requests to the uAPI using 
    provided user credentials and an IP address.

    Attributes:
        ip (str): The IP address of the network system, default set to '192.168.1.1'.
        user (str): Username for authentication with the network system.
        __password (str): Password for authentication, kept private within the class.
        url (str): Formatted URL string for making API requests.
        NotFoundInApiError (int): Custom error code for not found errors in API.
        SensorStatsNotAvailableError (int): Custom error code for unavailable sensor statistics.
        MissingArgumentError (int): Custom error code for missing arguments in method calls.
        sensor_stats (list[str]): List of available sensor statistics.

    Methods:
        __repr__: Returns a formal string representation of the ApiSetting instance.
        set_scenes: Sets a specific scene for a given location in the network system.
        set_policy: Activates a specific policy for a given location in the network system.

    The class primarily handles sending structured JSON requests to smartdirectors's uAPI to modify or set various 
    configurations. These configurations include scenes and policies which can be specified for different locations.

    Example:
        api_setting = ApiSetting(user='admin', password='password123')
        response = api_setting.set_scenes(location='101', scene_name='Evening')
        print(response)
    """
    def __init__(self, user: str, password: str, ipv4_adress: str="192.168.1.1"):
        self.ip = ipv4_adress
        self.user = user
        self.__password = password
        self.url = f"https://{ipv4_adress}/uApi"
        self.NotFoundInApiError = 8080
        self.SensorStatsNotAvailableError = 5050
        self.MissingArgumentError = 2020
        self.sensor_stats = [
            "illuminance",
            "ceillingTemperature",
            "roomTemperature",
            "power",
            "brightness",
            "motion",
            "temperature",
            "voc",
            "co2",
        ]


    def __repr__(self):
        return f"{__class__.__name__}({self.user}, {self.__password}, {self.ip})"


    def set_scenes(self, location: str=None, scene_name: str=None):
        if scene_name is None:
            raise ValueError(f"{self.MissingArgumentError}: Missing name of the scene")
        payload = {
            "protocolVersion" : "1",
            "schemaVersion" : "1.4.0",
            "requestType" : "set",
            "requestData" : {
            "location" : [
                {
                "id" : location,
                "sceneControl" : {
                    "activeSceneName" : scene_name
                }
                }
            ]
            }
        }
        json_payload = json.dumps(payload)
        response = requests.post(url=self.url, data=json_payload, verify=False, auth=(self.user, self.__password))
        return response
    



    
    def set_policy(self, location: str=None, policy_name: str=None):
        if policy_name is None:
            raise ValueError(f"{self.MissingArgumentError}: Missing name of the policy")
        payload = {
            "protocolVersion" : "1",
            "schemaVersion" : "1.4.0",
            "requestType" : "set",
            "requestData" : {
            "location" : [
                {
                "id" : location,
                "policyTrigger": [{
                    "name": policy_name,
                    "activeValue": 1 
                    }]
                }
            ]
            }
        }
        json_payload = json.dumps(payload)
        response = requests.post(url=self.url, data=json_payload, verify=False, auth=(self.user, self.__password))
        return response



def main():
    api = ApiSetting(user="admin", password="FiatLux007", ipv4_adress="192.168.178.10")
    api.set_policy(location=104, policy_name="100%")


if __name__ == "__main__":
    main()