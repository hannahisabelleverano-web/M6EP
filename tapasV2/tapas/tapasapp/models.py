from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    cook_time = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.pk) + ": " + self.name

    