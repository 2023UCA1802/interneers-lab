class InvalidAgeError(Exception):
    pass

class Greeting:
    def __init__(self,name:str,age:int):
        if not name or age is None:
            raise ValueError("Both Name and age are necessary")
        if age<0:
            raise InvalidAgeError("Age cannot be negative")
        self.name=name
        self.age=age
    def create_message(self)->str:
        return f"Hello {self.name}, you are {self.age} years old."