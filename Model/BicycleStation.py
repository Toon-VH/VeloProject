from json import JSONEncoder
from typing import List

from Model.Slot import Slot


class BicycleStation:

    def __init__(self, stationid, street, spots):
        self.street = street
        self.stationid = stationid
        self.spots = spots
        self.slots: List[Slot] = []

    def calculate_bicycles(self):
        count = 0
        for slot in self.slots:
            if slot.bicycle is not None:
                count += 1
        return count

    class StationEncoder(JSONEncoder):
        def default(self, obj):
            return obj.__dict__

    def __str__(self) -> str:
        return "Street: %s spots: %d Bicycles: %d" % (self.street, self.spots, self.calculate_bicycles())
