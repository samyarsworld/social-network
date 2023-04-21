from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.category_name


class Bid(models.Model):
    bid = models.FloatField()
    bid_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='user_bids')



class Listing(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='user_listings')
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    bid_price = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, blank=True, related_name='bid_listing')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category_listings')
    image_url = models.CharField(max_length=400, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='user_watchlists')

    def __str__(self):
        return self.name


class ListingComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='auction_user_comments')
    content = models.CharField(max_length=400)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name='auction_listing_comments')

    def __str__(self):
        return f'Written by {self.author}'