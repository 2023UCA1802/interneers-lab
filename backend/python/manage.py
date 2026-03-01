#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from fastapi import FastAPI
from shared.application.greet_usecase import Greet_Usecase
from shared.adapter.greeting_service import GreetingService

app = FastAPI()

greeting_service=GreetingService()
greet_usecase=Greet_Usecase(greeting_service)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/greet")
def greet(name:str,age:int):
    return greet_usecase.execute(name,age)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
