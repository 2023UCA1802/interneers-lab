from shared.port.greeting_port import Greeting_Port

class Greet_Usecase:

    def __init__(self,greeting_port:Greeting_Port):
        self.greeting_port=greeting_port
    
    def execute(self,name:str,age:int)->dict:
        message=self.greeting_port.generate_greeting(name,age)
        return {"message":message}
    