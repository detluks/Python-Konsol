

def login():
    while True:
        user = input("Username: ")
        if user == "ham":
            return user


class User:
    def __init__(self, name):
        self.name = name


user = User(login())