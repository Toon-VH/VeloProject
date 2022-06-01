from User import User


class Transporter(User):
    def __init__(self, userid, name, lastname, age, gender):
        super().__init__(userid, name, lastname, age, gender)
        self.capacity = 20

    def __str__(self) -> str:
        return super().__str__() + "Bicycles: %d/%d " % (len(self.bicycles), self.capacity)
