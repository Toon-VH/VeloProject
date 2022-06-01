import json
from typing import List

from Bicycle import Bicycle
from BicycleStation import BicycleStation
from Colors import Colors
from Transporter import Transporter
from User import User


class Repository:
    stations: List[BicycleStation] = []
    bicycles: List[Bicycle] = []
    users: List[User] = []
    transporters: List[Transporter] = []

    @staticmethod
    def save():
        print(Colors.OKGREEN + "Saving Stations..." + Colors.ENDC)
        with open('Resources/Data/Stations.json', 'w') as outfile:
            json.dump(Repository.stations, outfile, sort_keys=True, indent=4, cls=BicycleStation.StationEncoder)

        print(Colors.OKGREEN + "Saving Bicycles..." + Colors.ENDC)
        with open('Resources/Data/Bicycles.json', 'w') as outfile:
            json.dump(Repository.bicycles, outfile, sort_keys=True, indent=4, cls=Bicycle.BicycleEncoder)

        print(Colors.OKGREEN + "Saving Users..." + Colors.ENDC)
        with open('Resources/Data/Users.json', 'w') as outfile:
            json.dump(Repository.users, outfile, sort_keys=True, indent=4, cls=User.UserEncoder)

        print(Colors.OKGREEN + "Saving Transpoters..." + Colors.ENDC)
        with open('Resources/Data/Transpoters.json', 'w') as outfile:
            json.dump(Repository.transporters, outfile, sort_keys=True, indent=4, cls=Transporter.UserEncoder)

    @staticmethod
    def load():
        print(Colors.OKGREEN + "Loading Users..." + Colors.ENDC)
        with open('Resources/Data/Users.json', 'r') as f:
            data = json.load(f, )
            for user in data:
                Repository.users.append(User(user['id'], user['name'], user['lastname'], user['age'], user['gender']))
        f.close()

        print(Colors.OKGREEN + "Loading Stations..." + Colors.ENDC)
        with open('Resources/Data/Stations.json', 'r') as f:
            data = json.load(f)
            for station in data:
                bicycleStation = BicycleStation(station['id'], station['spots'])
                for i in range(len(station["slots"])):
                    bicycle = Bicycle(station['slots'][i]['bicycleid'])
                    bicycleStation.slots.append(bicycle)
                Repository.stations.append(bicycleStation)
        f.close()
