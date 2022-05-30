from json import JSONEncoder


class User:
    def __init__(self, userid, name, lastname, age, gender):
        self.userid = userid
        self.gender = gender
        self.lastname = lastname
        self.age = age
        self.name = name
        self.on_move = False
        self.bicycle = []
        self.capacity = 1

    def __str__(self) -> str:
        return "%s %s Age: %d Gender: %s " % (self.name, self.lastname, self.age, self.gender)

    class UserEncoder(JSONEncoder):
        def default(self, obj):
            return obj.__dict__
