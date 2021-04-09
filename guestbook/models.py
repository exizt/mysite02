from django.db import models


class Guestbook(models.Model):
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    message = models.TextField()
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Guestbook({self.name}, {self.message}, {self.reg_date})'
