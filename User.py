from json import JSONEncoder
from random import Random
from typing import List

from Bicycle import Bicycle


class User:
    def __init__(self, userid, name, lastname, age, gender):
        self.userid = userid
        self.gender = gender
        self.lastname = lastname
        self.age = age
        self.name = name
        self.on_move = False
        self.bicycles: List[Bicycle] = []
        self.capacity = 1
        self.min_to_arrive = 0

    def __str__(self) -> str:
        return "%s %s Age: %d Gender: %s " % (self.name, self.lastname, self.age, self.gender)

    def borrow(self, station, amount=1):
        self.on_move = True
        placing = True
        rdm = Random()
        while placing:
            rdm_slot = rdm.randint(0, station.spots - 1)
            slot = station.slots[rdm_slot]
            if slot.bicycle is not None:
                self.bicycles.append(slot.bicycle)
                slot.bicycle = None
                placing = False

    def bring_in(self, station, amount=1):
        placing = True
        while placing:
            rdm = Random()
            slot = station.slots[rdm.randint(0, station.spots - 1)]
            if slot.bicycle is None:
                slot.bicycle = self.bicycles.pop()
                self.on_move = False
                placing = False

    class UserEncoder(JSONEncoder):
        def default(self, obj):
            return obj.__dict__
