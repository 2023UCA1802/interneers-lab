from django.apps import AppConfig
from .db.mongo import init_db
from dotenv import load_dotenv
import os

class Inventory2Config(AppConfig):
    name = 'inventory2'
    def ready(self):
        load_dotenv()
        init_db()
        
    

