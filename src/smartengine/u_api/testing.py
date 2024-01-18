import requests
import json

json_text = '''{
  "location":[
    {
      "id":106,
      "sensorStats":{
        "illuminance":{
          "instant":25.0,
          "_c_instant":"MOD"
        }
      }
    }
  ]
}'''

print(json.loads(json_text))