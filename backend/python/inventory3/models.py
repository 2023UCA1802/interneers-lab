from mongoengine import Document,StringField,ReferenceField,ListField,ValidationError


class Brand(Document):
    name = StringField(required=True, unique=True)
    description = StringField(required=True)


class ProductCategory(Document):
    name = StringField(required=True, unique=True)
    description = StringField(required=True)



class Product(Document):
    name = StringField(required=True)
    brand = ReferenceField(Brand, required=True)

    categories = ListField(
        ReferenceField(ProductCategory, required=True)
    )

