from mongoengine import connect
import os


def init_db():
    connect(
        db=os.getenv("MONGO_DB", "product"),
        host=f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@"
             f"{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/"
             f"{os.getenv('MONGO_DB', 'product')}?authSource=admin"
    )
    print("Mongo Port:", os.getenv("MONGO_PORT"))
    print("Mongo DB:", os.getenv("MONGO_DB"))