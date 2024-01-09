from . import fixtures, locations

class rApi(fixtures.FixturesApi, locations.LocationsApi):

     def __repr__(self):
        return f"{__class__.__name__}({self.user}, {self.password}, ip_adress={self.ip})"
    
    
    def __str__(self):
        return json.dumps(self.json_["location"], indent=4)

    