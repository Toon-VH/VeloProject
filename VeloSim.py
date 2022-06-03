from prettytable import PrettyTable
from Colors import Colors
from Repository import Repository
from Simulation import Simulation
from SimulationBuilder import SimulationBuilder
import logging


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
    t = [t for t in Repository.transporters if t.userid == transporter_id]
    return t[0]


class VeloSim:

    def __init__(self):
        logging.basicConfig(filename="Resources/Data/displacements.log", level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S')

    @classmethod
    def start(cls):

        value = input(Colors.WARNING + "Do you want to continue with previous simulation (y/n): " + Colors.ENDC)
        if value.upper()[0] == 'Y':
            Repository.load()
            while True:
                cls.actions()
        elif value.upper()[0] == 'N':
            simulationBuilder = SimulationBuilder()
            simulationBuilder.createsimulation()
            while True:
                cls.actions()
        else:
            print(Colors.FAIL + "Wrong input" + Colors.ENDC)

    @classmethod
    def actions(cls):
        print(Colors.OKCYAN + Colors.BOLD + "<============ Actions ============>" + Colors.ENDC)
        print(Colors.OKCYAN + "Borrow Bicycle as user (1) " + Colors.ENDC)
        print(Colors.OKCYAN + "Bring in Bicycle as user (2) " + Colors.ENDC)
        print(Colors.OKCYAN + "Borrow Bicycles as transporter (3) " + Colors.ENDC)
        print(Colors.OKCYAN + "Bring in Bicycles as transporter (4) " + Colors.ENDC)
        print(Colors.OKCYAN + "Run Simulation (5) " + Colors.ENDC)
        print(Colors.OKCYAN + "Generate HTML (6) " + Colors.ENDC)
        print(Colors.OKCYAN + "Exit (7) " + Colors.ENDC)
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
                cls.start_simulation()
            case "6":
                pass
            case "7":
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
        user.borrow(station)
        logging.info(f"User: %s (%d) borrowed a bicycle from %s" % (user.name, user.userid, station.street))
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
                if station.calculate_bicycles() == station.spots:
                    print(Colors.FAIL + "This Station is Full" + Colors.ENDC)
                    cls.actions()
                else:
                    user.bring_in(station)
                    logging.info(f"User: %s (%d) Delivered a bicycle at %s" % (user.name, user.userid, station.street))
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
                transporter.borrow(station, amount)
                logging.info(f"Transporter: %s (%d) took %d  bicycles from %s" % (
                    transporter.name, transporter.userid, amount, station.street))
                print(Colors.OKGREEN + str(transporter.name) + " Took his bicycles!" + Colors.ENDC)

    @classmethod
    def bring_in_as_transporter(cls):
        print(Colors.OKBLUE + "Transporters with bicycles")
        t = PrettyTable(['Id', 'Transporter', 'Bicycles'])
        count = 0
        for transporter in Repository.transporters:
            if transporter.on_move:
                t.add_row([transporter.userid, str(transporter.name) + " " + str(transporter.lastname),
                           str(len(transporter.bicycles))])
                count += 1
        print(t)
        if count <= 0:
            print(Colors.FAIL + "There are no active transporters!" + Colors.ENDC)
        else:

            # Transporter
            transporter = get_transporter()
            if len(transporter.bicycles) == 0:
                print(Colors.FAIL + "The transporter has no bicycles! pick one from the table!" + Colors.ENDC)
                cls.actions()
            else:
                print(Colors.OKBLUE + "\t" + str(transporter) + Colors.ENDC)

                station = get_station()
                if station.calculate_bicycles() == station.spots:
                    print(Colors.FAIL + "The station is Full!" + Colors.ENDC)
                    cls.actions()
                else:
                    print(Colors.OKBLUE + "\t" + str(station) + Colors.ENDC)
                    if station.spots - station.calculate_bicycles() < len(transporter.bicycles):
                        max_bicycles = station.spots - station.calculate_bicycles()
                    else:
                        max_bicycles = len(transporter.bicycles)
                    print(Colors.WARNING + "How many bicycles do you want to leave?" + Colors.ENDC)
                amount = int(input(Colors.WARNING + "Option between 1 and " + str(max_bicycles) + ": " + Colors.ENDC))
                if amount < 1 or amount > max_bicycles:
                    print(Colors.FAIL + "Wrong Input" + Colors.ENDC)
                else:
                    transporter.bring_in(station, amount)
                    logging.info(f"Transporter: %s (%d) Delivered %d bicycles at %s" % (
                        transporter.name, transporter.userid, amount, station.street))
                    print(Colors.OKGREEN + str(transporter.name) + " placed his bicycles!" + Colors.ENDC)

    @classmethod
    def start_simulation(cls):
        print(Colors.WARNING + "please enter the speed factor Example(4 = 4x real time) :" + Colors.ENDC)
        speed = int(input(Colors.WARNING + "Option between 1 and 1000: " + Colors.ENDC))
        if speed < 1 or speed > 1000:
            print(Colors.FAIL + "Wrong Input" + Colors.ENDC)
            cls.start_simulation()
        print(Colors.WARNING + "please enter the amount of active users per minute:" + Colors.ENDC)
        actions = int(input(Colors.WARNING + "Option between 10 and 500: " + Colors.ENDC))
        if actions < 1 or actions > 500:
            print(Colors.FAIL + "Wrong Input" + Colors.ENDC)
            cls.start_simulation()
        simulation = Simulation(speed, actions)
        simulation.start()

    @classmethod
    def exit_sim(cls):
        Repository.save()
        print(Colors.HEADER + "Closing.." + Colors.ENDC)
        exit()
