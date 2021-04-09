from django.db import models


class Board(models.Model):
    title = models.CharField(max_length=200)
    contents = models.CharField(max_length=4000)
    hit = models.IntegerField()
    reg_date = models.DateTimeField(auto_now=True)
    g_no = models.IntegerField()
    o_no = models.IntegerField()
    depth = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return f'Board({self.title})'
