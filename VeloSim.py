from random import Random

from prettytable import PrettyTable

from BicycleStation import BicycleStation
from Colors import Colors
from Repository import Repository
from SimulationBuilder import SimulationBuilder


def get_station():
    station_id = int(input(Colors.WARNING + "Station ID between 0 and " + str(
        len(Repository.stations)) + ": " + Colors.ENDC))
    return [s for s in Repository.stations if s.stationid == station_id][0]


def get_user():
    user_id = int(input(
        Colors.WARNING + "User ID between 0 and " + str(len(Repository.users)) + ": " + Colors.ENDC))
    return [u for u in Repository.users if u.userid == user_id][0]


def get_transporter():
    transporter_id = int(input(
        Colors.WARNING + "Transporter ID between 0 and " + str(len(Repository.transporters)) + ": " + Colors.ENDC))
    return [t for t in Repository.transporters if t.userid == transporter_id][0]


class VeloSim:
    @classmethod
    def start(cls):
        AsciArt = r"""
              ______ _                 _        _____ _                 _       _             
              | ___ (_)               | |      /  ___(_)               | |     | |            
              | |_/ /_  ___ _   _  ___| | ___  \ `--. _ _ __ ___  _   _| | __ _| |_ ___  _ __ 
              | ___ \ |/ __| | | |/ __| |/ _ \  `--. \ | '_ ` _ \| | | | |/ _` | __/ _ \| '__|
              | |_/ / | (__| |_| | (__| |  __/ /\__/ / | | | | | | |_| | | (_| | || (_) | |   
              \____/|_|\___|\__, |\___|_|\___| \____/|_|_| |_| |_|\__,_|_|\__,_|\__\___/|_|   
                             __/ |                                                            
                            |___/     
              """
        print(Colors.HEADER + AsciArt + Colors.ENDC)
        value = input(Colors.WARNING + "Do you want to continue with previous simulation (y/n): " + Colors.ENDC)
        if value.upper()[0] == 'Y':
            print(Colors.OKBLUE + "Loading Data..." + Colors.ENDC)
            Repository.load()
            cls.actions()
        if value.upper()[0] == 'N':
            cls.build()
            while True:
                cls.actions()
        else:
            print(Colors.FAIL + "Wrong input" + Colors.ENDC)

    @classmethod
    def build(cls):

        print(Colors.OKBLUE + Colors.BOLD + "Building Simulation..." + Colors.ENDC)
        simulationBuilder = SimulationBuilder()
        simulationBuilder.createsimulation()

    @classmethod
    def actions(cls):
        print(Colors.OKCYAN + Colors.BOLD + "<============ Actions ============>" + Colors.ENDC)
        print(Colors.OKCYAN + "Borrow Bicycle as user (1) " + Colors.ENDC)
        print(Colors.OKCYAN + "Bring in Bicycle as user (2) " + Colors.ENDC)
        print(Colors.OKCYAN + "Borrow Bicycles as transporter (3) " + Colors.ENDC)
        print(Colors.OKCYAN + "Bring in Bicycles as transporter (4) " + Colors.ENDC)
        print(Colors.OKCYAN + "Generate HTML (5) " + Colors.ENDC)
        print(Colors.OKCYAN + "Exit (6) " + Colors.ENDC)
        print(Colors.OKCYAN + Colors.BOLD + "<=================================>" + Colors.ENDC)
        option = input(Colors.WARNING + "Action: " + Colors.ENDC)

        match option:
            case "1":
                cls.borrow_as_user()
            case "2":
                cls.bring_in_as_user()
            case "3":
                cls.borrow_as_transporter()
            case "4":
                cls.bring_in_as_transporter()
            case "5":
                pass
            case "6":
                cls.exit_sim()
            case _:
                print(Colors.FAIL + "Wrong input" + Colors.ENDC)

    @classmethod
    def borrow_as_user(cls):

        # User
        user = get_user()
        if user.on_move:
            print(Colors.FAIL + "User already has a bicycle" + Colors.ENDC)
            cls.actions()
        else:
            print(Colors.OKBLUE + "\t" + str(user) + Colors.ENDC)

        # Station
        station = get_station()
        if station.calculate_bicycles() == 0:
            print(Colors.FAIL + "There are no bicycles in this station" + Colors.ENDC)
            cls.actions()
        else:
            print(Colors.OKBLUE + "\t" + str(station) + Colors.ENDC)

        user.on_move = True
        placing = True
        rdm = Random()
        while placing:
            rdm_slot = rdm.randint(0, station.spots - 1)
            slot = station.slots[rdm_slot]
            if slot.bicycle is not None:
                user.bicycles.append(slot.bicycle)
                slot.bicycle = None
                placing = False
        print(Colors.OKGREEN + str(user.name) + " is good to go!" + Colors.ENDC)

    @classmethod
    def bring_in_as_user(cls):
        print(Colors.OKBLUE + "Users with bicycle")
        t = PrettyTable(['Id', 'User'])
        count = 0
        for user in Repository.users:
            if user.on_move:
                t.add_row([user.userid, str(user.name) + " " + str(user.lastname)])
                count += 1
        print(t)
        if count <= 0:
            print(Colors.FAIL + "There are no active users!" + Colors.ENDC)
        else:
            user = get_user()
            if not user.on_move:
                print(Colors.FAIL + "This user does not have a bicycle, pick an id from the table!" + Colors.ENDC)
            else:
                station = get_station()
                placing = True
                while placing:
                    rdm = Random()
                    slot = station.slots[rdm.randint(0, station.spots - 1)]
                    if slot.bicycle is None:
                        slot.bicycle = user.bicycles.pop()
                        user.on_move = False
                        placing = False
            print(Colors.OKGREEN + str(user.name) + " Delivered his bicycle!" + Colors.ENDC)

    @classmethod
    def borrow_as_transporter(cls):

        # Transporter
        transporter = get_transporter()
        if len(transporter.bicycles) == transporter.capacity:
            print(Colors.FAIL + "The transporter is Full!" + Colors.ENDC)
            cls.actions()
        else:
            print(Colors.OKBLUE + "\t" + str(transporter) + Colors.ENDC)
            # Station
            station = get_station()
            if station.calculate_bicycles() == 0:
                print(Colors.FAIL + "The station is Empty!" + Colors.ENDC)
                cls.actions()
            else:
                print(Colors.OKBLUE + "\t" + str(station) + Colors.ENDC)
                if station.calculate_bicycles() < transporter.capacity - len(
                        transporter.bicycles):
                    max_bicycles = station.calculate_bicycles()
                else:
                    max_bicycles = transporter.capacity - len(
                        transporter.bicycles)
                print(Colors.WARNING + "How many bicycles do you want to take?" + Colors.ENDC)
            amount = int(input(Colors.WARNING + "Option between 1 and " + str(max_bicycles) + ": " + Colors.ENDC))
            if amount < 1 or amount > max_bicycles:
                print(Colors.FAIL + "Wrong Input" + Colors.ENDC)
            else:
                rdm = Random()
                for i in range(amount):
                    taking = True
                    while taking:
                        slot = station.slots[rdm.randint(0, station.spots - 1)]
                        if slot.bicycle is not None:
                            transporter.bicycles.append(slot.bicycle)
                            slot.bicycle = None
                            taking = False
                print(Colors.OKGREEN + str(transporter.name) + " Took his bicycles!" + Colors.ENDC)

    @classmethod
    def bring_in_as_transporter(cls):
        pass

    @classmethod
    def exit_sim(cls):
        Repository.save()
        print(Colors.HEADER + "Closing.." + Colors.ENDC)
        exit()
