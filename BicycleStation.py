from json import JSONEncoder


class BicycleStation:
    def __init__(self, stationid, street, spots):
        self.street = street
        self.stationid = stationid
        self.spots = spots
        self.slots = []

    class StationEncoder(JSONEncoder):
        def default(self, obj):
            return obj.__dict__

    def __str__(self) -> str:
        return "Street: %s spots: %d Bicycles: %d" % (self.street, self.spots, len(self.slots))
