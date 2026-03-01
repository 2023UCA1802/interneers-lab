from abc import ABC, abstractmethod

class Greeting_Port(ABC):
    @abstractmethod
    def generate_greeting(self,name:str,age:int) -> str:
        pass 