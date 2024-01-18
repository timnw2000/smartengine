import requests
import json
import threading
import re


class ApiSubscription:
    def __init__(self, user: str, password: str, ipv4_adress: str="192.168.1.1"):
        self.ip = ipv4_adress
        self.user = user
        self.password = password
        self.url = f"https://{ipv4_adress}/uApi"
        self.sensor_stats = [
            "illuminance",
            "ceillingTemperature",
            "power",
            "brightness",
            "motion",
        ]

    def __repr__(self):
        return f"{__class__.__name__}({self.user}, {self.password}, {self.ip})"
    




    def stream_location_data(self, location=None, sensor_stat=None) -> dict:
        if not sensor_stat:
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
        elif sensor_stat in self.sensor_stats:
            payload = {
                "protocolVersion" : "1",
                "schemaVersion" : "1.4.0",
                "requestType" : "subscribe",
                "requestData" : {
                    "location" : [
                        {
                            "id" : location,
                            "sensorStats" : {
                                f"{sensor_stat}" : None,
                            }
                        }
                    ]
                }
            }
        else:
            raise ValueError("Specified Sensorstat is generally not available")
        
        json_payload = json.dumps(payload)
        chunks = ""
        # Send the post request with the payload
        #try:
        response = requests.post(self.url, data=json_payload, verify=False, auth=(self.user, self.password), stream=True)
        counter1 = 0
        counter2 = 0
        #for chunk in response.iter_content(chunk_size=128):
        for chunk in response.iter_content(chunk_size=128):
            if chunk:
                decoded_chunk = chunk.decode()
                if "responseData" in decoded_chunk:
                    if counter1 == 0:
                        counter1 += 1
                        continue
                    chunks = ""
                    chunks = chunks + decoded_chunk
                if "location" in decoded_chunk:
                    if counter2 == 0:
                        counter2 += 1
                        continue
                    chunks = chunks + decoded_chunk
                if "_c_instant" in decoded_chunk:

                    chunks = chunks + decoded_chunk
                    if "\r\n\r\n\r\n" in chunks:
                        #chunks = chunks.replace("\r\n\r\n\r\n", "")
                        #json_data = json.loads(chunks)
                    
                        chunks.replace("\r\n\r\n\r\n", "")
                        chunks = json.loads(chunks)
                        yield chunks
                        




def main():
    api = ApiSubscription(user="admin", password="smartengine", ipv4_adress="78.94.221.187:53311")

    generator = api.stream_location_data(147, "illuminance")
    for element in generator:
        print(element)





if __name__ == "__main__":
    main()






'''

# Define the request payload
payload = {
    "protocolVersion" : "1",
    "schemaVersion" : "1.4.0",
    "requestType" : "subscribe",
    "requestData" : {
        "location" : [
            {
                "id" : 144,
                "sensorStats" : {
                    "roomTemperature" : {}
                }
            },
        ]
    }
}





# Convert the payload to JSON format
json_payload = json.dumps(payload)
chunks = ""
# Send the post request with the payload
#try:
response = requests.post(url, data=json_payload, verify=False, auth=("admin", "FiatLux007"), stream=True)
counter1 = 0
counter2 = 0
counter3 = 0
#for chunk in response.iter_content(chunk_size=128):
for chunk in response.iter_content(chunk_size=128):

    if chunk:
        decoded_chunk = chunk.decode()
        if "responseData" in decoded_chunk:
            if counter1 == 0:
                counter1 += 1
                continue
            chunks = chunks + decoded_chunk
        if "location" in decoded_chunk:
            if counter2 == 0:
                counter2 += 1
                continue
            chunks = chunks + decoded_chunk
        if "_c_instant" in decoded_chunk:

            chunks = chunks + decoded_chunk
            if "\r\n\r\n\r\n" in chunks:
                #chunks = chunks.replace("\r\n\r\n\r\n", "")
                #json_data = json.loads(chunks)
            
                chunks.replace("\r\n\r\n\r\n", "")
                chunks = json.loads(chunks)

                temp = chunks["responseData"]["location"][0]["sensorStats"]["roomTemperature"]["instant"]
                print(temp)
            

            chunks = ""
       
'''