import requests
import json
import threading
import re


class ApiSubscription:
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


    def stream_location_data(self, location: int=None, sensor_stat: str=None) -> dict:
        """
        Generates a stream of data for a specified location its datapoints.

        This method creates a generator object that streams data from a server. It sends a JSON payload in a POST request 
        to the server to subscribe to data updates for a specified location and sensordata. The server sends data only 
        when there are changes in the data points. Every first payload includes all data points. 
        The method streams the response data in chunks and yields dictionaries 
        containing the updated data points as they become available.

        Parameters:
        - location (str, optional): ID of the location. If None, subscribes to to every location.
        - sensor_stat (str, optional): Specific room data to subscribe to. If None, subscribes to sensor data
        for the given location. Raises a ValueError if the specified sensor data is generally not available.

        Yields:
        - dict: A dictionary containing the streamed data for the specified location and its sensor data.

        Raises:
        - ValueError: If the provided 'sensor_stat' is generally not available.

        Note:
        This method utilizes a streaming HTTP request, and the yielded dictionaries depend on the response structure from 
        the server. It is designed to continuously yield data as long as the server provides it.        
        """
        if sensor_stat is None:
            payload = {
                "protocolVersion" : "1",
                "schemaVersion" : "1.4.0",
                "requestType" : "subscribe",
                "requestData" : {
                    "location" : [
                        {
                            "id" : location,
                            "sensorStats" : {}
                        }
                    ]
                }
            }
        elif sensor_stat not in self.sensor_stats:
            raise ValueError(f"Error: {self.SensorStatsNotAvailableError} - Specified Sensorstat is generally not available")
        else:
            payload = {
                "protocolVersion" : "1",
                "schemaVersion" : "1.4.0",
                "requestType" : "subscribe",
                "requestData" : {
                    "location" : [
                        {
                            "id" : location,
                            "sensorStats" : {
                                sensor_stat : {}
                            }
                        }
                    ]
                }
            }
        json_payload = json.dumps(payload)
        chunks = ""
        response = requests.post(self.url, data=json_payload, verify=False, auth=(self.user, self.__password), stream=True)
        for chunk in response.iter_content(chunk_size=128):
            chunks += (chunk.decode())
            if "\r\n\r\n\r\n" in chunk.decode():
                chunks.replace("\r\n\r\n\r\n", "")
                chunks = json.loads(chunks)
                response_object = chunks
                chunks = ""
                yield response_object
    




    def stream_fixture_data(self, fixture: str=None, sensor_stat: str=None) -> dict:
        """
        Generates a stream of data for a specified fixture its data.

        This method creates a generator object that streams data from a server. It sends a JSON payload in a POST request 
        to the server to subscribe to data updates for a specified fixture and sensor status. The server sends data only 
        when there are changes in the data points. Every first payload includes all data points. The method streams the response data in chunks and yields dictionaries 
        containing the updated data points as they become available.

        Parameters:
        - fixture (str, optional): Serial number of the fixture. If None, raises a ValueError indicating a missing fixture ID.
        - sensor_stat (str, optional): Specific sensor status to subscribe to. If None, subscribes to all sensor data 
        for the given fixture. Raises a ValueError if the specified sensor data is gerally not available.

        Yields:
        - dict: A dictionary containing the streamed data for the specified fixture and sensor status.

        Raises:
        - ValueError: If 'fixture' is not provided or if the provided 'sensor_stat' is generally not available.

        Note:
        This method utilizes a streaming HTTP request, and the yielded dictionaries depend on the response structure from 
        the server. It is designed to continuously yield data as long as the server provides it.        
        """
        if fixture is None:
            raise ValueError(f"Error: {self.MissingArgumentError} - Missing fixture Identification (Serialnumber)")
        if sensor_stat is None:
            payload = {
                "protocolVersion" : "1",
                "schemaVersion" : "1.4.0",
                "requestType" : "subscribe",
                "requestData" : {
                    "fixture" : [
                        {
                            "serialNum" : fixture,
                            "sensorStats" : {}
                        }
                    ]
                }
            }
        elif sensor_stat not in self.sensor_stats:
            raise ValueError(f"Error: {self.SensorStatsNotAvailableError} - Specified Sensorstat is generally not available")
        else:
            payload = {
                "protocolVersion" : "1",
                "schemaVersion" : "1.4.0",
                "requestType" : "subscribe",
                "requestData" : {
                    "fixture" : [
                        {
                            "serialNum" : fixture,
                            "sensorStats" : {
                                sensor_stat : {}
                            }
                        }
                    ]
                }
            }
        json_payload = json.dumps(payload)
        chunks = ""
        response = requests.post(self.url, data=json_payload, verify=False, auth=(self.user, self.__password), stream=True)
        for chunk in response.iter_content(chunk_size=128):
            chunks += (chunk.decode())
            if "\r\n\r\n\r\n" in chunk.decode():
                chunks.replace("\r\n\r\n\r\n", "")
                chunks = json.loads(chunks)
                response_object = chunks
                chunks = ""
                yield response_object








def main():
    api = ApiSubscription(user="admin", password="FiatLux007", ipv4_adress="192.168.178.10")

    generator = api.stream_location_data(104, sensor_stat="motion")
    for element in generator:
        print(element)





if __name__ == "__main__":
    main()
