from prettytable import PrettyTable

from BicycleStation import BicycleStation
from Colors import Colors
from Repository import Repository
from SimulationBuilder import SimulationBuilder


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
        print(Colors.OKCYAN + "Borrow Bicycle as transporter (3) " + Colors.ENDC)
        print(Colors.OKCYAN + "Bring in Bicycle as transporter (4) " + Colors.ENDC)
        print(Colors.OKCYAN + "Generate HTML (5) " + Colors.ENDC)
        print(Colors.OKCYAN + "Exit (6) " + Colors.ENDC)
        option = input(Colors.WARNING + "Action: " + Colors.ENDC)
        if option == '1':
            cls.borrow_as_user()
        elif option == "2":
            cls.bring_in_as_user()
        elif option == "3":
            cls.borrow_as_transporter()
        elif option == "4":
            cls.bring_in_as_transporter()
        elif option == "5":
            pass
        elif option == "6":
            cls.exit_sim()
        else:
            print(Colors.FAIL + "Wrong input" + Colors.ENDC)

    @classmethod
    def borrow_as_user(cls):

        # User
        user_id = int(input(
            Colors.WARNING + "User ID between 0 and " + str(len(Repository.users)) + ": " + Colors.ENDC))
        user = [u for u in Repository.users if u.userid == user_id][0]
        if user.on_move:
            print(Colors.FAIL + "User already has a bicycle" + Colors.ENDC)
            cls.actions()
        else:
            print("\t" + str(user))

        # Station
        station_id = int(input(Colors.WARNING + "Station ID between 0 and " + str(
            len(Repository.stations)) + ": " + Colors.ENDC))
        station = [s for s in Repository.stations if s.stationid == station_id][0]
        if len(station.slots) == 0:
            print(Colors.FAIL + "There are no bicycles in this station" + Colors.ENDC)
            cls.actions()
        else:
            print("\t" + str(station))

        user.on_move = True
        user.bicycle = station.slots.pop()
        print(Colors.OKGREEN + str(user.name) + " is good to go!" + Colors.ENDC)

    @classmethod
    def bring_in_as_user(cls):
        print(Colors.OKBLUE + "Users with bicycle")
        t = PrettyTable(['Id', 'User'])
        for user in Repository.users:
            if user.on_move:
                t.add_row([user.userid, str(user.name) + " " + str(user.lastname)])
        print(t)
        user_id = int(input(Colors.WARNING + 'Select a user Id from the table above: ' + Colors.ENDC))


    @classmethod
    def borrow_as_transporter(cls):
        pass

    @classmethod
    def bring_in_as_transporter(cls):
        pass

    @classmethod
    def exit_sim(cls):
        Repository.save()
        print(Colors.HEADER + "Closing.." + Colors.ENDC)
        exit()
