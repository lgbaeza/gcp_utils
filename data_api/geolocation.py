import requests
import json

def get_geolocation(ip_address):
    request_url = f'https://geolocation-db.com/jsonp/{ip_address}'
    response = requests.get(request_url).content.decode()
    result = response.split("(")[1].strip(")")
    result  = json.loads(result)
    
    country_name = result["country_name"]
    state = result["state"]
    latitude = result["latitude"]
    longitude = result["longitude"]

    return country_name, state, latitude, longitude