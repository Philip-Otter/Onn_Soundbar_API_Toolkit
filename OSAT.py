#!/usr/bin/python3

# Tested devices
# Onn 5_1_2 Atmos Soundbar - 0.0.1186.0x247b2ea 

import argparse
import os
import urllib.parse

parser = argparse.ArgumentParser(description='Onn Soundbar API Toolkit')

parser.add_argument('-l', action='store_true', default=False, dest='list_actions', help='List the possible commands')
parser.add_argument('-v', action='store_true', default=False, dest='verbose', help='Provide verbose output')
command = parser.add_argument_group('command')
command.add_argument('-a', action='store', dest='action', help='The toolkit action')
command.add_argument('--val', action='store', dest='value', help="The toolkit action's value")
target = parser.add_argument_group('target')
target.add_argument('-t', action='store', dest='target', help='The target Onn Atmos Soundbar')

arguments = parser.parse_args()

t = arguments.target
a = arguments.action
v = arguments.value

if arguments.list_actions:
    spacer = "================================================================================"
    print("\navailable commands:\n")
    print("                              DEVICE")
    print(spacer)
    print("getName:           Get the device name")
    print("setName:           Change the device name")
    print("getVersion:        Get the device version")
    print("\n                              AIRPLAY")
    print(spacer)
    print("getAirName:        Get the airplay name")
    print("setAirName:        Change the airplay name")
    print("getAirPass:        Get the airplay password (PROBABLY WONT WORK)")
    print("setAIrPass:        Set the airplay password (DANGEROUS AND UNTESTED)")
    print("\n                              SPOTIFY")
    print(spacer)
    print("getSpotifyUser:    Get the spotify username on the device")
    print("setSpotifyUser:    Change the Spotify username on the device")
    print("\n                              TESTING")
    print(spacer)
    print("injectGet:          Send a custom getData request to trial command injection")
    

if t is None and not arguments.list_actions:
    parser.print_help()

if arguments.verbose:
    vv = "-v"
    print("\nVERBOSE OUTPUT ENABLED")
else:
    vv = ""


# GET and POST Functions


def post(action, actionType):
    if action == 'setData':
        url_add = '/api/setData'

    if actionType == 'nameChange':
        print("\nATTEMPTING TO CHANGE NAME\n")
    elif actionType == 'passChange':
        print("\nATTEMPTING TO CHANGE PASSWORD\n")
    
    print("Making curl request now")
    os.system('curl ' + vv + ' "http://' + t + url_add +'" -X POST -H "Referer: http://' + t + '/settings.fcgi"  -H "Content-Type: application/json" -d "@data.json"')
    os.system('rm data.json')


def get(action):
    if action == 'name':
        url_add = '/api/getData?path=settings%3A%2FdeviceName&roles=value'
    elif action == 'version':
        url_add = '/api/getData?path=settings%3A%2Fversion&roles=value'
    elif action == 'airName':
        url_add = '/api/getData?path=settings%3A%2Fairplay%2FdeviceName&roles=value'
    elif action == 'airPass':
        url_add = '/api/getData?path=settings%3A%2Fairplay%2Fpassword&roles=value'
    elif action == 'spotifyUser':
        url_add = '/api/getData?path=settings%3A%2Fspotify%2Fusername&roles=value'
    
    os.system('curl ' + vv + ' "http://'+ t + url_add +'" -H "Referer: http://' + t + '/settings.fcgi"> output.txt')
    file()



# File Manipulation Functions


def file():
    with open('output.txt', 'r') as file:
        for line in file:
            print(line)
    file.close()
    os.system('rm ./output.txt')


def postDataFile(data):
    with open('data.json', 'w') as file:
        file.write(data)
    file.close()
    print("\nPOST DATA SET AS:  " + data)


if a is None and t is not None:
    print("ERROR:\nPlease provide an action!")
    exit()
else:
    if a == 'getName':
        get('name')
    elif a == 'setName':
        if v is not None:
            postData = '{"path":"settings:/deviceName","role":"value","value":{"type":"string_","string_":"' + v + '"}}'
            postDataFile(postData)
            post('setData', 'nameChange')
            get('name')    
        else:
            print("ERROR:\nPlease provide a value for the " + a + "action!")
    elif a == "getVersion":
        get('version')             
    elif a == 'getAirName':
        get('airName')
    elif a == 'setAirName':
        if v is not None:
            postData = '{"path":"settings:/airplay/deviceName","role":"value","value":{"type":"string_","string_":"' + v + '"}}'
            postDataFile(postData)
            post('setData', 'nameChange')
            get('airName')   
        else:
            print("ERROR:\nPlease provide a value for the " + a + "action!")
    elif a == 'getAirPass':
        get('airPass')
    elif a == 'setAirPass':
        if v is not None:
            postData = '{"path":"airplay:setPassword","role":"activate","activate":{"type":"string_","string_":"' + v + '"}}'
            postDataFile(postData)
            post('setData', 'passChange')
            get('airPass')
        else:
            print("ERROR:\nPlease provide a value for the " + a + "action!")         
    elif a == 'getSpotifyUser':
        get('spotifyUser')
    elif a == 'setSpotifyUser':
        if v is not None:
            postData = '{"path":"settings:/spotify/username","role":"value","value":{"type":"string_","string_":"' + v + '"}}'
            postDataFile(postData)
            post('setData', 'nameChange')
            get('spotifyUser') 
        else:
            print("ERROR:\nPlease provide a value for the " + a + "action!")
    elif a == 'injectGet':
        print("\nInjected value:  " + urllib.parse.unquote(v) + "\n" )
        os.system('curl -v "http://' + t + '/api/getData?path=settings%3A%2F' + v + '&roles=value" -H "Referer: http://' + t + '/settings.fcgi"> output.txt')
        file()
