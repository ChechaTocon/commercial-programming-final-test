from django.db import models
from django.utils import timezone

#Modelo para categoria
class Category(models.Model):

    name = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    createdAt = models.DateField(blank=True, null=True)
    updatedAt = models.DateField(blank=True, null=True)

    def __str__(self):

        return self.name

#Modelo para pelicula

class Movie(models.Model):

    poster = models.TextField()
    movieName = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    createdAt = models.DateField(blank=True, null=True)
    updatedAt = models.DateField(blank=True, null=True)

    category = models.ForeignKey(

        Category, related_name="categorys", on_delete=models.CASCADE
    )

    def __str__(self):

        return self.movieName

#modelo para el usuario
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.TextField()
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    role = models.BooleanField()
    createdAt = models.DateField(blank=True, null=True)
    updatedAt = models.DateField(blank=True, null=True)
    def __str__(self):

        return self.username

#Modelo para la rese;a
class Review(models.Model):
    
    comment = models.TextField()
    ranking = models.IntegerField()
    createdAt = models.DateField(blank=True, null=True)
    updatedAt = models.DateField(blank=True, null=True)

    movie = models.ForeignKey(

        Movie, related_name="movies", on_delete=models.CASCADE
    )
    user = models.ForeignKey(

        User, related_name="users", on_delete=models.CASCADE
    )

    def __str__(self):

        return self.comment
