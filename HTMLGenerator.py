from jinja2 import Environment, FileSystemLoader
from tabulate import tabulate
from Repository import Repository


def station_table():
    table = [["Id", "Street", "Spots", "Available Bicycles"]]
    for station in Repository.stations:
        table.append(
            [
                station.stationid,
                station.street,
                station.spots,
                station.calculate_bicycles()
            ]
        )
    return tabulate(table, headers="firstrow", tablefmt="html")


def user_table():
    table = [["Id", "Firstname", "LastName", "Moving", "Arriving In (min)"]]
    for user in Repository.users:
        table.append(
            [
                user.userid,
                user.name,
                user.lastname,
                user.on_move,
                user.min_to_arrive
            ]
        )

    return tabulate(table, headers="firstrow", tablefmt="html")


def transporter_table():
    table = [["Id", "Firstname", "LastName", "Amount Bicycles", "Moving", "Arriving In (min)"]]
    for transporter in Repository.transporters:
        table.append(
            [
                transporter.userid,
                transporter.name,
                transporter.lastname,
                len(transporter.bicycles),
                transporter.on_move,
                transporter.min_to_arrive
            ]
        )

    return tabulate(table, headers="firstrow", tablefmt="html")


class HTMLGenerator:

    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('Web'))

    def create_html(self):
        self.create_stations()
        self.create_users()
        self.create_transporters()

    def create_stations(self):
        template = self.env.get_template("table_layout.html")
        with open("Web/index.html", "w") as output_file:
            output_file.write(template.render(tabel=station_table()))

    def create_users(self):
        template = self.env.get_template("table_layout.html")
        with open("Web/users.html", "w") as output_file:
            output_file.write(template.render(tabel=user_table()))

    def create_transporters(self):
        template = self.env.get_template("table_layout.html")
        with open("Web/transporters.html", "w") as output_file:
            output_file.write(template.render(tabel=transporter_table()))
