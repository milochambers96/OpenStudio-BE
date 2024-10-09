from django.db import models
from django.core.validators import MaxLengthValidator


class Artwork(models.Model): 

    MEDIUM_CHOICES = [
        ('painting', 'Painting'),
        ('sculpture', 'Sculpture'),
        ('digital_art', 'Digital Art'),
        ('photography', 'Photography'),
        ('mixed_media', 'Mixed Media'),
        ('printmaking', 'Printmaking'),
        ('ceramics', 'Ceramics'),
        ('textile', 'Textile Art'),
    ]

    title = models.CharField(max_length=100)
    artist = models.ForeignKey("members.Member", related_name="artworks", on_delete=models.CASCADE)
    description = models.TextField(validators=[MaxLengthValidator(300)])
    year = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity_for_sale = models.IntegerField()
    is_for_sale = models.BooleanField(default=True)
    medium = models.CharField(max_length=30, choices=MEDIUM_CHOICES)
    material = models.CharField(max_length=50)

    ## Dimensions and Weight saved to feed into Shipping API on FE
    width = models.DecimalField(max_digits=6, decimal_places=2, help_text="Width in cm")
    depth = models.DecimalField(max_digits=6, decimal_places=2, help_text="Depth in cm")
    height = models.DecimalField(max_digits=6, decimal_places=2, help_text="Height in cm")
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight in kg")


    def __str__(self) -> str:
        return f'{self.title} by {self.artist}'
    
    




