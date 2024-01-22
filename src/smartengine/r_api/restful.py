from . import fixtures, locations

import json
import requests



class rApi(fixtures.FixturesApi, locations.LocationsApi):
    """
    A combined API class inheriting functionalities from FixturesApi and LocationsApi.

    This class integrates the capabilities of both FixturesApi and LocationsApi, providing a unified interface 
    for interacting with smartdirector's fixtures and locations. It inherits all methods and attributes from 
    the parent classes, allowing for comprehensive interactions with the smartdirector's API.

    Attributes:
        Inherits all attributes from FixturesApi and LocationsApi, including user credentials, IP address, 
        and JSON data pertaining to fixtures and locations.

    Methods:
        __repr__: Returns a formal string representation of the rApi instance.
        __str__: Returns a string representation of the raw response from the rApi endpoint.

    The rApi class is designed to be a versatile tool for managing and retrieving data from a smartdirector, 
    combining the functionalities related to fixtures and locations into one accessible class. It can be particularly 
    useful in scenarios where a unified approach is required to handle both fixture and location data.

    Example:
        api = rApi(user='admin', password='secret', ipv4_adress='192.168.0.10')
        locations = api.get_all_locations()
        fixitures = api.get_all_fixtures()
        print(locations)
        print(fixtures)
    """
    def __repr__(self):
        return f"{__class__.__name__}({self.user}, {self.password}, ip_adress={self.ip})"
    
    
    def __str__(self):
        return requests.get(f"https://{self.ip}/rApi", auth=(self.user, self.password), verify=False)

    