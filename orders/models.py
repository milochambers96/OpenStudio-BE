from django.db import models

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('ready to ship', 'Ready to Ship'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    buyer = models.ForeignKey("members.Member", related_name="buyer_orders", on_delete=models.CASCADE)
    seller = models.ForeignKey("members.Member", related_name="seller_orders", on_delete=models.CASCADE)
    artwork  = models.ForeignKey("artworks.Artwork", related_name="orders", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)

