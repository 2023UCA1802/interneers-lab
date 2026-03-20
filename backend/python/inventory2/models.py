from django.db import models
from mongoengine import Document,StringField,FloatField,IntField,DateTimeField
import datetime

class Product(Document):
    name = StringField(required=True, max_length=255, default="")
    description = StringField(required=True, max_length=255, default="")
    category = StringField(required=True, max_length=255, default="")
    brand = StringField(required=True, max_length=255, default="")
    price = FloatField(required=True,default=0)
    quantity = IntField(required=True, default=0)
    created_at= DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "collection": "products",
        "indexes": ["-created_at", "-updated_at","price","name","category","brand"]
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)
