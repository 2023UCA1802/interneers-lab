from mongoengine import Document,StringField,ReferenceField,ListField,ValidationError


class Brand(Document):
    name = StringField(required=True, unique=True)
    description = StringField(required=True, unique=True)


class ProductCategory(Document):
    name = StringField(required=True, unique=True)
    description = StringField(required=True, unique=True)



class Product(Document):
    name = StringField(required=True)

    # Initially allow null=True for migration
    brand = ReferenceField(Brand, required=False)

    categories = ListField(
        ReferenceField(ProductCategory)
    )

    def clean(self):
        # Enforce validation
        if not self.brand:
            raise ValidationError("Product must have a brand")
