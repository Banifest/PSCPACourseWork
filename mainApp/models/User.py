from django.contrib.auth.models import AbstractUser, User as default_user

class User(AbstractUser):

    def __str__(self):
        return self.username