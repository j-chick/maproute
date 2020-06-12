import os
import re
import subprocess

from config import DIR_TEMP_FILES

WHOIS_LOCATION_FIELDS = (
    # 'address', NOTE
    'city',
    'stateprov',
    'country'
)

def whois(host: str) -> int:
    cmd = ['whois', host]
    suffix = host.replace('.', '_')
    filename_output = os.path.join(DIR_TEMP_FILES, f'nslookup_{suffix}')
    with open(filename_output, 'w') as fp:
        cp = subprocess.run(cmd, stdout=fp)
        assert cp.returncode == 0
    return WhoisOutput(filename_output)

class WhoisOutput(list): #TODO inherit a class?
    def __init__(self, path_output: str) -> None:
        super(WhoisOutput, self).__init__()
        assert os.path.isfile(path_output)
        with open(path_output, 'r') as fp:
            output = fp.readlines()
        assert bool(output)
        section = dict()
        mid_section = False
        for line in map(lambda l: l[:-1], output):
            m = re.match(r'([A-Za-z]+): +(.+)$', line)
            if m is None:
                if mid_section:
                    mid_section = False
                    self.append(section)
                    section = dict()
            else:
                mid_section = True
                key = m.group(1).lower()
                value = m.group(2)
                if key in section.keys():
                    section[key] += f' {value}'
                else:
                    section[key] = value

if __name__ == '__main__':
    import requests, json
    def get_global_coordinates(location: str) -> tuple:
        response = requests.get(f'http://nominatim.openstreetmap.org/search?q={location}&format=json')
        data = json.loads(response.text)
        if len(data) == 0:
            return None
        best = data[0]
        lat = float(best['lat'])
        lon = float(best['lon'])
        return (lat, lon)
    
    def get_most_precise_location(sections: dict) -> tuple:
        locations = []
        for section in sections:
            location = {k:v for (k, v) in section.items() if k in WHOIS_LOCATION_FIELDS}
            if len(location.keys()) > 0:
                locations.append(location)
        if len(locations) == 0:
            return None
        location = locations[0] #NOTE naive selection
        search_string = ''
        most_precise_coords = None
        for location_field in reversed(WHOIS_LOCATION_FIELDS):
            if location_field in location.keys():
                search_string = f'{location[location_field]} {search_string}'
                coords = get_global_coordinates(search_string)
                if coords is not None:
                    most_precise_coords = coords
                print('===', coords, search_string)
        return most_precise_coords

    # sections = whois('128.193.4.112')
    # sections = whois('129.78.5.8')
    sections = whois('50.53.152.1')
    location = get_most_precise_location(sections)
    print('-->', location)
