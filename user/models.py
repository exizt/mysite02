from django.db import models


class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=32)
    gender = models.CharField(max_length=10)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User({self.name})'
