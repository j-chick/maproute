#!/usr/local/bin/python3
import argparse
import json
import os
import re
import requests
import shutil
import sys

from config import DIR_TEMP_FILES
from map import Map
from nslookup import nslookup
from traceroute import traceroute
from whois import whois, WHOIS_LOCATION_FIELDS

RE_IP = r'([0-9]{1,3}\.){3}([0-9]{1,3})'
RE_HOSTNAME = r'(www\.)?([0-9A-za-z]{1,63}\.)+([a-zA-Z]{2,4})'

# 129.78.5.8
# sydney.edu.au

def main(args):

    # Establish IPv4 address
    if not is_valid_ip(args.host):
        if is_valid_hostname(args.host):
            args.host = nslookup(args.host)
        else:
            raise IOError(f'Could not parse argument \'host\': {args.host}')
    print(args.host)

    # Trace the route
    if True: # FIXME
        traceroute_output = traceroute(args.host)
        ips = [l.ip for l in traceroute_output if l.ip is not None]
    else:
        ips = [
            '192.168.1.1',
            '50.53.152.1',
            '50.46.177.146',
            '50.46.176.48',
            '204.194.220.5',
            '107.191.236.64',
            '206.81.80.112',
            '202.158.194.120',
            '113.197.15.146',
            '113.197.15.12',
            '113.197.15.11',
            '138.44.161.3',
            '150.203.201.5',
            '150.203.201.33',
            '130.56.66.152'
        ]
    if True: # FIXME
        from pprint import pprint
        pprint(ips)

    # Write to map
    print('Generating map:')
    map_ = Map()
    coords_prev = None
    connect = []
    from map import Color # FIXME
    for ip in ips:
        whois_output = whois(ip)
        coords = get_most_precise_location(whois_output)
        if coords is None:
            print('-->', 'No location found. Skipping', ip)
            continue
        if coords == coords_prev:
            print('-->', 'Same location. Omitting', ip)
            continue
        map_.add_route_point(coords, color=Color.blue)
        # if coords_prev is not None:
        #     map_.add_route_segment(coords_prev, coords)
        connect.append(coords)
        coords_prev = coords
    for i in range(len(connect) - 1):
        map_.add_route_segment(connect[i], connect[i + 1])
    map_.save()
    exit(0)

    whois_output = whois(args.host)
    coords_endpoint = get_most_precise_location(whois_output)
    print(f'Endpoint location: {coords_endpoint}')

    # TODO add endpoint to map

    # return 0

def is_valid_hostname(hostname: str) -> bool:
    if bool(re.match(RE_HOSTNAME, hostname)):
        return True # TODO more granular checking
    return False
def is_valid_ip(ip: str) -> bool:
    if bool(re.match(RE_IP, ip)):
        return True # TODO check 0 <= chunk < 256
    return False

def get_global_coordinates(location: str) -> tuple:
    response = requests.get(f'http://nominatim.openstreetmap.org/search?q={location}&format=json')
    try:
        data = json.loads(response.text)
    except:
        print(response.text)
        return (0,0) # FIXME
    if len(data) == 0:
        return None
    best = data[0]
    lat = float(best['lat'])
    lon = float(best['lon'])
    return (lon, lat)

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('--only')
    args = parser.parse_args(sys.argv[1:])

    if os.path.isdir(DIR_TEMP_FILES):
        shutil.rmtree(DIR_TEMP_FILES)
    os.makedirs(DIR_TEMP_FILES)

    main(args)
