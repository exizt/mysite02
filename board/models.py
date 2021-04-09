from django.db import models

from user.models import User


class Board(models.Model):
    title = models.CharField(max_length=200, default='')
    contents = models.TextField(default='')
    hit = models.IntegerField(default=0)
    reg_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    g_no = models.IntegerField(default=0)
    o_no = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Board({self.title})'
