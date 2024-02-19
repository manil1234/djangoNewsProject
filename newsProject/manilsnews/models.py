from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, default='n/a')
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

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
    author = models.CharField(max_length=100)  # Assuming author's name is text
    date = models.DateField()
    details = models.CharField(max_length=DETAILS_MAX_LENGTH)

    def __str__(self):
        return self.headline
