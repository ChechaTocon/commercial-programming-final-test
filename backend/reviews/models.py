from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    createdAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    bithDate = models.DateTimeField(blank=True, null=True)
    createdAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('createdAt',)

class Myuser(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    createdAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('createdAt',)

class Book(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    publishDate = models.DateTimeField(blank=True, null=True) 
    categories = models.ForeignKey(
        Category, related_name="bookcat", on_delete=models.CASCADE, blank=True, null=True
    )
    authors = models.ForeignKey(
        Author, related_name="bookauth", on_delete=models.CASCADE, blank=True, null=True
    )
    users = models.ForeignKey(
        Myuser, related_name="bookuser", on_delete=models.CASCADE, blank=True, null=True
    )
    createdAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('createdAt',)
