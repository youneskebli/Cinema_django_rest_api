from django.db import models

# Create your models here.
class Movie(models.Model):
    hall = models.CharField(max_length=10,default="",blank=False)
    movieName = models.CharField(max_length=15,default="",blank=False)
    def __str__(self):
        return self.movieName


class Guest(models.Model):
    name = models.CharField(max_length=15,default="",blank=False)
    mobile = models.CharField(max_length=10,default="",blank=False)
    def __str__(self):
        return self.name

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE )
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.CASCADE )
    