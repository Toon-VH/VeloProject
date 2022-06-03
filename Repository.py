import json
from typing import List

from Bicycle import Bicycle
from BicycleStation import BicycleStation
from Colors import Colors
from Slot import Slot
from Transporter import Transporter
from User import User


class Repository:
    stations: List[BicycleStation] = []
    users: List[User] = []
    transporters: List[Transporter] = []

    @staticmethod
    def save():
        print(Colors.OKGREEN + "Saving Stations..." + Colors.ENDC)
        with open('Resources/Data/Stations.json', 'w') as outfile:
            json.dump(Repository.stations, outfile, sort_keys=True, indent=4, cls=BicycleStation.StationEncoder)

        print(Colors.OKGREEN + "Saving Users..." + Colors.ENDC)
        with open('Resources/Data/Users.json', 'w') as outfile:
            json.dump(Repository.users, outfile, sort_keys=True, indent=4, cls=User.UserEncoder)

        print(Colors.OKGREEN + "Saving Transpoters..." + Colors.ENDC)
        with open('Resources/Data/Transporters.json', 'w') as outfile:
            json.dump(Repository.transporters, outfile, sort_keys=True, indent=4, cls=Transporter.UserEncoder)

    @staticmethod
    def load():
        # Stations
        print(Colors.OKBLUE + "Loading Data..." + Colors.ENDC)
        print(Colors.OKGREEN + "Loading Stations..." + Colors.ENDC)
        with open('Resources/Data/Stations.json', 'r') as f:
            data = json.load(f)
            for station in data:
                bicycle_station = BicycleStation(station['stationid'], station['street'], station['spots'])
                for i in range(len(station["slots"])):
                    slot: Slot = Slot(station["slots"][i]['slotid'])
                    if station["slots"][i]["bicycle"] is not None:
                        bicycle = Bicycle(station["slots"][i]["bicycle"]['bicycleid'])
                        slot.bicycle = bicycle
                    bicycle_station.slots.append(slot)
                Repository.stations.append(bicycle_station)
        f.close()

        # Users
        print(Colors.OKGREEN + "Loading Users..." + Colors.ENDC)
        with open('Resources/Data/Users.json', 'r') as f:
            data = json.load(f, )
            for u in data:
                user = User(u['userid'], u['name'], u['lastname'], u['age'], u['gender'])
                user.on_move = u['on_move']
                user.min_to_arrive = u['min_to_arrive']
                for b in u['bicycles']:
                    user.bicycles.append(Bicycle(b['bicycleid']))
                Repository.users.append(user)
        f.close()

        # Transporters
        print(Colors.OKGREEN + "Loading Transporters..." + Colors.ENDC)
        with open('Resources/Data/Transporters.json', 'r') as f:
            data = json.load(f, )
            for t in data:
                transporter = Transporter(t['userid'], t['name'], t['lastname'], t['age'], t['gender'])
                transporter.on_move = t['on_move']
                transporter.min_to_arrive = t['min_to_arrive']
                for b in t['bicycles']:
                    transporter.bicycles.append(Bicycle(b['bicycleid']))
                Repository.transporters.append(transporter)
        f.close()
