import json
import requests


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
        set_scene: Sets a specific scene for a given location in the network system.
        set_policyTrigger: Activates a specific policy for a given location in the network system.

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
            "humidity",
            "pressure",
            "indoorAirQuality",
        ]


    def __repr__(self):
        return f"{__class__.__name__}({self.user}, {self.__password}, {self.ip})"


    def set_scene(self, location: int=None, scene_name: str=None) -> requests.Response:
        """
        Sets the scene for a given location.

        This method sends a POST request to the smartdirecor's endpoint with the
        desired scene configuration. The request sets the active scene for a
        specified location based on the scene_name provided. Note: This can only be successfull
        if a scene with the specified name exists in the specified location.

        Parameters:
        - location (str, optional): The unique identifier for the location where the scene is to be set.
        - scene_name (str, optional): The name of the scene to activate at the location.

        Returns:
        - requests.Response: The response object resulting from the POST request.

        Raises:
        - ValueError: If the scene_name is not provided.

        Note:
        The method disables SSL certificate verification and uses basic authentication
        with the stored user credentials. Make sure the URL and credentials are correctly set 
        for the instance before calling this method.

        Example usage:
        >>> response = set_scene(location="12345", scene_name="Evening Relaxation")
        >>> response.status_code
        200
        """
        if scene_name is None:
            raise ValueError(f"{self.MissingArgumentError}: scene_name argument was not specified")
        if location is None:
            raise ValueError(f"{self.MissingArgumentError}: location argument was not specified")
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
    
    



    def set_brightness(self, location: int=None, brightness: int=None) -> requests.Response:
        """
        Sends a request to set the brightness level for a specific location.

        This method configures the brightness of a specified location by
        sending a JSON payload via a POST request to the designated uApi. Both the location
        and brightness levels are required arguments. The method handles basic authentication 
        using the instance's user credentials and does not verify SSL certificates.

        Parameters:
        - location (int, required): The unique identifier (ID) for the target location.
        - brightness (int, required): The desired brightness level, where acceptable values
                                      range from 0 (off) to 100 (maximum brightness).

        Returns:
        - requests.Response: The response object from the POST request, which includes the 
                            status code and any returned data.

        Raises:
        - ValueError: If either 'location' or 'brightness' arguments are not provided.

        Examples:
        >>> response = set_brightness(location=123, brightness=75)
        >>> response.status_code
        200
        """
        if location is None:
            raise ValueError(f"{self.MissingArgumentError}: loctaion argument was not specfied")
        if brightness is None:
            raise ValueError(f"{self.MissingArgumentError}: brightness argument was not specified")
        payload = {
            "protocolVersion" : "1",
            "schemaVersion" : "1.4.0",
            "requestType" : "set",
            "requestData" : {
            "location" : [
                {
                    "id" : location,
                    "wallSwitch":{
                    "lowLevelControl":{
                        "brightness":brightness,
                        "activated":-9999999
                    }
                    }
                }
            ]
            }
        }
        json_payload = json.dumps(payload)
        response = requests.post(url=self.url, data=json_payload, verify=False, auth=(self.user, self.__password))
        return response
