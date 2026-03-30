# First week assignment done using fast api (Also done using django.http in the api folder)


# from fastapi import FastAPI,HTTPException
# from shared.application.greet_usecase import Greet_Usecase
# from shared.adapter.greeting_service import GreetingService
# from shared.domain.greeting import InvalidAgeError

# app = FastAPI()

# greeting_service=GreetingService()
# greet_usecase=Greet_Usecase(greeting_service)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/greet")
# def greet(name:str,age:int):
#     try:
#         return greet_usecase.execute(name,age)
#     except (InvalidAgeError,ValueError) as e:
#         raise HTTPException(status_code=400,detail=str(e))
