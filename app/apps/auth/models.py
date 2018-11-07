from app.utils.models import Model


class User(Model):
    """
    User scope class
    """

    class Meta:
        collection = 'users'
