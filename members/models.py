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

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
  
    ## Artist Members Fields
    bio = models.TextField(validators=[MaxLengthValidator(700)])
    website = models.URLField(max_length=200, blank=True)
    artist_address = models.CharField(max_length=255, blank=True)

    ## Collector Members Fields
    collector_address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.user_type}'
    
    
    


