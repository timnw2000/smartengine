from . import fixtures, locations

import json
import requests



class rApi(fixtures.FixturesApi, locations.LocationsApi):

    def __repr__(self):
        return f"{__class__.__name__}({self.user}, {self.password}, ip_adress={self.ip})"
    
    
    def __str__(self):
        return requests.get(f"https://{self.ip}/rApi", auth=(self.user, self.password), verify=False)

    