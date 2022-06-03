from random import Random

from Colors import Colors
from User import User


class Transporter(User):
    def __init__(self, userid, name, lastname, age, gender):
        super().__init__(userid, name, lastname, age, gender)
        self.capacity = 20

    def borrow(self, station, amount=1):
        rdm = Random()
        self.on_move = True
        for i in range(amount):
            taking = True
            while taking:
                slot = station.slots[rdm.randint(0, station.spots - 1)]
                if slot.bicycle is not None:
                    self.bicycles.append(slot.bicycle)
                    slot.bicycle = None
                    taking = False

    def bring_in(self, station, amount=1):
        rdm = Random()
        if amount == len(self.bicycles):
            self.on_move = False
        for i in range(amount):
            placing = True
            while placing:
                slot = station.slots[rdm.randint(0, station.spots - 1)]
                if slot.bicycle is None:
                    slot.bicycle = self.bicycles.pop()
                    placing = False

    def __str__(self) -> str:
        return super().__str__() + "Bicycles: %d/%d " % (len(self.bicycles), self.capacity)
