#!/usr/bin/python3

# Tested devices
# Onn 5_1_2 Atmos Soundbar - 0.0.1186.0x247b2ea 

import argparse
import os

parser = argparse.ArgumentParser(description='Onn Soundbar API Toolkit')

parser.add_argument('-l', action='store_true', default=False, dest='list_actions', help='List the possible commands')
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
    print("\navailable commands:\n")
    print("                          DEVICE")
    print("=============================================================")
    print("getName:           Get the device name")
    print("setName:           Change the device name")
    print("getVersion:        Get the device version")
    print("\n                          AIRPLAY")
    print("=============================================================")
    print("getAirName:        Get the airplay name")
    print("setAirName:        Change the airplay name")
    print("getAirPass:        Get the airplay password (PROBABLY WONT WORK)")
    print("setAIrPass:        Set the airplay password (DANGEROUS AND UNTESTED)")
    print("\n                          SPOTIFY")
    print("=============================================================")
    print("getSpotifyUser:    Get the spotify username on the device")
    print("setSpotifyUser:    Change the Spotify username on the device")

if t is None and not arguments.list_actions:
    parser.print_help()


def file():
    with open('output.txt', 'r') as file:
        for line in file:
            print(line)
    file.close()
    os.system('rm ./output.txt')


def getName():
    os.system('curl -v "http://'+ t + '/api/getData?path=settings%3A%2FdeviceName&roles=value" -H "Referer: http://' + t + '/settings.fcgi"> output.txt')
    file()


def getAirName():
    os.system('curl -v "http://' + t + '/api/getData?path=settings%3A%2Fairplay%2FdeviceName&roles=value" -H "Referer: http://' + t + '/settings.fcgi" > output.txt')
    file()


def getSpotifyUser():
    os.system('curl -v "http://' + t + '/api/getData?path=settings%3A%2Fspotify%2Fusername&roles=value" -H "Referer: http://' + t + '/settings.fcgi" > output.txt')
    file()


def postDataFile(data):
    with open('data.json', 'w') as file:
        file.write(data)
    file.close()


def getVersion():
    os.system('curl -v "http://' + t + '/api/getData?path=settings%3A%2Fversion&roles=value" -H "Referer: http://' + t + '/settings.fcgi"> output.txt')
    file()


if a is None and t is not None:
    print("ERROR:\nPlease provide an action!")
    exit()
else:
    if a == 'getName':
        getName()
    elif a == 'setName':
        if v is not None:
            postData = '{"path":"settings:/deviceName","role":"value","value":{"type":"string_","string_":"' + v + '"}}'
            postDataFile(postData)
            print("POST data set as :  " + postData)
            print("Attempting to change name")
            os.system('curl -v "http://'+ t + '/api/setData" -X POST -H "Referer: http://' + t + '/settings.fcgi"  -H "Content-Type: application/json" -d "@data.json"')
            getName()  
            os.system('rm data.json')  
        else:
            print("ERROR:\nPlease provide a value for the " + a + "action!")
    elif a == "getVersion":
        getVersion()             
    elif a == 'getAirName':
        getAirName()
    elif a == 'setAirName':
        if v is not None:
            postData = '{"path":"settings:/airplay/deviceName","role":"value","value":{"type":"string_","string_":"' + v + '"}}'
            postDataFile(postData)
            print("POST data set as :  " + postData)
            print("Attempting to change name")
            os.system('curl -v "http://'+ t + '/api/setData" -X POST -H "Referer: http://' + t + '/settings.fcgi"  -H "Content-Type: application/json" -d "@data.json"')
            getAirName()  
            os.system('rm data.json')  
        else:
            print("ERROR:\nPlease provide a value for the " + a + "action!")
    elif a == 'getAirPass':
        os.system('curl -v "http://' + t + '/api/getData?path=settings%3A%2Fairplay%2Fpassword&roles=value" -H "Referer: http://' + t + '/settings.fcgi"> output.txt')
        file()
    elif a == 'setAirPass':
        if v is not None:
            postData = '{"path":"airplay:setPassword","role":"activate","activate":{"type":"string_","string_":"' + v + '"}}'
            postDataFile(postData)
            print("POST data set as :  " + postData)
            print("Attempting to change name")
            os.system('curl -v "http://'+ t + '/api/setData" -X POST -H "Referer: http://' + t + '/settings.fcgi"  -H "Content-Type: application/json" -d "@data.json"')
            os.system('rm data.json')  
        else:
            print("ERROR:\nPlease provide a value for the " + a + "action!")         
    elif a == 'getSpotifyUser':
        getSpotifyUser()
    elif a == 'setSpotifyUser':
        if v is not None:
            postData = '{"path":"settings:/spotify/username","role":"value","value":{"type":"string_","string_":"' + v + '"}}'
            postDataFile(postData)
            print("POST data set as :  " + postData)
            print("Attempting to change name")
            os.system('curl -v "http://'+ t + '/api/setData" -X POST -H "Referer: http://' + t + '/settings.fcgi"  -H "Content-Type: application/json" -d "@data.json"')
            getSpotifyUser()
            os.system('rm data.json')  
        else:
            print("ERROR:\nPlease provide a value for the " + a + "action!")            
