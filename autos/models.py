from django.db import models


class Make(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class Auto(models.Model):
    nickname = models.CharField(max_length=200)
    mileage = models.IntegerField()
    comments = models.CharField(max_length=200)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nickname}: {self.comments} ({self.mileage}) - {self.make}'
