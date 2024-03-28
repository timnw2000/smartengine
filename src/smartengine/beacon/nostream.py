import requests


class Beacon:
    def __init__(self, user: str, password: str, ipv4_adress: str="192.168.1.1"):
        self.ip = ipv4_adress
        self.user = user
        self.password = password
        self.json_ = requests.get(f"https://{self.ip}/rApi", auth=(self.user, self.password), verify=False).json()
        self.system_name = self.json_["name"]
        self.recieve = # recieve uuids
        self.transmit = # transmit uuid
    
    # creating filter by posting to rApi
    def create_filter(self):
        ...

    # locating beacon by location name
    def locate_beacon_by_location(self):
        ...

    # locating beacon by
    def locate_beacon_by_fixture(self):
        ...

    # showing the fixture with the best signal to beacon
    def strongest_signal(self):
        ...
