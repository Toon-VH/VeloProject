class Bicycle:
    def __init__(self, bicycleid):
        self.bicycleid = bicycleid

    def __str__(self) -> str:
        return "Id is %s " % self.bicycleid
