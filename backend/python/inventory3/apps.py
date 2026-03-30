from django.apps import AppConfig
from .seed import seed_categories
from .migration import migrate_products

class Inventory3Config(AppConfig):
    name = 'inventory3'
    
    def ready(self):
        seed_categories()
        migrate_products()

