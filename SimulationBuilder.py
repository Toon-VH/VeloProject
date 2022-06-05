import random
from random import Random
from typing import List

from Model.Bicycle import Bicycle
from Model.BicycleStation import BicycleStation
from Colors import Colors
import json
import names

from Repository import Repository
from Model.Slot import Slot
from Model.Transporter import Transporter
from Model.User import User


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█',
                       printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(Colors.OKGREEN + f'\r\t\t {prefix} |{bar}| {percent}% {suffix}' + Colors.ENDC, end=printEnd)
    if iteration == total:
        print()


class SimulationBuilder:

    def createsimulation(self):
        print(Colors.OKBLUE + Colors.BOLD + "Building Simulation..." + Colors.ENDC)
        self.__generatebicyclestations()
        self.generate_bicycles()
        self.generate_users()
        self.generate_transporters()

    @classmethod
    def __generatebicyclestations(cls):
        print(Colors.OKBLUE + "\tGenerating Bicycle Stations..." + Colors.ENDC)
        f = open('Resources/Data/velo.geojson')
        data = json.load(f)
        counter = 1
        for st in data['features']:
            station = BicycleStation(counter, st['properties']['Straatnaam'], int(st['properties']['Aantal_plaatsen']))
            for i in range(station.spots):
                station.slots.append(Slot(i + 1))
            Repository.stations.append(station)
            counter += 1
        print(Colors.OKGREEN + "\t\t Made: " + str(len(Repository.stations)) + " stations" + Colors.ENDC)

    @classmethod
    def generate_bicycles(cls):
        bicycles: List[Bicycle] = []
        amoumt_bicycles = int(input(Colors.WARNING + "\tAmount of bicycles: " + Colors.ENDC))
        amount = 0
        for station in Repository.stations:
            amount += station.spots
        if amoumt_bicycles > amount:
            print(Colors.FAIL + "\tThere are more bicycles than spots (bicycles: " + str(
                amoumt_bicycles) + " spots: " + str(amount) + ")" + Colors.ENDC)
            cls.generate_bicycles()
        else:
            print(Colors.OKBLUE + "\tGenerating Bicycles..." + Colors.ENDC)
            counter = 1
            for bicycle in range(amoumt_bicycles):
                bicycles.append(Bicycle(counter))
                counter += 1
            print(Colors.OKGREEN + "\t\t Made: " + str(len(bicycles)) + " Bicycles" + Colors.ENDC)
            cls.allocating_bicycles(bicycles)

    @classmethod
    def allocating_bicycles(cls, bicycles):
        print(Colors.OKBLUE + "\tAllocating Bicycles..." + Colors.ENDC)
        counter = 0
        stations_ids = []
        for bicycle in bicycles:
            rdm = Random()
            placing = True
            while placing:
                rdm_station = rdm.randint(0, len(Repository.stations) - 1)

                # Check if slots are full
                station = Repository.stations[rdm_station]
                if station.calculate_bicycles() < station.spots:
                    rdm_slot = rdm.randint(0, station.spots - 1)

                    # Check if Slot is full
                    slot = station.slots[rdm_slot]
                    if slot.bicycle is None:
                        slot.bicycle = bicycle
                        placing = False

                        # Check if we already had this station for stats
                        if station.stationid not in stations_ids:
                            counter += 1
                            stations_ids.append(station.stationid)

        print(Colors.OKGREEN + "\t\t Allocated: " + str(len(bicycles)) + " Bicycles over " + str(
            counter) + " Stations" + Colors.ENDC)

    @classmethod
    def generate_users(cls):
        user = int(input(Colors.WARNING + "\tAmount of users: " + Colors.ENDC))
        print(Colors.OKBLUE + "\tGenerating Users..." + Colors.ENDC)
        rdm = Random()
        males = 0
        females = 0
        for i in range(user):
            print_progress_bar(i + 1, user, prefix='Progress:', suffix='Complete', length=25)
            if random.randint(0, 1) == 0:
                gender = 'female'
                females += 1
            else:
                gender = 'male'
                males += 1
            Repository.users.append(
                User(i + 1, names.get_first_name(gender=gender), names.get_last_name(), rdm.randint(18, 75), gender))
        print(
            Colors.OKGREEN + "\t\t Made: " + str(len(Repository.users)) + " Users " + str(males) + " Males and " + str(
                females) + " Females" + Colors.ENDC)

    @classmethod
    def generate_transporters(cls):
        transporter = int(input(Colors.WARNING + "\tAmount of transporters: " + Colors.ENDC))
        print(Colors.OKBLUE + "\tGenerating Transporters..." + Colors.ENDC)
        rdm = Random()
        males = 0
        females = 0
        for i in range(transporter):
            print_progress_bar(i + 1, transporter, prefix='Progress:', suffix='Complete', length=25)
            if random.randint(0, 1) == 0:
                gender = 'female'
                females += 1
            else:
                gender = 'male'
                males += 1
            Repository.transporters.append(
                Transporter(i + 1, names.get_first_name(gender=gender), names.get_last_name(), rdm.randint(18, 75),
                            gender))
        print(Colors.OKGREEN + "\t\t Made: " + str(len(Repository.users)) + " Transporters " + str(
            males) + " Males and " + str(
            females) + " Females" + Colors.ENDC)
