import requests

def get_weather(loc):
    url = "https://api.seniverse.com/v3/weather/now.json"
    params = {
        "key": "SuN1WD2-UBwjTCODF",
        "location": loc,
        "language": "zh-Hans",
        "unit": "c",
    }
    response = requests.get(url, params=params)
    temperature = response.json()
    return temperature['results'][0]['now']

print(get_weather('北京'))