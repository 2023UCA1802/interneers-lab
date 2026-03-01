class Greeting:
    def __init__(self,name:str,age:int):
        self.name=name
        self.age=age
    def create_message(self)->str:
        return f"Hello {self.name}, you are {self.age} years old."