import requests
import json

def search_with_vin(vin):
    url = "https://vindecoder.p.rapidapi.com/v2.0/decode_vin"
    querystring = {"vin": vin}
    headers = {
            "X-RapidAPI-Key": "744abc8a30msh83cdcbcce129559p1c2752jsn420d7c779154",
            "X-RapidAPI-Host": "vindecoder.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
   
    return json.loads(response.text)

