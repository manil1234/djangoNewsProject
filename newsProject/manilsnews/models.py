from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stories(models.Model):
    HEADLINE_MAX_LENGTH = 64        # Easy to change the length of the headline
    DETAILS_MAX_LENGTH = 128        # Easy to change the length of the details

    CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia'),
    ]

    REGION_CHOICES = [
        ('uk', 'UK'),
        ('eu', 'EU'),
        ('w', 'World'),
    ]

    headline = models.CharField(max_length=HEADLINE_MAX_LENGTH)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=2, choices=REGION_CHOICES)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Foreign Key to relate Stories to User - Delete all stories if user is deleted
    date = models.DateField(auto_now_add=True)  # Set to current date when object is created
    details = models.CharField(max_length=DETAILS_MAX_LENGTH)

    def __str__(self):
        return self.headline
