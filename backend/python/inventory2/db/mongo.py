from mongoengine import connect
import os


def init_db():
    connect(
        db=os.getenv("MONGO_DB", "product")
    )
    
    print("Mongo Port:", os.getenv("MONGO_PORT"))
    print("Mongo DB:", os.getenv("MONGO_DB"))