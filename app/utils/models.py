from app.utils import settings

__all__ = ['Model']


class ModelMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        new_class = super(ModelMetaClass, mcs).__new__(mcs, name, bases, attrs)
        new_class._meta = getattr(new_class, 'Meta')
        delattr(new_class, 'Meta')

        # Connect to MongoDB
        collection_name = new_class._meta.collection
        if collection_name:
            new_class.connection = settings.db[collection_name]

        return new_class


class Model(metaclass=ModelMetaClass):
    # MongoDB collection instance
    collection = None

    class Meta:
        # MongoDB collection name
        collection = None
