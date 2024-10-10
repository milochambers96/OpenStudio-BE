from django.db import models

class Gallery(models.Model): 
    curator = models.ForeignKey('members.Member', related_name='galleries', on_delete=models.CASCADE)
    artworks = models.ManyToManyField('artworks.Artwork', through='GalleryArtwork')

    def __str__(self):
        return f'Gallery curated by {self.curator.username}.'
    
class GalleryArtwork(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    artwork = models.ForeignKey('artworks.Artwork', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.artwork.title} in {self.gallery.curator.username}'s gallery."



    

