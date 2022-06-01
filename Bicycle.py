from json import JSONEncoder


class Bicycle:
    def __init__(self, bicycleid):
        self.bicycleid = bicycleid

    def __str__(self) -> str:
        return "Id is %s " % self.bicycleid

    class BicycleEncoder(JSONEncoder):
        def default(self, obj):
            return obj.__dict__
