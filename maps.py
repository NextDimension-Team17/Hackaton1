import requests


def get_streets():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area(30.1406, 59.8085, 30.5560, 60.1005);
    (way(area);<;);out;
    """
    r = requests.get(overpass_url, params={'data': overpass_query})
    
    open('./data/draft.txt', 'wb').write(r.content)
