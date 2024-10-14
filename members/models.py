from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models


class Member(AbstractUser):
    USER_TYPE_CHOICES = [
        ('artist', 'Artist'),
        ('collector', 'Collector'),
    ]

    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
  
    ## Artist Members Fields
    bio = models.TextField(validators=[MaxLengthValidator(700)], blank=True)
    website = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.username} - {self.user_type}'
    
    
    


