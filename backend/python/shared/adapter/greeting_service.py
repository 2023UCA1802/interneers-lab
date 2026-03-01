from shared.port.greeting_port import Greeting_Port
from shared.domain.greeting import Greeting

class GreetingService(Greeting_Port):

    def generate_greeting(self, name:str, age:int)->str:
        greeting=Greeting(name,age)
        return greeting.create_message()