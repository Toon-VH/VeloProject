import random
from random import Random
from prettytable import PrettyTable
from Bicycle import Bicycle
from BicycleStation import BicycleStation
from Colors import Colors
import json
import names

from Repository import Repository
from User import User


class SimulationBuilder:

    def createsimulation(self):
        self.__generatebicyclestations()
        self.__generatebicycles()
        self.__allocatingbicycles()
        self.__generateusers()
        # print(Colors.OKBLUE + "\tGenerating Bicycle Transporters" + Colors.ENDC)

    def __generatebicyclestations(self):
        print(Colors.OKBLUE + "\tGenerating Bicycle Stations..." + Colors.ENDC)
        f = open('Resources/Data/velo.geojson')
        data = json.load(f)
        counter = 1
        for st in data['features']:
            Repository.stations.append(
                BicycleStation(counter, st['properties']['Straatnaam'], int(st['properties']['Aantal_plaatsen'])))
            counter += 1
        print(Colors.OKGREEN + "\t\t Made: " + str(len(Repository.stations)) + " stations" + Colors.ENDC)

    def __generatebicycles(self):
        bicycles = int(input(Colors.WARNING + "\tAmount of bicycles: " + Colors.ENDC))
        amount = 0
        for station in Repository.stations:
            amount += station.spots
        if amount < bicycles:
            print(Colors.FAIL + "\tThere are more bicycles than spots (bicycles: " + str(
                bicycles) + " spots: " + str(amount) + ")" + Colors.ENDC)
            self.__generatebicycles()
        else:
            print(Colors.OKBLUE + "\tGenerating Bicycles..." + Colors.ENDC)
            counter = 1
            for bicycle in range(bicycles):
                Repository.bicycles.append(Bicycle(counter))
                counter += 1
            print(Colors.OKGREEN + "\t\t Made: " + str(len(Repository.bicycles)) + " Bicycles" + Colors.ENDC)

    def __allocatingbicycles(self):
        print(Colors.OKBLUE + "\tAllocating Bicycles..." + Colors.ENDC)
        counter = 0
        stationsids = []
        for bicycle in Repository.bicycles:
            random = Random()
            placing = True
            while placing:
                rdm = random.randrange(0, len(Repository.stations))
                if len(Repository.stations[rdm].slots) < Repository.stations[rdm].spots:
                    Repository.stations[rdm].slots.append(bicycle)
                    placing = False
                    if Repository.stations[rdm].stationid not in stationsids:
                        counter += 1
                        stationsids.append(Repository.stations[rdm].stationid)

        print(Colors.OKGREEN + "\t\t Allocated: " + str(len(Repository.bicycles)) + " Bicycles over "
              + str(counter) + " Stations" + Colors.ENDC)
        # self.__print()

    def __print(self):
        t = PrettyTable(['Id', 'Bycicles'])
        for station in Repository.stations:
            t.add_row([station.stationid, str(len(station.slots)) + "/" + str(station.spots)])
        print(t)

    def __generateusers(self):
        user = int(input(Colors.WARNING + "\tAmount of users: " + Colors.ENDC))
        print(Colors.OKBLUE + "\tGenerating Users..." + Colors.ENDC)
        rdm = Random()
        males = 0
        females = 0
        for i in range(user):
            printProgressBar(i + 1, user, prefix='Progress:', suffix='Complete', length=25)
            if random.randint(0, 1) == 0:
                gender = 'female'
                females += 1
            else:
                gender = 'male'
                males += 1
            Repository.users.append(
                User(i + 1, names.get_first_name(gender=gender), names.get_last_name(), rdm.randrange(18, 75), gender))
        print(
            Colors.OKGREEN + "\t\t Made: " + str(len(Repository.users)) + " Users " + str(males) + " Males and " + str(
                females) + " Females" + Colors.ENDC)


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(Colors.OKGREEN + f'\r\t\t {prefix} |{bar}| {percent}% {suffix}' + Colors.ENDC, end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
