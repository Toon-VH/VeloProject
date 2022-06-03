import logging
from random import Random
from time import sleep
from Colors import Colors
from Repository import Repository


def get_station_to_take():
    # print("station U..")
    rdm = Random()
    while True:
        station = Repository.stations[rdm.randint(0, len(Repository.stations)) - 1]
        if station.calculate_bicycles() != 0:
            # print("done")
            return station


def get_station_to_deliver():
    # print("station U..")
    rdm = Random()
    while True:
        station = Repository.stations[rdm.randint(0, len(Repository.stations)) - 1]
        if station.calculate_bicycles() != station.spots:
            # print("done")
            return station


def get_station_to_deliver_as_tranporter(amount):
    # print("station T..")
    placing = True
    rdm = Random()
    while placing:
        station = Repository.stations[rdm.randint(0, len(Repository.stations)) - 1]
        if station.calculate_bicycles() < station.spots / 2 and amount + station.calculate_bicycles() < station.spots:
            # print("done")
            return station


def get_user():
    # print("user..")
    rdm = Random()
    counter = 0
    while True:
        counter += 1
        user = Repository.users[rdm.randint(0, len(Repository.users)) - 1]
        if counter > len(Repository.users):
            # print("done")
            return None
        if not user.on_move:
            # print("done")
            return user


def get_transporter():
    # print("transporter..")
    for t in Repository.transporters:
        if not t.on_move:
            # print("done")
            return t
    return None


def get_random_time_user():
    rdm = Random()
    return rdm.randint(10, 60)


def get_random_time_transporter():
    rdm = Random()
    return rdm.randint(7, 25)


class Simulation:

    def __init__(self, speed, actions):
        self.actions = actions
        self.speed = speed
        logging.basicConfig(filename="Resources/Data/displacements.log", level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S')
        self.running = True

    def start(self):
        if self.running:
            try:
                while True:
                    self.execute()
                    sleep(60 / self.speed)
            except KeyboardInterrupt:
                pass

    def execute(self):
        print(Colors.HEADER + "<=========== Displacments ===========>")

        self.borrow_as_user()
        self.check_if_arrived()
        self.check_to_activate_transporter()
        print(Colors.WARNING + "Press CTLR + C to exit simulation" + Colors.ENDC)

    def borrow_as_user(self):
        finding_user = True
        for a in range(self.actions):
            if finding_user:
                station = get_station_to_take()
                user = get_user()
                if user is not None:
                    user.borrow(station)
                    logging.info(f"User: %s (%d) borrowed a bicycle from %s" % (user.name, user.userid, station.street))
                    print(Colors.HEADER + Colors.BOLD + "OUT " + Colors.ENDC + Colors.OKGREEN + "User: " + str(
                        user.name) + " borrowed a bicycle from " + str(
                        station.street) + Colors.ENDC)
                    user.min_to_arrive = get_random_time_user()
                else:
                    logging.warning("All registered users are on the move!")
                    print(Colors.FAIL + "All registered users are on the move!" + Colors.ENDC)
                    finding_user = False

    @classmethod
    def check_to_activate_transporter(cls):
        checking = True
        for station in Repository.stations:
            if checking:
                if station.calculate_bicycles() > station.spots * 0.8:
                    transporter = get_transporter()
                    if transporter is None:
                        logging.warning("All transporters are busy!")
                        print(Colors.FAIL + "All transporters are busy!" + Colors.ENDC)
                        checking = False
                    else:
                        amount = round(station.calculate_bicycles() * 0.3)
                        transporter.borrow(station, amount)
                        transporter.min_to_arrive = get_random_time_transporter()
                        logging.info(
                            f"Transporter: %s (%d) took %d  bicycles from %s" % (
                                transporter.name, transporter.userid, amount, station.street))
                        print(
                            Colors.HEADER + Colors.BOLD + "OUT " + Colors.ENDC + Colors.OKCYAN + "Transporter: " + str(
                                transporter.name) + " took " + str(
                                amount) + " bicycles from " + str(station.street) + Colors.ENDC)

    @classmethod
    def check_if_arrived(cls):
        for user in Repository.users:
            if user.on_move:
                if user.min_to_arrive <= 1:
                    station = get_station_to_deliver()
                    user.bring_in(station)
                    logging.info(f"User: %s (%d) Delivered a bicycle at %s" % (user.name, user.userid, station.street))
                    print(Colors.OKBLUE + Colors.BOLD + "IN " + Colors.ENDC + Colors.OKGREEN + "User: " + str(
                        user.name) + " Delivered a bicycle at " + str(
                        station.street) + Colors.ENDC)
                else:
                    user.min_to_arrive -= 1

        for transporter in Repository.transporters:
            if transporter.on_move:
                if transporter.min_to_arrive <= 1:
                    amount = len(transporter.bicycles)
                    station = get_station_to_deliver_as_tranporter(amount)
                    transporter.bring_in(station, amount)
                    logging.info(
                        f"Transporter: %s (%d) Delivered %d bicycles at %s" % (
                            transporter.name, transporter.userid, amount, station.street))
                    print(Colors.OKBLUE + Colors.BOLD + "IN " + Colors.ENDC + Colors.OKCYAN + "Transporter: " + str(
                        transporter.name) + " Delivered " + str(amount) + " bicycles at " + str(
                        station.street) + Colors.ENDC)
                else:
                    transporter.min_to_arrive -= 1
