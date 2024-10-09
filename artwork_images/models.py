from django.db import models


class ArtworkImage(models.Model):
    artwork = models.ForeignKey("artworks.Artwork", related_name="artworks_images", on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f'Image for {self.artwork}'

