from User import User


class Transporter(User):
    def __init__(self, userid, name, lastname, age, gender):
        super().__init__(userid, name, lastname, age, gender)
        self.capacity = 20
