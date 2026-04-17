from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=30)

    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password

    def __str__(self):
        return str(self.pk) + ": " + self.username + " " + self.password

class Dish(models.Model):
    name = models.CharField(max_length=300)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.pk) + ": " + self.name
    