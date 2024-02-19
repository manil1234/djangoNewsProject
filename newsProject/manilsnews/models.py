from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class News(models.Model):
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
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Foreign Key to relate News to User - Delete all news if user is deleted
    date = models.DateField()
    details = models.CharField(max_length=DETAILS_MAX_LENGTH)

    def __str__(self):
        return self.headline
