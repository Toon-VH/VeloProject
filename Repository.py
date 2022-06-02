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
            for u in data:
                user = User(u['id'], u['name'], u['lastname'], u['age'], u['gender'])
                user.on_move = u['on_move']
                user.bicycles = u['bicycles']
                Repository.users.append(user)
        f.close()

        print(Colors.OKGREEN + "Loading Transporters..." + Colors.ENDC)
        with open('Resources/Data/Trasporter.json', 'r') as f:
            data = json.load(f, )
            for u in data:
                Repository.transporters.append(Transporter(u['id'], u['name'], u['lastname'], u['age'], u['gender']))
        f.close()

        print(Colors.OKGREEN + "Loading Stations..." + Colors.ENDC)
        with open('Resources/Data/Stations.json', 'r') as f:
            data = json.load(f)
            for station in data:
                bicycle_station = BicycleStation(station['id'], station['spots'])
                for i in range(len(station["slots"])):
                    bicycle = Bicycle(station['slots'][i]['bicycleid'])
                    bicycle_station.slots.append(bicycle)
                Repository.stations.append(bicycle_station)
        f.close()
